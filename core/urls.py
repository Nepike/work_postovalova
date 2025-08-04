
from django.urls import path, include, reverse_lazy
from django.views.generic import RedirectView
from . import views

urlpatterns = [
	path('', views.home, name='home'),
]