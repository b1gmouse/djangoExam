from django.shortcuts import render
from .models import Post, News, Replies
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from .filters import PostFilter, NewsFilter, RepliesFilter
from django.contrib.auth.mixins import LoginRequiredMixin
from .permissions import ChangePermissionRequiredMixin
from .forms import PostForm
from django.core.mail import send_mail
from django.http.response import HttpResponseRedirect, HttpResponse
from django.conf import settings


class PostList(ListView):
    model = Post
    ordering = ['-created_date']
    template_name = 'posts.html'
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context

class PostDetail(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = context['post']
        return context


class PostCreate(LoginRequiredMixin, CreateView):
    raise_exception = False
    permission_required = ('board_change',)
    form_class = PostForm
    model = Post
    template_name = 'post_create.html'

    def image_upload_view(request):
        if request.method == 'POST':
            form = Post
            if form.is_valid():
                form.save()
                post_obj = form.instance
                return render(request, {'form': form, 'post_obj': post_obj})
        else:
            form = Post()
            return render(request, {'form': form})
class PostEdit(LoginRequiredMixin, ChangePermissionRequiredMixin, UpdateView):
    raise_exception = False
    permission_required = ('board_change',)
    form_class = PostForm
    model = Post
    template_name = 'post_create.html'

class NewsList(ListView):
    model = News
    ordering = '-time_in'
    template_name = 'news_list.html'
    context_object_name = 'news'
    paginate_by = 5

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = NewsFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context

class NewsDetail(DetailView):
    model = News
    template_name = 'news_detail.html'
    context_object_name = 'new'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        new = context['new']
        return context

def create_reply(request, pk):
    text = request.POST.get('text')
    pk = request.POST.get('pk')
    post = Post.objects.get(pk=pk)
    user = request.user
    reply = Replies(text=text, post=post, author=user)
    reply.save()
    next = request.GET.get('next')
    send_mail(
        subject=f"Появился отклик на ваше объявление '{post}'",
        message=f"{post.author}, вы получили отклик на ваше объявление '{post}'",
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[post.author.email]
    )
    return HttpResponseRedirect(next)

class RepliesList(LoginRequiredMixin, ListView):
    model = Replies
    ordering = '-time_in'
    template_name = 'replies_list.html'
    context_object_name = 'replies'
    paginate_by = 3

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context

def set_status_to_reply(request):
    pk = request.POST.get('pk')
    reply = Replies.objects.get(pk=pk)
    print(request.GET)
    print(request.POST)
    if request.POST.get('accept'):
        reply.status = 'A'
    elif request.POST.get('decline'):
        reply.status = 'D'
    reply.save()
    status = reply.get_status_display()
    print(status)
    next = request.GET.get('next')
    send_mail(
        subject=f"Реакция на отклик по '{reply.post}'",
        message=f"{reply.author}, ваш отклик на объявление '{reply.post}' {status}",
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[reply.author.email]
    )
    return HttpResponseRedirect(next)

def pass_view(request):
    context = {}
    return HttpResponse(render(request, 'pass.html', context))