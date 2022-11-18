from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import *
from django.contrib import messages

def home(request):
    context={}
    try:
        posts=Post.objects.all()
        context['posts']=posts
    except Exception as e:
        print("Blog Home Exception : ",e)
    return render(request,'blog/home.html',context)

def post(request,slug):
    context={}
    try:
        obj=Post.objects.get(slug=slug)
        context['post']=obj
        print('post :',obj)
    except Exception as e:
        print("Post Eexception : ",e)
        messages.warning(request,'URL not found!')
        return redirect("blog:home")
    return render(request,'blog/post_detail.html',context)