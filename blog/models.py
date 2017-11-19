from django.db import models
from django.contrib.auth.models import User
from ckeditor_uploader.fields import RichTextUploadingField


# Create your models here.
class Category(models.Model):
	name = models.CharField(max_length=50, verbose_name='分类名称')
	
	def __str__(self):
		return self.name
	
	class Meta:
		verbose_name = '分类'
		verbose_name_plural = '分类'


class Tag(models.Model):
	# 名称
	name = models.CharField(max_length=50, verbose_name='标签名称')
	
	def __str__(self):
		return self.name
	
	class Meta:
		verbose_name = '标签'
		verbose_name_plural = '标签'


class Article(models.Model):
	# 文章标题
	title = models.CharField(max_length=70, verbose_name="文章标题")
	# 文章内容
	body = RichTextUploadingField('文章内容', config_name='default',
	                              blank=True)
	# 创建时间
	created_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
	# 修改时间
	modified_time = models.DateTimeField(auto_now=True, verbose_name="修改时间")
	# 摘要
	excerpt = models.TextField(max_length=300, blank=True, verbose_name="摘要")
	# 分类
	category = models.ForeignKey(Category, verbose_name="分类")
	# 标签
	tags = models.ManyToManyField(Tag, blank=True, verbose_name=u"标签")
	# 作者
	author = models.ForeignKey(User, verbose_name="作者")
	# 浏览量
	views = models.PositiveIntegerField(default=0, verbose_name='浏览量')
	
	is_published = models.BooleanField(default=False, verbose_name='是否发布')
	
	class Meta:
		ordering = ["-modified_time"]
		verbose_name = '文章'
		verbose_name_plural = '文章'


class Comments(models.Model):
	Article_id = models.ForeignKey('Article', verbose_name='文章id')
	email = models.EmailField(verbose_name='用户')
	re_email = models.EmailField(verbose_name='回复用户')
	comment = models.CharField(max_length=400, verbose_name='评论内容')
	
	def __str__(self):
		return self.comment
	
	class Meta:
		verbose_name = '评论'
		verbose_name_plural = '评论'
