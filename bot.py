import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters
from google import genai
from google.genai import types

BOT_TOKEN = os.getenv("BOT_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=GEMINI_API_KEY)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🎮 MLBB Maç Analiz Botu hazır.\n\n"
        "Maç sonu ekran görüntünü gönder."
    )


async def photo_received(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = await update.message.reply_text(
        "📸 Görüntü alındı.\n⏳ Maç analiz ediliyor..."
    )

    try:
        photo = update.message.photo[-1]

        file = await context.bot.get_file(photo.file_id)
        image_bytes = await file.download_as_bytearray()

        prompt = """
Bu bir Mobile Legends: Bang Bang (MLBB) maç sonu ekran görüntüsüdür.

Görüntüyü dikkatlice analiz et.

Mümkünse şunları tespit et:
- Oyuncunun hero'su
- K/D/A
- Gold
- Hasar
- Alınan hasar
- Turret/objective katkısı
- MVP durumu
- Maç sonucu
- Takım arkadaşlarının genel performansı
- Rakip takımın güçlü oyuncuları

Ardından Türkçe ve anlaşılır bir maç analizi oluştur.

Şu formatı kullan:

🎮 MLBB MAÇ ANALİZİ

🏆 Sonuç:
🦸 Hero:
⚔️ K/D/A:
⭐ Performans: X/10

✅ Güçlü yönler:
- ...

❌ Geliştirilmesi gerekenler:
- ...

🧠 Maçın değerlendirmesi:
...

🎯 Bir sonraki maç için:
- ...

Ekrüntüde okunamayan bir bilgi varsa tahmin etme.
"Okunamıyor" olarak belirt.
"""

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=[
                types.Part.from_bytes(
                    data=bytes(image_bytes),
                    mime_type="image/jpeg",
                ),
                prompt,
            ],
        )

        await message.edit_text(response.text)

    except Exception as e:
        print("HATA:", e)

        await message.edit_text(
            "❌ Analiz sırasında bir hata oluştu.\n\n"
            "Lütfen Railway Logs bölümünü kontrol et."
        )


def main():
    if not BOT_TOKEN:
        raise RuntimeError("BOT_TOKEN bulunamadı!")

    if not GEMINI_API_KEY:
        raise RuntimeError("GEMINI_API_KEY bulunamadı!")

    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.PHOTO, photo_received))

    print("🎮 MLBB analiz botu çalışıyor...")

    app.run_polling()


if __name__ == "__main__":
    main()
