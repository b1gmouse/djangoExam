from django_filters import FilterSet, ModelChoiceFilter, CharFilter, DateFilter
from django.contrib.auth.models import User
from django.forms import DateInput
from .models import Post, Replies, News

class PostFilter(FilterSet):
    author = ModelChoiceFilter(
        field_name='author',
        queryset=User.objects.all(),
        lookup_expr='exact',
        label=('Автор'),
        empty_label='all'
    )

    title = CharFilter(
        lookup_expr='icontains',
        label='Объявление содержит',
    )

    text = CharFilter(
        lookup_expr='icontains',
        label='В содержании объявления',
    )

    class Meta:
        model = Post
        fields = {
            'category': ['exact'],
        }


class RepliesFilter(FilterSet):
    author = ModelChoiceFilter(
        field_name='author',
        queryset=User.objects.all(),
        lookup_expr='exact',
        label=('Автор'),
        empty_label='all',
    )

    class Meta:
        model = Replies
        fields = {
            'post': ['exact'],
            'status': ['exact'],
        }


class NewsFilter(FilterSet):
    time_in = DateFilter(
        field_name='time_in',
        lookup_expr='gt',
        label='Опубликовано с',
        widget=DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
    )

    title = CharFilter(
        lookup_expr='icontains',
        label='Заголовок содержит',
    )

    text = CharFilter(
        lookup_expr='icontains',
        label='Текст содержит',
        # widget=TextInput(attrs={'class': 'form-control'}),
    )

    class Meta:
        model = News
        fields = ['title', 'text', 'time_in']