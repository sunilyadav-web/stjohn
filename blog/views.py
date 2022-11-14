from django.shortcuts import render
from django.http import HttpResponse

def home(request):
    context={}
    try:
        pass
    except Exception as e:
        print("Blog Home Exception : ",e)
    return render(request,'blog/home.html')