import autoslug
from django.contrib.auth import views
from django.http import request
from django.shortcuts import redirect, render,HttpResponse,HttpResponseRedirect
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.template.loader import render_to_string
from .forms import CustomUserLoginForm,CustomUserCreationForm
from .models import*
from django.contrib.auth.views import LoginView,PasswordResetView,PasswordResetDoneView,PasswordResetCompleteView,PasswordResetConfirmView
from django.contrib.auth import authenticate, login
from .forms import PWDResetForm,SetPWDForm
from django.utils.translation import ugettext_lazy as _
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.views.generic.base import View
account_activation_token = PasswordResetTokenGenerator()

class SignInView(LoginView):
    authentication_form = CustomUserLoginForm
    template_name = 'account/registration/login.html'
        
    

class PwdResetView(PasswordResetView):
    form_class = PWDResetForm
    email_template_name = 'account/registration/password_reset_email.html'
    template_name = 'account/registration/password_reset_form.html'
    success_url = reverse_lazy('account:password_reset_done')

class PResetDoneView(PasswordResetDoneView):
    template_name = 'account/registration/password_reset_done.html'
    title = _('Password reset sent')

class PwdResetConfirmView(PasswordResetConfirmView):
    form_class = SetPWDForm
    template_name = 'account/registration/password_reset_confirm.html'
    success_url = reverse_lazy('account:password_reset_complete')


    

class PwdResetCompleteView(PasswordResetCompleteView):
    template_name = 'account/registration/password_reset_complete.html'



def signup(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/')
    else:
        form = CustomUserCreationForm()
        if request.method == 'POST':
            form = CustomUserCreationForm(request.POST)
            if form.is_valid():
                print(form)
                print(form.cleaned_data['email'])
                user = form.save(commit=False)
                user.email = form.cleaned_data['email']
                user.set_password(form.cleaned_data['password1'])
                user.is_active = False
                user.save()
                #send mail
                current_site = get_current_site(request)
                subject = 'Activate Your Account'
                message = render_to_string('account/registration/account_activation_email.html',{
                'user':user,
                'domain':current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':account_activation_token.make_token(user)
                })
                print('domain',current_site.domain)
                print()
                print()
            
                user.email_user(subject=subject,message=message)
                return render(request,'account/registration/reg_info.html')
                
                
        
        return render(request,'account/registration/signin.html',{'form':form})

def account_activate(request ,uidb64,token ):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        userobj = MyUser.objects.get(pk=uid)
        print('inside try block')
    except():
        print('inside except block')
        pass
    # user = authenticate(username = userobj.username,password=userobj.password)
    print(userobj)
    if userobj is not None and account_activation_token.check_token(userobj,token):
        print('insid user obk')
        userobj.is_active = True
        userobj.save()
        print('inside account activation')
        print(userobj.is_active)
        login(request,userobj,backend='django.contrib.auth.backends.ModelBackend')
        return HttpResponseRedirect('/')
    return HttpResponse('invalid login')
        
   
# class CustomerRegView(CreateView):
#     template_name = 'customer/customer_reg_form.html'
#     form_class = CustomerRegForm
#     success_url = reverse_lazy('cart:buy')

#     def form_valid(self,form):
#         obj = form.save(commit=False)
#         obj.customer = self.request.user
#         obj.save()
#         return redirect('cart:buy')