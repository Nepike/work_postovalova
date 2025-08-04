from django.shortcuts import render
import logging


logger = logging.getLogger(__name__)


def home(request):
    context = {}
    return render(request, "core/home.html", context)