from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import post_save, m2m_changed, pre_save
from django.dispatch import receiver

from posts.models import Post
from posts.tasks import send_mail


@receiver(m2m_changed, sender=Post.categories.through)
def product_categories_changed(sender, instance, action, **kwargs):
    if action != 'post_add' or instance.is_update:
        return

    # Post.sending_mail(instance)
    # emails = User.objects.filter(
    #     subscriptions__category__in=instance.categories.all()
    # ).values_list('email', flat=True)
    #
    # subject = f'Новый пост среди выбранных вами категорий'
    #
    # text_content = (
    #     f'Заголовок: {instance.header}\n'
    #     f'Ссылка: http://127.0.0.1:8000{instance.get_absolute_url()}'
    # )
    # html_content = (
    #     f'Заголовок: {instance.header}<br>'
    #     f'<a href="http://127.0.0.1{instance.get_absolute_url()}">'
    #     f'Ссылка на пост</a>'
    # )
    # for email in emails:
    #     msg = EmailMultiAlternatives(subject, text_content, None, [email])
    #     msg.attach_alternative(html_content, "text/html")
    #     msg.send()


@receiver(post_save, sender=Post)
def product_created(instance, created, **kwargs):
    if not created:
        # Вынужденная мера, поскольку в момент создания поста категории еще не записаны в базу
        '''Если нужно чтобы отправлялось письмо, даже если пост уже создан, но добавлена категория,
        Тогда этот код лишний'''
        instance.is_update = True
        return

    send_mail.apply_async([instance.id], countdown=5)

    # emails = User.objects.filter(
    #     subscriptions__category__in=instance.categories.all()
    # ).values_list('email', flat=True)
    #
    # subject = f'Новый пост'
    #
    # text_content = (
    #     f'Заголовок: {instance.header}\n'
    #     f'Ссылка: http://127.0.0.1:8000{instance.get_absolute_url()}'
    # )
    # html_content = (
    #     f'Заголовок: {instance.header}<br>'
    #     f'<a href="http://127.0.0.1{instance.get_absolute_url()}">'
    #     f'Ссылка на пост</a>'
    # )
    # for email in emails:
    #     msg = EmailMultiAlternatives(subject, text_content, None, [email])
    #     msg.attach_alternative(html_content, "text/html")
    #     msg.send()
