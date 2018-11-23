from django.db import models
from django.utils import timezone
from mdeditor.fields import MDTextField


class Category(models.Model):
    name = models.CharField(verbose_name="博客类别", max_length=20)
    # number为该类别下存在多少博客
    number = models.IntegerField()

    class Meta:
        verbose_name = "类别"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(verbose_name="博客标签", max_length=20)
    # number为对应标签下存在的博客,这里设置默认值是因为该字段是后续添加的
    number = models.IntegerField()

    class Meta:
        verbose_name = "标签"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Blog(models.Model):
    title = models.CharField(max_length=50, verbose_name='标题')
    content = MDTextField(verbose_name='博客内容')
    create_time = models.DateTimeField(verbose_name='创建时间', default=timezone.now)
    click_nums = models.IntegerField(verbose_name='点击量', default=0)
    # 类别和博客是一对多的关系
    category = models.ForeignKey(Category, verbose_name='文章类别', on_delete=models.CASCADE)
    # 博客和标签是多对多的关系
    tag = models.ManyToManyField(Tag, verbose_name='文章标签')

    class Meta:
        verbose_name = "博客"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title
