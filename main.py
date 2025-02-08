import telebot
from deep_translator import GoogleTranslator
from dotenv import load_dotenv
import os
import logging
import sys

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("bot.log"),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)

user_language = {}

lang_flags = {
    'uz': '🇺🇿',
    'en': '🇬🇧',
    'ru': '🇷🇺'
}

@bot.message_handler(commands=['start'])
def start(message):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
    markup.add(
        telebot.types.KeyboardButton("🇺🇿 Uzbek"),
        telebot.types.KeyboardButton("🇬🇧 English"),
        telebot.types.KeyboardButton("🇷🇺 Russian")
    )
    text = "Assalomu alaykum! Tarjimon botga xush kelibsiz.\nTarjima qilish tilini tanlang:"
    bot.send_message(message.chat.id, text, reply_markup=markup)
    logger.info(f"Foydalanuvchi {message.chat.id} botni ishga tushirdi")

@bot.message_handler(content_types=['text'])
def handle_text(message):
    chat_id = message.chat.id

    if message.text in ["🇺🇿 Uzbek", "🇬🇧 English", "🇷🇺 Russian"]:
        if message.text == "🇺🇿 Uzbek":
            user_language[chat_id] = 'uz'
            response = "Tarjima qilish tili 🇺🇿 Uzbek o'zgartirildi"
        elif message.text == "🇬🇧 English":
            user_language[chat_id] = 'en'
            response = "Tarjima qilish tili 🇬🇧 English o'zgartirildi"
        else:
            user_language[chat_id] = 'ru'
            response = "Tarjima qilish tili 🇷🇺 Russian o'zgartirildi"

        bot.send_message(chat_id, response)
        logger.info(f"Foydalanuvchi {chat_id} tilni {user_language[chat_id]} ga o'zgartirdi")

    else:
        target_lang = user_language.get(chat_id, 'uz')
        try:
            translated = GoogleTranslator(source='auto', target=target_lang).translate(message.text)
            flag = lang_flags.get(target_lang, '🇺🇿')
            bot.reply_to(message, f"{flag} Tarjima:\n{translated}")
            logger.info(f"Tarjima qilindi: {message.text} -> {translated} ({target_lang})")
        except Exception as e:
            bot.reply_to(message, f"Xato yuz berdi: {e}\nQayta urinib ko'ring.")
            logger.error(f"Xato: {str(e)}")


if __name__ == "__main__":
    logger.info("Bot ishga tushdi...")
    bot.polling(none_stop=True)
