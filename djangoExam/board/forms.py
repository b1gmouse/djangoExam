from django import forms
from django.core.exceptions import ValidationError

from .models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['category',
                  'title',
                  'text',
                  'pictures'
                  ]

    def clean(self):
        cleaned_data = super().clean()
        title, text = cleaned_data.get('title', ''), cleaned_data.get('text','')
        if title is not None and title.lower() in text.lower():
           error_text = 'Избегайте повтора текста в содержании.'
           raise ValidationError({'tittle': error_text})
        return cleaned_data

    def clean_tittle(self):
        title = self.cleaned_data['tittle']
        if title and title[0].islower():
            raise ValidationError('Начните с заглавной буквы')
        return title