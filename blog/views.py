from django.forms import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from .models import Post
from django.contrib.auth.models import User
from django.views.generic import (ListView,
                                  DetailView, 
                                  CreateView,
                                  UpdateView,
                                  DeleteView,)

from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin


def home(request):
    # return HttpResponse('<h1>Blog Home</h1>')
    context={
        'posts':Post.objects.all()
    }
    return render(request,'blog/home.html',context)

class PostListView(ListView):
    model=Post
    template_name = 'blog/home.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    ordering = ['-date'] #to show the latest posts first
    paginate_by=5 #5 posts per page
    
   
        
        
    
    
class UserPostListView(ListView):
    model=Post
    template_name = 'blog/user_posts.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    # ordering = ['-date'] #to show the latest posts first
    paginate_by=5 #5 posts per page
    
    def get_queryset(self):
        user=get_object_or_404(User,username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date')
    
    
class PostDetailView(DetailView): #this is to get the details of a specific post
    model=Post
   
# this mixin class is used so that you can create a
# post only when you are logged in
class PostCreateView(LoginRequiredMixin,CreateView):
    model=Post
    fields=['title','content']
    
    def form_valid(self, form: BaseModelForm):
       form.instance.author=self.request.user
       return super().form_valid(form)
   
class PostUpdateView(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
    model=Post
    fields=['title','content']
    
    def form_valid(self, form: BaseModelForm):
       form.instance.author=self.request.user
       return super().form_valid(form)
   
    #this is so that only the author is able to update his post
    def test_func(self):
        post=self.get_object()
        if self.request.user == post.author:
            return True
        return False

class PostDeleteView(LoginRequiredMixin,UserPassesTestMixin,DeleteView): 
    model=Post
    def test_func(self):
        post=self.get_object()
        if self.request.user == post.author:
            return True
        return False
    
    success_url='/' #to redirect to the home page
    
    
def about(request):
    return render(request,'blog/about.html',{'title':'About'})




# from django.http import HttpResponse

# posts=[
#     {
#         'author':'CoreyMS',
#         'title':'Blog Post 1',
#         'content':'First Post content',
#         'date':'July 8, 2024'
#     },
# ]
