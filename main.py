from flask import Flask, request
import requests

app = Flask(__name__)

# ----------- تنظیمات ربات -----------
BOT_TOKEN = "BEBAFI0RPLLTDTXJNEOQRMLKZVYZTPRVCCNOJLWILPWIEFEJCZLNZOEZATGLZQPM"  # جایگزین توکن ربات روبیکا

# ----------- ارسال پیام به کاربر -----------
def send_message(chat_id, text):
    try:
        requests.get(
            f"https://api.robika.ir/bot{BOT_TOKEN}/sendMessage",
            params={"chat_id": chat_id, "text": text}
        )
    except Exception as e:
        print("ارسال پیام موفق نبود:", e)

# ----------- پاسخ ساده AI داخلی ----------
def ai_reply(question):
    # پاسخ ساده فارسی، بدون نیاز به API خارجی
    question = question.lower()
    if "سلام" in question:
        return "سلام! خوشحالم که با من چت می‌کنید 😊"
    elif "خوبی" in question:
        return "من خوبم، مرسی از شما! 😄"
    elif "ربات" in question:
        return "من ربات صواب AI هستم و آماده پاسخگویی به شما هستم 🤖"
    else:
        # اگر سوال ناشناخته بود، یک جواب پیشفرض بده
        return "متاسفم 😅 متوجه سوال شما نشدم، لطفاً دوباره امتحان کنید."

# ----------- webhook ----------
@app.route(f"/{BOT_TOKEN}", methods=['POST'])
def webhook():
    data = request.json
    if 'message' in data:
        chat_id = data['message']['chat']['id']
        text = data['message'].get('text', '')

        # ---------- دستورات ----------
        if text == "/start":
            reply = "🌟 سلام! خوش آمدید به ربات صواب AI.\nمن دستیار هوشمند شما هستم."
        elif text == "/help":
            reply = (
                "📖 راهنمای استفاده از ربات:\n"
                "/start - شروع ربات و خوش‌آمدگویی\n"
                "/help - راهنمای دستورات\n"
                "/ai [سوال شما] - پاسخ هوش مصنوعی داخلی\n"
                "/post [متن] - ساخت پست برای کانال"
            )
        elif text.startswith("/ai"):
            question = text[4:].strip()
            if question:
                reply = ai_reply(question)
            else:
                reply = "لطفاً بعد از /ai سوال خود را وارد کنید."
        elif text.startswith("/post"):
            content = text[6:].strip()
            if content:
                reply = f"📝 پست شما آماده شد: {content}"
            else:
                reply = "لطفاً بعد از /post متن پست را وارد کنید."
        else:
            reply = "❌ دستور نامعتبر. لطفاً /help را امتحان کنید."

        send_message(chat_id, reply)
    return "ok"

# ----------- اجرای سرور ----------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)