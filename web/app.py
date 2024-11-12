from flask import Flask, send_file, request, redirect # type: ignore
import sys
import os
from flask_cors import CORS # type: ignore
from generate import generateReport
import json
import logging
import time

logging.basicConfig(level=logging.INFO)

App = Flask(__name__)
CORS(App)

# def start_ngrok():
#     # Get the dev server port (default is 5000)
#     port = sys.argv[sys.argv.index("--port") + 1] if "--port" in sys.argv else 5000
#     # Open an ngrok tunnel to the dev server
#     public_url = ngrok.connect(port).public_url
#     print(f" * ngrok tunnel \"{public_url}\" -> \"http://127.0.0.1:{port}\"")
#     # Update any base URLs or webhooks to use the public ngrok URL
#     App.config["BASE_URL"] = public_url

@App.route("/")
def slash():
    return "Hello world"

@App.route("/report", methods = ["GET", "POST"])
def report():
    if request.method == "GET":
        if os.path.exists("./report.pdf"):
            return send_file("./report.pdf", mimetype = "application/pdf", as_attachment = True, download_name = "report.pdf")
        else:
            return "No report"
    elif request.method == "POST":
        with open("./data.json", "a") as f:
            f.write(json.dumps(json.loads(request.data)))
            time.sleep(2)
        return redirect("/", code = 301)

if __name__ == "__main__":
    App.run(debug = True)
