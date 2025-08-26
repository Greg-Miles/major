from .models import Publication

def categories(request):
    """
    Контекстный процессор для добавления категорий публикаций в контекст шаблонов."""
    return {
        'categories': Publication.category.field.choices
    }