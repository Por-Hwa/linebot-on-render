import os
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

# 從環境變數讀取 Channel Token 和 Secret
LINE_TOKEN = os.getenv("LINE_TOKEN")
LINE_SECRET = os.getenv("LINE_SECRET")

app = Flask(__name__)
line_bot_api = LineBotApi(LINE_TOKEN)
handler = WebhookHandler(LINE_SECRET)

@app.route("/")
def index():
    return "Line Bot is running!"

@app.route("/callback", methods=['POST'])
def callback():
    # 確認 LINE Signature
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    incoming_text = event.message.text.lower()
    reply = "您說的是：" + incoming_text
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=reply)
    )

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)


    # ✅ 顯示圖片：蛋白質對照圖
    if "蛋白質對照" in user_input:
        image1 = ImageSendMessage(
            original_content_url='https://i.postimg.cc/ZRh7McZd/1.png',
            preview_image_url='https://i.postimg.cc/ZRh7McZd/1.png'
        )
        image2 = ImageSendMessage(
            original_content_url='https://i.postimg.cc/tTZCp73n/0713-2.png',
            preview_image_url='https://i.postimg.cc/tTZCp73n/0713-2.png'
        )
        line_bot_api.reply_message(event.reply_token, [image1, image2])
        return

    # ✅ Inbody 圖片顯示
    if any(k in user_input for k in ["inbody", "身理指數介紹"]):
        urls = [
            'https://i.postimg.cc/Xq9txZm9/1.png',
            'https://i.postimg.cc/9fGTmC6J/2.png',
            'https://i.postimg.cc/dQ7C3Rch/3.png',
            'https://i.postimg.cc/pXfp5qGL/4.png',
            'https://i.postimg.cc/C1nKhNnY/5.png'
        ]
        images = [ImageSendMessage(original_content_url=url, preview_image_url=url) for url in urls]
        line_bot_api.reply_message(event.reply_token, images)
        return

    # ✅ 疲勞衰弱介紹圖片
    if "介紹" in user_input:
        urls = [
            'https://i.postimg.cc/kGxX8gyp/Inbody1.png',
            'https://i.postimg.cc/hG6S5dyY/Inbody2.png',
            'https://i.postimg.cc/h49S2h9C/Inbody3.png',
            'https://i.postimg.cc/Vv1PxBjK/Inbody4.png',
            'https://i.postimg.cc/pTbwjY1P/Inbody5.png'
        ]
        images = [ImageSendMessage(original_content_url=url, preview_image_url=url) for url in urls]
        line_bot_api.reply_message(event.reply_token, images)
        return

    # ✅ 判斷與回應邏輯
    food_units = ["肉", "蛋", "豆", "豆漿", "喝", "吃", "湯", "飲", "cc", "ml", "罐", "瓶", "片", "份", "包", "塊", "匙", "條", "球"]
    if re.search(r"\d+.*蛋白質", user_input):
        reply = "已記錄您今天攝取的蛋白質。"
    elif any(k in user_input for k in ["你好", "體重"]):
        reply = "您好，請輸入您的體重（公斤），我會幫您計算高蛋白飲食中，每日所需的蛋白質份數。"
    elif any(k in user_input for k in ["量表", "衰弱疲勞評估", "每日蛋白質紀錄", "問卷"]):
        reply = "需填寫表單：\n1.衰弱疲勞評估量表(一週一次)\n連結：https://forms.gle/NHG9k7qjEiaBwDGF7\n\n2.每日蛋白質紀錄量表\n連結：https://forms.gle/uNtt1y9SYGBYGN9N7"
    else:
        match = re.search(r"(\d+\.?\d*)", user_input)
        if match:
            number = float(match.group())

            if re.fullmatch(r"\d+\.?\d*", user_input):
                if number >= 40:
                    protein_portion = int((number * 1.2) / 7)
                    reply = f"建議您的每日蛋白質攝取為 {protein_portion} 份。"
                else:
                    reply = f"已記錄您今天攝取 {number} 份蛋白質。"
            elif any(k in user_input for k in food_units):
                reply = "已記錄您今天攝取的蛋白質。"
        else:
            reply = "請輸入體重（公斤）或蛋白質攝取情形，例如：70、喝了300cc豆漿、吃了2份肉等。"

    if reply:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply))

# ✅ 啟動伺服器
if __name__ == "__main__":
    app.run()
