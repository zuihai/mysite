from django.shortcuts import render, render_to_response, get_object_or_404, redirect
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.views.generic import ListView, DetailView, FormView
from django.core.urlresolvers import reverse

from .models import Article, Category, Comments, Tag
from .forms import ArticlecommentForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
import re


# Create your views here.

def index(request):
	if request.user.is_authenticated:
		user = request.user
	else:
		user = None
	# title = 'Report Management System'
	articles_all = Article.objects.filter(is_published=True)
	# 文章分类
	articlecategory = Category.objects.filter(article__is_published=True)
	# 阅读排行
	articleviewranks = Article.objects.filter(is_published=True).order_by('-views')[:10]
	paginator = Paginator(articles_all, 10)
	page = request.GET.get('page')
	try:
		articles = paginator.page(page)
	except PageNotAnInteger:
		articles = paginator.page(1)
	except EmptyPage:
		articles = paginator.page(paginator.num_pages)
	if user:
		return render_to_response('index.html', {"articles": articles, "articlecategory": articlecategory, \
		                                         "articleviewranks": articleviewranks, "user": user})
	else:
		return render_to_response('index.html', {"articles": articles, "articlecategory": articlecategory, \
		                                         "articleviewranks": articleviewranks})


def myarticle(request):
	if not request.user.is_authenticated:
		render_to_response('login.html')
	user = request.user
	articles_all = Article.objects.filter(author=user)
	# 文章分类
	articlecategory = Category.objects.filter(article__author=user)
	# 阅读排行
	articleviewranks = Article.objects.filter(author=user).order_by('-views')[:10]
	paginator = Paginator(articles_all, 10)
	page = request.GET.get('page')
	try:
		articles = paginator.page(page)
	except PageNotAnInteger:
		articles = paginator.page(1)
	except EmptyPage:
		articles = paginator.page(paginator.num_pages)
	return render_to_response('index.html', {"articles": articles, "articlecategory": articlecategory, \
	                                         "articleviewranks": articleviewranks, 'user': user})


def articledetail(request, id):
	if request.user.is_authenticated:
		article = get_object_or_404(Article, pk=id)
		# 增加阅读量
		article.views = article.views + 1
		article.save()
		return render_to_response('articledetail.html', {"articledetail": article, "user": request.user})
	else:
		article = get_object_or_404(Article, pk=id)
		# 增加阅读量
		article.views = article.views + 1
		article.save()
		return render_to_response('articledetail.html', {"articledetail": article})


# class ArticleDetailView(DetailView):
# 	model = Article
# 	template_name = "articledetail.html"
# 	context_object_name = "articledetail"
# 	pk_url_kwarg = 'id'
#
# 	def get_object(self, queryset=None):
# 		obj = super(ArticleDetailView, self).get_object()
# 		obj.views = obj.views + 1
# 		obj.save()
# 		return obj


def Articlecomment(request, article_id):
	p = get_object_or_404(Article, pk=article_id)
	email = request.POST['email']
	# re_email = email
	comment = request.POST['comment']
	p.comments_set.create(email=email, comment=comment).save()
	return HttpResponse('success!!')


# class Articlecomment(FormView):
# 	form_class = ArticlecommentForm
# 	template_name = 'articledetail.html'
#
# 	def form_invalid(self, form):
# 		target_article = get_object_or_404(Article, pk=self.kwargs['id'])
# 		comment = sform.sav

@csrf_exempt
def regist(request):
	if request.method == 'POST':
		username = request.POST['UserName']
		password = request.POST['Password']
		repassword = request.POST['RePassword']
		email = request.POST['email']
		if not username:
			return HttpResponse('请输入用户名!')
		if not email:
			return HttpResponse('请输入邮箱地址!')
		reg_str = r'^[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+){0,4}@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+){0,4}$'
		if not re.match(reg_str, email):
			return HttpResponse('邮箱地址不正确!')
		if not password:
			return HttpResponse('请输入密码!')
		if password != repassword:
			return HttpResponse('2次输入的密码不一致!')
		if len(User.objects.filter(username=username)) > 0:
			return HttpResponse('用户已存在!')
		User.objects.create_user(username=username, email=email, password=password).save()
		user = authenticate(request, username=username, password=password)
		login(request, user)
	return HttpResponse('注册成功!')


@csrf_exempt
def userlogin(request):
	if request.method == 'POST':
		username = request.POST['uname']
		password = request.POST['psw']
		# print(username, password)
		if not username:
			return HttpResponse('请输入用户名!')
		if not password:
			return HttpResponse('请输入密码!')
		user = authenticate(request, username=username, password=password)
		# print(user)
		if user is not None:
			login(request, user)
			# title = 'Report Management System'
			articles_all = Article.objects.filter(is_published=True)
			# 文章分类
			articlecategory = Category.objects.filter(article__is_published=True)
			# 阅读排行
			articleviewranks = Article.objects.filter(is_published=True).order_by('-views')[:10]
			paginator = Paginator(articles_all, 10)
			page = request.GET.get('page')
			try:
				articles = paginator.page(page)
			except PageNotAnInteger:
				articles = paginator.page(1)
			except EmptyPage:
				articles = paginator.page(paginator.num_pages)
			return HttpResponse('登录成功!')
		else:
			return HttpResponse('用户名或者密码错误!')
	return HttpResponseRedirect('/')


def uesrlogout(request):
	logout(request)
	return redirect(reverse(index))


# return HttpResponseRedirect(index)

def updateuserpassword(requests):
	if not requests.user.is_authenticated:
		return HttpResponse("请先登录!")
	if requests.method == 'POST':
		username = None
		if requests.user.is_authenticated:
			username = requests.user
		# print(username)
		if not username:
			return HttpResponse('请先使用旧的密码登录!')
		oldpassword = requests.POST['oldpassword']
		newpassword = requests.POST['newpassword']
		renewpassword = requests.POST['renewpassword']
		if not oldpassword:
			return HttpResponse('请输入旧密码!')
		if not newpassword:
			return HttpResponse('请输入新密码!')
		if newpassword != renewpassword:
			return HttpResponse('2次输入的密码不一致')
		user = authenticate(requests, username=username, password=oldpassword)
		if user:
			u = User.objects.get(username=username)
			u.set_password(newpassword)
			u.save()
			user = authenticate(requests, username=username, password=newpassword)
			login(requests, user)
			return HttpResponse('修改成功!')
		else:
			return HttpResponse('旧密码不正确')
	return HttpResponse('非法操作')


def addarticle(requests):
	if not requests.user.is_authenticated:
		return HttpResponse("请先登录!")
	categorys = Category.objects.all()
	return render_to_response('addarticle.html', {"categorys": categorys, "user": requests.user})


def addarticlesave(requests):
	if not requests.user.is_authenticated:
		return HttpResponse("请先登录!")
	if requests.method == 'POST':
		if not requests.user.is_authenticated:
			return HttpResponse("请先登录")
		username = requests.user
		author_id = User.objects.filter(username=username).first().id
		# print(author_id)
		title = requests.POST['title']
		body = requests.POST['body']
		if Article.objects.filter(title=title, body=body):
			return HttpResponse("您已经保存过了!")
		category = requests.POST['category']
		tags = requests.POST['tags']
		tags = tags[:-1]
		excerpt = requests.POST['excerpt']
		try:
			ispublish = requests.POST['ispublish']
			ispublish = 1
		except:
			ispublish = 0
		art = Article.objects.create(title=title, body=body, category_id=category, excerpt=excerpt,
		                             is_published=ispublish, author_id=author_id)
		for tg in tags.split(','):
			tag = Tag.objects.create(name=tg)
			art.tags.add(tag)
		return HttpResponse("保存成功")
	return HttpResponse("非法请求!")


def feeds(request):
	return render_to_response('feeds.html')
