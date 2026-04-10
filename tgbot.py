import yaml
import telebot
from telebot import apihelper
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup
import os
from postovalova.settings.base import BASE_DIR
import django


CONFIG_PATH = BASE_DIR / 'config.yml'
with open(CONFIG_PATH) as f:
	SITE_CONFIG = yaml.safe_load(f.read())

PROXY_IP = SITE_CONFIG["proxy"].get("ip", None)
PROXY_PORT = SITE_CONFIG["proxy"].get("port", None)
PROXY_LOGIN = SITE_CONFIG["proxy"].get("login", None)
PROXY_PASSWORD = SITE_CONFIG["proxy"].get("password", None)

PROXY = f"http://{PROXY_LOGIN}:{PROXY_PASSWORD}@{PROXY_IP}:{PROXY_PORT}" if PROXY_IP else None

if PROXY:
	apihelper.proxy = {'https': PROXY}
bot = telebot.TeleBot(SITE_CONFIG["telegram_bot"]["token"])


@bot.message_handler(commands=['start'])
def start(message):
	# reply_markup = InlineKeyboardMarkup(keyboard=[
	# 	[InlineKeyboardButton(text='✅ Пометить как решенное', callback_data=f"feedback-close-issue_{144}")],
	# 	[InlineKeyboardButton(text='❗️ Пометить как спам', callback_data=f"feedback-report-spam_{441}")],
	# ])
	reply_markup = None
	bot.reply_to(message, "Бот онлайн!", reply_markup=reply_markup)


@bot.message_handler(commands=['get_chat_id'])
def get_chat_id(message):
	bot.reply_to(message, f"Chat: `{message.chat.id}`\nThread: `{message.message_thread_id}`", parse_mode="MarkdownV2")


@bot.callback_query_handler(func=lambda call: call.data.startswith("feedback-close-issue_"))
def feedback_close_callback(call):
	from core.models import FeedbackRequest

	message_content = call.message.text or call.message.caption

	try:
		issue_id = int(call.data.split("_")[1])
		issue = FeedbackRequest.objects.get(id=issue_id)
		issue.solved = True
		issue.save()

		new_text = (
			f"{message_content}\n"
			f"----------------------\n"
			f"✅ Обращение было помечено как решенное пользователем {call.from_user.username}!"
		)

	except FeedbackRequest.DoesNotExist:
		new_text = (
			f"{message_content}\n"
			f"----------------------\n"
			f"🤡 Обращение не найдено в БД"
		)

	if call.message.text:
		bot.edit_message_text(text=new_text, chat_id=call.message.chat.id, message_id=call.message.message_id)
	else:
		bot.edit_message_caption(caption=new_text, chat_id=call.message.chat.id, message_id=call.message.message_id)

	bot.unpin_chat_message(chat_id=call.message.chat.id, message_id=call.message.message_id)


@bot.callback_query_handler(func=lambda call: call.data.startswith("feedback-report-spam_"))
def feedback_spam_callback(call):
	from core.models import FeedbackRequest

	message_content = call.message.text or call.message.caption

	try:
		issue_id = int(call.data.split("_")[1])
		issue = FeedbackRequest.objects.get(id=issue_id)
		issue.fishy = True
		issue.save()

		new_text = (
			f"{message_content}\n"
			f"----------------------\n"
			f"🚫 Обращение было помечено как спам пользователем {call.from_user.username}!"
		)

	except FeedbackRequest.DoesNotExist:
		new_text = (
			f"{message_content}\n"
			f"----------------------\n"
			f"🤡 Обращение не найдено в БД"
		)

	if call.message.text:
		bot.edit_message_text(
			text=new_text,
			chat_id=call.message.chat.id,
			message_id=call.message.message_id
		)
	else:
		bot.edit_message_caption(
			caption=new_text,
			chat_id=call.message.chat.id,
			message_id=call.message.message_id
		)

	bot.unpin_chat_message(chat_id=call.message.chat.id, message_id=call.message.message_id)


if __name__ == "__main__":
	if SITE_CONFIG["env"] == 'dev':
		os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'postovalova.settings.dev')
	else:
		os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'postovalova.settings.prod')
	django.setup()

	print("Bot started polling...")
	bot.infinity_polling()


