from django.contrib import admin
from blog.models import *


@admin.register(Category)
class Category_Admin(admin.ModelAdmin):
    list_display = ('id', 'name')


@admin.register(Tag)
class Tag_Admin(admin.ModelAdmin):
    list_display = ('id', 'name')


@admin.register(Blog)
class Blog_Admin(admin.ModelAdmin):
    list_display = ('id', 'title', 'content',  'click_nums', 'category', 'create_time')

    # 重写模型保存的方法，保存博客时将该博客的分类数与标签数分别添加到对应的表中
    def save_model(self, request, obj, form, change):
        obj.save()
        # 博客分类数据的统计更新
        obj_category = obj.category  # 获取博客类别对象
        print("博客类别：", obj_category)
        category_number = obj_category.blog_set.count()     # 反向查询
        print("类别关联的博客数量:", category_number)
        obj_category.number = category_number
        obj_category.save()
        print("更新后的数量:", obj_category.number, "\n")

        # 博客标签的统计更新，因为博客和标签是多对多关系，所以先获取所有的标签，
        # 然后逆向查讯每个标签下对应的博客数量,
        obj_tag_list = obj.tag.all()
        # obj.id为当前文章id
        # print("标签数据:", obj_tag_list)
        # for obj_tag in obj_tag_list:
        #     print("当前标签:", obj_tag)
        #     tag_number = obj_tag.blog_set.count()
        #     print("标签数量:", tag_number)
        #     obj_tag.number = tag_number
        #     obj_tag.save()
        #     print("更新后的标签数量:", tag_number, "\n")

    # 对应的博客删除时，修改对应的分类数和标签数
    def delete_model(self, request, obj):
        obj.delete()
        # 博客分类数据的统计更新
        obj_category = obj.category  # 获取博客类别对象
        print("博客类别：", obj_category)
        category_number = obj_category.blog_set.count()  # 反向查询
        print("类别关联的博客数量:", category_number)
        obj_category.number = category_number
        obj_category.save()
        print("更新后的数量:", obj_category.number)
        # print(obj.tag)
        # 博客标签的统计更新，
        # obj_tag_list = obj.tag.all()

        # obj.id为当前文章id
        # print("标签数据:", obj_tag_list)
        # for obj_tag in obj_tag_list:
        #     print("当前标签:", obj_tag)
        #     tag_number = obj_tag.blog_set.count()
        #     print("标签数量:", tag_number)
        #     obj_tag.number = tag_number
        #     obj_tag.save()
        #     print("更新后的标签数量:", tag_number, "\n")
