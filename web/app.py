from flask import Flask
import sys
from flask_cors import CORS

App = Flask(__name__)
CORS(App)

@App.route("/")
def slash():
    return "Hello world"

if __name__ == "__main__":
    if len(sys.argv) > 1:
        App.run(debug = True, host = "0.0.0.0", port = 3000)
    else:
        App.run(host = "0.0.0.0", port = 3000)
