from pathlib import Path
import yaml

from telegram import Update, Bot, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, PicklePersistence, ContextTypes, CallbackQueryHandler

import os
import django
from asgiref.sync import sync_to_async

BASE_DIR = Path(__file__).resolve().parent
PARENT_DIR = BASE_DIR.parent
CONFIG_PATH = BASE_DIR / 'config.yml'
with open(CONFIG_PATH) as f:
	SITE_CONFIG = yaml.safe_load(f.read())


# Singleton для импортов в другие файлы
class TelegramBot:
	_instance = None

	@classmethod
	def get_bot(cls):
		if cls._instance is None:
			cls._instance = Bot(token=SITE_CONFIG["telegram_bot"]["token"])
		return cls._instance


async def start(update, context):
	reply_markup = InlineKeyboardMarkup(inline_keyboard=[
		[InlineKeyboardButton(text='✅ Пометить как решенное', callback_data=f"feedback-close-issue_{1}")],
		[InlineKeyboardButton(text='❗️ Пометить как спам', callback_data=f"feedback-report-spam_{1}")],
	])
	reply_markup = None
	await update.message.reply_text("Бот онлайн!", reply_markup=reply_markup)


async def get_chat_id(update, context):
	await update.message.reply_text(text=f"Chat: `{update.message.chat.id}`\n"
										 f"Thread: `{update.message.message_thread_id}`",
									parse_mode="MarkdownV2")


async def on_callback(update, context):
	query = update.callback_query
	await query.answer()

	async def edit_message(new_text):
		if query.message.text:
			await query.edit_message_text(new_text)
		else:
			await query.edit_message_caption(caption=new_text)

	message_content = query.message.text or query.message.caption

	if query.data.startswith("feedback-close-issue_"):
		from core.models import FeedbackRequest
		try:
			issue_id = int(query.data.split("_")[1])
			issue = await sync_to_async(FeedbackRequest.objects.get)(id=issue_id)
			issue.solved = True
			await sync_to_async(issue.save)()
		except FeedbackRequest.DoesNotExist:
			await edit_message(
				f"{message_content}\n"
				f"----------------------\n"
				f"🤡 Обращение не найдено в БД")
			return
		await edit_message(
			f"{message_content}\n"
			f"----------------------\n"
			f"✅ Обращение было помечено как решенное пользователем {query.from_user.username}!")
	elif query.data.startswith("feedback-report-spam_"):
		from core.models import FeedbackRequest
		try:
			issue_id = int(query.data.split("_")[1])
			issue = await sync_to_async(FeedbackRequest.objects.get)(id=issue_id)
			issue.fishy = True
			await sync_to_async(issue.save)()
		except FeedbackRequest.DoesNotExist:
			await edit_message(
				f"{message_content}\n"
				f"----------------------\n"
				f"🤡 Обращение не найдено в БД")
			return
		await edit_message(
			f"{message_content}\n"
			f"----------------------\n"
			f"🚫 Обращение было помечено как спам пользователем {query.from_user.username}!")


if __name__ == "__main__":
	if SITE_CONFIG["env"] == 'dev':
		os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'postovalova.settings.dev')
	else:
		os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'postovalova.settings.prod')
	django.setup()

	# persistence = PicklePersistence(PARENT_DIR/'bot_state.pkl')
	app = (
		ApplicationBuilder()
		.token(SITE_CONFIG["telegram_bot"]["token"])
		# .persistence(persistence)
		.build()
	)
	app.add_handler(CommandHandler("start", start))
	app.add_handler(CommandHandler("get_chat_id", get_chat_id))
	app.add_handler(CallbackQueryHandler(on_callback))
	app.run_polling()
