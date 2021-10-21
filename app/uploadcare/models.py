from django.db import models
from pyuploadcare.dj.models import ImageField, ImageGroupField


class Post(models.Model):
    title = models.CharField(max_length=1024)
    content = models.TextField()
    logo = ImageField()
    attachments = ImageGroupField(blank=True, null=True)
