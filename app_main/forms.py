from django import forms
from django.forms import fields
from app_main.models import Todo


class Create_Todo_Form(forms.ModelForm):
    content = forms.CharField(widget=forms.Textarea(attrs={"rows": 3}), label="İçerik")
    color = forms.ChoiceField(label="Renk (html5 color)", choices=Todo.COLORS)
    is_marked = forms.BooleanField(label="İşaretlensin", required=False)

    class Meta:
        model = Todo
        fields = ("content", "color", "is_marked")
