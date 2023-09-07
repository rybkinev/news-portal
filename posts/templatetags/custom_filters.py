from django import template
from django.template.defaultfilters import stringfilter

from posts.models import Censor

register = template.Library()


@register.filter
def censor(value):
    """
    фильтр будет обрабатывать Текст на предмет нежелательных слов.
    При нахождении таких слов, будет их заменять на * кроме первого и последнего символа.
    Нежелательные слова хранятся в БД, чтобы была возможность из админки менять список
    :param value: str
    :return: str
    """
    if not isinstance(value, str):
        raise TypeError("Фильтр цензурирования можно применить только к строкам")

    cens_all = Censor.objects.all()
    for i in cens_all:
        word = i.word
        if word.lower() in value.lower():
            new_word = word[0] + '*' * (len(word)-2) + word[-1]
            value = value.replace(word, new_word)

    return value
