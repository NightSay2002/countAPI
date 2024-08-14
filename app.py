from flask import Flask
from datetime import datetime
import threading

app = Flask(__name__)
lock = threading.Lock()

def log_time_to_file():
    current_time = datetime.now().isoformat()
    with lock:
        with open("request_times.txt", "a") as file:
            file.write(current_time + "\n")
    return current_time

@app.route('/log_time', methods=['GET'])
def log_time():
    current_time = log_time_to_file()
    return {"message": "Time logged successfully", "time": current_time}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000,debug=True)

