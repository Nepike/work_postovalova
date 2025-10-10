from django.db import models
from tgbot import TelegramBot


TGBOT = TelegramBot.get_bot()


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

    async def send_message(self, text, pinned=None, **kwargs):
        msg = await TGBOT.sendMessage(chat_id=self.chat_id, text=text, message_thread_id=self.first_message_id, **kwargs)

        if pinned:
            try:
                await TGBOT.pin_chat_message(chat_id=self.chat_id, message_id=msg.message_id)
            except Exception as e:
                error_message = "Не удалось закрепить сообщение: " + str(e)
                await TGBOT.sendMessage(chat_id=self.chat_id, text=error_message, reply_to_message_id=msg.message_id)

    async def send_document(self, document, pinned=None, **kwargs):
        msg = await TGBOT.sendDocument(chat_id=self.chat_id, document=document, message_thread_id=self.first_message_id, **kwargs)

        if pinned:
            try:
                await TGBOT.pin_chat_message(chat_id=self.chat_id, message_id=msg.message_id)
            except Exception as e:
                error_message = "Не удалось закрепить сообщение: " + str(e)
                await TGBOT.sendMessage(chat_id=self.chat_id, text=error_message, reply_to_message_id=msg.message_id)


