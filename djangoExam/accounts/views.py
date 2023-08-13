from django.contrib.auth.models import User, Group
from django.views.generic.edit import CreateView, UpdateView
from .forms import SignUpForm, SignUpConfirmForm
from django.urls import reverse_lazy
from django.http.response import HttpResponse
from django.contrib.auth import logout
from django.shortcuts import render
from django.views.generic import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from .permissions import ProfileUserPermissionRequiredMixin
class SignUp(CreateView):
    model = User
    form_class = SignUpForm
    success_url = reverse_lazy('signup_mail')
    template_name = 'registration/signup.html'

def signup_mail_view(request):
    context = {}
    logout(request)
    return HttpResponse(render(request, 'registration/signup_email.html', context))

class SignUpConfirm(UpdateView):
    raise_exception = True
    form_class = SignUpConfirmForm
    model = User
    template_name = 'registration/confirm   _signup.html'
    success_url = reverse_lazy('login')

    def from_valid(self, form):
        response = super().form_valid(form)
        user = form.cleaned_data.get('user')
        user.is_active = True
        user_auth = Group.objects.get(name="user_auth")
        user.groups.add(user_auth)
        user.save()
        return response

class UserProfile(LoginRequiredMixin, ProfileUserPermissionRequiredMixin, DetailView):
    raise_exception = False
    permission_required = ('auth.view_user',)
    model = User
    template_name = 'accounts/profile_user.html'
    context_object_name = 'user'
