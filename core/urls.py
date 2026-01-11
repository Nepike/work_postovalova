
from django.urls import path, include, reverse_lazy
from django.views.generic import RedirectView
from . import views

urlpatterns = [
	path('', RedirectView.as_view(url='/home/', permanent=False)),
	path('home/', views.home, name='home'),
	path('groups/', views.groups, name='groups'),

]