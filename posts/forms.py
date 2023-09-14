from django import forms
from django.core.exceptions import ValidationError

from accounts.models import Author
from .models import Post, Category


class NewsForm(forms.ModelForm):
    header = forms.CharField(label='Header', max_length=200)
    text = forms.TextInput()
    created_by = forms.ModelChoiceField(label='Author', queryset=Author.objects.all())
    # type_post = forms.ModelChoiceField(
    #     label='Category', queryset=Category.objects.all()
    # )

    class Meta:
        model = Post
        # fields = '__all__'
        fields = [
            'created_by',    # TODO поля не должно быть. действия доступны только авторизованным
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
