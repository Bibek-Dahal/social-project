from django.contrib import admin
from .models import *

# @admin.site.unregister(Post)
@admin.register(Post)
class XYZ(admin.ModelAdmin):
    list_display = ['id','user','title','return_desc','likedby','pic','created_at','updated_at']

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['id','text','user','post','created_at','updated_at']

@admin.register(Like)
class Like(admin.ModelAdmin):
    list_displa = ['id','user','post','created_at','updated_at']