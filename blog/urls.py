# -*- encoding:utf8 -*-
from django.urls import path
from blog import views

urlpatterns = [
    path('index/', views.blog_index, name="blog_index"),
    path('content/<title>', views.blog_content, name="blog_content"),
    path('class/<title>', views.blog_class, name="blog_class"),
    path('class_details/<title>', views.blog_class_details, name="blog_class_details"),
    path('tags/<title>', views.tags, name='blog_tags'),
    path('tag/<title>', views.tag, name='blog_tag'),
]


