#!/usr/bin/env python  
# encoding: utf-8   

""" 
@version: v1.0 
@author: YangXiaodi 
@license: Apache Licence  
@contact: 15564219@qq.com 
@software: PyCharm 
@file: forms.py 
@time: 2017/11/6 23:45 
"""

from django import forms
from .models import Comments


class ArticlecommentForm(forms.Form):
	email = forms.EmailField()
	comment = forms.CharField(max_length=400)
	