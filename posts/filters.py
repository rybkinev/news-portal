from django.forms import DateTimeInput
from django_filters import FilterSet, DateTimeFilter, ChoiceFilter
from .models import Post, POST_TYPES


class PostFilter(FilterSet):
    created_after = DateTimeFilter(
        field_name='created_at',
        lookup_expr='gt',
        widget=DateTimeInput(
            format='%Y-%m-%dT%H:%M',
            attrs={'type': 'datetime-local'},
        ),
    )
    type_post = ChoiceFilter(
        label='Type', choices=POST_TYPES
    )

    class Meta:
        # В Meta классе мы должны указать Django модель,
        # в которой будем фильтровать записи.
        model = Post
        # В fields мы описываем по каким полям модели
        # будет производиться фильтрация.
        fields = {
            # поиск по названию
            'header': ['icontains'],
            # количество товаров должно быть больше или равно
            # 'type_post': ['icontains'],
        }
