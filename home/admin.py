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
    list_display=['enrollment_no','name','datetime']
admin.site.register(Certificate, CertificateAdmin)
    

class IdCardAdmin(admin.ModelAdmin):
      list_display = ['enrollment_no','name','datetime']
admin.site.register(IdCard, IdCardAdmin)



# Register your models here.

admin.site.register(Apply)
admin.site.register(Course_desc)


class Sem1Admin(admin.TabularInline):
    model = Semester
        
# class Sem2Admin(admin.TabularInline):
#     model = Semester_2

# class Sem3Admin(admin.TabularInline):
#     model = Semester_3

# class Sem4Admin(admin.TabularInline):
#     model = Semester_4

# class Sem5Admin(admin.TabularInline):
#     model = Semester_5

# class Sem6Admin(admin.TabularInline):
#     model = Semester_6

class ProfileAdmin(admin.ModelAdmin):
    # inlines = [Sem1Admin,Sem2Admin,Sem3Admin,Sem4Admin,Sem5Admin,Sem6Admin]
    inlines = [Sem1Admin]
    list_display = ['enrollment_no','name','father_name','course','specialization','academic_year','year_of_passing','created_at','updated_at']

admin.site.register(Profile,ProfileAdmin)

admin.site.register(ResultHighlightControl)
admin.site.register(SiteDown)


# @admin.register(Profile)
# class ProfileAdmin(ImportExportModelAdmin):
#     list_display = ['enrollment_no','name','father_name']
#     pass 