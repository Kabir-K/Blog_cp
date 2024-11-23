from django.contrib import admin
from .models import User,Post,Comment,Like
# Register your models here.
class LikeAdmin(admin.ModelAdmin):
    def delete_model(self, request, obj):
        # Decrement the like count for the associated post before deleting the like
        obj.post.like_count -= 1
        obj.post.save()  # Save the post to reflect the change in the like count
        super().delete_model(request, obj)

admin.site.register(User)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Like,LikeAdmin)