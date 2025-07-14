from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, ImageSendMessage
import os
import re

app = Flask(__name__)

# ✅ 使用環境變數讀取 LINE 機器人 token 與 secret
LINE_CHANNEL_ACCESS_TOKEN = os.environ.get("LINE_TOKEN")
LINE_CHANNEL_SECRET = os.environ.get("LINE_SECRET")

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

@app.route("/callback", methods=['POST'])
def callback():
    # 取得 X-Line-Signature 標頭值
    signature = request.headers['X-Line-Signature']

    # 取得請求內容主體
    body = request.get_data(as_text=True)

    try:
        # 驗證簽名並處理事件
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    msg = event.message.text
    response = None

    # 圖片連結（記得之後換成自己的）
    protein_images = [
        "https://i.imgur.com/9f3pO0p.jpg",  # 蛋白質對照圖1
        "https://i.imgur.com/4CJ8KfF.jpg"   # 蛋白質對照圖2
    ]
    inbody_images = [
        "https://i.imgur.com/a1.jpg",  # 範例：Inbody 圖片1
        "https://i.imgur.com/a2.jpg",
        "https://i.imgur.com/a3.jpg",
        "https://i.imgur.com/a4.jpg",
        "https://i.imgur.com/a5.jpg"
    ]
    intro_images = inbody_images  # 同用一組圖片，也可改為其他網址

    # 自動回應邏輯
    if "蛋白質對照圖" in msg or "蛋白質對照" in msg:
        for img_url in protein_images:
            line_bot_api.reply_message(event.reply_token, ImageSendMessage(original_content_url=img_url, preview_image_url=img_url))
        return

    if "Inbody" in msg or "身理指數介紹" in msg:
        for img_url in inbody_images:
            line_bot_api.reply_message(event.reply_token, ImageSendMessage(original_content_url=img_url, preview_image_url=img_url))
        return

    if "介紹" in msg:
        for img_url in intro_images:
            line_bot_api.reply_message(event.reply_token, ImageSendMessage(original_content_url=img_url, preview_image_url=img_url))
        return

    if "量表" in msg or "衰弱疲勞評估" in msg:
        form_url = "https://example.com/form"  # 替換為實際表單連結
        response = TextSendMessage(text=f"這是您的衰弱評估量表連結：\n{form_url}")

    elif "每日蛋白質紀錄" in msg:
        record_url = "https://example.com/record"  # 替換為實際紀錄連結
        response = TextSendMessage(text=f"每日蛋白質紀錄表單：\n{record_url}")

    elif re.search(r"[0-9]+", msg) and ("蛋白質" in msg or "克" in msg or "g" in msg.lower()):
        number = re.search(r"[0-9]+", msg).group()
        response = TextSendMessage(text=f"已記錄：蛋白質攝取 {number} 克。")

    elif "你好" in msg or "體重" in msg:
        response = TextSendMessage(text="請輸入您的體重，我將幫您計算每日蛋白質建議攝取量。")

    else:
        response = TextSendMessage(text="請輸入蛋白質攝取量、查看蛋白質對照圖或輸入『介紹』來獲得更多資訊。")

    if response:
        line_bot_api.reply_message(event.reply_token, response)

# 本地測試時用，部署上雲端會由平台指定 port
if __name__ == "__main__":
    app.run()
