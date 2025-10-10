from django.db import models
from tgbot import TelegramBot
import asyncio

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

    def send_message(self, text, parse_mode=None, disable_web_page_preview=None, disable_notification=None, reply_to_message_id=None, reply_markup=None, pinned=False):

        msg = asyncio.run(TGBOT.sendMessage(self.chat_id, text,
                          parse_mode=parse_mode,
                          disable_web_page_preview=disable_web_page_preview,
                          disable_notification=disable_notification,
                          reply_to_message_id=(reply_to_message_id or self.first_message_id),
                          reply_markup=reply_markup))

        # if pinned:
        #     try:
        #         TGBOT.pinChatMessage(self.chat_id, msg['message_id'])
        #     except Exception as e:
        #         error_message = "Не удалось закрепить сообщение: " + str(e)
        #         TGBOT.sendMessage(self.chat_id, error_message,reply_to_message_id=msg['message_id'])

    def send_photo(self, photo, caption=None, parse_mode=None, disable_notification=None, reply_to_message_id=None, reply_markup=None, pinned=False):
        msg = asyncio.run(TGBOT.sendDocument(self.chat_id, photo,
                        caption=caption,
                        parse_mode=parse_mode,
                        disable_notification=disable_notification,
                        reply_to_message_id=(reply_to_message_id or self.first_message_id),
                        reply_markup=reply_markup))

        # if pinned:
        #     try:
        #         TGBOT.pinChatMessage(self.chat_id, msg['message_id'])
        #     except Exception as e:
        #         error_message = "Не удалось закрепить сообщение: " + str(e)
        #         TGBOT.sendMessage(self.chat_id, error_message, reply_to_message_id=msg['message_id'])


