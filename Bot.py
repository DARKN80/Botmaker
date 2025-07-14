import os
from dotenv import load_dotenv
import telebot
from telebot import types

# Load environment variables
load_dotenv()
API_TOKEN = os.getenv("BOT_TOKEN")

OWNER_ID = 7752955793
MANDATORY_CHANNELS = ["@DARKN80", "@Darkn8botmaker"]

bot = telebot.TeleBot(API_TOKEN)

# Dictionary to store user's created bots
user_bots = {}

print("🤖 Bot is running...")

# --- Function to check if user joined required channels ---
def has_joined_all_channels(user_id):
    for channel in MANDATORY_CHANNELS:
        try:
            member = bot.get_chat_member(channel, user_id)
            if member.status not in ['member', 'administrator', 'creator']:
                return False
        except:
            return False
    return True

# --- START Command ---
@bot.message_handler(commands=['start'])
def send_start(message):
    chat_id = message.chat.id

    welcome_text = (
        "🤗 <b>Welcome to DARKN8 BotMaker bot</b>\n\n"
        "Create And Build Free Telegram Bots Here\n\n"
        "Now, Join Our Official Channels."
    )

    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("📢 OFFICIAL CHANNEL 1", url="https://t.me/DARKN80"))
    markup.add(types.InlineKeyboardButton("📢 OFFICIAL CHANNEL 2", url="https://t.me/Darkn8botmaker"))
    markup.add(types.InlineKeyboardButton("✅ Joined", callback_data="joined"))

    bot.send_message(chat_id, welcome_text, parse_mode="HTML", reply_markup=markup)

# --- JOINED Button ---
@bot.callback_query_handler(func=lambda call: call.data == "joined")
def check_joined_channels(call):
    user_id = call.from_user.id
    chat_id = call.message.chat.id

    if has_joined_all_channels(user_id):
        menu = types.ReplyKeyboardMarkup(resize_keyboard=True)
        menu.row("📦 Create Bot", "🤖 My Bots")
        menu.row("🛠️ Tools", "📢 Promotion", "🗑 Delete Bot")
        bot.send_message(chat_id, "✅ Access granted! You're in. Choose an option below.", reply_markup=menu)
    else:
        bot.answer_callback_query(call.id, "❗ Please make sure you've joined all channels.", show_alert=True)

# --- Handle all Button Text Commands ---
@bot.message_handler(func=lambda message: True)
def handle_text(message):
    user_id = message.from_user.id
    chat_id = message.chat.id
    text = message.text.strip()

    if text == "📦 Create Bot":
        # Ask user to choose a template
        bot.send_message(chat_id, "🧾 Choose a template:", reply_markup=template_menu())

    elif text == "🤖 My Bots":
        bots = user_bots.get(user_id, [])
        if not bots:
            bot.send_message(chat_id, "😕 You haven't created any bots yet.")
        else:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            markup.row("🔙 Back to Menu")
            for botname in bots:
                markup.row(f"🗑 Delete {botname}")
            bot.send_message(chat_id, "🤖 Your Bots:", reply_markup=markup)

    elif text.startswith("🗑 Delete"):
        botname = text.split("🗑 Delete ")[-1].strip()
        if user_id in user_bots and botname in user_bots[user_id]:
            user_bots[user_id].remove(botname)
            bot.send_message(chat_id, f"✅ {botname} has been deleted.")
        else:
            bot.send_message(chat_id, "❌ Bot not found.")

    elif text == "🛠️ Tools":
        bot.send_message(chat_id, "🧰 Tools:\n• Remove Forward Tag ➡ @forwardtag0bot")

    elif text == "📢 Promotion":
        bot.send_message(chat_id, "📢 Free Promotion Available!\nDM @DARKN8002 with proof of funds.")

    elif text == "🔙 Back to Menu":
        menu = types.ReplyKeyboardMarkup(resize_keyboard=True)
        menu.row("📦 Create Bot", "🤖 My Bots")
        menu.row("🛠️ Tools", "📢 Promotion", "🗑 Delete Bot")
        bot.send_message(chat_id, "🔘 Back to main menu:", reply_markup=menu)

# --- Handle Template Button Clicks ---
@bot.callback_query_handler(func=lambda call: call.data.startswith("template_"))
def handle_template_choice(call):
    user_id = call.from_user.id
    chat_id = call.message.chat.id
    bot.send_message(chat_id, "🧾 Send your BotFather API token here:")
    bot.register_next_step_handler(call.message, handle_token_submission)

# --- Token Submission Handler ---
def handle_token_submission(message):
    token = message.text.strip()
    user_id = message.from_user.id
    chat_id = message.chat.id

    if not has_joined_all_channels(user_id):
        bot.send_message(chat_id, "❗ You must join all required channels before creating a bot.")
        return

    if len(token.split(":")) != 2:
        bot.send_message(chat_id, "❌ Invalid token format.")
        return

    try:
        new_bot = telebot.TeleBot(token)
        me = new_bot.get_me()
        bot_username = f"@{me.username}"

        if user_id not in user_bots:
            user_bots[user_id] = []

        if bot_username in user_bots[user_id]:
            bot.send_message(chat_id, f"⚠️ Bot {bot_username} already exists.")
            return

        user_bots[user_id].append(bot_username)
        bot.send_message(chat_id, f"✅ Bot created: {bot_username}\nSend /adminaccess in your bot to configure.")

    except Exception as e:
        bot.send_message(chat_id, f"❌ Error: {str(e)}")

# --- Template Selector Menu ---
def template_menu():
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.row(
        types.InlineKeyboardButton("🎨 Template 1", callback_data='template_1'),
        types.InlineKeyboardButton("🔍 View", url="https://example.com/template1")
    )
    markup.row(
        types.InlineKeyboardButton("🎨 Template 2", callback_data='template_2'),
        types.InlineKeyboardButton("🔍 View", url="https://example.com/template2")
    )
    markup.row(
        types.InlineKeyboardButton("🎨 Template 3", callback_data='template_3'),
        types.InlineKeyboardButton("🔍 View", url="https://example.com/template3")
    )
    markup.row(
        types.InlineKeyboardButton("🎨 Template 4", callback_data='template_4'),
        types.InlineKeyboardButton("🔍 View", url="https://example.com/template4")
    )
    return markup

# --- Start the bot ---
bot.infinity_polling()
