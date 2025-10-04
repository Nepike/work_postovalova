from django import forms
from django_recaptcha.fields import ReCaptchaField
from django_recaptcha.widgets import ReCaptchaV2Checkbox
from django.core.exceptions import ValidationError


class FeedbackForm(forms.Form):
    issue = forms.CharField(
        label='Услуга или запрос',
        max_length=1000,
        min_length=10,
        widget=forms.Textarea(attrs={'rows': 5}),
        required=True,
    )

    name = forms.CharField(
        label='Имя',
        max_length=100,
        required=True,
    )

    contact = forms.CharField(
        label='Контакт для связи',
        max_length=100,
        required=True,
    )

    def validate_file_size(value):
        filesize = value.size

        if filesize > 10 * 1024 * 1024:  # 10MB
            raise ValidationError("Размер файла не должен превышать 10МБ.")
        return value

    photo = forms.ImageField(
        label='Вложение (необязательно)',
        required=False,
        validators=[validate_file_size]
    )

    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox)
