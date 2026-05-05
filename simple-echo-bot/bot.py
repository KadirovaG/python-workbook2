# bot.py
import os

from dotenv import load_dotenv
from storage import JsonStorage
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

load_dotenv()


class EchoBot:
    """A Telegram bot that echoes every text message back to the sender."""

    def __init__(self) -> None:
        self.token = os.getenv("BOT_TOKEN")
        self.storage = JsonStorage()
        self.app = Application.builder().token(self.token).build()
        self._register_handlers()

    def _register_handlers(self) -> None:
        """Attach command and message handlers to the application."""
        self.app.add_handler(CommandHandler("start", self._handle_start))
        self.app.add_handler(
            MessageHandler(filters.TEXT & ~filters.COMMAND, self._handle_message)
        )

    async def _handle_start(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> None:
        """/start — introduce the bot."""
        username = update.effective_user.username or update.effective_user.first_name
        self.storage.save(
            chat_id=update.effective_chat.id,
            username=username,
            text=update.message.text,
        )
        await update.message.reply_text(
            "Bot is running. Send any message and it will be echoed back."
        )

    async def _handle_message(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> None:
        """Echo any plain text message back to the sender and save it."""
        username = update.effective_user.username or update.effective_user.first_name
        text = update.message.text

        self.storage.save(
            chat_id=update.effective_chat.id,
            username=username,
            text=text,
        )

        await update.message.reply_text(f"You said: {text}")

    def run(self) -> None:
        """Start the bot using long polling."""
        print(f"Bot started. Messages are saved to: {self.storage.filepath}")
        print("Press Ctrl+C to stop.")
        self.app.run_polling()
