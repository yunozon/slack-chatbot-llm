import os
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from slack_bolt import App
from slack_bolt.adapter.flask import SlackRequestHandler
from dotenv import find_dotenv, load_dotenv
from flask import Flask, request

# .envファイルから環境変数を読み込む
load_dotenv(find_dotenv())

SLACK_BOT_TOKEN = os.environ["SLACK_BOT_TOKEN"]
SLACK_SIGNING_SECRET = os.environ["SLACK_SIGNING_SECRET"]
SLACK_BOT_USER_ID = os.environ["SLACK_BOT_USER_ID"]

# Slackアプリを初期化
app = App(token=SLACK_BOT_TOKEN, signing_secret=SLACK_SIGNING_SECRET)

# Flaskアプリを初期化
flask_app = Flask(__name__)
handler = SlackRequestHandler(app)

# Slackのイベントポイント設定
@flask_app.route("/slack/events", methods=["POST"])
def slack_events():
    return handler.handle(request)

# カスタム関数の定義(botの機能 : 入力されたテキストを大文字に変換)
def my_function(text):
    response = text.upper()
    return response

# イベントリスナーの設定
@app.event("app_mention")
def handle_mentions(body, say):
    text = body["event"]["text"]
    mention = f"<@{SLACK_BOT_USER_ID}>"
    text = text.replace(mention, "").strip()
    response = my_function(text)
    say(response)


