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
def get_bot_user_id():
    """
    Get the bot user ID from the Slack API
    Returns:
        str: The bot user ID
    """
    try:
        # Slack クライアントを初期化
        slack_client = WebClient(token=SLACK_BOT_TOKEN)
        response = slack_client.auth_test() # ユーザー情報を取得
        return response["user_id"]
    except SlackApiError as e: # Slack API エラーが発生した場合
        assert e.response["error"] # エラーメッセージを表示


def my_function(text):
    """
    Custom function 
    in function, the input text to uppercase

    Args:
        text (str): input text

    Returns:
        str: text to uppercase
    """
    response = text.upper()
    return response

@app.event("app_mention")
def handle_app_mentions(body, say):
    """
    Event listener for mentions in Slack.
    When bot is mentioned, the function is called.
    the function will convert the input text to uppercase.

    Args:
        body (dict): The event data received from Slack
        say (callable): A function for sending a message back to Slack
    """
    text = body["event"]["text"]

    mention = f"<@{SLACK_BOT_USER_ID}>"
    text = text.replace(mention, "").strip()
    response = my_function(text)
    say(response)

@flask_app.route("/slack/events", methods=["POST"])
def slack_events():
    """
    Route for handling Slack events.
    This function passes the income HTTP request to the SlackRequestHandler for processing.

    Returns:
        Response: The result of handling the request
    """
    return handler.handle(request)