from django.db import models

# Create your models here.
class User(models.Model):
    user_name=models.CharField(max_length=64)
    email = models.EmailField()
    password = models.CharField(max_length=128)

    def __str__(self):
        return self.user_name
    
class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    content = models.TextField()
    uploaded_at = models.DateTimeField(auto_now_add=True)
    like_count = models.IntegerField(default=0)
    image = models.ImageField(upload_to='post_images/', blank=True, null=True)

    def __str__(self):
        return f"Post {self.id} by {self.user.user_name}"
    
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    comment = models.TextField()
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment {self.id} by {self.user.user_name} on Post {self.post.id}"
    
class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="likes")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="likes")
    time = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('post', 'user') 

    def __str__(self):
        formatted_time = self.time.strftime('%Y-%m-%d %H:%M:%S')
        return f"Like {self.id} by {self.user.user_name} on Post {self.post.id} by {self.post.user.user_name} at time {formatted_time}"
    
    def save(self, *args, **kwargs):
            if not self.pk:  
                self.post.like_count += 1
                self.post.save()
            super().save(*args, **kwargs) 

    def delete(self, *args, **kwargs):
        self.post.like_count -= 1
        self.post.save()
        super().delete(*args, **kwargs)

from django.db.models.signals import post_delete
from django.dispatch import receiver

@receiver(post_delete, sender=Like)
def decrement_like_count(sender, instance, **kwargs):
    instance.post.like_count -= 1
    instance.post.save()