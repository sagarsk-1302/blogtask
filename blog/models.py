from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Post(models.Model):
    title = models.CharField(max_length=200, unique=True)
    author = models.ForeignKey(User, on_delete= models.CASCADE,related_name='blog_posts')
    content = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    image_urls = models.JSONField()

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return self.title



class Comments(models.Model):
    post = models.ForeignKey(Post, on_delete= models.CASCADE)
    user = models.ForeignKey(User, on_delete= models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)
    body = models.TextField()

    def __str__(self):
        return self.user.username+"->"+self.post.title 