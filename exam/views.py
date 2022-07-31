from django.shortcuts import render
from django.http import HttpResponse
from home.models import *
# Create your views here.
def home(request):
    context={}
    try:
        notice=AddNotice.objects.last()
        rh=ResultHighlightControl.objects.get(id=1)
        context['rh']=rh
        context['notice']=notice
    except Exception as e:
        print('Exam Home Exception : ',e)
    return render(request,'exam/exam.html',context)