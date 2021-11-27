
import json
from django.http.response import HttpResponseRedirect,HttpResponse
from django.shortcuts import render
from account.models import MyUser
from django.views.generic.base import TemplateView
import random 
from django.contrib.auth.decorators import login_required
from .models import *
from myapp.models import FriendRequest,Profile
from django.db.models import query
import random
from django.http import JsonResponse
from rest_framework.response import Response
val=[]
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
from post.models import*
from chat.models import*


def userProfile(request):
    profile_obj = Profile.objects.get(user=request.user)
    profile_pic = profile_obj.get_profile().order_by('-created_at').first()
    cover_pic = profile_obj.get_cover().order_by('-created_at').first()
    posts = Post.objects.filter(user=profile_obj)
    print(Post.objects.filter(user=profile_obj))
    print(posts)
    return render(request,'myapp/user_profile.html',{'profile_pic':profile_pic,'cover_pic':cover_pic,'posts':posts,'friends':profile_obj.show_friends(),'array':MyUser.objects.all()[:6]})

@csrf_exempt
def createPrivateChat(request):
    if request.method == 'GET':
        return HttpResponse('GET request')
    if request.method == 'POST':
        print(request.POST)
        emp = []
        sender = request.POST.get('sender')
        receiver = request.POST.get('receiver')
        room_name = request.POST.get('room_name')
        text = request.POST.get('msg')
        # dicval = json.loads(emp[0])
        # x = request.POST
        # for p in x:
        #     print(json.loads(p))
        #     val = json.loads(p)
        #     sender = val.get('sender')
        #     receiver = val.get('receiver')
        #     room_name = val.get('room_name')
        #     text = val.get('msg')
        
        private_room_obj = PrivateRoom.objects.get(room=room_name)
        print(sender)
        print(room_name)
        print(text)
        print('sender',sender)
        print('receiver',receiver)
        print(private_room_obj)
        obj = PrivateChat(privateroom=private_room_obj,sender=MyUser.objects.get(username=sender),receiver=MyUser.objects.get(username=receiver),message=text)
        p1 = MyUser.objects.get(username=sender)
        # print('p1',p1)
        p2 = MyUser.objects.get(username=receiver)
        obj.save()
        obj.user.add(p1,p2)

        
        return JsonResponse({'msg':'created'})
        
def privateChat(request,user):
    #print(type)
    
    receiver = MyUser.objects.get(username=user)
    user_name = MyUser.objects.get(username=request.user)
    print(type(user_name.username))
    print(user+user_name.username)
    room_name = user+user_name.username
    friends = Profile.objects.get(user=request.user)
    q=PrivateChat.objects.filter( Q(user=user_name.id)  & (Q(sender=user_name.id) & Q(receiver=receiver.id)| Q(sender=receiver.id) & Q(receiver=user_name.id)))
    print(q)
    # print('query',q.query)
    # print('length',len(q))
    try:
        # sender = request.user
        # x=user+user_name.username
        
        print('inside try')
        obj = PrivateRoom.objects.get(Q(room=user+user_name.username) | Q(room=user_name.username+user))
        msg = PrivateChat.objects.filter(privateroom= obj)
        # print(len(msg))
        print(msg)
        print(obj)
        print(obj.room)
        print(user_name.username)
        print(user)
        # print(msg)
        # return HttpResponse('hello')

        
        return render(request,'myapp/private_chat.html',{'msg':msg,'room_name':obj.room,'user_name':user_name.username,'receiver':user,'sender':user_name.username})
    except:
        print('inside except')
        PrivateRoom.objects.create(room=room_name)
        obj = PrivateRoom.objects.get(Q(room=user+user_name.username) | Q(room=user_name.username+user))
        return render(request,'myapp/private_chat.html',{'room_name':obj.room,'user_name':user_name.username,'receiver':user,'friends':friends.show_friends()})



  
def searchUser(request):
    result = request.GET.get('user',None)
    if result:
        users = MyUser.objects.filter(username__icontains=request.GET.get('user'))
        return render(request,'myapp/find_friends.html',{'friends':users,'condition':False})
    return JsonResponse('helo')
    
    
@login_required
def EnterRoom(request):
    return render(request,'myapp/Room_form.html')

@login_required
def ROom(request,room_name):
   
    request_user = MyUser.objects.get(username = request.user)
    created = Room.objects.filter(room_name = room_name).exists()
    if created:
        pass
    else:
        Room.objects.create(room_name = room_name,created_by = request_user)
    print("\n\n\nu ")
   
    user_name = request_user.username
    print(request_user.username)
    
    return render(request,'myapp/index.html',{'room_name':room_name,'user_name':user_name})


@login_required
def User_Profile(request):
    profile_obj = Profile.objects.filter(user= request.user)
    return render(request, 'myapp/profile.html',{"images":profile_obj.get_profile()})
    
@login_required
def HomePage(request):
    profile_obj = Profile.objects.get(user=request.user)
    print(profile_obj.get_cover())
    print(profile_obj.get_profile())
    print(MyUser.objects.all())
    context = {'user':profile_obj,'friends':profile_obj.show_friends()}
    print(FriendRequest.objects.all())
    x = FriendRequest.objects.filter(from_user=Profile.objects.filter(user=request.user))
    
    return render(request,'myapp/home.html',context)
   
    # return HttpResponse('htllo')

@login_required
def Add_Friend(request,id):
    if request.is_ajax and request.method == 'POST':
        uname = Profile.objects.get(user__id = id)
        qset = FriendRequest.objects.filter(from_user=Profile.objects.get(user=request.user),to_user=uname).exists()
        if qset:
            return render(request,'myapp/find_friends.html')
    
        else:
            obj = FriendRequest.objects.create(from_user=Profile.objects.get(user=request.user),to_user=uname)
            return JsonResponse({'msg':'created','info':id,'fr_id':obj.id},status=200)

        # instance = FriendRequest.objects.get_or_create(from_user = request.user, to_user =uname.user )
        # obj = FriendRequest.objects.get_or_create(from_user=request.user,to_user=uname.user )
        # print(obj)
         
        # return HttpResponseRedirect('/find_friends/')
    return JsonResponse({},status=400)
    

@login_required
def See_Friend_Requests(request):
    objs1 = FriendRequest.objects.filter(to_user=Profile.objects.get(user=request.user))
    context = {'objs':objs1}
    return render(request,'myapp/see_friend_request.html',context)


@login_required
def My_Friends(request):
    y  = Profile.objects.get(user=request.user)
    
    context = {'my_frns':y.friends.all()}
    print(context)
    # print(context)
    # print(y.friends.all())
    # print(MyUser.objects.all())
    # for x in y.friends.all():
    #     print('email',x.email)
    return render(request,'myapp/my_friends.html',context)
    # return HttpResponse('hello')

@login_required
def Pending_Requests(request):
    objs1= FriendRequest.objects.filter(from_user=Profile.objects.get(user=request.user))
    for f in objs1:
        print(f.from_user)

    context = {'objs':objs1,"pending_req_count":len(objs1)}
    return render(request,'myapp/pending_req.html',context)

@login_required
def Cancel_Req(request,id):
    if request.is_ajax and request.method == 'POST':
        try:
            get_id = FriendRequest.objects.get(id = id)
            get_id.delete()
            # return HttpResponseRedirect('/pending_friend_requests/')
            return JsonResponse({'msg':'deleted'})
        except:
            print('gello')
            return HttpResponseRedirect('/pending_friend_requests/')
@login_required
def Accept_Friend_Request(request,id):
    if request.method == 'POST':
        get_name = FriendRequest.objects.get(id = id)
    
        receiver_obj= Profile.objects.get(user = request.user)  
        receiver_obj.add_friend(get_name.from_user,request.user,id)
        # print(get_name.from_user)
        # # User_Profile.friends.add( get_name.from_user)
        return HttpResponse('hello')
        

   
def Find_Friends(request):
    
    emp_list = []
    friend_obj = Profile.objects.get(user = request.user)
    user_friends = friend_obj.show_friends()
    all_users = MyUser.objects.exclude(username = request.user)
    pending_request_list = FriendRequest.objects.filter(from_user = friend_obj)

    if pending_request_list  or user_friends:
        for x in pending_request_list:
            emp_list.append(x.to_user)


        User_obj_of_pending_req_list = MyUser.objects.filter(username__in=tuple(emp_list))
        user_fr_pending = User_obj_of_pending_req_list.union(MyUser.objects.filter(username__in=tuple(user_friends)))
        
        my_friend_friends = MyUser.objects.none()
        # return HttpResponse(friends_1)
        
        if user_friends:
            
            for u in friend_obj.friends.all():
                print(type(u))
                f = Profile.objects.get(user = u )
                fr = f.show_friends()
                if fr:
                    u_obj = MyUser.objects.filter(username__in = tuple(fr)).exclude(username = request.user)
                    my_friend_friends = my_friend_friends.union(u_obj)
       
                after_union = list(my_friend_friends)
                if after_union:
                    for f in list(user_fr_pending):
                        if f in after_union :
                            after_union.remove(f)
                    
        
            if after_union:
                return render(request,'myapp/find_friends.html',{'friends':after_union,'condition':False})
                

        return render(request,'myapp/find_friends.html',
        {
            'friends':random.sample(list(all_users.difference(user_fr_pending)),min(len(list(all_users.difference(user_fr_pending))),4)),'condition':False
                        
        })
    
    else:
        # return render(request,'myapp/find_friends.html',{'friends':random.sample(list(all_users),1)})
        return render(request,'myapp/find_friends.html',{'friends':random.sample(list(all_users),min(len(list(all_users)),5))})
        
    # data = {'msg':'success'}     
    # return JsonResponse(data)
    
   


def find_fr(request):
    if request.is_ajax and request.method == 'GET':
        print(json.loads(request.GET))
        res = {'msg':'BIBE'}
        return JsonResponse(res)