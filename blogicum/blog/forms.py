from django import forms
from django.utils import timezone   

from .models import Post, Comment

class PostForm(forms.ModelForm):
    pub_date = forms.DateTimeField(
        initial=timezone.now,
        required=True,
        widget=forms.DateTimeInput(
            attrs={
                "type": "datetime-local",
            },
            format="%Y-%m-%dT%H:%M",
        ),
    )
 

    class Meta:

        # Указываем модель, на основе которой должна строиться форма.
        model = Post
        # Указываем, что надо отобразить все поля.
        fields = (
            
            "title",
            "image",
            "text",
            "pub_date",
            "location",
            "category",
            "is_published",
        )

            
        
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = '__all__'