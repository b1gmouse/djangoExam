from django.urls import path
from django.conf.urls.static import static
from django.conf import settings

from .views import PostList, PostDetail



urlpatterns = [
    path('posts/', PostList.as_view(), name='posts'),
    path('posts/<int:pk>/', PostDetail.as_view(), name='post')
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)