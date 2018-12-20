from django.shortcuts import render, HttpResponseRedirect, reverse, HttpResponse
from django.contrib.auth.decorators import login_required
from pure_pagination import PageNotAnInteger, Paginator
from blog.models import *
from .forms import MDEditorForm
import markdown


# 首页显示，分页的使用
def blog_index(request):
    print(request.user.is_authenticated)
    # 设置session一天后过期
    request.session.set_expiry(86400)
    for i in User.objects.all():
        print(i.username, "最后登录时间:", i.last_login)
    blog = Blog.objects.all().order_by("-create_time")
    # 分页测试
    try:
        # 获取当前页面，默认为1
        page = request.GET.get('page', 1)
    except PageNotAnInteger:
        page = 1
    paginator = Paginator(blog, 2, request=request)
    data = paginator.page(page)
    return render(request, 'blog/index.html', locals())


# 内容和评论数据的渲染
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
    # 评论的表单和数据显示
    form = MDEditorForm()
    comments = Comments.objects.filter(blog=data)
    test = []
    for comm in comments:
        b = {}
        b["id"] = comm.id
        b["content"] = markdown.markdown(comm.content, extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
            'markdown.extensions.toc',
        ])
        test.append(b)
    return render(request, 'blog/content.html', locals())


def blog_class(request, title):
    categories = Category.objects.all()
    return render(request, 'blog/classify.html', locals())


def blog_class_details(request, title):
    data = Category.objects.get(name=title)
    # 反向查询从表blog中的数据
    result = data.blog_set.all()
    return render(request, 'blog/classify_details.html', locals())


def tags(request, title):
    tags = Tag.objects.all()
    obj_tag_list = Tag.objects.all()
    # 更新标签的数量
    for obj_tag in obj_tag_list:
        tag_number = obj_tag.blog_set.count()
        obj_tag.number = tag_number
        obj_tag.save()
    return render(request, 'blog/tags.html', locals())


def tag(request, title):
    # 标签文章显示
    data = Tag.objects.get(name=title)
    result = data.blog_set.all()
    return render(request, 'blog/tag.html', locals())


@login_required
def profile(request, title):
    # 用户信息详情
    if request.method == "POST":
        name = request.POST.get("name")
        user_id = request.user.id
        try:
            # 判断是否已经存在该用户名
            user = User.objects.get(username=name)
            return HttpResponse("0")
        except:
            user = User.objects.get(id=user_id)
            user.username = name
            user.save()
            return HttpResponse("1")
    return render(request, 'blog/profile.html', locals())


def logout(request):
    # 退出登录
    request.session.delete()
    return HttpResponseRedirect(reverse("blog_index"))


# 评论内容的提交
def submit_comment(request):
    # 评论者为登录用户，回复对象为评论表对象，可以为空，blog为评论对应的文章，content为评论的内容
    user_id = request.user.id
    reply = request.POST.get("reply")
    blog = request.POST.get("blog")
    content = request.POST.get("content")
    Comments.objects.create(content=content, blog_id=blog, parent_comment_id=reply, user_id=user_id)
    return HttpResponse("1")

