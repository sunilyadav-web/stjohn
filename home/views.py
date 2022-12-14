from io import BytesIO
import random
from time import time
from django.shortcuts import redirect, render, get_object_or_404
from .models import *
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .helper import *
import razorpay
from blog.models import *
from stjohn.settings import RAZORPAY_API_KEY,RAZORPAY_API_SECRET_KEY


def index(request):
    context = {}
    try:
        notice = AddNotice.objects.last()
        rh = ResultHighlightControl.objects.get(id=1)
        posts=Post.objects.all()[0:4]
        print('All Posts in Home  : ',posts)
        context['posts']=posts
        context['rh'] = rh
        context['notice'] = notice
        sd = SiteDown.objects.get(id=1)
        context['site-down'] = sd
        if sd.display == True:
            caption = sd.caption
            link = sd.add_link
            return render(request, 'under_construction.html', {'link': link, 'caption': caption})
    except Exception as e:
        print('Index Exception :', e)
    return render(request, 'home/index.html', context)


def about(request):
    context = {}
    notice = AddNotice.objects.last()
    rh = ResultHighlightControl.objects.get(id=1)
    context['rh'] = rh
    context['notice'] = notice

    return render(request, 'home/about.html', context)


def aboutVision(request):
    context = {}
    notice = AddNotice.objects.last()
    rh = ResultHighlightControl.objects.get(id=1)
    context['rh'] = rh
    context['notice'] = notice

    return render(request, 'home/about_vision.html', context)


def contact(request):
    context = {}
    notice = AddNotice.objects.last()
    context['notice'] = notice
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        contact_no = request.POST.get('contact_no')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        contact_entry = Contact(
            name=name, email=email, contact_no=contact_no, subject=subject, message=message)
        contact_entry.save()
        messages.success(
            request, 'THANKS FOR CONTACTING US! WE WILL REACH TO U ASAP')
        

        res=contactusMail(name,email,contact_no,subject,message)
        print(res)


        return HttpResponseRedirect(reverse('index:index'))
    return render(request, 'home/contact.html', context)

@login_required()
def result(request):
    context = {}
    notice = AddNotice.objects.last()
    context['notice'] = notice

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
            student_percentage = round(percentage, 2)

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
            context = {'semesters': sem, 'profile': profile, "total_max_marks": total_max_marks, "total_min_marks": total_min_marks,
                       "total_obtained_marks": total_obtained_marks, 'student_percentage': student_percentage, 'grade': grade, 'notice': notice}

            return render(request, 'home/result.html', context)

        except Exception as e:
            print('Result Exception : ', e)
            messages.error(
                request, 'Please Enter Correct Enrollment Number !!')
            return render(request, 'home/result.html', context)
            

        # getting Result for authenticated user
    if request.user.is_authenticated:

        try:
            user = UserEnrollment.objects.get(user=request.user)
        except:
            messages.error(request, 'Your Enrollment Number not found!')
            return render(request, 'home/result.html', context)
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
            student_percentage = round(percentage, 2)

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
            context = {'semesters': sem, 'profile': profile, "total_max_marks": total_max_marks, "total_min_marks": total_min_marks,
                       "total_obtained_marks": total_obtained_marks, 'student_percentage': student_percentage, 'grade': grade, 'notice': notice}

            return render(request, 'home/result.html', context)

        except Exception as e:
            messages.warning(request, 'Your Result Not Genrated Yet !!')

    # messages.success(request, 'Your profile was updated.')
    return render(request, 'home/result.html', context)


def apply(request):
    context = {}
    notice = AddNotice.objects.last()
    context['notice'] = notice
    if request.method == 'POST':
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
        res=applyMail(name,email,phone,subject,course,query)
        print(res)
        return HttpResponse("THANKS FOR APPLYING FOR COURSES <br> <p><a href='/'> HOME </a> </p>")
    return render(request, 'home/apply.html', context)


def courses(request):
    context = {}
    notice = AddNotice.objects.last()
    context['notice'] = notice
    return render(request, 'home/courses.html', context)

@login_required()
def admitcard(request):
    context = {}
    notice = AddNotice.objects.last()
    context['notice'] = notice

    if request.method == 'POST':
        enrollment_no = request.POST.get('enrollment_no')
        print(enrollment_no)

        try:
            admitcard = AdmitCard.objects.get(enrollment_no=enrollment_no)
            return render(request, 'home/admitcard.html', {'admitcard': admitcard,'notice':notice})

        except Exception as e:
            messages.warning(
                request, 'Please Enter Correct Enrollment Number!!')
            return render(request, 'home/admitcard.html', context)

    # getting admitcard for authenticated user
    if request.user.is_authenticated:
        try:
            user = UserEnrollment.objects.get(user=request.user)
        except:
            messages.warning(request, 'Your Enrollment not found!')
            return render(request, 'home/admitcard.html', context)
        try:
            admitcard = AdmitCard.objects.get(enrollment_no=user.enrollment_no)
            context['admitcard'] = admitcard

        except Exception as e:
            messages.warning(request, 'Your Admit Card Not Generated Yet!!')
    return render(request, 'home/admitcard.html', context)


def certificate(request):
    context = {}
    notice = AddNotice.objects.last()
    context['notice'] = notice

    if request.method == 'POST':
        searched = request.POST['center_id']
        queryset = Certificate.objects.filter(center_id=searched)
        context['queryset'] = queryset
        if not queryset:
            messages.warning(request, 'Please Enter Correct Cenrter Id!')
        # return render(request,'home/certificate.html',context)

      # getting certificate for login user
    # if request.user.is_authenticated:
    #     try:
    #         user=UserEnrollment.objects.get(user=request.user)
    #     except:
    #         messages.warning(request,'Your Enrollment Not Found!')
    #         return render(request,'home/certificate.html',context)
    #     try:
    #         certificate = Certificate.objects.filter(enrollment_no=user.enrollment_no)
    #         context['queryset']=certificate
    #         if not certificate:
    #             messages.warning(request, 'Certificate Not Generated Yet !!')
    #     except Exception as e:
    #         print('Certificate Exception : ',e)

    return render(request, 'home/certificate.html', context)

@login_required()
def admit_render_pdf_view(request, en_no):
    template_path = 'home/pdf1.html'
    queryset = get_object_or_404(AdmitCard, enrollment_no=en_no)
    context = {'myvar': queryset}

    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')

    # if directly download
    response['Content-Disposition'] = 'attachment; filename="report.pdf"'

    # if u want to open a proper pdf format
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

@login_required()
def idcard(request):
    context = {}
    notice = AddNotice.objects.last()
    context['notice'] = notice

    if request.method == 'POST':
        enrollment_no = request.POST.get('enrollment_no')
        print(enrollment_no)

        try:
            idcard = IdCard.objects.get(enrollment_no=enrollment_no)
            return render(request, 'home/idcard.html', {'idcard': idcard,'notice':notice})

        except Exception as e:
            messages.warning(
                request, 'Please Enter correct Enrollment number!!')
            return render(request, 'home/idcard.html', context)

        # getting id card for authenticated user
    if request.user.is_authenticated:
        try:
            user = UserEnrollment.objects.get(user=request.user)
        except:
            messages.error(request, 'Your Your Enrollment Number not found')
            return render(request, 'home/idcard.html', context)
        try:
            idcard = IdCard.objects.get(enrollment_no=user.enrollment_no)
            context['idcard'] = idcard

        except Exception as e:
            messages.warning(request, 'Your Id Card Not Generated Yet !!')

    return render(request, 'home/idcard.html', context)

@login_required()
def idcard_render_pdf_view(request, en_no):
    template_path = 'home/pdf2.html'
    queryset = get_object_or_404(IdCard, enrollment_no=en_no)
    context = {'myvar': queryset}
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')

    # if directly download
    #response['Content-Disposition'] = 'attachment; filename="report.pdf"'

    # if u want to open a proper pdf format
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
        questions_pool = list(QuizQuestion.objects.all())
        random.shuffle(questions_pool)

        questions = questions_pool[0:5]
        if request.method == 'POST':
            qid = list()
            answer = list()
            quizTime = request.POST['time']

            total_right = 0
            total_attempt = 0
            total_wrong = 0

            for i in range(1, 6):
                qid.append(request.POST['qid'+str(i)])
                answer.append(request.POST['answer'+str(i)])
            a = 0
            for id in qid:
                question = QuizQuestion.objects.get(id=id)
                if question.answer == answer[a]:
                    total_right += 1
                    total_attempt += 1
                elif answer[a] == 'default':
                    pass
                else:
                    total_attempt += 1
                    total_wrong += 1
                a += 1
                score = (total_right/5)*100
            qr = QuizResult.objects.create(user=request.user)
            qr.total_right = total_right
            qr.total_wrong = total_wrong
            qr.total_attempt = total_attempt
            qr.time = quizTime
            qr.save()

            param = {'total_attempt': total_attempt, 'total_right': total_right,
                     'total_wrong': total_wrong, 'score': score, 'quizTime': quizTime}
            return render(request, 'home/result_quiz.html', param)

    except Exception as e:
        print("Quiz Excption : ", e)

    return render(request, 'home/start_quiz.html', {'questions': questions})


@login_required
def quizResults(request):
    context = {}
    try:
        queryset = QuizResult.objects.filter(user=request.user)
        context['results'] = queryset
    except Exception as e:
        print('Quiz Result Exception :', e)

    return render(request, 'home/quiz_all_results.html', context)


def health_science_courses(request):
    course_desc = Course_desc.objects.filter(branch="Health Science Courses")
    context = {'course_desc': course_desc}
    notice = AddNotice.objects.last()
    context['notice'] = notice
    return render(request, 'home/health_science_courses.html', context)


def engineering_courses(request):
    course_desc = Course_desc.objects.filter(branch="Engineering Courses")
    context = {'course_desc': course_desc}
    notice = AddNotice.objects.last()
    context['notice'] = notice
    return render(request, 'home/engineering_courses.html', context)


def management_courses(request):
    course_desc = Course_desc.objects.filter(branch="Management Courses")
    context = {'course_desc': course_desc}
    notice = AddNotice.objects.last()
    context['notice'] = notice
    return render(request, 'home/management_courses.html', context)


def certified_courses(request):
    course_desc = Course_desc.objects.filter(branch="Certified Courses")
    context = {'course_desc': course_desc}
    notice = AddNotice.objects.last()
    context['notice'] = notice
    return render(request, 'home/certified_courses.html', context)


def regularAdmission(request):
    context={}
    try:
        notice = AddNotice.objects.last()
        context['notice'] = notice
    except Exception as e:
        print('Regular Admission Exception : ',e)
    return render(request,'home/admission_regular.html',context)

def onlineAdmission(request):
    context={}
    try:
        notice = AddNotice.objects.last()
        context['notice'] = notice
    except Exception as e:
        print('Online Admission Exception : ',e)
    return render(request,'home/admission_online.html',context)

def eveningAdmission(request):
    context={}
    try:
        notice = AddNotice.objects.last()
        context['notice'] = notice
    except Exception as e:
        print('Evening Admission Exception : ',e)
    return render(request,'home/admission_evening.html',context)

def downloadDocument(request):
    context={}
    try:
        notice = AddNotice.objects.last()
        context['notice'] = notice
        download_documents=DownloadDocument.objects.all()
        context['documents']=download_documents
        

    except Exception as e:
        print('Download Document Exception : ',e)
    return render(request,'home/download_document.html',context)

def checkout(request,id):
    context={}
    try:
        print('id : ',id)
        notice = AddNotice.objects.last()
        context['notice'] = notice
        obj=DownloadDocument.objects.filter(id=id).exists()
        print('Obj ',obj)
        if obj:
            document=DownloadDocument.objects.get(id=id)
            print('Document ',document)
            context['document']=document
            context['api_key']=RAZORPAY_API_KEY
            client = razorpay.Client(auth=(RAZORPAY_API_KEY, RAZORPAY_API_SECRET_KEY))
            DATA = {
                "amount": (document.price)*100,
                "currency": "INR",
                "payment_capture":1,
                }
            payment=client.order.create(data=DATA)
            payment_price=float(payment['amount'])
            print('Prices type ',type(payment_price))
            purchase_obj=DocumentPurchasedStudent.objects.create(order_id=payment['id'],document=document,price=payment_price/100)
            print(purchase_obj)
            print("Order : ",payment)

            context['payment']=payment

    except Exception as e:
        print('Checkout Page Exception : ',e)
    return render(request,'home/checkout.html',context)

def paymentSuccess(request):
    context={}
    try:
        payment_id=request.GET['payment_id']
        order_id=request.GET['order_id']
        signature=request.GET['signature']
        obj=DocumentPurchasedStudent.objects.filter(order_id=order_id).exists()
        if obj:
            document_obj=DocumentPurchasedStudent.objects.get(order_id=order_id)
            document_obj.payment_id=payment_id
            document_obj.signature=signature
            document_obj.status=True
            document_obj.save()
            print('document obj ',document_obj)
           
            context['order_id']=order_id
            context['document']=document_obj.document

    except Exception as e:
        print('Payment Success Exception : ',e)
        messages.error(request,"You are not authrised!")
        return redirect('/')
    return render(request,'home/payment_success.html',context)



def rti(request):
    context={}
    try:
        notice = AddNotice.objects.last()
        context['notice'] = notice
    except Exception as e:
        print("RTI Exception : ",e)
    return render(request,'home/rti.html',context)