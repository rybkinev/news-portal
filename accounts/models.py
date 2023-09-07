from django.db import models
from django.db.models import Sum

from posts.models import Post, Comment


class Author(models.Model):
    system_user = models.OneToOneField('auth.User', on_delete=models.PROTECT)
    rating = models.IntegerField(null=False, default=0)
    hide_posts = models.BooleanField(default=False)    # Скрыть все посты автора

    def update_rating(self):
        total_rating_list = []

        # rating_posts = Post.objects.filter(created_by=self.id).aggregate(total_sum=Sum('rating')).get('total_sum', 0)
        rating_posts = self.posts.all().aggregate(total_sum=Sum('rating')).get('total_sum', 0)
        if rating_posts:
            total_rating_list.append(rating_posts * 3)

        # rating_com = Comment.objects.filter(created_by=self.id).aggregate(total_sum=Sum('rating')).get('total_sum', 0)
        rating_com = self.comments.all().aggregate(total_sum=Sum('rating')).get('total_sum', 0)
        if rating_com:
            total_rating_list.append(rating_com)

        sum_rating_com_post = Comment.objects.filter(
            post_id__created_by=self.id
        ).aggregate(total_sum=Sum('rating')).get('total_sum', 0)
        if sum_rating_com_post:
            total_rating_list.append(sum_rating_com_post)

        total_rating = 0
        for i in total_rating_list:
            total_rating += i

        self.rating = total_rating
        self.save()

    class Meta:
        verbose_name = 'Автор'
        verbose_name_plural = 'Авторы'
