from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin, UserPassesTestMixin
from django.core.cache import cache
from django.db.models import Exists, OuterRef
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_protect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .filters import PostFilter
from .forms import NewsForm, CommentForm
from .models import Post, Comment, Category, Subscription
from accounts.models import Author


class PostsView(ListView):
    model = Post
    ordering = '-created_at'
    template_name = 'news_list.html'
    context_object_name = 'news'
    paginate_by = 10
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
        context['is_admin'] = self.request.user.groups.filter(name='admin').exists()
        user = self.request.user
        context['author'] = user.author if user.id else None

        for post in context['news']:
            post.visible_comments_count = post.comment_set.filter(visible=True).count()

        return context


class PostDetailsView(DetailView):
    model = Post
    template_name = 'news_detail.html'
    context_object_name = 'post'

    def get_object(self, *args, **kwargs):  # переопределяем метод получения объекта, как ни странно
        obj = cache.get(f'post-{self.kwargs["pk"]}', None)

        # если объекта нет в кэше, то получаем его и записываем в кэш
        if not obj:
            obj = super().get_object(queryset=self.queryset)
            cache.set(f'post-{self.kwargs["pk"]}', obj)
        return obj

    def get_context_data(self, **kwargs):
        context = super(PostDetailsView, self).get_context_data(**kwargs)
        context['comments'] = Comment.objects.filter(visible=True, post_id=context['post'])
        context['comment_form'] = CommentForm()
        return context

    def post(self, request, *args, **kwargs):
        post = self.get_object()
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post_id = post
            user = self.request.user
            comment.created_by = Author.objects.get(system_user=user)
            comment.save()
        return self.get(request, *args, **kwargs)


class NewsCreateView(PermissionRequiredMixin, CreateView):
    permission_required = ('posts.add_post',)
    form_class = NewsForm
    model = Post
    template_name = 'post_edit.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.type_post = 'news'

        user = self.request.user
        post.created_by = Author.objects.get(system_user=user)

        return super(NewsCreateView, self).form_valid(form)


class PostEditView(PermissionRequiredMixin, UserPassesTestMixin, UpdateView):
    permission_required = ('posts.change_post',)
    form_class = NewsForm
    model = Post
    template_name = 'post_edit.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.update_at = datetime.now()

        return super(PostEditView, self).form_valid(form)

    def test_func(self):
        is_admin = self.request.user.groups.filter(name='admin').exists()
        post = self.get_object()
        return is_admin or self.request.user == post.created_by.system_user


class PostDeleteView(PermissionRequiredMixin, UserPassesTestMixin, DeleteView):
    permission_required = ('posts.delete_post',)
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('news')

    def test_func(self):
        is_admin = self.request.user.groups.filter(name='admin').exists()
        post = self.get_object()
        return is_admin or self.request.user == post.created_by.system_user


class ArticleCreateView(PermissionRequiredMixin, CreateView):
    permission_required = ('posts.add_post',)
    form_class = NewsForm
    model = Post
    template_name = 'post_edit.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.type_post = 'article'

        user = self.request.user
        post.created_by = Author.objects.get(system_user=user)

        return super(ArticleCreateView, self).form_valid(form)


@login_required
@csrf_protect
def subscriptions(request):
    if request.method == 'POST':
        category_id = request.POST.get('category_id')
        category = Category.objects.get(id=category_id)
        action = request.POST.get('action')

        if action == 'subscribe':
            Subscription.objects.create(user=request.user, category=category)
        elif action == 'unsubscribe':
            Subscription.objects.filter(
                user=request.user,
                category=category,
            ).delete()

    categories_with_subscriptions = Category.objects.annotate(
        user_subscribed=Exists(
            Subscription.objects.filter(
                user=request.user,
                category=OuterRef('pk'),
            )
        )
    ).order_by('name')
    return render(
        request,
        'subscriptions.html',
        {'categories': categories_with_subscriptions},
    )
