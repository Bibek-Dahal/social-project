from django.urls import path,include
from post import views
app_name = 'post'
urlpatterns = [
    path('create_post/',views.PostCreateView.as_view(),name='create'),
    path('update_post/<int:pk>/',views.UpdatePostView.as_view(),name='update'),
    path('delete_post/<int:pk>/',views.DeletePostView.as_view(),name='delete'),
    path('comment/<int:pk>/',views.CommentView.as_view(),name='comment'),
]