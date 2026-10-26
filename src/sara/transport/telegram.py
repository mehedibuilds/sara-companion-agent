from telegram import Update
from telegram.ext import Application, ContextTypes, MessageHandler, filters
from sara.models import Turn

def build_telegram_app(token: str, graph):
    app = Application.builder().token(token).build()
    async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        message, user = update.effective_message, update.effective_user
        if message is None or user is None or not message.text:
            return
        state: Turn = {"chat_id": message.chat_id, "user_id": user.id, "text": message.text}
        result = await graph.ainvoke(state)
        await message.reply_text(result["response"])
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    return app