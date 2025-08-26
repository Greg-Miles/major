from django import forms
from django_ckeditor_5.widgets import CKEditor5Widget
from .models import PageContent

class PageContentForm(forms.ModelForm):
    """
    Форма для редактирования контента страниц.
    """
    class Meta:
        model = PageContent
        fields = ['content',]
        widgets = {
            'content': CKEditor5Widget(attrs={'rows': 10, 'cols': 80, }),
        }
        labels = {
            'content': 'Содержимое страницы',
        }