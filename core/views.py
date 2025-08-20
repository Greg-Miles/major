from django.shortcuts import render, redirect
from django.http import HttpResponseForbidden
from django.views.generic import TemplateView, ListView
import bleach
from .models import Publication, Lesson, PageContent
from .forms import PageContentForm


def get_page_content(page_for):
    """
    Получает контент страницы по названию шаблона.
    """
    try:
        return PageContent.objects.get(page_for=page_for)

    except PageContent.DoesNotExist:
        return None

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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        page_content = get_page_content(self.template_name)
        context['page_content'] = page_content
        # Форма только для суперпользователя
        if self.request.user.is_superuser:
            initial = {'content': page_content.content} if page_content else {}
            context['form'] = PageContentForm(initial=initial)
        return context
    
    def post(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            return HttpResponseForbidden("Только для администратора")
        page_content = get_page_content(self.template_name)
        form = PageContentForm(request.POST, instance=page_content)
        if form.is_valid():
            bleached_content = bleach.clean(form.cleaned_data['content'], tags=['p', 'br', 'strong', 'em', 'a'], attributes={'a': ['href', 'title']})
            form.instance.content = bleached_content
            form.instance.page_for = self.template_name
            form.instance.page_name = 'Контакты'
            form.save()
            return redirect('contacts')
        context = self.get_context_data(form=form)
        return self.render_to_response(context)

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