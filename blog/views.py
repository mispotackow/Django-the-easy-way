from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import permission_required
from taggit.models import Tag
from django.core.paginator import Paginator
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.pagination import PageNumberPagination

from .models import Post
from .serializers import PostSerializer
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


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def blog_api_view(request):
    if request.method == 'GET':
        paginator = PageNumberPagination()
        paginator.page_size = 5
        post_objects = Post.objects.all()
        result = paginator.paginate_queryset(post_objects, request)

        # serializer без пагинации
        #serializer = PostSerializer(Post.objects.all(), many=True)
        serializer = PostSerializer(result, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,
                            status=status.HTTP_201_CREATED)
        return Response(serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def blog_api_detail_view(request, pk=None):
    try:
        post = Post.objects.get(pk=pk)
    except post.DoesNotExist:
        return Response(status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'GET':
        serializer = PostSerializer(post)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = PostSerializer(post, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(post.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# для дополнительной настройки если IsAuthenticated не подходит
# @permission_classes([CustomPermission])
class CustomPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.has_perm('mysite.add_post'):
            return True
        return True
