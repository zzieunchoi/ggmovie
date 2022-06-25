from django.db import models
from django.conf import settings
# Create your models here.

class Community(models.Model):
    category = models.CharField(max_length=50)
    title = models.CharField(max_length=50)
    content = models.TextField()
    # 빈값 넣었을 때 처리, 사진 업로드 의무도 아님 !
    imgfile = models.ImageField(null=True, upload_to="", blank=True)
    like = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name = 'like_community')
    updated_at = models.DateTimeField(auto_now = True) 
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class CommunityComment(models.Model):
    title = models.ForeignKey(Community, on_delete=models.CASCADE)
    content = models.TextField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    updated_at = models.DateTimeField(auto_now = True) 
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.content
