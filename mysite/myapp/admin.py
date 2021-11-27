from django.contrib import admin
from .models import*
from post.models import Post



@admin.register(User_Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['id','user','bio','slug','return_response']

@admin.register(FriendRequest)
class FriendAdmin(admin.ModelAdmin):
    list_display = ['id','to_user','from_user']



@admin.register(ProfilePic)
class ProfilePicAadmin(admin.ModelAdmin):
    list_display = ['id','user','caption','likedby','pic','created_at','updated_at']

@admin.register(CoverPic)
class CoverPicAadmin(admin.ModelAdmin):
    list_display = ['id','user','caption','likedby','pic','created_at','updated_at']




@admin.register(Profile)
class FriendsAdmin(admin.ModelAdmin):
    list_display = ['id','user','first_name','last_name','Friends']

