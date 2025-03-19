import os
import sys
import pathlib
sys.path.append(pathlib.Path(os.path.abspath(__file__)).parent.parent.__str__())
from src.mainframe_orchestra import Task, Agent, OpenaiModels, Conduct, set_verbosity,DeepseekModels
from src.mainframe_orchestra  import HackerTools
from dotenv import load_dotenv
import logging


load_dotenv()
set_verbosity(1)


# 定义 orchestra llm
if os.getenv("OPENAI_API_KEY") is not None:
    # openai gpt-4o llm
    OrchestraLLM = OpenaiModels.gpt_4o
elif os.getenv("DEEPSEEK_API_KEY") is not None:
    # deepseek llm
    OrchestraLLM = DeepseekModels.custom_model(os.getenv("COMMON_MODE_NAME"))  # 使用自定义模型
else:
    logging.error("No valid API key found for Orchestra LLM.")
    exit(1)

# Define the team of agents in the workflow
website_testing_agent = Agent(
    agent_id="Website Tester",
    role="Website Tester",
    goal="Perform comprehensive security testing of the target website using provided tools.",
    attributes="""
    Your task is to thoroughly test the target website for security vulnerabilities using the available tools.
    - **Login Procedure:**
        - If you receive valid user credentials, JUST log in using **non-administrative** credentials.
        - If you do not receive any valid credentials, perform testing that does not require authentication.
    - **Tool Usage:** Just Use the website_testing_tools, this tools can Automate the testing of your website.
    - **Output:**  Touch up the output of the tool and tell the user that the full penetration test report is in result.html.
    - 使用中文交流和输出。
    ATTENTION: It is sufficient to use only one set of valid credentials logins for the testing, DO NOT repeat the logins for the testing.JUST TEST ONCE!
    """,
    llm=OrchestraLLM,
    tools={HackerTools.website_testing_tools}
)

authorization_vulnerability_agent = Agent(
    agent_id="Authorization Vulnerability Analyst",
    role="Authorization Vulnerability Analyst",
    goal="Identify authorization and access control vulnerabilities in the target website.",
    attributes="""
    You have expertise in authorization detection use the tools to test the website for authorization vulnerabilities.
    - **Tool Usage:** Use the `authorization_vulnerability_Check_tool` to test for authorization flaws.
    - **Output:** Report any successful privilege escalation attempts, detailing the credentials used, the actions performed, and the expected vs. actual outcome.
    - 使用中文交流和输出。
    """,
    llm=OrchestraLLM,
    tools={HackerTools.authorization_vulnerability_Check_tool}
)

login_brute_force_agent = Agent(
    agent_id="Login Brute Forcer",
    role="Login Brute Force Analyst",
    goal="Analyze the url for login vulnerabilities.",
    attributes="You have expertise in login detection and vulnerability analysis, use the tools to test the website for login vulnerabilities. Return any discovered valid username and password combinations.  If no valid credentials are found, report that the brute-force attempt was unsuccessful.",
    llm=OrchestraLLM,
    tools={HackerTools.login_brute_force_tool}
)

report_agent = Agent(
    agent_id="Reporter",
    role="Security Report Compiler",
    goal="Compile a comprehensive security report summarizing all identified vulnerabilities.",
    attributes="""
    Your task is to generate a clear and concise security report based on the findings of other agents.

    - **Input:** You will receive reports and outputs from other agents, including the `website_testing_agent`, `authorization_vulnerability_agent`, and `login_brute_force_agent`. You MUST TO access to the `get_pentest_report` tool to retrieve reports directly from vulnerability scanning tools.
    - **Report Structure:** The report should include the following sections:
        - **Executive Summary:** A brief overview of the most critical findings and overall security posture.
        - **Vulnerability Details:**  For each discovered vulnerability:
            - Vulnerability Name
            - Description
            - Affected URLs/Parameters
            - Vulnerability Type (e.g., SQLi, XSS, Broken Authentication)
            - Severity (e.g., Critical, High, Medium, Low) - You may need to determine this based on the vulnerability description and potential impact.
            - Remediation Recommendations
        - **Methodology:**  Describe the testing process and the tools used.
        - **Credentials Found (if any):**  List any valid credentials discovered by the `login_brute_force_agent`.
        - **Failed Attempts (Summary):** Summarize any failed attempts (e.g., unsuccessful brute-force attempts), without including extensive lists of failed passwords.
    - **Clarity:**  Ensure the report is easy to understand for both technical and non-technical audiences.  Use clear and concise language.
    - **Tool Usage:**  Use the `get_pentest_report` tool to access and incorporate information from automated vulnerability scans.
    - 使用中文交流和输出。
    """,
    llm=OrchestraLLM,
    tools={HackerTools.get_pentest_report}
)

conductor_agent = Agent(
    agent_id="conductor_agent",
    role="Penetration Testing Team Lead", 
    goal="Lead a team of specialized agents to conduct a comprehensive penetration test of the target website and generate a detailed report.",
    attributes="""You are an experienced penetration testing team leader responsible for coordinating a team to assess the security of a website.  Your workflow is as follows:
    1. **Credential Brute-Forcing:**
       - Initiate the `login_brute_force_agent` to attempt to discover valid user credentials.
    2. **Website Vulnerability Scanning:**
           - Instruct the `website_testing_agent` to perform vulnerability scanning.
           - Provide the discovered credentials to the `website_testing_agent`.
    3. **Authorization Testing:**
       - If *two or more* sets of valid credentials are found, instruct the `authorization_vulnerability_agent` to test for authorization vulnerabilities.
       - Provide all discovered credentials to the `authorization_vulnerability_agent`.
    4. **Report Generation:**
        - Finally, instruct the `report_agent` to compile a comprehensive security report based on the findings of all other agents.

    **Error Handling:**
    - If any agent encounters an error or is unable to complete its task, it should report the issue.  You should then decide whether to continue with other tasks or halt the testing process.
    - If the `login_brute_force_agent` is unsuccessful, proceed with unauthenticated testing using the `website_testing_agent`.

    **Communication:**
    - Clearly communicate your instructions to each agent.
    - Monitor the progress of each agent and provide guidance as needed.
    - The final output, Report, contains the necessary line breaks and serial numbers.
    - 使用中文交流和输出。
    """,
    llm=OrchestraLLM,
    tools=[Conduct.conduct_tool(login_brute_force_agent, website_testing_agent, authorization_vulnerability_agent,report_agent)])


def task_go(conversation_history, userinput):
    return Task.create(
        agent=conductor_agent,
        messages=conversation_history,
        instruction=userinput
    )


