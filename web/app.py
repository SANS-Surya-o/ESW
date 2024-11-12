from flask import Flask, send_file, request # type: ignore
import sys
import os
from flask_cors import CORS # type: ignore
from generate import generateReport
import json

App = Flask(__name__)
CORS(App)

@App.route("/")
def slash():
    return "Hello world"

@App.route("/report")
def report():
    if request.method == "GET":
        if os.path.exists("./report.pdf"):
            return send_file("./report.pdf", mimetype = "application/pdf", as_attachment = True, download_name = "report.pdf")
        else:
            return "No report"
    elif request.method == "POST":
        print("heler")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        App.run(debug = True, host = "0.0.0.0", port = 3000)
    else:
        App.run(host = "0.0.0.0", port = 3000)
