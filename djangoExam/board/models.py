from django.db import models
from django.conf import settings
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from crum import get_current_user


def user_directory_path(instance, filename):
    return 'user_{0}/{1}'.format(instance.id, filename)

class Post(models.Model):
    CATEGORIES = [
        ('TA', 'Танки'),
        ('HL', 'Хилы'),
        ('DD', 'ДД'),
        ('TR', 'Торговцы'),
        ('GM', 'Гилдмастеры'),
        ('QG', 'Квестгиверы'),
        ('SM', 'Кузнецы'),
        ('TN', 'Кожевники'),
        ('PT', 'Зельевары'),
        ('SP', 'Мастера заклинаний'),
    ]

    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='post', editable=False,
                               blank=True, null=True, default=None)
    title = models.CharField(max_length=64)
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)
    pictures = models.ImageField(upload_to='pictures', blank=True)
    category = models.CharField(max_length=2, choices=CATEGORIES, default='TA')
    text = models.TextField()

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.pk:
            user = get_current_user()
            self.author = user
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('post', args=[str(self.pk)])


class Replies(models.Model):
    STATUSES = [
        ('A', 'принят'),
        ('N', 'получен'),
        ('D', 'отменён'),
    ]

    text = models.TextField()
    status = models.CharField(max_length=1, choices=STATUSES, default='N')
    time_in = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='reply', editable=False,
                             blank=True, null=True, default=None)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reply', editable=False,
                               blank=True, null=True, default=None)

    def save(self, *args, **kwargs):
        if not self.pk:
            user = get_current_user()
            self.author = user
            if kwargs.get('pk') and not self.post:
                pk = int(kwargs['pk'])
                self.post = Post.objects.get(pk=pk)
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.text}'

    def show_date(self):
        return self.time_in.date()

class News(models.Model):
    title = models.CharField(max_length=64)
    text = models.TextField()
    pictures = models.ImageField(upload_to='pictures', blank=True)
    time_in = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='news',
                               editable=False, blank=True, null=True, default=None)

    def save(self, *args, **kwargs):
        user = get_current_user()
        if not self.pk:
            self.author = user
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('news_detail', args=[str(self.pk)])

    def show_preview(self):
        return f'{self.text[:64]}...'

    def date_in(self):
        return self.time_in.date()