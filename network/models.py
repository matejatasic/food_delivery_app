from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Post(models.Model):
    content = models.CharField(blank=False, null=False, max_length=1000)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=True, related_name="posts")
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
       return f"Post by {self.user.username}"

class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="likes")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="likes")

class Follow(models.Model):
   user_following = models.ForeignKey(User, on_delete=models.CASCADE, related_name="follows_to")
   user_followed = models.ForeignKey(User, on_delete=models.CASCADE, related_name="follows_from")

   def __str__(self):
       return f"{self.user_following} follows {self.user_followed}"
