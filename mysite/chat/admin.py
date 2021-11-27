from django.contrib import admin
from .models import *
@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    list_display = ['id','room_name','message','author','created_at']

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ['id','room_name','created_by']

@admin.register(PrivateRoom)
class PrivateRoomAdmin(admin.ModelAdmin):
    list_display = ['id','room','created_at']

@admin.register(PrivateChat)
class PrivateChatAdmin(admin.ModelAdmin):
    list_display = ['id','return_user','privateroom','sender','receiver','message']