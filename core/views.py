from django.shortcuts import render
from django.views.generic import TemplateView, ListView
from .models import Publication, Lesson

class LandingView(TemplateView):
    """
    Главная страница сайта.
    """
    template_name = 'landing.html'

class PublicationListView(ListView):
    """
    Список публикаций.
    """
    model = Publication
    template_name = 'publication_list.html'
    context_object_name = 'publications'
    paginate_by = 10

    def get_queryset(self):
        return Publication.objects.all().order_by('-created_at')


# class ScheduleView(ListView):

class ContactPageView(TemplateView):
    """
    Страница контактов.
    """
    template_name = 'contact.html'