import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters

TOKEN = os.getenv("BOT_TOKEN")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🎮 MLBB Maç Analiz Botu hazır.\n\n"
        "Maç sonu ekran görüntünü gönder."
    )


async def photo_received(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📸 Maç ekran görüntüsü alındı.\n\n"
        "⏳ Görüntü analiz sistemi hazırlanıyor..."
    )


def main():
    if not TOKEN:
        raise RuntimeError("BOT_TOKEN bulunamadı!")

    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.PHOTO, photo_received))

    print("🎮 MLBB analiz botu çalışıyor...")
    app.run_polling()


if __name__ == "__main__":
    main()
