
from django.urls import path, include, reverse_lazy
from django.views.generic import RedirectView
from . import views

urlpatterns = [
	path('home/', views.home, name='home'),
	path('groups/', views.home, name='groups'),

]