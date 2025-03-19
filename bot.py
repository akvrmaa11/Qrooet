import telebot
import google.generativeai as genai
import os

# 🔑 API Keys
TELEGRAM_API_KEY = os.getenv("7695925870:AAFmdDWXPRNFNAi04Zwcr08-6kWl_2oxwKc")  # Railway में सेट करना
GEMINI_API_KEY = os.getenv("AIzaSyARo-Y4EET4wWs1XT2z1pkO_ZWq99KGMow")  # Railway में सेट करना

# 🚀 Telegram Bot Init
bot = telebot.TeleBot(TELEGRAM_API_KEY)

# 🎯 Gemini AI Init
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-pro")

# 🛠 Admin Group Chat ID (तुम्हारे ग्रुप में डिटेल भेजेगा)
ADMIN_GROUP_CHAT_ID = -4726359058  # **यही ID जो तुमने दी थी**

# 🎯 AI से Response लेने का Function
def get_ai_response(prompt):
    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return "अरे भाई! कुछ गड़बड़ हो गई, फिर से पूछ ना! 😂"

# 📩 जब कोई मैसेज भेजे
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    user_text = message.text
    user_id = message.from_user.id
    first_name = message.from_user.first_name
    username = message.from_user.username if message.from_user.username else "N/A"

    # 🎯 Gemini AI से Reply लो
    response = get_ai_response(user_text)
    bot.reply_to(message, response)

    # 📌 **हर यूजर की डिटेल ग्रुप में भेजो**
    user_info = f"👤 **New User Interaction** 👤\n\n"
    user_info += f"🆔 **User ID:** `{user_id}`\n"
    user_info += f"👤 **Name:** {first_name}\n"
    user_info += f"🔗 **Username:** @{username}\n"
    user_info += f"💬 **Message:** `{message.text}`\n\n"
    user_info += f"🚀 **Bot से बात कर रहा है!** 😎🔥"

    bot.send_message(ADMIN_GROUP_CHAT_ID, user_info, parse_mode="Markdown")

# 🚀 Bot Start
print("✅ Bot चालू हो गया!")
bot.polling(none_stop=True, interval=0)
