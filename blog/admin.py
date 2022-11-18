from django.contrib import admin
from .models import *


class PostAdmin(admin.ModelAdmin):
    list_display = ("title",  "created_at","status",)

admin.site.register(Post,PostAdmin) 
