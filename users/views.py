import json
from django.shortcuts import render,get_object_or_404
from .models import User,Post,Comment,Like
# Create your views here.
def index(request):
    return render(request,"users/index.html",{
        "users":User.objects.all()
    })

def user(request,user_id):
    user=User.objects.get(pk=user_id)
    posts=user.posts.all()
    users = User.objects.all()
    return render(request,"users/user.html",{
        "user":user,
        "posts": posts,
        "users":users
    })


def post_likes(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    likes = post.likes.all() 
    return render(request, "users/post_likes.html", {
        "post": post,
        "likes": likes
    })

def post_comments(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    comments = post.comments.all()
    return render(request, "users/post_comments.html", {
        "post": post,
        "comments": comments
    })


from django.shortcuts import redirect, get_object_or_404
from django.http import HttpResponse
from .models import Post, User, Like

def like_post(request, post_id):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')  # Get the selected user ID from the form
        post = get_object_or_404(Post, pk=post_id)
        user = get_object_or_404(User, pk=user_id)
        
        # Check if the user has already liked the post
        if Like.objects.filter(user=user, post=post).exists():
            return HttpResponse('You have already liked this post.')
        
        # Create a new like
        Like.objects.create(user=user, post=post)

        # Redirect back to the same page after liking the post
        return redirect('user', user_id=post.user.id)

    return HttpResponse('Invalid request', status=400)


def add_comment(request, post_id):
    post = get_object_or_404(Post, pk=post_id)

    if request.method == 'POST':
        comment_text = request.POST.get('comment')
        user_id = request.POST.get('user_id')  # Retrieve user ID from the form
        user = get_object_or_404(User, pk=user_id)

        # Save the comment to the database
        Comment.objects.create(user=user, post=post, comment=comment_text)

        # Redirect to the post comments page
        return redirect('post_comments', post_id=post.id)

    return render(request, 'users/add_comment.html', {
        'post': post,
        'user_id': request.user.id if request.user.is_authenticated else None
    })
