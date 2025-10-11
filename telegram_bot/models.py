from django.db import models
from django.conf import settings
import telebot


TGBOT = telebot.TeleBot(settings.TGBOT_TOKEN)


class TelegramChat(models.Model):
    class Meta:
        verbose_name = "чат"
        verbose_name_plural = "чаты"

    name = models.CharField(verbose_name="название чата", max_length=30)
    description = models.TextField(verbose_name="описание", max_length=150, null=True, blank=True)
    chat_id = models.BigIntegerField(verbose_name="chat ID")
    first_message_id = models.BigIntegerField(verbose_name="Айди первого сообщения (для топиков)", blank=True, null=True)

    def __str__(self):
        return self.name

    def send_message(self, text, pinned=None, **kwargs):
        msg = TGBOT.send_message(chat_id=self.chat_id, text=text, message_thread_id=self.first_message_id, **kwargs)

        if pinned:
            try:
                TGBOT.pin_chat_message(chat_id=self.chat_id, message_id=msg.message_id)
            except Exception as e:
                error_message = "Не удалось закрепить сообщение: " + str(e)
                TGBOT.send_message(chat_id=self.chat_id, text=error_message, reply_to_message_id=msg.message_id)

    def send_document(self, document, pinned=None, **kwargs):
        msg = TGBOT.send_document(chat_id=self.chat_id, document=document, message_thread_id=self.first_message_id, **kwargs)

        if pinned:
            try:
                TGBOT.pin_chat_message(chat_id=self.chat_id, message_id=msg.message_id)
            except Exception as e:
                error_message = "Не удалось закрепить сообщение: " + str(e)
                TGBOT.send_message(chat_id=self.chat_id, text=error_message, reply_to_message_id=msg.message_id)


