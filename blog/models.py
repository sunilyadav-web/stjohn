from django.db import models
from ckeditor.fields import RichTextField
from .utils import *


class Category(models.Model):
    category_name=models.CharField(max_length=150,unique=True)
    created_at=models.DateTimeField(auto_now_add=True)
    upload_to=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.category_name


STATUS = (
    (0,"Draft"),
    (1,"Publish")
) 
class Post(models.Model):
    title=models.CharField(max_length=1000,)    
    image=models.ImageField(upload_to='blog',null=True,blank=True)
    content=RichTextField()
    category=models.ForeignKey(Category,on_delete=models.SET_NULL, null=True,blank=True)
    meta_description=models.TextField(blank=True,null=True)
    meta_keyword=models.TextField(blank=True,null=True)
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