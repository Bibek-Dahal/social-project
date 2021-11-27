from django.http.response import HttpResponse,HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import redirect, render
from django.views.generic.base import View
from django.views.generic.edit import CreateView, DeleteView,UpdateView
from .models import*
from .forms import*
from myapp.models import Profile

class PostCreateView(CreateView):
    template_name = 'post/create_post.html'  # Replace with your template.
    form_class = PostCreateForm
    success_url = '/create_post/'  # Replace with your URL or reverse().

    def form_valid(self,form):
        user =Profile.objects.get(user=self.request.user)
        post = form.save(commit=False)
        post.user=user
        post.save()
        return redirect('post:create')

class UpdatePostView(UpdateView):
    model = Post
    template_name = 'post/update_post.html' 
    form_class = PostUpdateForm
    def form_valid(self,form):
        form.save()
        return redirect('post:create')

class DeletePostView(DeleteView):
    model  = Post
    template_name = 'post/delete_post.html'
    success_url = '/user_profile/'

class CommentView(View):
    def get(self,request,pk):
        form = CommentForm()
        print('pk',pk)
        return render(request,'post/comment_post.html',{"form":form})

    def post(self,request,pk):
        print('post',pk)
        form = CommentForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = Profile.objects.get(user=self.request.user)
            post_id = Post.objects.get(id=pk)
            instance.post = post_id
            instance.save()

        return HttpResponse("post request")
    

    
        
       
            



        
    
    
       