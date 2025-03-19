import os
import sys
import pathlib
import io
import threading
import time
from flask import Flask, request, jsonify, Response
from flask_sse import sse
from flask_cors import CORS
from ez_agent import task_go
from dotenv import load_dotenv

load_dotenv()




sys.path.append(pathlib.Path(os.path.abspath(__file__)).parent.parent.__str__())

app = Flask(__name__, static_folder='templates', static_url_path='')
app.register_blueprint(sse, url_prefix='/stream')
CORS(app, resources=r'/*') 

# 全局变量用于存储输出和控制状态
output_buffer = io.StringIO(newline='\n')
test_running = False
test_thread = None
original_stdout = sys.stdout



def run_test_task(url):
    """
    在后台线程中运行测试任务，并将输出写入 output_buffer。
    """
    global test_running, original_stdout
    test_running = True
    sys.stdout = output_buffer
    conversation_history = []
    conversation_history.append({"role": "user", "content": url})
    try:
        response = task_go(conversation_history, url)
        conversation_history.append({"role": "assistant", "content": response})
        print(f"{response}")
    except Exception as e:
        print(f"Error during test: {e}")
    finally:
        sys.stdout = original_stdout
        test_running = False
        print("Test finished.")

@app.route('/start_test', methods=['POST'])
def start_test():
    """
    接收 URL，启动测试任务。
    """
    global test_thread, test_running, output_buffer

    if test_running:
        return jsonify({"status": "error", "message": "Test is already running."}), 400

    data = request.get_json()
    if not data or 'url' not in data:
        return jsonify({"status": "error", "message": "URL is required."}), 400
    url = data['url']

    output_buffer.seek(0)
    output_buffer.truncate()

    test_thread = threading.Thread(target=run_test_task, args=(url,))
    test_thread.daemon = True
    test_thread.start()

    return jsonify({"status": "success", "message": "Test started."})



@app.route('/stream_output')
def stream_output():
    def event_stream():
        global test_running, output_buffer
        last_pos = 0
        yield "data: 连接成功\n\n"

        while True:
            if not test_running and output_buffer.tell() <= last_pos:
                time.sleep(0.1)
                continue

            output_buffer.seek(last_pos)
            data = output_buffer.read()
            if data:
                formatted_data = "\n".join(f"data: {line}" for line in data.splitlines())
                yield f"{formatted_data}\n\n"
                last_pos = output_buffer.tell()

            time.sleep(0.1)

    return Response(
        event_stream(),
        mimetype="text/event-stream",
        headers={
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'Access-Control-Allow-Origin': '*'
        }
    )


if __name__ == "__main__":
    
    app.run(debug=True, threaded=True,port=5555,host="0.0.0.0")
