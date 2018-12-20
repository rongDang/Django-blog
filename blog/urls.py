# -*- encoding:utf8 -*-
from django.urls import path
from blog import views

urlpatterns = [
    path('', views.blog_index, name="blog_index"),
    path('content/<title>', views.blog_content, name="blog_content"),
    path('class/<title>', views.blog_class, name="blog_class"),
    path('class_details/<title>', views.blog_class_details, name="blog_class_details"),
    path('tags/<title>', views.tags, name='blog_tags'),
    path('tag/<title>', views.tag, name='blog_tag'),
    # 关于allauth中的模板，我们只需要对其进行美化就可以，accounts/<title>是allauth中的链接，这里我们给它写上对应的视图函数
    path('accounts/<title>', views.profile, name='profile'),
    path('logout/', views.logout, name='logout'),
    path('submit_comment/', views.submit_comment, name='submit_comment'),
]


