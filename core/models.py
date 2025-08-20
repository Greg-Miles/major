from django.db import models

class Publication(models.Model):
    """
    Модель публикации.
    """
    title = models.CharField(max_length=200, verbose_name='Заголовок')
    content = models.TextField(verbose_name='Содержание')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    file = models.FileField(upload_to='publications/', blank=True, null=True, verbose_name='Файл')
    is_published = models.BooleanField(default=False, verbose_name='Опубликовано')

    class Meta:
        verbose_name = 'Публикация'
        verbose_name_plural = 'Публикации'
        ordering = ['-created_at']

    def __str__(self):
        return self.title
    

class Lesson(models.Model):
    """
    Модель урока.
    """
    students_name = models.CharField(max_length=100, verbose_name='Имя ученика')
    weekday = models.IntegerField(choices=[
        (0, 'Понедельник'),
        (1, 'Вторник'),
        (2, 'Среда'),
        (3, 'Четверг'),
        (4, 'Пятница'),
        (5, 'Суббота'),
        (6, 'Воскресенье')
    ], verbose_name='День недели')
    lesson_time = models.TimeField(verbose_name='Время занятия')
    students_phone = models.CharField(max_length=15, verbose_name='Телефон ученика')
    lesson_duration = models.PositiveIntegerField(verbose_name='Продолжительность занятия (минуты)', default=60)

    class Meta:
        verbose_name = 'Занятие'
        verbose_name_plural = 'Занятия'
        ordering = ['weekday', 'lesson_time']

class PageContent(models.Model):
    """
    Модель для хранения контента страниц.
    """
    page_name = models.CharField(max_length=100, unique=True, verbose_name='Имя страницы')
    content = models.TextField(verbose_name='Содержимое страницы')
    page_for = models.CharField(max_length=50, verbose_name='Для станицы')

    class Meta:
        verbose_name = 'Контент страницы'
        verbose_name_plural = 'Контент страниц'

    def __str__(self):
        return self.page_name