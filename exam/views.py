from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib import messages
from home.models import *
from .models import *
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

def examStart(request):
    context={}
    ec=ExamControl.objects.latest('id')
    if ec.start_exam:
        if request.method == 'POST':
            return HttpResponse('Examt start')
        return render(request,'exam/start_exam.html',context)
    else:
        messages.warning(request,'exam will start soon!')
    return redirect('exam:home')

def examSubmission(request):
    return HttpResponse('exam submission')
