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


# @receiver(user_logged_in)
# def handle_user_logged_in(sender, request, user, **kwargs):
#     print('logged_in')
