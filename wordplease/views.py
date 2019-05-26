from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404

#
from django.views import View
from django.views.generic import ListView

from wordplease.forms import PostForm
from wordplease.models import Blog, Post


class BlogListView(ListView):
    template_name = 'blogs/list.html'

    def get_queryset(self):
        queryset = Blog.objects.order_by('-creation_date')
        return queryset


class BlogDetailView(View):
    def get(self, request, owner):

        blog = get_object_or_404(Blog.objects.filter(owner__username=owner))
        context = {'blog': blog}

        html = render(request, 'blogs/detail.html', context)

        return HttpResponse(html)

class PostDetailView(View):
    def get(self, request, owner, pk):
        post = get_object_or_404(Post, pk=pk)
        context = {'post': post}
        html = render(request, 'blogs/post_detail.html', context)
        return HttpResponse(html)

class PostListView(ListView):
    template_name = 'blogs/post_list.html'

    def get_queryset(self):
        queryset = Post.objects.all()
        return queryset

class NewPostView(LoginRequiredMixin, View):

    def get(self, request):
        form = PostForm()
        context = {'form': form}
        return render(request, 'blogs/new_post.html', context)

    def post(self, request):
        post = Post()
        blog = get_object_or_404(Blog.objects.filter(owner=request.user))
        post.published_on = blog
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            new_post = form.save()
            messages.success(request, 'Post created with ID {0}'.format(new_post.pk))
            form = PostForm
        context = {'form': form}
        return render(request, 'blogs/new_post.html', context)

