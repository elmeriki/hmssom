from django.db import models
from hmmauth.models import *

# Create your models here.
class Region(models.Model):
    name =  models.CharField(max_length=200,null=True,blank=True)
    status = models.CharField(max_length=200,default=0,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    