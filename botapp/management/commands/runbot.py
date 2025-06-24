from django.core.management.base import BaseCommand
from telegram.ext import Updater, CommandHandler
from botapp.models import TelegramUser
from django.conf import settings

def start(update, context):
    telegram_id = str(update.effective_user.id)
    username = update.effective_user.username
    first_name = update.effective_user.first_name

    # Save or update user
    user, created = TelegramUser.objects.get_or_create(telegram_id=telegram_id)
    user.username = username
    user.first_name = first_name
    user.save()

    update.message.reply_text(f"Hello {first_name or username}! You have been registered.")

class Command(BaseCommand):
    help = 'Runs the Telegram bot'

    def handle(self, *args, **kwargs):
        updater = Updater(settings.TELEGRAM_BOT_TOKEN, use_context=True)
        dp = updater.dispatcher

        dp.add_handler(CommandHandler("start", start))

        self.stdout.write("Telegram bot is running...")
        updater.start_polling()
        updater.idle()
