from django.db import models
from textwrap import shorten
import enum

# TODO Отметил несколько мест где код можно улучшить и доработать:
# - В моделях Post и Comment вы можете добавить параметр related_name для поля created_by,
# чтобы сделать обратные связи более ясными и читаемыми.

post_types = [
    ('news', 'Новость'),
    ('article', 'Статья')
]


def change_rating(obj, like):
    if like:
        obj.rating += 1
    else:
        obj.rating -= 1
    obj.save()


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
        # self.rating += 1
        # self.save()
        change_rating(self, True)

    def dislike(self):
        # self.rating -= 1
        # self.save()
        change_rating(self, False)

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
        change_rating(self, True)

    def dislike(self):
        # self.rating -= 1
        # self.save()
        change_rating(self, False)

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'


class Censor(models.Model):
    word = models.CharField(max_length=20, null=False)

    class Meta:
        verbose_name = 'Цензура'
        verbose_name_plural = 'Цензура'
