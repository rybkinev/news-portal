import datetime

from django.contrib.auth.models import User
from django.core.cache import cache
from django.core.mail import EmailMultiAlternatives
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

    @property
    def absolute_url(self):
        return reverse('news_detail', args=[str(self.id)])

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

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        cache.delete(f'product-{self.pk}')

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'

    @staticmethod
    def sending_mail(post_id):
        instance = Post.objects.get(id=post_id)

        emails = User.objects.filter(
            subscriptions__category__in=instance.categories.all()
        ).values_list('email', flat=True)

        subject = f'Новый пост среди выбранных вами категорий'

        text_content = (
            f'Заголовок: {instance.header}\n'
            f'Ссылка: http://127.0.0.1:8000{instance.get_absolute_url()}'
        )
        html_content = (
            f'Заголовок: {instance.header}<br>'
            f'<a href="http://127.0.0.1{instance.get_absolute_url()}">'
            f'Ссылка на пост</a>'
        )
        for email in emails:
            msg = EmailMultiAlternatives(subject, text_content, None, [email])
            msg.attach_alternative(html_content, "text/html")
            msg.send()

    @staticmethod
    def sending_new_posts():

        today = datetime.datetime.today()
        today = today.replace(hour=0, minute=0, second=0, microsecond=0)
        last_sending = today - datetime.timedelta(days=7)

        last_posts = Post.objects \
            .filter(
            visible=True,
            created_at__gt=last_sending
        ).order_by('-created_at')

        emails = Subscription.objects \
            .filter(category__post__in=last_posts) \
            .values_list('category__post', 'user__email') \
            .distinct().order_by('user__email')

        sending_dict = dict()
        for post_id, email in emails:
            post = Post.objects.get(id=post_id)
            if email in sending_dict:
                sending_dict[email].append(post)
            else:
                sending_dict[email] = [post]

        subject = f'Новые посты с {last_sending.strftime("%x")}'
        text_content = (
            'Новые посты на портале:\n'
        )
        html_content = (
            'Новые посты на портале:<br>'
        )
        for mail, posts in sending_dict.items():
            msg = EmailMultiAlternatives(
                subject,
                text_content + '\n'.join([f'http://127.0.0.1{i.get_absolute_url()}' for i in posts]),
                None,
                [mail]
            )

            msg.attach_alternative(
                html_content + '<br>'.join(
                    [f'<a href="http://127.0.0.1{i.get_absolute_url()}">{i.header}</a>' for i in posts]),
                "text/html"
            )
            msg.send()


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
