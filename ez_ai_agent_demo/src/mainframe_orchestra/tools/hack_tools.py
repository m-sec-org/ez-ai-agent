from browser_use import Agent as BrowserAgent
from browser_use import  Controller
from browser_use.browser.browser import Browser, BrowserConfig
import os
import re
import json
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI
from steel import Steel
from browser_use.browser.browser import Browser, BrowserConfig
import logging
import sys
from dotenv import load_dotenv
load_dotenv()

use_visionx=True
# 定义 browser-use LLM
if os.getenv("GEMINI_API_KEY") is not None:
    # Gemini 2.0 llm 
    BrowserAgent_llm = ChatGoogleGenerativeAI(
        model="gemini-2.0-flash",
        temperature=1.0,
        api_key=os.getenv("GEMINI_API_KEY")
    )
elif os.getenv("DASHSCOPE_API_KEY") is not None:
    # QWEN llm
    BrowserAgent_llm = ChatOpenAI(
        model=os.getenv("BROWSER_USE_MODE_NAME"),
        api_key=os.getenv("DASHSCOPE_API_KEY"),
        base_url=os.getenv("DASHSCOPE_API_URL"),
    )
else:
    logging.error("No valid API key found for LLM.")
    exit(1)

use_visionx = os.getenv("USE_VISION")



# 定义 Steel 浏览器客户端
client = Steel(
    base_url="http://steel-api:3000",
    steel_api_key="keys"
)
controller = Controller()


class HackerTools:
    @staticmethod
    async def website_testing_tools(website: str, username: str = "admin", password: str = "Passwword") -> str:
        """Use browser-use to perform functional testing on target website, and the traffic will be tested by professional equipment for vulnerabilities.

        Args:
            website (str): the website to test
            username (str): the username to login
            password (str): the password to login
        Returns:
            str: Result of functional testing
        """
        print("[website_testing_tools] Start!")
        task_prompt_en = f"""
**🎯 Objective:**  Utilize an automated Agent to perform functional testing on a target website. This involves **traversing all accessible pages and interacting with key interactive elements, recording the testing process, and avoiding duplicate actions.**

        **🛠️ Task Breakdown:**

        1. **Systematic Page Exploration and Interaction (Agent Simulation):**
            * **Goal:** Starting from the website's homepage, **systematically explore all accessible pages** and interact with **key interactive elements** on each page.
            * **Exploration Method:** From the current page, **prioritize clicking on links** to navigate to new pages. On each page, interact with important interactive elements in the order of their element index.
            * **Operation Flow Simulation:** Simulate basic functional testing workflows, such as:
                * Homepage -> Navigation Menu -> Subpages
                * Listing Page -> Detail Page
                * Form Filling and Submission (e.g., login forms, contact forms, etc.)
            * **Note:** The Agent needs to **cover as many pages and key interactive functionalities as possible**, but is not required to deeply understand the content details like a real user.

        2. **Testing Order (Step-by-Step Depth):**
            * **Important:** Please **strictly adhere** to the following testing order:
                FIRST. **Non-Login Features:**  Initially, test all website features and pages that are accessible without login(Test only a *few representative* pages of similar types. Focus on functional differences, not exhaustive data variations.  For example, if you've tested `/product/123`, testing `/product/124` might be unnecessary *unless* you expect different functionality.).
                SECOND. **Login Functionality:** Next, test the user login function (using username `{username}` and password `{password}`). **If a CAPTCHA error or login failure is encountered, immediately stop login testing.**
                THIRD. **Post-Login Features:** After successful login, continue testing features and pages that require login to access. (ALL BACKEND FEATURES after login **MUST** be tested, this is a key focus! IF YOU FORGET TO TEST ANY OF THE BACKEND FEATURES, YOU FAIL!!!)
                FOURTH. **Logout Functionality:** Finally, test the user logout function.
            * **Prohibited Actions:** **Strictly refrain from performing password modification (other content modification is allowed) and any deletion operations.**

        3. **Test Recording and Deduplication (Efficient Testing):**
            * **Memory (URL Tracking):**
                * **Recording Timing:** **Immediately after successfully accessing a new URL, record that URL into "Memory."**
                * **Recorded Content:** Record the **complete URL** of the accessed page.
                * **Recording Format:** Use URL string format, for example: `"https://www.example.com/product/123"`. Reflect the Memory content in the `current_state.memory` field.
            * **Avoiding Duplicate Testing (URL Deduplication):**
                * **Pre-Navigation Check:** **Before attempting to navigate to any new URL, first check if that URL already exists in the "Memory" record.**
                * **Deduplication Logic:** If the target URL is already in "Memory," **skip testing that URL** to avoid redundant visits.
                * **Intelligent Deduplication:** For pages with highly similar content (e.g., article listing pages, product listing pages,  https://www.example.com/product/123 and https://www.example.com/product/124 , Article 1 and Article 2, ...), only test **a few representative pages**. There's no need to exhaustively traverse all similar pages. **Focus on covering functional logic, not data enumeration.**
                * **Important Feature Testing:** ALL backend features after login **must** be tested. 

        4. **Test Completion Criteria (Clear End Conditions):**
            * **Criteria:** When the Agent **can no longer find new unvisited links** and has already **tested all important interactive elements on the current page**, the testing is considered basically complete. The `done` action can be used to end the task.
            * **Agent Self-Check:** The Agent can check its "Memory" record to see the number of URLs visited and whether there are obvious website modules or functional areas that have not been accessed (e.g., whether all links in the navigation menu have been visited).

        **⚠️ Important Notes (Must Be Followed):**

        * **Login CAPTCHA Handling:** When encountering a **CAPTCHA error or login failure during login, immediately stop login testing and do not retry.**
        * **Prohibition of Uploading and Deleting:** **Strictly prohibit testing any upload functions and delete functions.**
        * **Memory Maintenance:** The Agent needs to maintain the list of visited URLs in the `current_state.memory` field.
        * **Login Credentials:** Username `{username}`, password `{password}`.
        * **URL Recording is Key:** The Agent's testing progress and avoidance of duplicate testing primarily rely on the URL records in "Memory."
        * **Testing Order:** Please follow the specified testing order. **Do not test login functionality first!!!**
        * **Webpage Operation Rules:** On a webpage, click only one interactive element at a time. Do not click the same element multiple times or click multiple elements simultaneously, as this may cause page navigation chaos.
        * If it is a blog, shopping site, etc., for articles and products, etc., only need to click on the test 2 can be, the rest do not need to click, because they are the same logic of the background code, do not need to test too much.

        * **Key Testing Items:** ALL backend features of the website, including but not limited to: user management, product management, order management, permission management, configuration management, etc. MUST BE CLICK AND TESTING!

        **🚀 Start Testing! Please strictly follow the above instructions and act as an automated Agent to perform website functional testing tasks. After each operation, please reply in JSON format, including `current_state` and `action`.**
        ---
        The Website to Test: 
        {website}
        """

        session = client.sessions.create(
            proxy_url=os.getenv("EZ_PASSIVE_URL"),  # 设置EZ代理
        )
        browser = Browser(
            config=BrowserConfig(
                headless=False,
                cdp_url=f'ws://steel-api:3000',
            )
        )
        agent = BrowserAgent(
            task=task_prompt_en,
            llm=BrowserAgent_llm,
            max_actions_per_step=5,
            controller=controller,
            browser=browser,
            use_vision=use_visionx
        )

        result = await agent.run(max_steps=200)
        await browser.close()
        if session:
            client.sessions.release(session.id)

        print("[website_testing_tools] "+result.final_result())
        return result.final_result()

    @staticmethod
    async def authorization_vulnerability_Check_tool(url: str, admin_user: str, admin_pass: str, user: str,
                                                     passwowrd: str) -> str:
        """Use browser to perform authorization vulnerability Check.
        Args:
            url (str): The login Page URL.
            admin_user (str): the admin account's username.
            admin_pass (str): the admin account's password.
            user (str): the normal account's username.
            passwowrd (str): the normal account's password.
        Returns:
            str: the result of the authorization vulnerability Check.
        """
        print("[Authorization_vulnerability_Check_Agent] Start!")
        task_prompt_en = f"""
        Task: Detect Horizontal AND Vertical Privilege Escalation Vulnerabilities.  This is a two-part task; you MUST attempt to find BOTH types of vulnerabilities.  The presence of one type of vulnerability does NOT mean the task is complete.  You must explicitly test for BOTH.  Assume vulnerabilities *potentially* exist in both directions.

You are tasked with identifying potential privilege escalation vulnerabilities within a web application.  You will be provided with two sets of credentials:

*   **Normal User:**  Username: `{user}`, Password: `{passwowrd}`
*   **Admin User:** Username: `{admin_user}`, Password: `{admin_pass}`
*   **Login URL:** `{url}`
* **Webpage Operation Rules:** On a webpage, click only one interactive element at a time. Do not click the same element multiple times or click multiple elements simultaneously, as this may cause page navigation chaos.

You will simulate actions of both users and compare their access to resources and functionalities to identify potential vulnerabilities.  Follow this process:

**STEP 1: Normal User Exploration and Data Gathering**

1.  **Login as Normal User:** Log in to the application using the `{user}` user credentials.
2.  **Explore Functionality:** Navigate through the application as a normal user.  Identify key features and data accessible to this user.  Pay close attention to:
    *   Any resources the user can access (e.g., documents, data entries, etc.). Note specific IDs or unique identifiers associated with these resources (e.g., user IDs, document IDs, etc.).
    *   Available actions the user can perform (e.g., create, edit, delete).
    *   Click on each unique functionality you find and record the corresponding URL.
3.  **Extract and store unique Identifiers:** Use `extract_content` or observe URLs to gather unique identifiers of data viewed by the normal user.  Store this information in the `memory` in a structured format, like this:
    ```
      "user_profile_url": "/user/???.php?user=6",
      "accessible_urls": ["/docs/view.php?doc_id=456", "/reports/view.php?report_id=789"],
      "user_id": "2"
    ```
4.  **Logout:** Log out of the normal user account.

**STEP 2: Admin User Exploration (Baseline)**

1.  **Login as Admin User:** Log in to the application using the `{admin_user}` credentials.
2.  **Explore Admin Functionality:** Explore the application, *specifically* focusing on functionalities NOT encountered during the normal user exploration.  This is crucial for identifying vertical escalation targets.  Look for:
    *   User management features (e.g., creating, deleting, or modifying *other* users).  This is VERY IMPORTANT.
    *   System-wide settings or configurations.
    *   Features labeled as "Admin," "Settings," "Management," or similar.
    *   Click on each unique functionality you find and record the corresponding URL.
3.  **Identify Admin-Only Actions/URLs:**  Record the URLs and a brief description of any actions or pages that appear to be restricted to administrators in the `memory`.  Use a structured format:
    ```
      "manage_users_url": "/admin/???.php",
      "privilege_control_url": "/admin/????.php",
      "admin_dashboard_url": "/admin/?????.php"
    ```
4.  **Logout:** Log out of the admin account.

**STEP 3: Horizontal Privilege Escalation Test**

1.  **Login as Normal User:** Log back in as the `{user}` user.
2.  **Attempt Direct Access (Horizontal):**
    *   Try to access resources belonging to *other* users.  Use patterns observed in resource IDs (from Step 1).  For example:
        *   If you saw `user_id=2`, try `user_id=1` or `user_id=3`.
        *   If you saw `doc_id=456`, try `doc_id=455` or `doc_id=457`.
    *   Use `go_to_url` with the modified identifiers.
    *   **If Access is Successful:** Record the specific URL and a description of the accessed data in the `memory`.  **Do NOT stop here. Continue to Step 4.**
    *  **If No Access:** Proceed to step 4.

**STEP 4: Vertical Privilege Escalation Test (CRITICAL)**

1.  **Login as Normal User (if not already logged in):**  Ensure you are logged in as the `{user}` user.
2.  **Attempt Direct Access (Vertical):**
    *   Try to access the admin-only functionalities identified in Step 2, *using the URLs stored in memory*.
    *   Use `go_to_url` to navigate directly to these admin URLs.
    *   **If Access is Successful:**  Record the specific URL and a description of the accessed functionality in the `memory`.
    *   **If Access is NOT successful,** that is expected behavior. Proceed to STEP 5

**STEP 5: Reporting (Comprehensive)**

1.  **Report ALL Findings:** Use the `done` action to report your findings.  This report *must* include:
    *   **Horizontal Escalation Results:**  Report whether you successfully accessed other users' data.  Include the URLs used and a description of the data accessed.  If no horizontal escalation was found, explicitly state that.
    *   **Vertical Escalation Results:** Report whether you successfully accessed any admin-only functionality.  Include the URLs used and a description of the functionality accessed. If no vertical escalation was found, explicitly state that.

    **Examples:**

    *   **Both Vulnerabilities Found:**
        ```json
        {{
          "done": {{
            "text": "Vulnerabilities Found:\n\nHorizontal Privilege Escalation: Logged in as 'test', I accessed user profile data for user_id=1 (admin) via /user/profile.php?user_id=1.\n\nVertical Privilege Escalation: Logged in as 'test', I accessed the admin user management page via /admin/manage_users.php."
          }}
        }}
        ```
    *   **Only Horizontal Vulnerability Found:**
    ...
    *  **Only Vertical Vulnerability Found**
    ...
    *   **No Vulnerabilities Found:**

    使用中文输出结果。
    ... """
        session = client.sessions.create(
            proxy_url=os.getenv("EZ_PASSIVE_URL"),  # 设置EZ代理
        )
        browser = Browser(
            config=BrowserConfig(
                headless=False,
                cdp_url=f'ws://steel-api:3000',
            )
        )

        agent = BrowserAgent(
            task=task_prompt_en,
            llm=BrowserAgent_llm,
            max_actions_per_step=5,
            controller=controller,
            browser=browser,
            use_vision=use_visionx
        )
        result = await agent.run(max_steps=100)
        await browser.close()
        if session:
            client.sessions.release(session.id)

        print("[authorization_vulnerability_Check_Agent]"+ result.final_result())
        return result.final_result()

    @staticmethod
    async def login_brute_force_tool(url: str) -> str:
        """Use a brute force tool to perform login detection. It can find the login url and brute force the login.
        Args:
            url (str): the target url to perform login detection.
        Returns:
            str: the result of the login detection, include username and password.
        """
        print("[login_brute_force_agent] Start!")

        task_prompt_en = f"""
        Task: Find the login url of the {url} website.
        goto the {url} website, click the login button,and return the login url.
        JUST return the login url.
        like: https://example.com/login
        """
        session = client.sessions.create(
            proxy_url=os.getenv("EZ_PASSIVE_URL"),  # 设置EZ代理
        )
        browser = Browser(
            config=BrowserConfig(
                headless=False,
                cdp_url=f'ws://steel-api:3000',
            )
        )
        agent = BrowserAgent(
            task=task_prompt_en,
            llm=BrowserAgent_llm,
            max_actions_per_step=5,
            controller=controller,
            browser=browser,
            use_vision=use_visionx
        )
        history = await agent.run(max_steps=10)
        login_url = history.final_result()
        await browser.close()
        if session:
            client.sessions.release(session.id)

        import subprocess
        import platform
        machine = platform.machine()
        system = sys.platform

        if system == "darwin":
            if machine == "x86_64":
                cmd = f"./ez_tools/ez_brute_tools/ez_brute_darwin_amd64 -u {login_url}"
            elif machine == "arm64":
                cmd = f"./ez_tools/ez_brute_tools/ez_brute_darwin_arm64 -u {login_url}"
            else:
                cmd = f"./ez_tools/ez_brute_tools/ez_brute_darwin_amd64 -u {login_url}"
        elif system.startswith("linux"):
            cmd = f"./ez_tools/ez_brute_tools/ez_brute_linux_amd64 -u {login_url}"
        elif system.startswith("win"):
            cmd = f"./ez_tools/ez_brute_tools/ez_brute_win.exe -u {login_url}"
        else:
            logging.error("Unsupported platform.")
            return "ez_brute_tools 不支持该平台。"
            

        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        stdout, stderr = p.communicate()  
        output_str = stdout.decode("utf-8")
        error_str = stderr.decode("utf-8")
        if p.returncode != 0:  
            return f"Command failed with error (code {p.returncode}):\n{error_str}"
        else:
            print("[login_brute_force_tool]"+ output_str)
            return output_str

    @staticmethod
    async def get_pentest_report() -> str:
        """Get the penetration test report generated by the vulnerability scanning tool.
        Returns:
            str: the pentest report detail.
        """
        print("[get_pentest_report_agent] Start!")

        with open("/app/ez/result.html", "r") as f:
            result = f.read()
        html_report = result
        regex = r"<script class='web-vulns'>webVulns\.push\((.*?)\)</script>"
        matches = re.findall(regex, html_report)
        processed_data = []
        for match in matches:
            try:
                vuln_json = json.loads(match)
                if "detail" in vuln_json and "snapshot" in vuln_json["detail"]:
                    del vuln_json["detail"]["snapshot"]
                processed_data.append(vuln_json)
            except json.JSONDecodeError:
                print(f"Warning: Could not decode JSON from match: {match}")
                continue  
        processed_vulns = json.dumps(processed_data, indent=4, ensure_ascii=False)
        return processed_vulns
