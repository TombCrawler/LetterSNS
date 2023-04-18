from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("allPosts", views.allPosts, name="allPosts"),
    path("post/<int:post_id>", views.post, name="post"),
    path("category/", views.category, name="category"),
    path("category_detail/<str:category>", views.category_detail, name="category_detail"),
    path("createP", views.createP, name="createP"),
    path("profile/<str:username>", views.profile, name="profile"),
    path("followToggle/<str:username>", views.followToggle, name="followToggle"),
    path("following_page", views.following_page, name="following_page"),
    path("update_post/<int:post_id>", views.update_post, name="update_post"),
    path("like_post/<int:post_id>", views.like_post, name='like_post'),
    path("unlike_post/<int:post_id>", views.unlike_post, name="unlike_post"),
    path("backup/", views.backup, name="backup"),
]

