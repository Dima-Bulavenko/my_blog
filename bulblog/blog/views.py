from django.contrib.auth import logout, login
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.views import LoginView
from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import ListView, DetailView, CreateView

from .forms import *
from .models import *
from .utils import *
from django.contrib.auth.mixins import LoginRequiredMixin


class AddPostViews(LoginRequiredMixin, DataMixin, CreateView):
    form_class = AddPostForm
    template_name = "blog/add_post.html"
    success_url = reverse_lazy("index")
    login_url = reverse_lazy('login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context_def = self.get_user_context(title="Добавить пост")
        return dict(list(context.items()) + list(context_def.items()))


class IndexViews(DataMixin, ListView):
    model = Blog
    context_object_name = "posts"
    template_name = "blog/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context_def = self.get_user_context(title="Главная страница")
        return dict(list(context.items()) + list(context_def.items()))

    def get_queryset(self):
        return Blog.objects.order_by("-creat_time")

    def get_object(self):
        obj = super().get_object()
        # Record the last accessed date
        obj.last_accessed = timezone.now()
        obj.save()
        return obj


class ShowPostView(DataMixin, DetailView):
    model = Blog
    template_name = "blog/post.html"
    context_object_name = "post"
    slug_url_kwarg = "post_slug"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context_def = self.get_user_context(title=context["post"])
        return dict(list(context.items()) + list(context_def.items()))


class ShowCatView(DataMixin, ListView):
    paginate_by = None
    model = Categories
    template_name = "blog/cat.html"
    context_object_name = "cats"

    def get_queryset(self):
        return Categories.objects.all().order_by("name")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context_def = self.get_user_context(title="Категории")
        return dict(list(context.items()) + list(context_def.items()))


class ShowPostsByCat(DataMixin, ListView):
    model = Blog
    context_object_name = "posts"
    template_name = "blog/posts_by_cat.html"

    def get_queryset(self):
        return Blog.objects.filter(cat__slug=self.kwargs["cat_slug"]).order_by("-creat_time")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c = Categories.objects.get(slug=self.kwargs['cat_slug'])
        context_def = self.get_user_context(title=f"Категория - {c.name}")
        return dict(list(context.items()) + list(context_def.items()))


class RegisterUser(DataMixin, CreateView):
    form_class = UserCreationForm
    template_name = "blog/register.html"
    success_url = reverse_lazy("index")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cont_def = self.get_user_context(title="Регистрация")
        return dict(list(context.items()) + list(cont_def.items()))

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect("index")


class LoginUser(DataMixin, LoginView):
    form_class = AuthenticationForm
    template_name = "blog/login.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cont_def = self.get_user_context(title="Авторизация")
        return dict(list(context.items()) + list(cont_def.items()))

    def get_success_url(self):
        return reverse_lazy("index")


def logout_user(request):
    logout(request)
    return redirect("index")
