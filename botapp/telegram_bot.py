
import logging
from telegram.ext import Updater, CommandHandler
from django.conf import settings
from botapp.models import TelegramUser

# Setup logger
logging.basicConfig(level=logging.INFO)

def start(update, context):
    telegram_id = update.effective_user.id
    username = update.effective_user.username
    first_name = update.effective_user.first_name

    TelegramUser.objects.get_or_create(
        telegram_id=telegram_id,
        defaults={'username': username, 'first_name': first_name}
    )

    update.message.reply_text(f"Hello {first_name or username}! You're now connected.")

def run_bot():
    updater = Updater(settings.TELEGRAM_BOT_TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    updater.start_polling()
    updater.idle()
