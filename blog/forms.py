from django import forms

from .models import Post

class PostForm(forms.ModelForm):

    # use model (class)Post to create this form
    class Meta:
        model = Post
        fields = ('title', 'text',)