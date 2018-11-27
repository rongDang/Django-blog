from django.contrib import admin
from blog.models import *

# 初始后台登录页面的显示标题
admin.site.site_header = '小白博客登录'
admin.site.site_title = '登录账号'


@admin.register(Category)
class Category_Admin(admin.ModelAdmin):
    list_display = ('id', 'name')
    # 不让数目显示出来
    exclude = ('number', )


@admin.register(Tag)
class Tag_Admin(admin.ModelAdmin):
    list_display = ('id', 'name')
    exclude = ('number',)


@admin.register(Blog)
class Blog_Admin(admin.ModelAdmin):
    list_display = ('id', 'title', 'click_nums', 'category', 'create_time')
    list_display_links = ('id', 'title')    # 设置点击可以进入到编辑页面的字段
    fields = (('title', 'category'), 'content',  'tag')     # 编辑页面显示的字段
    filter_horizontal = ('tag',)        # 使多对多字段更方便操作

    # admin筛选器操作
    search_fields = ('title', 'content')  # 搜索字段
    list_filter = ('category__name', 'tag')  # 过滤器

    # 重写模型保存的方法，保存博客时将该博客的分类数与标签数分别添加到对应的表中
    def save_model(self, request, obj, form, change):
        # obj是当前保存的博客内容，
        obj.save()
        # 博客分类数据的统计更新
        obj_category = obj.category  # 获取博客类别对象
        category_number = obj_category.blog_set.count()  # 反向查询
        obj_category.number = category_number
        obj_category.save()
        # 博客标签的统计更新，因为博客和标签是多对多关系，所以先获取所有的标签，后逆向查讯每个标签下对应的博客数量
        # 关于标签更新问题: obj.tag.all()不能获取到当前文章的标签，所以不能根据当前文章更新标签中的数目，
        # 也就只能在下次保存文章时再更新上次的标签数量，所以在视图函数中再写一遍更新
        obj_tag_list = Tag.objects.all()
        for obj_tag in obj_tag_list:
            tag_number = obj_tag.blog_set.count()
            obj_tag.number = tag_number
            obj_tag.save()

    # 对应的博客删除时，修改对应的分类数和标签数
    def delete_model(self, request, obj):
        obj.delete()
        # 博客分类数据的统计更新
        obj_category = obj.category
        category_number = obj_category.blog_set.count()
        obj_category.number = category_number
        obj_category.save()

        # 博客标签的统计更新，
        obj_tag_list = Tag.objects.all()
        for obj_tag in obj_tag_list:
            tag_number = obj_tag.blog_set.count()
            obj_tag.number = tag_number
            obj_tag.save()
