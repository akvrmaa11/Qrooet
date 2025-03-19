import os
from dotenv import load_dotenv
import telebot
import google.generativeai as genai  # 🔹 Gemini API

# 🔹 .env फाइल से वैल्यू लोड करो
load_dotenv()

# 🔹 API Keys लोड करो
TELEGRAM_API_KEY = os.getenv("7695925870:AAFmdDWXPRNFNAi04Zwcr08-6kWl_2oxwKc")
GEMINI_API_KEY = os.getenv("AIzaSyARo-Y4EET4wWs1XT2z1pkO_ZWq99KGMow")

# 🚨 Debugging: Keys प्रिंट करो (Production में हटाना)
print(f"Loaded TELEGRAM_API_KEY: {TELEGRAM_API_KEY}")
print(f"Loaded GEMINI_API_KEY: {GEMINI_API_KEY}")

if TELEGRAM_API_KEY is None or TELEGRAM_API_KEY.strip() == "":
    print("🚨 TELEGRAM_API_KEY लोड नहीं हो रहा! Railway में Environment Variables चेक करो।")
    exit()

if GEMINI_API_KEY is None or GEMINI_API_KEY.strip() == "":
    print("🚨 GEMINI_API_KEY लोड नहीं हो रहा! Railway में Environment Variables चेक करो।")
    exit()

# ✅ अगर API Keys सही हैं, तो Bot स्टार्ट करो
bot = telebot.TeleBot(TELEGRAM_API_KEY)
genai.configure(api_key=GEMINI_API_KEY)

def get_gemini_response(user_input):
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(user_input)
    return response.text if response else "❌ कुछ गड़बड़ है, दोबारा कोशिश करें।"

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "👋 हेलो! मैं Qrooet बॉट हूँ। कोई भी सवाल पूछो!")

@bot.message_handler(func=lambda msg: True)
def chat_with_gemini(message):
    user_message = message.text
    bot.reply_to(message, "🤖 सोच रहा हूँ...")
    
    try:
        gemini_response = get_gemini_response(user_message)
        bot.reply_to(message, gemini_response)
    except Exception as e:
        bot.reply_to(message, "❌ कुछ गलत हो गया।")
        print(f"🚨 Error: {e}")

print("✅ Bot Successfully Started! Telegram पर /start भेजकर टेस्ट करो।")

# 🔹 Bot को चलाते रहो
bot.polling()
