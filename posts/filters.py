from django.forms import DateTimeInput, Select
from django_filters import FilterSet, DateTimeFilter, ChoiceFilter, ModelChoiceFilter
from .models import Post, POST_TYPES, Category


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
        label='Type',
        choices=POST_TYPES
    )
    # TODO в списке должно быть наименование, а не объект
    categories = ModelChoiceFilter(
        field_name='categories',
        to_field_name='name',
        queryset=Category.objects.filter(valid=True),
        label='Categories',
        # widget=Select(attrs={'class': 'form-control'}),
    )

    class Meta:
        # В Meta классе мы должны указать Django модель,
        # в которой будем фильтровать записи.
        model = Post
        # В fields мы описываем по каким полям модели
        # будет производиться фильтрация.
        fields = {
            'header': ['icontains'],
        }
