from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseForbidden, FileResponse, JsonResponse
from django.conf import settings
from django.contrib import messages
from django.views.generic import TemplateView, ListView
from django.db.models import F
import bleach
from bleach.css_sanitizer import CSSSanitizer
from .models import Publication, Lesson, PageContent
from .forms import PageContentForm


def handle_page_content_post(request, template_name, page_name, redirect_url):
    """
    Универсальная обработка POST-запроса для редактирования PageContent.
    """
    #запрет что-то делать не администратору
    if not request.user.is_superuser:
        return HttpResponseForbidden("Только для администратора")
    #получение или создание контента страницы
    page_content = PageContent.objects.filter(page_for=template_name).first()
    form = PageContentForm(request.POST, instance=page_content)
    if form.is_valid():
        #если форма валидна, сохраняем в модель, предварительно очистив от нежелательного HTML
        try:
            bleached_content = bleach.clean(
                form.cleaned_data['content'],
                tags=settings.ALLOWED_TAGS,
                attributes=settings.ALLOWED_ATTRIBUTES,
                strip=True,
                css_sanitizer=CSSSanitizer(),
            )
            form.instance.content = bleached_content
            form.instance.page_for = template_name
            form.instance.page_name = page_name
            form.save()
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                #возвращаем JSON-ответ с очищенным контентом
                return JsonResponse({'success': True, 'content': bleached_content})
        except Exception as e:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                #возвращаем JSON-ответ с ошибкой
                return JsonResponse({'success': False, 'error': str(e)})
            messages.error(request, f"Ошибка при сохранении: {e}")
        return redirect(redirect_url)
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        #возвращаем JSON-ответ с ошибками формы
        return JsonResponse({'success': False, 'errors': form.errors})
    return None, form

def download_file(request, pk):
    """
    Отдает файл для скачивания и увеличивает счетчик загрузок,
    предотвращая повторный подсчет для одного пользователя в рамках сессии.
    """
    pub = get_object_or_404(Publication, pk=pk)

    # Получаем список уже скачанных файлов из сессии.
    # Если списка нет, создаем пустой.
    downloaded_files = request.session.get('downloaded_files', [])

    # Проверяем, был ли этот файл уже скачан в текущей сессии
    if pub.pk not in downloaded_files:
        # Используем F() для атомарного увеличения счетчика на уровне БД,
        # чтобы избежать состояния гонки.
        pub.downloads_count = F('downloads_count') + 1
        pub.save(update_fields=['downloads_count'])
        
        # Добавляем ID файла в список скачанных в сессии
        downloaded_files.append(pub.pk)
        request.session['downloaded_files'] = downloaded_files
        
        # Явно помечаем сессию как измененную, чтобы Django ее сохранил.
        # В некоторых случаях, когда изменяются вложенные структуры данных,
        # это необходимо сделать вручную.
        request.session.modified = True

    # Отдаем файл пользователю
    return FileResponse(pub.presentation_file.open(), as_attachment=True, filename=pub.presentation_file.name)

class LandingView(TemplateView):
    """
    Главная страница сайта.
    """
    template_name = 'landing.html'

    def get_context_data(self, form=None, **kwargs):
        """
        Метод обработки конекста с добавления формы редактирования контента страницы в контекст
        """
        context = super().get_context_data(**kwargs)
        if self.request.user.is_superuser:
            if form is not None:
                context['form'] = form
            else:
                page_content = PageContent.objects.filter(page_for=self.template_name).first()
                initial = {'content': page_content.content} if page_content else {}
                context['form'] = PageContentForm(initial=initial)
        return context
    
    def post(self, request, *args, **kwargs):
        """
        Метод для обработки POST-запроса для редактирования контента страницы
        """
        #выносим логику в отдельную функцию
        result = handle_page_content_post(
            request,
            self.template_name,
            'Главная страница',
            'landing'
        )
        if isinstance(result, (JsonResponse, HttpResponseForbidden)):
            # если результат - это JsonResponse или HttpResponseForbidden, возвращаем его напрямую
            return result
        _, form = result
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
        """
        Возвращает queryset с учетом поискового запроса.
        """
        search_query = self.request.GET.get('q', '')
        category = self.request.GET.get('category', None)
        queryset = Publication.objects.all().order_by('-created_at')

        if search_query:
            queryset = queryset.filter(
                title__icontains=search_query
            ) | queryset.filter(
                content__icontains=search_query
            )
            queryset = queryset.distinct().order_by('-created_at')

        if category:
            queryset = queryset.filter(category=category)

        return queryset




class ContactPageView(TemplateView):
    """
    Страница контактов.
    """
    template_name = 'contacts.html'

    def get_context_data(self, **kwargs):
        """
        Метод обработки конекста с добавления формы редактирования контента страницы в контекст
        """
        context = super().get_context_data(**kwargs)
        if self.request.user.is_superuser:
            page_content = PageContent.objects.filter(page_for=self.template_name).first()
            initial = {'content': page_content.content} if page_content else {}
            context['form'] = PageContentForm(initial=initial)
        return context
    
    def post(self, request, *args, **kwargs):
        """
        Метод для обработки POST-запроса для редактирования контента страницы
        """
        result = handle_page_content_post(
            request,
            self.template_name,
            'Контакты',
            'contacts'
        )
        if isinstance(result, (JsonResponse, HttpResponseForbidden)):
            return result
        _, form = result
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
        """
        Метод возвращает отсортированный по дню недели и времени уроков queryset.
        """
        return Lesson.objects.all().order_by('weekday', 'lesson_time')
    
    def get_context_data(self, **kwargs):
        """
        Метод обработки контекста с группировкой уроков по дням недели
        и добавления формы редактирования контента страницы в контекст
        """
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
        if self.request.user.is_superuser:
            page_content = PageContent.objects.filter(page_for=self.template_name).first()
            initial = {'content': page_content.content} if page_content else {}
            context['form'] = PageContentForm(initial=initial)
        return context
    
    def post(self, request, *args, **kwargs):
        """
        Обработка POST-запроса для редактирования контента страницы
        """
        result = handle_page_content_post(
            request,
            self.template_name,
            'Расписание уроков',
            'lessons_schedule'
        )
        if isinstance(result, (JsonResponse, HttpResponseForbidden)):
            return result
        _, form = result
        context = self.get_context_data(form=form)
        return self.render_to_response(context)
    