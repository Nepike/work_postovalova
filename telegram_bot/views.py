# import json
# import re
#
# import telepot
# from django.contrib.auth.decorators import user_passes_test
# from django.http import JsonResponse
# from django.shortcuts import render
# from django.template.loader import render_to_string
# from django.views.decorators.csrf import csrf_exempt
#
# from core.models import FeedbackRequest
#
# from .models import TGBOT
# from .models import TelegramChat
#
#
# @csrf_exempt
# def webhook(request):
#     if request.method == 'POST':
#         update = request.body.decode('utf-8')
#         handle(update)
#         return JsonResponse({'status': 'ok'})
#     return JsonResponse({'status': 'not ok'})
#
#
# def handle(msg):
#     """Эта функция отвечает за ВСЁ, что бот ПОЛУЧАЕТ"""
#     msg = json.loads(msg)
#
#     if 'callback_query' in msg:
#         handle_callback_query(msg['callback_query'])
#     elif 'message' in msg:
#         handle_message(msg['message'])
#
#
# def handle_callback_query(callback_query):
#     callback_data = callback_query['data']
#     input_string = callback_query['message'].get('caption', callback_query['message'].get('text', ''))
#
#     regex_pattern = r"\(#(\d+)\)"
#     match = re.search(regex_pattern, input_string)
#
#     if match:
#         issue_id = int(match.group(1))
#         try:
#             issue = FeedbackRequest.objects.get(id=issue_id)
#             if callback_data == 'feedback_close_issue':
#                 issue.solved = True
#             elif callback_data == 'feedback_report_spam':
#                 issue.fishy = True
#                 issue.solved = True
#             issue.save()
#         except FeedbackRequest.DoesNotExist:
#             print(f"Issue with ID {issue_id} not found")
#
#         additional_info = {
#             'feedback_close_issue': 'решенное',
#             'feedback_report_spam': 'спам',
#         }
#         additional = (f'-------------------\n'
#                       f'ℹ️ Данное обращение было помечено как {additional_info[callback_data]} пользователем {callback_query["from"]["username"]}!')
#
#         rendered = render_to_string('telegram_bot/msg_feedback.html', {'issue': issue, 'additional': additional})
#
#         message_identifier = (callback_query['message']['chat']['id'], callback_query['message']['message_id'])
#
#         if 'caption' in callback_query['message']:
#             TGBOT.editMessageCaption(
#                 caption=rendered,
#                 parse_mode="HTML",
#                 msg_identifier=message_identifier,
#                 reply_markup=None
#             )
#         else:
#             TGBOT.editMessageText(
#                 text=rendered,
#                 parse_mode="HTML",
#                 msg_identifier=message_identifier,
#                 reply_markup=None
#             )
#
#
# def handle_message(message):
#     if message.get('text') == "/get_chat_id":
#         TGBOT.sendMessage(message['chat']['id'], f"ID: {message['chat']['id']}", reply_to_message_id=message.get('message_id'))
#     else:
#         pass
#         # TGBOT.sendMessage(message['chat']['id'], f"Получено сообщение: {message.get('text', 'неизвестное сообщение')}")
