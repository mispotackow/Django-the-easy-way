from django.urls import path, include
from . import views

app_name = 'blog'

urlpatterns = [
    path('api/', views.blog_api_view, name='blog_api_view'),
    path('api/<int:pk>/', views.blog_api_detail_view, name='blog_api_detail_view'),
    path('api/auth/', include('rest_auth.urls')),
    path('api/auth/registration/', include('rest_auth.registration.urls')),
    path('create/', views.create, name='create'),
    path('edit/<int:pk>/', views.edit, name='edit'),
    path('delete/<int:pk>/', views.delete, name='delete'),
    path('tags/<slug:tag>', views.home, name='posts_by_tag'),
    path('<slug:slug>/', views.detail, name='detail'),
]