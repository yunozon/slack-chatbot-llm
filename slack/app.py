import os
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from slack_bolt import App
from slack_bolt.adapter.flask import SlackRequestHandler
from dotenv import find_dotenv, load_dotenv
from flask import Flask, request
import functions # 関数をインポート

# .envファイルから環境変数を読み込む
load_dotenv(find_dotenv())

SLACK_BOT_TOKEN = os.environ["SLACK_BOT_TOKEN"]
SLACK_SIGNING_SECRET = os.environ["SLACK_SIGNING_SECRET"]
SLACK_BOT_USER_ID = os.environ["SLACK_BOT_USER_ID"]
OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]

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

@app.event("app_mention")
def handle_mentions(body, say):
    """
    Slack内でBotがメンションされたときの処理を行う関数
    メンションされたとき、メッセージを受け取り、draft_email関数を使ってメールの下書きを作成する。

    Args:
        body (dict): Slackイベント情報
        say (function): Slackにメッセージを送信する関数
    """
    text = body["event"]["text"]

    mention = f"<@{SLACK_BOT_USER_ID}>"
    text = text.replace(mention, "").strip() # textでmentionが含まれているので、mentionを削除
    response = functions.draft_email_with_gemini(text) # geminiでのメール下書き
    # response = functions.draft_email_with_chatgpt(text) # chatgptでのメール下書き
    # AIMessageオブジェクトからテキストを取得
    response_text = response.content if hasattr(response, 'content') else str(response)
    say(response_text)

@flask_app.route("/slack/events", methods=["POST"])
def slack_events():
    """
    Route for handling Slack events.
    This function passes the income HTTP request to the SlackRequestHandler for processing.

    Returns:
        Response: The result of handling the request
    """
    return handler.handle(request)

# Run Flask app
if __name__ == "__main__":
    flask_app.run(port=3000)