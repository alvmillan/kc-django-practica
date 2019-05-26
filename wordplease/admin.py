from django.contrib import admin

# Register your models here.
from wordplease.models import Category, Post, Blog

admin.site.register(Category)
admin.site.register(Blog)
admin.site.register(Post)
