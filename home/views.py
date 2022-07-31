from io import BytesIO
import random
from time import time
from django.shortcuts import render,get_object_or_404
from .models import *
from django.contrib import messages
from django.http import HttpResponseRedirect,HttpResponse
from django.urls import reverse
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.contrib.auth.decorators import login_required
from django.db.models import Q

def index(request):
    context={}
    try:
        notice=AddNotice.objects.last()
        rh=ResultHighlightControl.objects.get(id=1)
        context['rh']=rh
        context['notice']=notice
    except Exception as e:
        print('Index Exception :',e)
    return render(request,'home/index.html',context)

def about(request):
    context={}
    notice=AddNotice.objects.last()
    rh=ResultHighlightControl.objects.get(id=1)
    context['rh']=rh
    context['notice']=notice
    
    return render(request,'home/about.html',context)

def contact(request):
    context={}
    notice=AddNotice.objects.last()
    context['notice']=notice
    if request.method == 'POST':
        name=request.POST.get('name')
        email=request.POST.get('email')
        contact_no=request.POST.get('contact_no')
        subject=request.POST.get('subject')
        message=request.POST.get('message')
        contact_entry=Contact(name=name,email=email,contact_no=contact_no,subject=subject,message=message)
        contact_entry.save()
        messages.success(request,'THANKS FOR CONTACTING US! WE WILL REACH TO U ASAP')
        return HttpResponseRedirect(reverse('index:index'))
    return render(request,'home/contact.html',context)


def result(request):
    context={}
    notice=AddNotice.objects.last()
    context['notice']=notice

    # getting Result for authenticated user

    if request.user.is_authenticated:
        
        try:
            user=UserEnrollment.objects.get(user=request.user)
        except:
            messages.error(request,'Your result not found')
        try:
            profile = Profile.objects.get(enrollment_no=user.enrollment_no)

            sem = Semester.objects.filter(profile=profile)
            # print(sem)
            
            # TOTAL CALCULATION
            total_max_marks = 0
            total_min_marks = 0
            total_obtained_marks = 0
            
            for semester in sem:
                total_max_marks = semester.max_marks + total_max_marks
                total_min_marks = semester.min_marks + total_min_marks
                total_obtained_marks = semester.obtained + total_obtained_marks

                print(f"{semester}", semester.min_marks)
                print(f"{semester}", semester.max_marks)

            percentage = (total_obtained_marks/total_max_marks)*100
            student_percentage = round(percentage,2)

            # FINDING GRADE FOR STUDENT
            grade = "Fail"
            if student_percentage > 60: 
                grade = "First Class"
            elif student_percentage > 50:
                grade = "Second Class" 
            elif student_percentage > 35 and student_percentage < 50:
                grade = "Third Class"
            else:
                grade = "Fail"            
            context = {'semesters':sem,'profile':profile,"total_max_marks": total_max_marks,"total_min_marks":total_min_marks,"total_obtained_marks":total_obtained_marks,'student_percentage':student_percentage,'grade':grade, 'notice':notice}

            return render(request, 'home/result.html', context)
        
        except Exception as e:
            messages.error(request, 'Your Result Not found!!')

            return render(request, 'home/result.html', context)

    if request.method == 'POST':
        
        enrollment_no = request.POST.get('enrollment_no')
    
        try:
            profile = Profile.objects.get(enrollment_no=enrollment_no)

            sem = Semester.objects.filter(profile=profile)
            # print(sem)
            
            # TOTAL CALCULATION
            total_max_marks = 0
            total_min_marks = 0
            total_obtained_marks = 0
            
            for semester in sem:
                total_max_marks = semester.max_marks + total_max_marks
                total_min_marks = semester.min_marks + total_min_marks
                total_obtained_marks = semester.obtained + total_obtained_marks

                print(f"{semester}", semester.min_marks)
                print(f"{semester}", semester.max_marks)

            percentage = (total_obtained_marks/total_max_marks)*100
            student_percentage = round(percentage,2)

            # FINDING GRADE FOR STUDENT
            grade = "Fail"
            if student_percentage > 60: 
                grade = "First Class"
            elif student_percentage > 50:
                grade = "Second Class" 
            elif student_percentage > 35 and student_percentage < 50:
                grade = "Third Class"
            else:
                grade = "Fail"            
            context = {'semesters':sem,'profile':profile,"total_max_marks": total_max_marks,"total_min_marks":total_min_marks,"total_obtained_marks":total_obtained_marks,'student_percentage':student_percentage,'grade':grade, 'notice':notice}

            return render(request, 'home/result.html', context)
        
        except Exception as e:
            messages.error(request, 'Please enter correct enrollment number!!')

            return render(request, 'home/result.html', context)
    # messages.success(request, 'Your profile was updated.')
    return render(request, 'home/result.html',context)

def apply(request):
    context={}
    notice=AddNotice.objects.last()
    context['notice']=notice
    if request.method =='POST':
        apply = Apply()
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        subject = request.POST.get('subject')
        query = request.POST.get('query')
        course = request.POST.get('course')
        apply.name = name
        apply.email = email
        apply.phone = phone
        apply.subject = subject
        apply.query = query
        apply.applying_for = course
        apply.save()
        return HttpResponse("THANKS FOR APPLYING FOR COURSES <br> <p><a href='/'> HOME </a> </p>")
    return render(request, 'home/apply.html',context)

def courses(request):
    context={}
    notice=AddNotice.objects.last()
    context['notice']=notice
    return render(request,'home/courses.html',context)


def admitcard(request):
    context={}
    notice=AddNotice.objects.last()
    context['notice']=notice 

    # getting admitcard for authenticated user
    
    if request.user.is_authenticated:
        try:
            user=UserEnrollment.objects.get(user=request.user)
        except:
            messages.error(request,'Your result not found')
        try:
            admitcard = AdmitCard.objects.get(enrollment_no=user.enrollment_no)
            return render(request,'home/admitcard.html',{'admitcard':admitcard})

        except Exception as e:
            messages.warning(request, 'Admit card not found !!')
        
    if request.method == 'POST':
        enrollment_no = request.POST.get('enrollment_no')
        print(enrollment_no)

        try:
            admitcard = AdmitCard.objects.get(enrollment_no=enrollment_no)
            return render(request,'home/admitcard.html',{'admitcard':admitcard})

        except Exception as e:
            messages.warning(request, 'Please enter correct enrollment number!!')
            return render(request, 'home/admitcard.html')
    return render(request,'home/admitcard.html',context)

def certificate(request):
    context={}
    notice=AddNotice.objects.last()
    context['notice']=notice
    if request.user.is_authenticated:
        try:
            user=UserEnrollment.objects.get(user=request.user)
        except:
            messages.error(request,'Your Certificate not found')
        try:
            certificate = Certificate.objects.filter(enrollment_no=user.enrollment_no)
            context['queryset']=certificate
        except Exception as e:
            messages.warning(request, 'Certificate card not found !!')
        
    if request.method == 'POST':
        searched=request.POST['search']
        queryset=Certificate.objects.filter(Q(enrollment_no__icontains=searched) | Q(center_id__icontains=searched))
        context['queryset']=queryset

    return render(request,'home/certificate.html',context)

def admit_render_pdf_view(request,en_no):
    template_path = 'home/pdf1.html'
    queryset=get_object_or_404(AdmitCard,enrollment_no=en_no)
    context = {'myvar': queryset}
    
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    
    #if directly download
    response['Content-Disposition'] = 'attachment; filename="report.pdf"'

    #if u want to open a proper pdf format
    response['Content-Disposition'] = 'filename="report.pdf"'

    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)


    # create a pdf
    pisa_status = pisa.CreatePDF(
       html, dest=response)
    
   
    response['Content-Disposition'] = 'filename="report.pdf"'
    
    # if error then show some funny view
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response
    
    

def idcard(request):
    context={}
    notice=AddNotice.objects.last()
    context['notice']=notice

    # getting id card for authenticated user
    if request.user.is_authenticated:
        try:
            user=UserEnrollment.objects.get(user=request.user)
        except:
            messages.error(request,'Your result not found')
            
        try:
            idcard= IdCard.objects.get(enrollment_no=user.enrollment_no)
            return render(request,'home/idcard.html',{'idcard':idcard})

        except Exception as e:
            messages.warning(request, 'Id card not found !!')

    if request.method == 'POST':
        enrollment_no = request.POST.get('enrollment_no')
        print(enrollment_no)

        try:
            idcard= IdCard.objects.get(enrollment_no=enrollment_no)
            return render(request,'home/idcard.html',{'idcard':idcard})

        except Exception as e:
            messages.warning(request, 'Please enter correct enrollment number!!')
            return render(request, 'home/idcard.html')
    return render(request,'home/idcard.html',context)


def idcard_render_pdf_view(request,en_no):
    template_path = 'home/pdf2.html'
    queryset=get_object_or_404(IdCard,enrollment_no=en_no)
    context = {'myvar': queryset}
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    
    #if directly download
    #response['Content-Disposition'] = 'attachment; filename="report.pdf"'

    #if u want to open a proper pdf format
    response['Content-Disposition'] = 'filename="report.pdf"'

    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
       html, dest=response)
    # if error then show some funny view
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response

@login_required
def quiz(request):
    try:
        questions_pool=list(QuizQuestion.objects.all())
        random.shuffle(questions_pool)

        questions=questions_pool[0:5]
        if request.method == 'POST':
            qid=list()
            answer=list()
            quizTime=request.POST['time']
            
            total_right=0
            total_attempt=0
            total_wrong=0
            
            for i in range(1,6):
                qid.append(request.POST['qid'+str(i)])
                answer.append(request.POST['answer'+str(i)])
            a=0   
            for id in qid:
                question=QuizQuestion.objects.get(id=id)
                if question.answer == answer[a]:
                    total_right+=1
                    total_attempt+=1
                elif answer[a] == 'default':
                    pass
                else:
                    total_attempt+=1            
                    total_wrong+=1
                a+=1
                score=(total_right/5)*100
            qr=QuizResult.objects.create(user=request.user)
            qr.total_right=total_right
            qr.total_wrong=total_wrong
            qr.total_attempt=total_attempt
            qr.time=quizTime
            qr.save()
            
            param={'total_attempt':total_attempt,'total_right':total_right,'total_wrong':total_wrong,'score':score,'quizTime':quizTime}
            return render(request,'home/result_quiz.html',param)

                
    except Exception as e:
        print("Quiz Excption : ",e)

    return render(request,'home/start_quiz.html',{'questions':questions})


@login_required
def quizResults(request):
    context={}
    try:
        queryset=QuizResult.objects.filter(user=request.user)
        context['results']=queryset
    except Exception as e:
        print('Quiz Result Exception :',e)
        
    return render(request,'home/quiz_all_results.html',context)




def health_science_courses(request):
    course_desc = Course_desc.objects.filter(branch="Health Science Courses")
    context = {'course_desc':course_desc}
    notice=AddNotice.objects.last()
    context['notice']=notice
    return render(request, 'home/health_science_courses.html',context)

def engineering_courses(request):
    course_desc = Course_desc.objects.filter(branch="Engineering Courses")
    context = {'course_desc':course_desc}
    notice=AddNotice.objects.last()
    context['notice']=notice
    return render(request, 'home/engineering_courses.html',context)

def management_courses(request):
    course_desc = Course_desc.objects.filter(branch="Management Courses")
    context = {'course_desc':course_desc}
    notice=AddNotice.objects.last()
    context['notice']=notice
    return render(request, 'home/management_courses.html',context)

def certified_courses(request):
    course_desc = Course_desc.objects.filter(branch="Certified Courses")
    context = {'course_desc':course_desc}
    notice=AddNotice.objects.last()
    context['notice']=notice
    return render(request, 'home/certified_courses.html',context)