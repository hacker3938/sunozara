import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler, ContextTypes, filters

BOT_TOKEN = os.getenv("7409757167:AAF8WPU0KHv83Qkf2QFXTMfvDbqvxIO1WQI")
GROUP_CHAT_ID = int(os.getenv("1002396195406"))

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👀 Tell me your secret anonymously...")

async def handle_confession(update: Update, context: ContextTypes.DEFAULT_TYPE):
    confession = update.message.text
    context.user_data["confession"] = confession

    keyboard = [
        [InlineKeyboardButton("✅ Yes, send", callback_data="send"),
         InlineKeyboardButton("❌ Cancel", callback_data="cancel")]
    ]
    await update.message.reply_text("Send this anonymously to group?", reply_markup=InlineKeyboardMarkup(keyboard))

async def handle_decision(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "send":
        confession = context.user_data.get("confession")
        if confession:
            await context.bot.send_message(
                chat_id=GROUP_CHAT_ID,
                text=f"🕊️ *Anonymous Confession:*

_{confession}_",
                parse_mode="Markdown"
            )
            await query.edit_message_text("✅ Sent anonymously!")
    else:
        await query.edit_message_text("❌ Cancelled.")

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_confession))
    app.add_handler(CallbackQueryHandler(handle_decision))
    app.run_polling()

if __name__ == "__main__":
    main()
