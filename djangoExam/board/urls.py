from django.urls import path
from django.conf.urls.static import static
from django.conf import settings

from .views import PostList, PostDetail, PostCreate, PostEdit, create_reply, RepliesList, set_status_to_reply, NewsList, NewsDetail, pass_view



urlpatterns = [
    path('posts/', PostList.as_view(), name='posts'),
    path('posts/<int:pk>/', PostDetail.as_view(), name='post'),
    path('posts/post_create/', PostCreate.as_view(), name='post_create'),
    path('posts/post_edit/<int:pk>', PostEdit.as_view(), name='post_edit'),
    path('posts/<int:pk>/reply_create', create_reply, name='reply_create'),
    path('posts/author/replies', RepliesList.as_view(), name='replies_list'),
    path('posts/set_status_to_reply/', set_status_to_reply, name='set_status'),
    path('posts/news/', NewsList.as_view(), name='news_list'),
    path('posts/news/<int:pk>/', NewsDetail.as_view(), name='news_detail'),
    path('posts/pass/', pass_view, name='pass'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)