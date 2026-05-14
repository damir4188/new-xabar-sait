from django.contrib import admin
from .models import Article, Category, Like, Comment

admin.site.register(Category)
admin.site.register(Article)
admin.site.register(Like)
admin.site.register(Comment)