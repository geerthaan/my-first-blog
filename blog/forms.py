from django import forms

from .models import Post, Comment


class PostForm(forms.ModelForm):
    # use model (class)Post to create this form
    class Meta:
        model = Post
        fields = ('title', 'text',)


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('author', 'text',)
