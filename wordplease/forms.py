from django.forms import ModelForm

from wordplease.models import Post


class PostForm(ModelForm):

    class Meta:
        model = Post
        fields = ['title', 'introduction', 'body', 'media_url', 'publication_date', 'categories']