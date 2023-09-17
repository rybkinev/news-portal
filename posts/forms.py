from django import forms
from django.core.exceptions import ValidationError

from accounts.models import Author
from .models import Post, Category, Comment


class NewsForm(forms.ModelForm):
    header = forms.CharField(label='Header', max_length=200)
    text = forms.TextInput()

    class Meta:
        model = Post
        # fields = '__all__'
        fields = [
            'header',
            'text',
        ]

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
