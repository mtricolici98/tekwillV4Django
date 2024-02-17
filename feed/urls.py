"""
URL configuration for tekwillV4Django project.

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
from django.urls import path

from feed.views import get_comments_for_post, add_comment, get_post_list, add_post, login, register, \
    get_comments_for_user, like_post

urlpatterns = [
    path('user/login', login),
    path('user/register', register),
    path('post/list', get_post_list),
    path('post/add', add_post),
    path('post/like/<post_id>', like_post),
    path('comments/add', add_comment),
    path('comments/get/user', get_comments_for_user),
    path('comments/get/<post_id>', get_comments_for_post),
]
