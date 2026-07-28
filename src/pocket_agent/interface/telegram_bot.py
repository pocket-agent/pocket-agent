import logging

from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

from pocket_agent.core.agent import AgentCore
from pocket_agent.config.models import AppSettings

logger = logging.getLogger(__name__)


class TelegramBot:
    def __init__(self, settings: AppSettings, agent: AgentCore) -> None:
        self._settings = settings
        self._agent = agent
        self._app: Application | None = None

    def build_application(self) -> Application:
        token = self._settings.telegram_bot_token
        if not token:
            raise ValueError("TELEGRAM_BOT_TOKEN is required")

        app = Application.builder().token(token).build()
        app.add_handler(CommandHandler("start", self._on_start))
        app.add_handler(CommandHandler("help", self._on_help))
        app.add_handler(CommandHandler("nas", self._on_nas))
        app.add_handler(CommandHandler("index", self._on_index))
        app.add_handler(CommandHandler("search", self._on_search))
        app.add_handler(CommandHandler("read", self._on_read))
        app.add_handler(CommandHandler("pdf", self._on_pdf))
        app.add_handler(CommandHandler("excel", self._on_excel))
        app.add_handler(CommandHandler("edit_excel", self._on_edit_excel))
        app.add_handler(CommandHandler("edit_word", self._on_edit_word))
        app.add_handler(CommandHandler("edit_pdf", self._on_edit_pdf))
        app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self._on_message))
        self._app = app
        return app

    def _is_allowed(self, user_id: int) -> bool:
        allowed = self._settings.allowed_user_ids()
        if not allowed:
            return False
        return user_id in allowed

    async def _on_start(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        if not update.effective_user or not update.message:
            return
        if not self._is_allowed(update.effective_user.id):
            await update.message.reply_text("Access denied.")
            return
        await update.message.reply_text(
            "Pocket Agent online.\n"
            "Use /help for commands or send a message for LLM assistance."
        )

    async def _on_help(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        if not update.effective_user or not update.message:
            return
        if not self._is_allowed(update.effective_user.id):
            await update.message.reply_text("Access denied.")
            return
        await update.message.reply_text(
            "Commands:\n"
            "/index — rebuild file index on NAS\n"
            "/nas — list files at NAS root\n"
            "/search <query> — search indexed files\n"
            "/read <path> — read TXT, DOCX, PDF, XLSX summary\n"
            "/pdf <path> — extract PDF text\n"
            "/excel <path> — analyze Excel workbook\n"
            "/edit_excel <path> <sheet> <cell>=<value> — safe cell edit\n"
            "/edit_word <path> append <text> — append paragraph\n"
            "/edit_word <path> replace_last <text> — replace last paragraph\n"
            "/edit_pdf <path> add_page <text> — add PDF page with text\n"
            "/help — this message\n\n"
            "Or send any message for LLM assistance."
        )

    async def _on_nas(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        if not update.effective_user or not update.message:
            return
        if not self._is_allowed(update.effective_user.id):
            await update.message.reply_text("Access denied.")
            return
        reply = await self._agent.handle_message("/nas", chat_id=update.effective_chat.id)
        await update.message.reply_text(reply)

    async def _on_search(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        if not update.effective_user or not update.message:
            return
        if not self._is_allowed(update.effective_user.id):
            await update.message.reply_text("Access denied.")
            return
        query = " ".join(context.args).strip()
        if not query:
            await update.message.reply_text("Usage: /search <query>")
            return
        reply = await self._agent.handle_message(
            f"/search {query}",
            chat_id=update.effective_chat.id,
        )
        await update.message.reply_text(reply)

    async def _on_index(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        if not update.effective_user or not update.message:
            return
        if not self._is_allowed(update.effective_user.id):
            await update.message.reply_text("Access denied.")
            return
        reply = await self._agent.handle_message("/index", chat_id=update.effective_chat.id)
        await update.message.reply_text(reply)

    async def _on_read(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        if not update.effective_user or not update.message:
            return
        if not self._is_allowed(update.effective_user.id):
            await update.message.reply_text("Access denied.")
            return
        path = " ".join(context.args).strip()
        if not path:
            await update.message.reply_text("Usage: /read <path>")
            return
        reply = await self._agent.handle_message(
            f"/read {path}",
            chat_id=update.effective_chat.id,
        )
        await update.message.reply_text(reply)

    async def _on_pdf(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        if not update.effective_user or not update.message:
            return
        if not self._is_allowed(update.effective_user.id):
            await update.message.reply_text("Access denied.")
            return
        path = " ".join(context.args).strip()
        if not path:
            await update.message.reply_text("Usage: /pdf <path>")
            return
        reply = await self._agent.handle_message(
            f"/pdf {path}",
            chat_id=update.effective_chat.id,
        )
        await update.message.reply_text(reply)

    async def _on_excel(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        if not update.effective_user or not update.message:
            return
        if not self._is_allowed(update.effective_user.id):
            await update.message.reply_text("Access denied.")
            return
        path = " ".join(context.args).strip()
        if not path:
            await update.message.reply_text("Usage: /excel <path>")
            return
        reply = await self._agent.handle_message(
            f"/excel {path}",
            chat_id=update.effective_chat.id,
        )
        await update.message.reply_text(reply)

    async def _on_edit_excel(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        if not update.effective_user or not update.message:
            return
        if not self._is_allowed(update.effective_user.id):
            await update.message.reply_text("Access denied.")
            return
        if len(context.args) < 3:
            await update.message.reply_text("Usage: /edit_excel <path> <sheet> <cell>=<value>")
            return
        text = f"/edit_excel {' '.join(context.args)}"
        reply = await self._agent.handle_message(text, chat_id=update.effective_chat.id)
        await update.message.reply_text(reply)

    async def _on_edit_word(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        if not update.effective_user or not update.message:
            return
        if not self._is_allowed(update.effective_user.id):
            await update.message.reply_text("Access denied.")
            return
        if len(context.args) < 3:
            await update.message.reply_text("Usage: /edit_word <path> append|replace_last <text>")
            return
        text = f"/edit_word {' '.join(context.args)}"
        reply = await self._agent.handle_message(text, chat_id=update.effective_chat.id)
        await update.message.reply_text(reply)

    async def _on_edit_pdf(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        if not update.effective_user or not update.message:
            return
        if not self._is_allowed(update.effective_user.id):
            await update.message.reply_text("Access denied.")
            return
        if len(context.args) < 3:
            await update.message.reply_text("Usage: /edit_pdf <path> add_page <text>")
            return
        text = f"/edit_pdf {' '.join(context.args)}"
        reply = await self._agent.handle_message(text, chat_id=update.effective_chat.id)
        await update.message.reply_text(reply)

    async def _on_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        if not update.effective_user or not update.message or not update.message.text:
            return
        if not self._is_allowed(update.effective_user.id):
            await update.message.reply_text("Access denied.")
            return

        reply = await self._agent.handle_message(
            update.message.text,
            chat_id=update.effective_chat.id,
        )
        await update.message.reply_text(reply)

    async def run_polling(self) -> None:
        app = self.build_application()
        logger.info("Starting Telegram bot (polling)")
        await app.run_polling()
