from django.shortcuts import render
from pure_pagination import PageNotAnInteger, Paginator
from blog.models import *
import markdown


def blog_index(request):
    blog = Blog.objects.all().order_by("-create_time")
    # 分页测试
    try:
        # 获取当前页面，默认为1
        page = request.GET.get('page', 1)
    except PageNotAnInteger:
        page = 1
    paginator = Paginator(blog, 2, request=request)
    data = paginator.page(page)
    return render(request, 'index.html', locals())


def blog_content(request, title):
    data = Blog.objects.get(title=title)
    # 正向查询该博客关联的类别，标签
    categoty = data.category.name
    tags = data.tag.all()
    # 使用markdown解析数据库中的博客内容
    content = markdown.markdown(data.content, extensions=[
        'markdown.extensions.extra',
        'markdown.extensions.codehilite',
        'markdown.extensions.toc',
    ])
    return render(request, 'content.html', locals())


def blog_class(request, title):
    categories = Category.objects.all()
    return render(request, 'classify.html', locals())


def blog_class_details(request, title):
    data = Category.objects.get(name=title)
    # 反向查询从表blog中的数据
    result = data.blog_set.all()
    return render(request, 'classify_details.html', locals())


def tags(request, title):
    tags = Tag.objects.all()
    obj_tag_list = Tag.objects.all()
    # 更新标签的数量
    for obj_tag in obj_tag_list:
        tag_number = obj_tag.blog_set.count()
        obj_tag.number = tag_number
        obj_tag.save()
    return render(request, 'tags.html', locals())


def tag(request, title):
    data = Tag.objects.get(name=title)
    result = data.blog_set.all()
    return render(request, 'tag.html', locals())
