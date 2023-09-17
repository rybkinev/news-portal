from django.urls import path, include

from . import views

news_patterns = [
    path('', views.PostsView.as_view(), name='news'),
    path('<int:pk>', views.PostDetailsView.as_view(), name='news_detail'),
    path('search/', views.PostsView.as_view(search=True), name='news_search'),
    path('create/', views.NewsCreateView.as_view(), name='news_create'),
    path('<int:pk>/edit/', views.PostEditView.as_view(), name='news_update'),
    path('<int:pk>/delete/', views.PostDeleteView.as_view(), name='news_delete'),
]

article_patterns = [
    path('create/', views.ArticleCreateView.as_view(), name='article_create'),
    path('<int:pk>/edit/', views.PostEditView.as_view(), name='article_update'),
    path('<int:pk>/delete/', views.PostDeleteView.as_view(), name='article_delete'),
]

urlpatterns = [
    path('news/', include(news_patterns)),
    path('article/', include(article_patterns))
]
