from django.contrib import admin
from .models import *


# Register your models here.


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
	#    , DIMTABLEID, REALVALUE, DISPLAYVALUE, DIM_ID
	# list_display = ('DIM', 'REALVALUE', 'DISPLAYVALUE')
	list_per_page = 20
# list_filter = ('DIM',)  # 过滤器
# search_fields = ('REALVALUE', 'DISPLAYVALUE')  # 搜索字段


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
	#    , DIMTABLEID, REALVALUE, DISPLAYVALUE, DIM_ID
	# list_display = ('DIM', 'REALVALUE', 'DISPLAYVALUE')
	list_per_page = 20
# list_filter = ('DIM',)  # 过滤器
# search_fields = ('REALVALUE', 'DISPLAYVALUE')  # 搜索字段


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
	def get_queryset(self, request):
		qs = super(ArticleAdmin, self).get_queryset(request)
		if request.user.is_superuser:
			return qs
		return qs.filter(author=request.user)
	
	list_per_page = 20
	# list_filter = ('DIM',)  # 过滤器
	# search_fields = ('REALVALUE', 'DISPLAYVALUE')  # 搜索字段
	list_display = (
		'title', 'category', 'author', 'created_time', 'modified_time', 'views', 'is_published')
	list_filter = ('category', 'author', 'is_published')  # 过滤器
	search_fields = ('title', )  # 搜索字段
	date_hierarchy = 'modified_time'  # 详细时间分层筛选


admin.site.site_header = "Yangxiaodi'Blog"
admin.site.site_title = "Yangxiaodi'Blog"
