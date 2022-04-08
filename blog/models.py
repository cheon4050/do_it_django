from django.contrib.auth.models import User
from django.db import models

import os
# Create your models here.

class Post(models.Model):
    title = models.CharField(max_length=30)
    hook = models.CharField(max_length=30, null=True)
    content = models.TextField()

    head_image = models.ImageField(upload_to='blog/images/%Y/%m/%d/', blank=True)
    attached_file = models.FileField(upload_to='blog/files/%Y/%m/%d/', blank=True)

    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    author = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    #methods
    def __str__(self):
        return f'[{self.pk}]  [{self.title}] :: {self.author}'

    def get_absolute_url(self):
        return f'/blog/{self.pk}/'

    def get_file_name(self):
        return os.path.basename(self.attached_file.name)

