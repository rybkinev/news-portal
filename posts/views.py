from django.shortcuts import render
from django.views.generic import ListView, DetailView

from posts.models import Post


class PostsView(ListView):
    model = Post
    ordering = '-created_at'
    template_name = 'news.html'
    context_object_name = 'news'
    paginate_by = 3

    def get_queryset(self):
        # Получение и фильтрация записей из базы данных
        queryset = super().get_queryset()  # Получение изначального QuerySet
        queryset = queryset.filter(visible=True)  # Применение фильтрации

        return queryset


class PostDetailsView(DetailView):
    model = Post
    template_name = 'news_detail.html'
    context_object_name = 'post'
