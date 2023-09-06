from django.db import models
from textwrap import shorten


post_types = [
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
    created_by = models.ForeignKey('accounts.Author', on_delete=models.PROTECT)
    update_at = models.DateTimeField(auto_now=True)
    type_post = models.CharField(
        max_length=10,
        choices=post_types,
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
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'


class PostCategory(models.Model):
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE)
    category_id = models.ForeignKey(Category, on_delete=models.PROTECT)


class Comment(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('accounts.Author', on_delete=models.PROTECT)
    update_at = models.DateTimeField(auto_now=True)
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE)
    text = models.TextField(null=False)
    rating = models.IntegerField(null=False, default=0)
    visible = models.BooleanField(default=True)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
