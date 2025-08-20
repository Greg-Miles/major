from django import forms
from .models import PageContent

class PageContentForm(forms.ModelForm):
    """
    Форма для редактирования контента страниц.
    """
    class Meta:
        model = PageContent
        fields = ['content', ]
        widgets = {
            'content': forms.Textarea(attrs={'rows': 10, 'cols': 80, 'class':'form-control'}),
        }
        labels = {
            'page_name': 'Имя страницы',
            'content': 'Содержимое страницы',
        }