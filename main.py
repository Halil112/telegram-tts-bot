from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from gtts import gTTS
import os

BOT_TOKEN = "5348986903:AAGLv5DCELLmXx5jYmPuU4PJpd1-bKlooeg"

# Kullanıcı dili kaydı
user_languages = {}

# Dil seçimi komutu
async def set_language(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [['🇬🇧 English', '🇹🇷 Türkçe', '🇪🇸 Español']]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
    await update.message.reply_text("Please choose a language / Lütfen bir dil seçin:", reply_markup=reply_markup)

# Dil ayarını al
async def handle_language_selection(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    text = update.message.text

    if 'English' in text:
        user_languages[user_id] = 'en'
        await update.message.reply_text("Language set to English.")
    elif 'Türkçe' in text:
        user_languages[user_id] = 'tr'
        await update.message.reply_text("Dil Türkçe olarak ayarlandı.")
    elif 'Español' in text:
        user_languages[user_id] = 'es'
        await update.message.reply_text("Idioma cambiado a español.")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Merhaba! Bana bir metin gönder, ses dosyasını sana çevireyim.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    tts = gTTS(text, lang='tr')
    file_path = f"{update.message.chat_id}_speech.mp3"
    tts.save(file_path)
    await update.message.reply_voice(voice=open(file_path, 'rb'))
    os.remove(file_path)

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

print("Bot çalışıyor...")
app.run_polling()

