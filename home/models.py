import datetime
from django.db import models
from django.core.validators import validate_image_file_extension
from PIL import Image
from django.contrib.auth.models import User

class Contact(models.Model):
    name=models.CharField(max_length=100)
    email=models.EmailField(max_length=100,blank=False)
    contact_no=models.CharField(max_length=100,blank=False)
    subject=models.CharField(max_length=100,blank=False)
    message=models.TextField(blank=False)
    contacted_on=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name}-{self.contacted_on.year}-{self.contacted_on.month}-{self.contacted_on.day}"
    
    class Meta:
        verbose_name_plural='Contact'
        ordering = ['-contacted_on']

class Apply(models.Model):
    REMARKS = (
        ('Health Science Courses','Health Science Courses'),
        ('Engineering Courses','Engineering Courses'),
        ('Management Courses','Management Courses'),
        ('Certified Courses','Certified Courses'),
        ('Other Courses','Other Courses'),
    )

    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=100)
    subject = models.CharField(max_length=100)
    applying_for = models.CharField(max_length=50,choices = REMARKS)
    query = models.TextField()

    def __str__(self):
        return self.name

class Course_desc(models.Model):
    REMARKS = (
        ('Health Science Courses','Health Science Courses'),
        ('Engineering Courses','Engineering Courses'),
        ('Management Courses','Management Courses'),
        ('Certified Courses','Certified Courses'),
    )

    title = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=100)
    pre_requisite = models.CharField(max_length=100)
    duration = models.CharField(max_length=100)
    fee = models.CharField(max_length=100)
    breif_desc = models.CharField(max_length=100)

    branch = models.CharField(max_length=50,choices = REMARKS)

    def __str__(self):
        return self.title

class Profile(models.Model):
    enrollment_no = models.CharField(max_length=40,unique=True)
    name = models.CharField(max_length=40)
    father_name = models.CharField(max_length=40)
    course = models.CharField(max_length=40)
    specialization = models.CharField(max_length=40)
    academic_year = models.CharField(max_length=40) 
    year_of_passing = models.IntegerField()
    profile_pic = models.ImageField(upload_to='uploads/student_images/',blank=True)
    certificate=models.FileField(upload_to='Result_Certificate',blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True,blank=True,null=True)
    updated_at = models.DateTimeField(auto_now=True,blank=True,null=True)
    

    def __str__(self):
        return self.name

    @property
    def getCertificate(self):
        try:
            url=self.certificate.url
        except:
            url=None
        return url

    @property
    def profileImage(self):
        try:
            url=self.profile_pic.url
        except:
            url=None
        return url    
class Semester(models.Model):

    REMARKS = (
        ('Pass','Pass'),
        ('Fail','Fail')
    )
    particular = models.CharField(max_length=100)
    profile = models.ForeignKey("home.Profile", on_delete=models.CASCADE)
    max_marks = models.IntegerField()
    min_marks = models.IntegerField()
    obtained = models.IntegerField()
    remarks = models.CharField(max_length=50,choices = REMARKS)

    def __str__(self):
        return f"{self.particular}"


class AdmitCard(models.Model):
    enrollment_no=models.CharField(max_length=40,unique=True)
    name=models.CharField(max_length=200)
    admit_card=models.FileField(upload_to="admitcard_pdf's",blank=True, verbose_name="Admit Card PDF")
    datetime=models.DateTimeField(auto_now=True, null=True , blank=True)
    
    class Meta:
        ordering=['-id']
        
    @property
    def admitcardURL(self):
        try:
            url=self.admit_card.url
        except:
            url=''
        return url

    def __str__(self):
        return self.name


class IdCard(models.Model):
    enrollment_no=models.CharField(max_length=40,unique=True)
    name=models.CharField(max_length=100)
    id_card=models.FileField(upload_to='id_cards',null=True,blank=True, verbose_name="Id Card PDF File")
    datetime=models.DateTimeField(auto_now=True, null=True , blank=True)

   
    class Meta:
        ordering=['-id']

    @property
    def idcardURL(self):
        try:
            url=self.id_card.url
        except:
            url=''
        return url
    def __str__(self):
        return self.name

class QuizQuestion(models.Model):
    options = (
        ('A','A'),
        ('B','B'),
        ('C','C'),
        ('D','D'),
    )
    question_statement=models.CharField(max_length=250)
    option_a=models.CharField(max_length=70)
    option_b=models.CharField(max_length=70)
    option_c=models.CharField(max_length=70)
    option_d=models.CharField(max_length=70)
    answer=models.CharField(max_length=10, choices=options)
    datetime=models.DateTimeField(auto_now=True, null=True , blank=True)
    

class QuizResult(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    total_right=models.CharField(max_length=10)
    total_wrong=models.CharField(max_length=10)
    total_attempt=models.CharField(max_length=10)
    time=models.CharField(max_length=10)
    datetime=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username

class UserEnrollment(models.Model):
    enrollment_no=models.CharField(max_length=50)
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    datetime=models.DateTimeField(auto_now=True, null=True , blank=True)
    
    def __str__(self):
        return self.user.username

class AddNotice(models.Model):
    notice=models.CharField(max_length=70, null=True, blank=True, default='Welcome to St. John')
    notice_date=models.DateTimeField(auto_created=True,auto_now=True)

class Certificate(models.Model):
    title=models.CharField(max_length=40,unique=True)
    name=models.CharField(max_length=100)
    office_at=models.CharField(max_length=100)
    period_of=models.CharField(max_length=100)
    period_to=models.CharField(max_length=100)
    place=models.CharField(max_length=100)
    registration_date=models.DateField()
    center_id=models.CharField(max_length=100)
    file=models.FileField(blank=True,null=True)
    datetime=models.DateTimeField(auto_now=True,null=True, blank=True)
    

    class Meta:
        ordering=['-id']

    def __str__(self):
        return self.title+'  '+self.name
        
    @property
    def certificateFile(self):
        try:
            url=self.file.url
        except:
            url=None
        return url

class ResultHighlightControl(models.Model):
    display=models.BooleanField(default=False)

    def __str__(self):
        return f"RESULTSTYLEDISPLAY-{self.display}"


class SiteDown(models.Model):
    display=models.BooleanField(default=False)
    add_link=models.CharField(max_length=100,null=True,blank=True)
    caption=models.CharField(max_length=20,null=True,blank=True)


    def __str__(self):
        return f"SITEDOWN-{self.display}"


class DownloadDocument(models.Model):
    name=models.CharField(max_length=100)
    description=models.TextField(max_length=250)
    price=models.FloatField()
    sample=models.FileField(upload_to="document_semple")
    thankyou_message=models.TextField(max_length=150)
    created_at= models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class DocumentPurchasedStudent(models.Model):
    order_id=models.CharField(max_length=300, null=True,blank=True)
    payment_id=models.CharField(max_length=300, null=True,blank=True)
    signature=models.CharField(max_length=300, null=True,blank=True)
    document=models.ForeignKey(DownloadDocument, on_delete=models.SET_NULL, null=True,blank=True)
    price=models.FloatField()
    status=models.BooleanField(default=False)
    created_at= models.DateTimeField(auto_now_add=True, null=True,blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True,blank=True)
    def __str__(self):
        return self.document.name