import asyncio
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from openai import AsyncOpenAI

# اینجا توکن ربات تلگرام و کلید OpenAI رو وارد کن
TELEGRAM_TOKEN = "7156009984:AAFqU7EIjCE47ZYYETn1VXcrwNCVZQdHZsM"
OPENAI_API_KEY = "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"

# لاگ گیری فعال
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ساخت کلاینت OpenAI
client = AsyncOpenAI(api_key=OPENAI_API_KEY)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("سلام! 🎯 من ربات چت هوشمند هستم.\nهر سوالی داری بپرس!")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    try:
        response = await client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": user_message}]
        )
        bot_reply = response.choices[0].message.content
        await update.message.reply_text(bot_reply)
    except Exception as e:
        logger.error(f"خطا در ارتباط با OpenAI: {e}")
        await update.message.reply_text("متاسفم، مشکلی پیش آمد. لطفا دوباره تلاش کنید.")

async def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    await app.initialize()
    await app.start()
    logger.info("ربات با موفقیت اجرا شد ✅")
    await app.updater.start_polling()
    await asyncio.Event().wait()  # برای اجرای مداوم

if __name__ == '__main__':
    asyncio.run(main())
