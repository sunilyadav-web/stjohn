from django.urls import path
from . import views

app_name='index'

urlpatterns = [
    path('',views.index,name='index'),   
    path('about/',views.about,name='about'),
    path('vision-and-mission/',views.aboutVision,name='vision-and-mission'),
    path('result/', views.result,name='result'),
    path('apply/', views.apply,name='apply'),
    path('admitcard/',views.admitcard,name='admitcard'),
    path('certificate/',views.certificate,name="certificate"),
    path('admit-pdf/<str:en_no>/',views.admit_render_pdf_view,name='admit-pdf-view'),
    path('idcard/',views.idcard,name='idcard'),
    path('idcard-pdf/<str:en_no>/',views.idcard_render_pdf_view,name='idcard-pdf-view'),
    path('contact/',views.contact,name='contact'),


    path('quiz/',views.quiz,name='quiz'),
    path('quiz-results/',views.quizResults,name='quiz-results'),

    path('courses/',views.courses,name='courses'),
    path('health-science-courses/', views.health_science_courses,name='health_science_courses'),
    path('engineering-courses/', views.engineering_courses,name='engineering_courses'),
    path('management-courses/', views.management_courses,name='management_courses'),
    path('certified-courses/', views.certified_courses,name='certified_courses'),

    path('admission-regular',views.regularAdmission,name='admission-regular'),
    path('admission-online',views.onlineAdmission,name='admission-online'),
    path('admission-evening',views.eveningAdmission,name='admission-evening'),
    path('download-document/',views.downloadDocument,name='download-document'),
    path('checkout/<id>/',views.checkout,name='checkout'),
    path('payment-success/',views.paymentSuccess,name='payment-success'),
    path('rti/',views.rti,name='rti'),


]