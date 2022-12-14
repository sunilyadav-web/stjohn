from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(QuizResult)

admin.site.register(UserEnrollment)

admin.site.register(AddNotice)

admin.site.register(Contact)

class QuizQuestionAdmin(admin.ModelAdmin):
    list_display=['question_statement','datetime']
admin.site.register(QuizQuestion,QuizQuestionAdmin)



from django.contrib import admin

class AdmitCardAdmin(admin.ModelAdmin):
    list_display=['enrollment_no','name','datetime']
admin.site.register(AdmitCard,AdmitCardAdmin)

class CertificateAdmin(admin.ModelAdmin):
    list_display=['title','name','datetime']
admin.site.register(Certificate, CertificateAdmin)

class IdCardAdmin(admin.ModelAdmin):
      list_display = ['enrollment_no','name','datetime']
admin.site.register(IdCard, IdCardAdmin)



# Register your models here.

admin.site.register(Apply)
admin.site.register(Course_desc)


class Sem1Admin(admin.TabularInline):
    model = Semester
        


class ProfileAdmin(admin.ModelAdmin):
    # inlines = [Sem1Admin,Sem2Admin,Sem3Admin,Sem4Admin,Sem5Admin,Sem6Admin]
    inlines = [Sem1Admin]
    list_display = ['enrollment_no','name','father_name','course','specialization','academic_year','year_of_passing','created_at','updated_at']

admin.site.register(Profile,ProfileAdmin)

admin.site.register(ResultHighlightControl)
admin.site.register(SiteDown)
admin.site.register(DownloadDocument)
class DocuemntPurchasedStudentAdmin(admin.ModelAdmin):
    list_display = ['order_id','payment_id','signature','status','created_at','updated_at']
admin.site.register(DocumentPurchasedStudent,DocuemntPurchasedStudentAdmin)

