from django.http import HttpResponseBadRequest
from django.shortcuts import render
import logging

from django.template.loader import render_to_string
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup
from telegram_bot.models import TelegramChat


from .forms import FeedbackForm
from .models import FeedbackRequest
from django.conf import settings
from akismet import Akismet


logger = logging.getLogger(__name__)


def home(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST, request.FILES)
        if form.is_valid():
            issue = form.cleaned_data['issue']
            name = form.cleaned_data['name']
            contact = form.cleaned_data['contact']
            photo = form.cleaned_data.get('photo')
            user_ip = request.META.get('REMOTE_ADDR')
            user_agent = request.META.get('HTTP_USER_AGENT', '')

            if settings.AKISMET_API_KEY:
                akismet_api = Akismet(key=settings.AKISMET_API_KEY, blog_url=settings.AKISMET_BLOG_URL)

                fishy = akismet_api.comment_check(
                    user_ip=user_ip,
                    user_agent=user_agent,
                    comment_type='contact-form',
                    comment_author=name,
                    comment_content=issue,
                )

            else:
                fishy = False

            issue = FeedbackRequest.objects.create(
                name=name,
                contact=contact,
                issue=issue,
                photo=photo,
                fishy=fishy
            )

            if fishy:
                return HttpResponseBadRequest("Спам обнаружен")
            else:
                rendered = render_to_string('telegram_bot/msg_feedback.html', {'issue': issue})

                reply_markup = InlineKeyboardMarkup(keyboard=[
                    [InlineKeyboardButton(text='✅ Пометить как решенное', callback_data=f"feedback-close-issue_{issue.id}")],
                    [InlineKeyboardButton(text='❗️ Пометить как спам', callback_data=f"feedback-report-spam_{issue.id}")],
                ])

                if photo:
                    path = issue.photo.path
                    with open(path, 'rb') as local_file:
                        TelegramChat.objects.filter(name="support").first().send_document(
                            document=local_file,
                            caption=rendered,
                            pinned=True,
                            parse_mode="HTML",
                            reply_markup=reply_markup,
                        )
                else:
                    TelegramChat.objects.filter(name="support").first().send_message(
                        text=rendered,
                        pinned=True,
                        parse_mode="HTML",
                        reply_markup=reply_markup,
                    )

                form = FeedbackForm()
                return render(request, "core/home.html", context={'form': form, 'alert_success': "Сообщение отправлено!"})
    else:
        form = FeedbackForm()

    return render(request, "core/home.html", {'form': form})

def groups(request):
    return render(request, "core/groups.html")
