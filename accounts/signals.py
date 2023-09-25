from django.core.mail import EmailMultiAlternatives
from django.dispatch import receiver
from allauth.account.signals import user_signed_up, user_logged_in
from django.contrib.auth.models import Group
from .models import Author


@receiver(user_signed_up)
def handle_user_signed_up(sender, request, user, **kwargs):
    print('signed_up')
    group = Group.objects.get(name='authors')
    if group:
        user.groups.add(group)

    # create author
    Author.objects.create(system_user=user)

    subject = 'Добро пожаловать в наш интернет-магазин!'
    text = f'{user.username}, вы успешно зарегистрировались на сайте!'
    html = (
        f'<b>{user.username}</b>, вы успешно зарегистрировались на '
        f'<a href="http://127.0.0.1:8000">сайте</a>!'
    )
    msg = EmailMultiAlternatives(
        subject=subject, body=text, from_email=None, to=[user.email]
    )
    msg.attach_alternative(html, "text/html")
    msg.send()


@receiver(user_logged_in)
def handle_user_logged_in(sender, request, user, **kwargs):
    print('logged_in')

    subject = 'Добро пожаловать в наш интернет-магазин!'
    text = f'{user.username}, вы успешно зарегистрировались на сайте!'
    html = (
        f'<b>{user.username}</b>, вы успешно зарегистрировались на '
        f'<a href="http://127.0.0.1:8000">сайте</a>!'
    )
    msg = EmailMultiAlternatives(
        subject=subject, body=text, from_email=None, to=[user.email]
    )
    msg.attach_alternative(html, "text/html")
    msg.send()
