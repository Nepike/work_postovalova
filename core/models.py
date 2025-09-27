from django.db import models
from django.utils import timezone


class FeedbackRequest(models.Model):
    class Meta:
        verbose_name = "сообщение обратной связи"
        verbose_name_plural = "сообщения обратной связи"

    datetime = models.DateTimeField("дата и время", default=timezone.now, editable=False)
    name = models.CharField("имя", max_length=50)
    contact = models.CharField("контакт", max_length=100)
    issue = models.TextField("сообщение", max_length=1000)
    photo = models.ImageField("фото", upload_to='feedback_photos/', blank=True, null=True)

    fishy = models.BooleanField("подозрительно?", default=False)

    solved = models.BooleanField("Решено?", default=False)

    def __str__(self):
        return f"{self.name} - {self.datetime}"
