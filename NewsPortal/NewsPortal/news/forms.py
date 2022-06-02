from django.forms import ModelForm
from .models import Post


# Создаём модельную форму
class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ['caption', 'text', 'category', 'Author']

