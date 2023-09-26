from django.contrib.auth.models import User
from django.db import models
from textwrap import shorten
import enum

from django.urls import reverse

POST_TYPES = [
    ('news', 'Новость'),
    ('article', 'Статья')
]


class Category(models.Model):
    name = models.CharField(
        max_length=255,
        null=False,
        unique=True
    )
    valid = models.BooleanField(default=True)   # Не актуальная категория будет недоступна к выбору

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Post(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('accounts.Author', on_delete=models.PROTECT, related_name='posts')
    update_at = models.DateTimeField(auto_now=True)
    is_update = models.BooleanField(default=False)
    type_post = models.CharField(
        max_length=10,
        choices=POST_TYPES,
        default='article'
    )
    header = models.CharField(
        max_length=200,
        default=''
    )
    text = models.TextField(null=False)
    rating = models.IntegerField(null=False, default=0)
    visible = models.BooleanField(default=True)     # Видимость статьи

    categories = models.ManyToManyField(Category, through='PostCategory')

    @property
    def preview(self):
        return shorten(str(self.text), 124, placeholder='...')

    def like(self):
        # self.rating += 1
        # self.save()
        self.change_rating(self, True)

    def dislike(self):
        # self.rating -= 1
        # self.save()
        self.change_rating(self, False)

    @staticmethod
    def change_rating(obj, like):
        if like:
            obj.rating += 1
        else:
            obj.rating -= 1
        obj.save()

    def get_absolute_url(self):
        return reverse('news_detail', args=[str(self.id)])

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'


class PostCategory(models.Model):
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE)
    category_id = models.ForeignKey(Category, on_delete=models.PROTECT)


class Comment(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('accounts.Author', on_delete=models.PROTECT, related_name='comments')
    update_at = models.DateTimeField(auto_now=True)
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE)
    text = models.TextField(null=False)
    rating = models.IntegerField(null=False, default=0)
    visible = models.BooleanField(default=True)

    def like(self):
        # self.rating += 1
        # self.save()
        Post.change_rating(self, True)

    def dislike(self):
        # self.rating -= 1
        # self.save()
        Post.change_rating(self, False)

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'


class Censor(models.Model):
    word = models.CharField(max_length=20, null=False)

    class Meta:
        verbose_name = 'Цензура'
        verbose_name_plural = 'Цензура'


class Subscription(models.Model):
    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name='subscriptions',
    )
    category = models.ForeignKey(
        to='Category',
        on_delete=models.CASCADE,
        related_name='subscriptions',
    )
