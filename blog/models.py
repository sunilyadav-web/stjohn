from django.db import models
from ckeditor.fields import RichTextField
from .utils import *

STATUS = (
    (0,"Draft"),
    (1,"Publish")
) 
class Post(models.Model):
    title=models.CharField(max_length=1000,)    
    image=models.ImageField(upload_to='blog',null=True,blank=True)
    content=RichTextField()
    slug=models.SlugField(max_length=1000, unique=True,null=True,blank=True)
    status=models.IntegerField(choices=STATUS, default=0)
    created_at=models.DateTimeField(auto_now_add=True)
    upload_to=models.DateTimeField(auto_now=True)

    @property
    def imageURL(self):
        try:
            URL=self.image.url
        except:
            URL=''
        return URL




    class Meta:
        ordering = ['-created_at']  

    def __str__(self):
        return self.title 
    def save(self,  *args, **kwargs):
        s=generate_slug(self.title)
        print('this is slug',s)
        self.slug=s
        super(Post,self).save(*args, **kwargs)