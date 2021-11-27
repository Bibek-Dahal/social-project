from django.urls import path,include
from .import views

from django.conf.urls import url
urlpatterns = [
    path('',views.HomePage,name = 'home'),
    path('find_friends/',views.Find_Friends,name = 'find_friends'),
    path('see_friend_requests/',views.See_Friend_Requests,name = 'see_friend_requests'),
    path('add_friend/<int:id>/',views.Add_Friend,name = 'add_friend'),
    path('my_friends/',views.My_Friends,name = 'my_friends'),
    path('pending_friend_requests/',views.Pending_Requests,name = 'pending_friend_requests'),
    path('cancel_friend_request/<int:id>/',views.Cancel_Req,name = 'cancel_friend_request'),
    path('accept_friend_request/<int:id>/',views.Accept_Friend_Request,name = 'accept_friend_request'),
    path('profile/',views.User_Profile,name = "profile"),
    path('room/',views.EnterRoom,name = "enterroom"),
    path('chat/<str:room_name>/',views.ROom,name = "chat"),
    path('find_fr/',views.find_fr,name='find_fr'),
    path('search/',views.searchUser,name="search"),
    path('user_profile/',views.userProfile,name='userProfile'),
    path('private/<str:user>/',views.privateChat,name="private"),
    path('create_msg/',views.createPrivateChat,name="createPrivateMsg"),
]
    