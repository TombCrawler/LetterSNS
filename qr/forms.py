from django import forms
from .models import *

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'description', 'image', 'category']
        labels = {
           'description' : 'Body',
           'image' : 'Image Gift'
        }
        exclude=['create_date', 'user']

class ProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['profile_picture', 'bio']