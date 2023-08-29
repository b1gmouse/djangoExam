from django.contrib import admin
from .models import Post, News

admin.site.register(Post)
admin.site.register(News)
fields = ['image_tag']
readonly_fields = ['image_tag']
