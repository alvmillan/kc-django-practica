"""Pyblog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from users.views import LoginView, LogoutView, SignUpView
from wordplease.views import BlogListView, BlogDetailView, PostListView, PostDetailView, NewPostView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login', LoginView.as_view(), name='login'),
    path('logout', LogoutView.as_view(), name='logout'),
    path('signup', SignUpView.as_view(), name='sign_up'),
    path('blogs/', BlogListView.as_view(), name='blog_list'),
    path('new-post', NewPostView.as_view(), name='new_post'),
    path('blogs/<slug:owner>', BlogDetailView.as_view(), name="blog_detail"),
    path('blogs/<slug:owner>/<int:pk>', PostDetailView.as_view(), name="post_detail"),
    path('', PostListView.as_view(), name='home')
]
