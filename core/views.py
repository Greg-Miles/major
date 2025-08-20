from django.shortcuts import render, redirect
from django.http import HttpResponseForbidden
from django.conf import settings
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
    page_content = get_page_content(template_name)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Получаем контент страницы
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
            bleached_content = bleach.clean(
                form.cleaned_data['content'],
                tags=settings.ALLOWED_TAGS,
                attributes=settings.ALLOWED_ATTRIBUTES,
                strip=True
                )
            form.instance.content = bleached_content
            form.instance.page_for = self.template_name
            form.instance.page_name = 'Главная страница'
            form.save()
            return redirect('landing')
        context = self.get_context_data(form=form)
        return self.render_to_response(context)

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
    page_content = get_page_content(template_name)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context['page_content'] = self.page_content
        # Форма только для суперпользователя
        if self.request.user.is_superuser:
            initial = {'content': self.page_content.content} if self.page_content else {}
            context['form'] = PageContentForm(initial=initial)
        return context
    
    def post(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            return HttpResponseForbidden("Только для администратора")
        page_content = get_page_content(self.template_name)
        form = PageContentForm(request.POST, instance=page_content)
        if form.is_valid():
            bleached_content = bleach.clean(
                form.cleaned_data['content'],
                tags=settings.ALLOWED_TAGS,
                attributes=settings.ALLOWED_ATTRIBUTES,
                strip=True
                )
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
    page_content = get_page_content(template_name)

    def get_queryset(self):
        return Lesson.objects.all().order_by('weekday', 'lesson_time')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        lessons = self.get_queryset()
        lessons_by_weekday ={}
        # Инициализируем словарь для хранения уроков по дням недели
        for weekday_num, weekday_name in Lesson.weekday.field.choices:
            lessons_by_weekday[weekday_num] = []
        # Группируем уроки по дням недели
        for lesson in lessons:
            lessons_by_weekday[lesson.weekday].append(lesson)
        # Формируем список для шаблона
        schedule = []
        for weekday_num, weekday_name in Lesson.weekday.field.choices:
            schedule.append((weekday_num, weekday_name, lessons_by_weekday[weekday_num]))
        context['schedule'] = schedule
        # Добавляем контент страницы
        context['page_content'] = self.page_content
        if self.request.user.is_superuser:
            initial = {'content': self.page_content.content} if self.page_content else {}
            context['form'] = PageContentForm(initial=initial)
        return context
    
    def post(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            return HttpResponseForbidden("Только для администратора")
        page_content = get_page_content(self.template_name)
        form = PageContentForm(request.POST, instance=page_content)
        if form.is_valid():
            bleached_content = bleach.clean(
                form.cleaned_data['content'],
                tags=settings.ALLOWED_TAGS,
                attributes=settings.ALLOWED_ATTRIBUTES,
                strip=True
                )
            form.instance.content = bleached_content
            form.instance.page_for = self.template_name
            form.instance.page_name = 'Расписание уроков'
            form.save()
            return redirect('lessons_schedule')
        context = self.get_context_data(form=form)
        return self.render_to_response(context)