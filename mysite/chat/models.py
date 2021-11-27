from django.db import models
from account.models import MyUser


class Room(models.Model):
    room_name = models.CharField(max_length = 20,unique=True)
    created_by = models.ForeignKey(MyUser,related_name='created_by',on_delete = models.CASCADE,default = "")

class Chat(models.Model):
    room_name = models.CharField(max_length = 20 )
    author = models.ForeignKey(MyUser,on_delete=models.CASCADE,related_name='author')
    message = models.CharField(max_length = 205)
    created_at = models.DateTimeField(auto_now_add= True)

    def last_ten_msg(self,name):
        print(name)
        return Chat.objects.filter(room_name = name).order_by('created_at')[:10]
    def __str(self):
        return self.room_name


class PrivateRoom(models.Model):
    room = models.CharField(max_length = 60,unique=True)
    
    created_at = models.DateTimeField(auto_now_add=True)

    # def __str__(self):
    #     return self.room

class PrivateChat(models.Model):
    user = models.ManyToManyField(MyUser,related_name='user')
    privateroom = models.ForeignKey(PrivateRoom,on_delete=models.SET_NULL,null=True, related_name='privateroom')
    sender = models.ForeignKey(MyUser,on_delete=models.SET_NULL,null=True,related_name='sender')
    receiver = models.ForeignKey(MyUser,on_delete=models.SET_NULL,null=True,related_name='receiver')
    message = models.TextField(default='')
    created_at = models.DateTimeField(auto_now_add=True)
    

    def return_user(self):
        return ",".join(str(p) for p in self.user.all())

   

