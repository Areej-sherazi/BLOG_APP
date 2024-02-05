"""
URL configuration for blogApp project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
# from signup.views import CustomUserViewSet


# urlpatterns = [
#     path('admin/', admin.site.urls),
#     path('auth/', include('djoser.urls')),
#     path('post/', include('blog_post.urls')),
#     path('auth/verify_code/<str:email>/', CustomUserViewSet.as_view({'post': 'verify_code'}), name='verify_code'),
#     path('register/', CustomUserViewSet.as_view({'post': 'register_user'}), name='register_user'),
#     path('login/', CustomUserViewSet.as_view({'post': 'sign_in'}), name='sign_in'),
#     path('auth/resend_code/', CustomUserViewSet.as_view({'post': 'resend_code'}), name='resend_code'),
# ]

from django.urls import path, include
from rest_framework.routers import DefaultRouter
# from blog_post.views import BlogPostViewSet
from signup.views import CustomUserViewSet
# router = DefaultRouter()
# router.register(r'posts', BlogPostViewSet, basename='blogpost')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('post/', include('blog_post.urls')),  # Include blog_post URLs first
    path('auth/', include('djoser.urls')),
    path('auth/verify_code/<str:email>/', CustomUserViewSet.as_view({'post': 'verify_code'}), name='verify_code'),
    path('register/', CustomUserViewSet.as_view({'post': 'register_user'}), name='register_user'),
    path('login/', CustomUserViewSet.as_view({'post': 'sign_in'}), name='sign_in'),
    path('auth/resend_code/', CustomUserViewSet.as_view({'post': 'resend_code'}), name='resend_code'),
]

   
