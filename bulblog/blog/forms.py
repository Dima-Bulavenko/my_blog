from django import forms
from django.core.exceptions import ValidationError

from .models import *


class AddPostForm(forms.ModelForm):
    cat = forms.ModelChoiceField(queryset=Categories.objects.all(), empty_label="Категория не выбрана")

    class Meta:
        model = Blog
        fields = ["name", "slug", "content", "cat"]

    def clean_name(self):
        name = self.cleaned_data["name"]
        if len(name) > 99:
            raise ValidationError("Длина превышает 100 символов")
        return name
