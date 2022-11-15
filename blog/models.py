from django.db import models
from ckeditor.fields import RichTextField

STATUS = (
    (0,"Draft"),
    (1,"Publish")
)
class Post(models.Model):
    title=models.CharField(max_length=1000, unique=True)    
    image=models.ImageField(upload_to='blog',null=True,blank=True)
    content=RichTextField()
    slug=models.SlugField(max_length=1000, unique=True)
    status=models.IntegerField(choices=STATUS, default=0)
    created_at=models.DateTimeField(auto_now_add=True)
    upload_to=models.DateTimeField(auto_now=True)


    class Meta:
        ordering = ['-created_at']  

    def __str__(self):
        return self.title 