from django.contrib.auth.models import User
from django.db import models

import os
# Create your models here.

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=200, unique=True, allow_unicode=True)
    def __str__(self):
        return self.name
    def get_absolute_url(self):
        return f'/blog/tag/{self.slug}'

class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=200, unique=True, allow_unicode=True)
    def __str__(self):
        return self.name
    def get_absolute_url(self):
        return f'/blog/category/{self.slug}'
    class Meta:
        verbose_name_plural = 'categories'


class Post(models.Model):
    title = models.CharField(max_length=30)
    hook = models.CharField(max_length=30, null=True)
    content = models.TextField()

    head_image = models.ImageField(upload_to='blog/images/%Y/%m/%d/', blank=True)
    attached_file = models.FileField(upload_to='blog/files/%Y/%m/%d/', blank=True)

    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    author = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    category = models.ForeignKey(Category, blank=True,null=True, on_delete=models.SET_NULL)
    tags = models.ManyToManyField(Tag, blank=True)
    #methods
    def __str__(self):
        return f'[{self.pk}]  [{self.title}] :: {self.author}'

    def get_absolute_url(self):
        return f'/blog/{self.pk}/'
    def get_pk(self):
        return self.pk
    def get_file_name(self):
        return os.path.basename(self.attached_file.name)

