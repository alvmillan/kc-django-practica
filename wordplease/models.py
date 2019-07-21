from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Category(models.Model):
    name = models.CharField(max_length=30)

    class Meta:
        verbose_name_plural = "categories"

    def __unicode__(self):
        return self.name


class Blog(models.Model):

    name = models.CharField(max_length=150)
    description = models.TextField(null=True, blank=True)
    creation_date = models.DateTimeField(auto_now_add=True)
    modification_date = models.DateTimeField(auto_now=True)
    owner = models.OneToOneField(User, related_name='blog', on_delete=models.CASCADE)

    def get_absolute_url(self):
        return reverse('blog_detail', args=[self.owner.username])

    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(max_length=50)
    introduction = models.TextField()
    body = models.TextField()
    media_url = models.URLField(null=True)
    publication_date = models.DateTimeField()
    creation_date = models.DateTimeField(auto_now_add=True)
    modification_date = models.DateTimeField(auto_now=True)
    published_on = models.ForeignKey(Blog, related_name='posts', on_delete=models.CASCADE)
    categories = models.ManyToManyField(Category, related_name='post')

    class Meta:
        ordering = ['-creation_date']

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post_detail', args=[self.published_on.owner.username, self.pk])

    def get_author(self):
        return '{0} {1}'.format(self.published_on.owner.first_name, self.published_on.owner.last_name)
