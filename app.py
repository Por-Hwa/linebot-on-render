import os
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, ImageSendMessage
)

app = Flask(__name__)

# ✅ 讀取環境變數
LINE_TOKEN = os.getenv("LINE_TOKEN")
LINE_SECRET = os.getenv("LINE_SECRET")

line_bot_api = LineBotApi(LINE_TOKEN)
handler = WebhookHandler(LINE_SECRET)

@app.route("/")
def home():
    return "LINE Bot is running!"

@app.route("/callback", methods=["POST"])
def callback():
    signature = request.headers["X-Line-Signature"]
    body = request.get_data(as_text=True)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return "OK"

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    msg = event.message.text.lower()

    if "蛋白質對照圖" in msg or "蛋白質對照" in msg:
        img1 = ImageSendMessage(
            original_content_url="https://i.imgur.com/u5kG7sN.jpg",
            preview_image_url="https://i.imgur.com/u5kG7sN.jpg"
        )
        img2 = ImageSendMessage(
            original_content_url="https://i.imgur.com/yiVgA7L.jpg",
            preview_image_url="https://i.imgur.com/yiVgA7L.jpg"
        )
        line_bot_api.reply_message(event.reply_token, [img1, img2])

    elif "你好" in msg or "體重" in msg:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="建議蛋白質攝取量：每公斤體重 × 1.2~2.0 公克")
        )

    elif "量表" in msg or "衰弱疲勞評估" in msg or "每日蛋白質紀錄" in msg:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="📋 表單連結：\n\n- 衰弱疲勞評估：https://forms.gle/xxxxxx\n- 每日蛋白質紀錄：https://forms.gle/yyyyyy")
        )

    elif "inbody" in msg or "身理指數介紹" in msg:
        image_urls = [f"https://i.imgur.com/{code}.jpg" for code in ["1", "2", "3", "4", "5"]]
        messages = [ImageSendMessage(original_content_url=url, preview_image_url=url) for url in image_urls]
        line_bot_api.reply_message(event.reply_token, messages)

    elif "介紹" in msg:
        fatigue_urls = [f"https://i.imgur.com/f{i}.jpg" for i in range(1, 6)]
        messages = [ImageSendMessage(original_content_url=url, preview_image_url=url) for url in fatigue_urls]
        line_bot_api.reply_message(event.reply_token, messages)

    else:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=f"收到訊息：{msg}")
        )

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
