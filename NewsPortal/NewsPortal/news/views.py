from django.shortcuts import render, reverse, redirect
from django.views.generic import ListView, UpdateView, CreateView, DetailView, DeleteView
from django.core.paginator import Paginator
from .models import Post, Category, UserCategory, PostCategory
from .filters import PostFilter
from django.core.mail import send_mail, EmailMultiAlternatives
from datetime import datetime
from .forms import PostForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.template.loader import render_to_string


class PostList(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'posts.html'
    context_object_name = 'posts'
    queryset = Post.objects.order_by('-id')
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        context['filter'] = PostFilter(self.request.GET, queryset=self.get_queryset())
        return context


class SearchList(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'search.html'
    context_object_name = 'posts'
    queryset = Post.objects.order_by('-id')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        context['filter'] = PostFilter(self.request.GET, queryset=self.get_queryset())
        return context


class PostDetail(LoginRequiredMixin, DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'


class PostCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('news.add_post',)
    template_name = 'create.html'
    form_class = PostForm


class PostUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = ('news.change_post',)
    template_name = 'create.html'
    form_class = PostForm

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)


class PostDelete(DeleteView):
    template_name = 'delete.html'
    queryset = Post.objects.all()
    success_url = '/posts/'


class CategoryList(ListView):
    model = Category
    template_name = 'category.html'
    context_object_name = 'category'
    queryset = Category.objects.all()
    success_url = '/posts/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = Category.objects.all()
        return context

    def post(self, request, *args, **kwargs):
        category_id = request.POST['category']
        subscriber = request.user.username
        send_mail(
            subject=f'{subscriber}: подписка на рассылку новостей',
            message=f'{subscriber}: Вы подписаны на рассылку новостей по категории {Category.objects.get(id=category_id)}',
            from_email='anel031@yandex.ru',
            recipient_list=['anel04tileulieva05@gmail.com']  #request.user.email
        )
        return redirect('/posts/')


@login_required
def subscribe_me(request, pk):
    user = request.user
    category = Category.objects.get(id=pk)
    subscribe = UserCategory(user_id=user.id, category_id=category.id)
    subscribe.save()
    return redirect('/posts/')

