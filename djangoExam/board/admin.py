from django.contrib import admin
from .models import Post

admin.site.register(Post)
fields = ['image_tag']
readonly_fields = ['image_tag']
