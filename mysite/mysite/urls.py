
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static

from django.views.generic.base import TemplateView
# from django.contrib.auth import views as reg_view
import django_private_chat 

urlpatterns = [
    # path('api/',include('api.urls',namespace = 'api')),
    path('account/',include('account.urls',namespace = 'account')),
    path('admin/', admin.site.urls),
    path('',include('myapp.urls')),
    path('post/',include('post.urls',namespace='post')),
    # path('accounts/',include('allauth.urls')),
  
]+ static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)
