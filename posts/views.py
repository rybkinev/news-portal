from django.shortcuts import render
from django.views.generic import ListView, DetailView

from posts.filters import PostFilter
from posts.models import Post


class PostsView(ListView):
    model = Post
    ordering = '-created_at'
    template_name = 'news.html'
    context_object_name = 'news'
    paginate_by = 3
    search = False

    def __init__(self, search=False):
        super(PostsView, self).__init__()
        self.search = search

    def get_queryset(self):
        # Получение и фильтрация записей из базы данных
        queryset = super().get_queryset()  # Получение изначального QuerySet
        queryset = queryset.filter(visible=True)  # Применение фильтра по видимости

        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        context['search'] = self.search
        return context


class PostDetailsView(DetailView):
    model = Post
    template_name = 'news_detail.html'
    context_object_name = 'post'
