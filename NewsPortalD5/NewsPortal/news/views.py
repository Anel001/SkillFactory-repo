from django.shortcuts import render
from django.views.generic import ListView, UpdateView, CreateView, DetailView, DeleteView
from django.core.paginator import Paginator
from .models import Post, Category
from .forms import PostForm
from .filters import PostFilter
from datetime import datetime
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin


class PostList(ListView):
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


class SearchList(ListView):
    model = Post
    template_name = 'searchposts.html'
    context_object_name = 'posts'
    queryset = Post.objects.order_by('-id')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        context['filter'] = PostFilter(self.request.GET, queryset=self.get_queryset())
        return context


class PostDetail(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'


class PostCreateView(PermissionRequiredMixin, CreateView):
    permission_required = ('news.add_post',)
    template_name = 'create.html'
    form_class = PostForm


class PostUpdateView(PermissionRequiredMixin, UpdateView):
    permission_required = ('news.change_post',)
    template_name = 'create.html'
    form_class = PostForm

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)


class PostDeleteView(DeleteView):
    template_name = 'delete.html'
    queryset = Post.objects.all()
    success_url = '/posts/'

