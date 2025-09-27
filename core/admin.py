from django.contrib import admin

from core.models import FeedbackRequest


@admin.register(FeedbackRequest)
class FeedbackRequestAdmin(admin.ModelAdmin):
    list_display = ('datetime', 'name', 'contact', 'issue', 'fishy', 'solved')
    search_fields = ('name', 'contact', 'issue')
    list_filter = ('fishy', 'solved')
    readonly_fields = ('datetime',)

