from django.db import models
from hmmauth.models import *
from hospital.models import *
# Create your models here.
class Region(models.Model):
    name =models.CharField(max_length=200,null=True,blank=True)
    status = models.CharField(max_length=200,default=0,null=True,blank=True)
    color = models.CharField(max_length=200,default=0,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name_plural = "Region List"
        
    def __str__(self):
        return self.name
    
class Curency(models.Model):
    symbol =models.CharField(max_length=200,null=True,blank=True)
    desc =models.CharField(max_length=200,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name_plural = "Curency List"
        
    def __str__(self):
        return self.symbol