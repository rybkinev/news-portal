from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from posts.filters import PostFilter
from posts.forms import NewsForm
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
        queryset = queryset.filter(visible=True, created_by__hide_posts=False)  # Применение фильтров по видимости

        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        context['search'] = self.search
        context['count_posts'] = Post.objects.filter(visible=True, created_by__hide_posts=False).count()

        return context


class PostDetailsView(DetailView):
    model = Post
    template_name = 'news_detail.html'
    context_object_name = 'post'


class NewsCreateView(CreateView):
    form_class = NewsForm
    model = Post
    template_name = 'post_edit.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.type_post = 'news'
        return super(NewsCreateView, self).form_valid(form)


class NewsEditView(UpdateView):
    form_class = NewsForm
    model = Post
    template_name = 'post_edit.html'


class NewsDeleteView(DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('news')


class ArticleCreateView(CreateView):
    form_class = NewsForm
    model = Post
    template_name = 'post_edit.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.type_post = 'article'
        return super(ArticleCreateView, self).form_valid(form)
