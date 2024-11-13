from flask import Flask, request

flask_app = Flask(__name__)

@flask_app.route("/")
def home():
    return "Hello, World!"

if __name__ == "__main__":
    flask_app.run(debug=True)