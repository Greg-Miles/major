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
    template_name = 'contacts.html'

class LessonScheduleView(ListView):
    """
    Расписание уроков.
    """
    model = Lesson
    template_name = 'lessons_schedule.html'
    context_object_name = 'lessons'


    def get_queryset(self):
        return Lesson.objects.all().order_by('weekday', 'lesson_time')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        lessons = self.get_queryset()
        lessons_by_weekday ={}
        for weekday_num, weekday_name in Lesson.weekday.field.choices:
            lessons_by_weekday[weekday_num] = []
        for lesson in lessons:
            lessons_by_weekday[lesson.weekday].append(lesson)
        # Формируем список для шаблона
        schedule = []
        for weekday_num, weekday_name in Lesson.weekday.field.choices:
            schedule.append((weekday_num, weekday_name, lessons_by_weekday[weekday_num]))
        context['schedule'] = schedule
        return context