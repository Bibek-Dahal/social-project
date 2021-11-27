from django import forms
from .models import Comment, Post
class PostCreateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title','description','pic')

class PostUpdateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title','description','pic')

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)

