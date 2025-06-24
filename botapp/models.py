from django.db import models

class TelegramUser(models.Model):
    telegram_id = models.CharField(max_length=100, unique=True)
    username = models.CharField(max_length=100, blank=True, null=True)
    first_name = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.username or self.telegram_id
