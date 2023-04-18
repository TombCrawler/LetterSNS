from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.exceptions import ValidationError, PermissionDenied


class User(AbstractUser):
    following = models.ManyToManyField("self", blank=True, related_name="followers", symmetrical=False)
    liked_posts = models.ManyToManyField("Post", blank=True, related_name="liked_posts")
    
    def __str__(self):
        return f"{self.id}: {self.username}"


class Post(models.Model):
    category_item ={
        ("Hip-Hop", "Hip-Hop"),
        ("Diary", "Diary"),
        ("Romance", "Romance"),
        ("Bucket", "Bucket")
    }
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=False, null=False, related_name="posts")
    title = models.CharField(max_length=255)
    description = models.TextField(max_length=220)
    image = models.ImageField(upload_to='product_images/', blank=True)
    qr_code = models.ImageField(upload_to='qr_codes/', blank=True)
    category = models.CharField(max_length=20, choices=category_item)
    body = models.TextField(max_length=140)
    create_date = models.DateTimeField(auto_now_add=True)
    likes =models.ManyToManyField(User, blank=True, related_name="liked_by")
    
    def __str__(self):
        return f"{self.id}: {self.title} - Posted by {self.user.username}/ Likes {self.likes.count()}"


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to="profile_pictures/", blank=True)
    bio = models.TextField(max_length=500, blank=True)
    
    def is_valid_profile(self):
       return len(self.bio) <= 500

    def __str__(self):
        return self.user.username


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(max_length=140, null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.text} posted by {self.user.username} on {self.created_date}"
        

