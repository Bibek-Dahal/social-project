from random import sample
from django.db import models
# from django.conf import settings
from autoslug import AutoSlugField
import random
from django.db.models.deletion import SET_NULL
from django.urls import reverse

from django.http.response import JsonResponse
from account.models import MyUser



class Profile(models.Model):
    first_name = models.CharField(max_length=100,blank=True)
    last_name = models.CharField(max_length=100,blank=True)
    user = models.OneToOneField(MyUser,on_delete=models.CASCADE,default='')
    bio = models.TextField(default='',blank=True,null=True)
    friends = models.ManyToManyField(MyUser,related_name = 'user_friends',blank=True)

    def __str__(self):
        return self.user.username

    def Friends(self):
        return ",".join([str(p) for p in self.friends.all()])
        
    def show_friends(self):
        fr = self.friends.all()
        return fr
    
    def add_friend(self,from_user,to_user,id):
        # sender_obj = Profile.objects.get(user = from_user)
        from_user.friends.add(to_user)
        self.friends.add(MyUser.objects.get(username=from_user))
        obj_1 = FriendRequest.objects.get(id = id)
        obj_1.delete()

    def get_post(self):
        self.posts.all()

    def get_profile(self):
        return self.profiles.all()

    def get_cover(self):
        return self.covers.all()
        
        

    @property
    def call_me(self,a):
        print('hey friend class call_me called')
        return reverse('facebook:find_friends')



class CoverPic(models.Model):
    caption = models.CharField(max_length=500,blank = True)
    user = models.ForeignKey(Profile,on_delete=models.CASCADE,related_name="covers",default='')
    pic = models.ImageField( upload_to = 'Cover_Pic/Images',default="default/avatar.png")
    liked_by = models.ManyToManyField(Profile,related_name = 'likes',blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now= True)

    def likedby(self):
        return  ",".join([str(p) for p in self.liked_by.all()])

class ProfilePic(models.Model):
    caption = models.CharField(max_length=500,blank = True)
    user = models.ForeignKey(Profile,on_delete=models.CASCADE,related_name="profiles",default='')
    pic = models.ImageField( upload_to = 'Profile_Pic',default = "default/avatar.png")
    liked_by = models.ManyToManyField(Profile,related_name = 'liked_by',blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add = True)

    def likedby(self):
        return  ",".join([str(p) for p in self.liked_by.all()])

class FriendRequest(models.Model):
    to_user  = models.ForeignKey(Profile,on_delete = models.CASCADE,related_name = 'to_user')
    from_user = models.ForeignKey(Profile,on_delete = models.CASCADE,related_name = 'fromUser')
    
class User_Profile(models.Model):
    user = models.OneToOneField(MyUser,on_delete = models.CASCADE)
    bio = models.CharField(max_length = 285,blank = True)
    # friends = models.ManyToManyField(MyUser,blank = True,related_name = 'friends')
    slug = AutoSlugField(populate_from = 'user')

    def get_absolute_url(self):


        pass
    
    # def get_friends(self):
    #     friend = ",".join([str(p) for p in self.friends.all()])
    #     return friend
    
    def return_response(self):
        return('its me hello')

    
