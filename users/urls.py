from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),  
    path("<int:user_id>",views.user,name="user"),
    path("post/<int:post_id>/likes/", views.post_likes, name="post_likes"),
    path("post/<int:post_id>/comments/", views.post_comments, name="post_comments"),
    path("like-post/<int:post_id>/", views.like_post, name="like_post"),
    path("post/<int:post_id>/add_comment/", views.add_comment, name="add_comment"),
    
]