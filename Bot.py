from flask import Flask
import telebot
import os
from dotenv import load_dotenv

load_dotenv()
API_TOKEN = os.getenv("BOT_TOKEN")

OWNER_ID = 7752955793
MANDATORY_CHANNELS = ["@DARKN80", "@Darkn8botmaker"]

bot = telebot.TeleBot(API_TOKEN)
user_bots = {}

app = Flask(__name__)

@app.route('/')
def home():
    return "🤖 Bot is alive!"

@app.route('/health')
def health_check():
    return "✅ OK", 200

def has_joined_all_channels(user_id):
    for channel in MANDATORY_CHANNELS:
        try:
            member = bot.get_chat_member(channel, user_id)
            if member.status not in ['member', 'administrator', 'creator']:
                return False
        except:
            return False
    return True

@bot.message_handler(commands=['start'])
def send_start(message):
    chat_id = message.chat.id
    welcome_text = (
        "🤗 <b>Welcome to DARKN8 BotMaker</b>\n\n"
        "Create and build free Telegram bots here!\n\n"
        "👉 Join our official channels first to continue."
    )
    markup = telebot.types.InlineKeyboardMarkup()
    markup.add(telebot.types.InlineKeyboardButton("📢 Channel 1", url="https://t.me/DARKN80"))
    markup.add(telebot.types.InlineKeyboardButton("📢 Channel 2", url="https://t.me/Darkn8botmaker"))
    markup.add(telebot.types.InlineKeyboardButton("✅ Joined", callback_data="joined"))

    bot.send_message(chat_id, welcome_text, parse_mode="HTML", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == "joined")
def check_joined_channels(call):
    user_id = call.from_user.id
    chat_id = call.message.chat.id

    if has_joined_all_channels(user_id):
        menu = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
        menu.row("📦 Create Bot", "🤖 My Bots")
        menu.row("🛠️ Tools", "📢 Promotion", "🗑 Delete Bot")
        bot.send_message(chat_id, "✅ Access granted! Choose an option below.", reply_markup=menu)
    else:
        bot.answer_callback_query(call.id, "❗ Please join all required channels first.", show_alert=True)

@bot.message_handler(func=lambda message: True)
def handle_text(message):
    user_id = message.from_user.id
    chat_id = message.chat.id
    text = message.text.strip()

    if text == "📦 Create Bot":
        bot.send_message(chat_id, "🔧 Choose a template first.")

    elif text == "🤖 My Bots":
        bots = user_bots.get(user_id, [])
        if not bots:
            bot.send_message(chat_id, "😕 You haven't created any bots yet.")
        else:
            markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
            markup.row("🔙 Back to Menu")
            for botname in bots:
                markup.row(f"🗑 Delete {botname}")
            bot.send_message(chat_id, "🤖 Your Bots:", reply_markup=markup)

    elif text.startswith("🗑 Delete"):
        botname = text.split("🗑 Delete ")[-1].strip()
        if user_id in user_bots and botname in user_bots[user_id]:
            user_bots[user_id].remove(botname)
            bot.send_message(chat_id, f"✅ {botname} deleted.")
        else:
            bot.send_message(chat_id, "❌ Bot not found.")

    elif text == "🛠️ Tools":
        bot.send_message(chat_id, "🔧 Tools:\n1️⃣ Remove Forward Tag ➡ @forwardtag0bot")

    elif text == "📢 Promotion":
        bot.send_message(chat_id, "📢 Free Promotion Available!\nDM @DARKN8002 with proof of funds.")

    elif text == "🔙 Back to Menu":
        menu = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
        menu.row("📦 Create Bot", "🤖 My Bots")
        menu.row("🛠️ Tools", "📢 Promotion", "🗑 Delete Bot")
        bot.send_message(chat_id, "👋 Back to main menu:", reply_markup=menu)

# Start the Flask app and bot polling
if __name__ == "__main__":
    import threading

    def run_bot():
        print("🤖 Bot polling started...")
        bot.infinity_polling()

    def run_flask():
        print("🌐 Flask uptime server running...")
        app.run(host="0.0.0.0", port=10000)

    threading.Thread(target=run_bot).start()
    threading.Thread(target=run_flask).start()
