from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import permission_required
from taggit.models import Tag
from django.core.paginator import Paginator
from .models import Post

from .forms import PostForm, PostDeleteForm


def home(request, tag=None):
    tag_obj = None

    if not tag:
        posts = Post.objects.all()
    else:
        tag_obj = get_object_or_404(Tag, slug=tag)
        posts = Post.objects.filter(tags__in=[tag_obj])

    paginator = Paginator(posts, 1)
    page = request.GET.get('page')
    posts = paginator.get_page(page)

    return render(request, 'home.html',
                  {'section': 'home',
                   'posts': posts,
                   'tag': tag_obj
                   })


def detail(request, slug=None):
    post = get_object_or_404(Post, slug=slug)

    return render(request, 'blog/detail.html',
                  {'section': 'blog_detail',
                   'post': post,
                   })


@permission_required('blog.add_post', raise_exception=True)
def create(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('home')
    else:
        form = PostForm()
    return render(request, 'blog/create.html',
                  {'section': 'blog_create',
                   'form': form,
                   })


@permission_required('blog.change_post', raise_exception=True)
def edit(request, pk=None):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect('blog:detail', slug=post.slug)
    else:
        form = PostForm(instance=post)

    return render(request, 'blog/edit.html',
                  {'section': 'blog_edit',
                   'form': form,
                   'post': post,
                   })


@permission_required('blog.delete_post', raise_exception=True)
def delete(request, pk=None):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        print(request)
        form = PostDeleteForm(request.POST, instance=post)
        if form.is_valid():
            post.delete()
            return redirect('home')
    else:
        form = PostDeleteForm(instance=post)
    return render(request, 'blog/delete.html',
                  {'section': 'blog_delete',
                   'form': form,
                   'post': post,
                   })
