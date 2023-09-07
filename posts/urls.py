from django.urls import path

from .views import PostsView, PostDetailsView

urlpatterns = [
    path('', PostsView.as_view()),
    path('<int:pk>', PostDetailsView.as_view()),
]