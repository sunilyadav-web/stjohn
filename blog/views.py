from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import *
from django.contrib import messages

def home(request):
    context={}
    try:
        posts=Post.objects.all()
        categories=Category.objects.all()
        context['categories']=categories
        context['posts']=posts
        val=request.GET.get('category')
        if val != None:
            obj=Category.objects.filter(category_name=val).exists()
            print("Oobj check ",obj)
            if obj:
                category_obj=Category.objects.get(category_name=val)
                context['category']=category_obj
                posts=Post.objects.filter(category=category_obj)
                context['posts']=posts
            else:
                messages.warning(request,'Category does not Exist!')
            return render(request,'blog/home.html',context)
    except Exception as e:
        print("Blog Home Exception : ",e)
    return render(request,'blog/home.html',context)

def post(request,slug):
    context={}
    try:
        obj=Post.objects.get(slug=slug)
        categories=Category.objects.all()
        context['categories']=categories
        context['post']=obj
        print('post :',obj)
    except Exception as e:
        print("Post Eexception : ",e)
        messages.warning(request,'URL not found!')
        return redirect("blog:home")
    return render(request,'blog/post_detail.html',context)

