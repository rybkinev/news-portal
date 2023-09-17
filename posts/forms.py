from django import forms
from django.core.exceptions import ValidationError

from .models import Post, Category, Comment


class NewsForm(forms.ModelForm):
    header = forms.CharField(label='Header', max_length=200)
    text = forms.TextInput()
    categories = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(),
        label='Categories',
        widget=forms.CheckboxSelectMultiple(),
    )

    class Meta:
        model = Post
        # fields = '__all__'
        fields = [
            'header',
            'categories',
            'text',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['categories'].widget.choices = [(category.id, category.name) for category in Category.objects.all()]
        self.fields['categories'].label_from_instance = lambda obj: obj.name

    def clean(self):
        perm_len = 200
        cleaned_data = super().clean()
        header = cleaned_data.get("description")
        if header is not None and len(header) > perm_len:
            raise ValidationError({
                "header": f"Описание не может быть Более {perm_len} символов."
            })

        return cleaned_data


class CommentForm(forms.ModelForm):
    text = forms.TextInput()

    class Meta:
        model = Comment
        fields = ['text']
