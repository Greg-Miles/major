from django.shortcuts import render
from django.views.generic import TemplateView, ListView

class LandingView(TemplateView):
    """
    Главная страница сайта.
    """
    template_name = 'landing.html'

