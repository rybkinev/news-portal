from django.urls import path, include

from .views import PostsView, PostDetailsView, NewsCreateView, NewsEditView, NewsDeleteView, ArticleCreateView

news_patterns = [
    path('', PostsView.as_view(), name='news'),
    path('<int:pk>', PostDetailsView.as_view(), name='news_detail'),
    path('search/', PostsView.as_view(search=True), name='news_search'),
    path('create/', NewsCreateView.as_view(), name='news_create'),
    path('<int:pk>/edit/', NewsEditView.as_view(), name='news_update'),
    path('<int:pk>/delete/', NewsDeleteView.as_view(), name='news_delete'),
]

article_patterns = [
    path('create/', ArticleCreateView.as_view(), name='article_create'),
    path('<int:pk>/edit/', NewsEditView.as_view(), name='article_update'),
    path('<int:pk>/delete/', NewsDeleteView.as_view(), name='article_delete'),
]

urlpatterns = [
    path('news/', include(news_patterns)),
    path('article/', include(article_patterns))
]
