from __future__ import annotations

import os

from dotenv import load_dotenv
from flask import Flask, abort, request
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

from analysis.engine import analyze_dialogue


load_dotenv()

app = Flask(__name__)

line_bot_api: LineBotApi | None = None
handler: WebhookHandler | None = None


def get_line_clients() -> tuple[LineBotApi, WebhookHandler]:
    global line_bot_api, handler

    if line_bot_api and handler:
        return line_bot_api, handler

    access_token = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")
    channel_secret = os.getenv("LINE_CHANNEL_SECRET")
    if not access_token or not channel_secret:
        raise RuntimeError("LINE_CHANNEL_ACCESS_TOKEN and LINE_CHANNEL_SECRET are required.")

    line_bot_api = LineBotApi(access_token)
    handler = WebhookHandler(channel_secret)
    register_handlers(handler)
    return line_bot_api, handler


@app.get("/")
def health_check() -> tuple[str, int]:
    return "trip_assistant_bot is running", 200


@app.get("/favicon.ico")
def favicon() -> tuple[str, int]:
    return "", 204


@app.post("/callback")
def callback() -> str:
    _, webhook_handler = get_line_clients()
    signature = request.headers.get("X-Line-Signature", "")
    body = request.get_data(as_text=True)

    try:
        webhook_handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return "OK"


def register_handlers(webhook_handler: WebhookHandler) -> None:
    @webhook_handler.add(MessageEvent, message=TextMessage)
    def handle_text_message(event: MessageEvent) -> None:
        api, _ = get_line_clients()
        result = analyze_dialogue(event.message.text)

        if not result.should_intervene:
            return

        reply_text = result.intermediate_reply if result.requires_external_search else result.suggested_reply
        if not reply_text:
            reply_text = result.suggested_reply or "I am checking this for you."

        api.reply_message(event.reply_token, TextSendMessage(text=reply_text))


if __name__ == "__main__":
    host = os.environ.get("HOST", "127.0.0.1")
    port = int(os.environ.get("PORT", "5000"))
    app.run(host=host, port=port)
