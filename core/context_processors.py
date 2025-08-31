from .models import Publication, PageContent

def categories(request):
    """
    Контекстный процессор для добавления категорий публикаций в контекст шаблонов."""
    # Нужно для работы выпадающего списка категорий в шаблонах
    return {
        'categories': Publication.category.field.choices
    }

def page_content(request):
    """
    Добавляет объект PageContent в контекст по имени шаблона.
    """
    template_name = getattr(request.resolver_match, 'url_name', None)
    if not template_name:
        return {}
    content = PageContent.objects.filter(page_for=template_name + '.html').first()
    return {'page_content': content}