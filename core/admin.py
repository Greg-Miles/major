from django.contrib import admin
from .models import Publication, Lesson

# Register your models here.

class PublicationAdmin(admin.ModelAdmin):
    """
    Админка для модели публикации.
    """
    list_display = ('title', 'created_at', 'category', 'is_published', 'downloads_count')
    search_fields = ('title',)
    list_filter = ('is_published', 'created_at')
    ordering = ('-created_at',)

class LessonAdmin(admin.ModelAdmin):
    """
    Админка для модели урока.
    """
    list_display = ('students_name', 'weekday', 'lesson_time', 'students_phone', 'lesson_duration')
    search_fields = ('students_name', 'students_phone')
    list_filter = ('weekday',)
    ordering = ('weekday', 'lesson_time')

admin.site.register(Publication, PublicationAdmin)
admin.site.register(Lesson, LessonAdmin)