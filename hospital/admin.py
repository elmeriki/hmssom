from django.contrib import admin
from hospital.models import *

# Register your models here.

admin.site.register(Department)
admin.site.register(Hospital)
admin.site.register(Notices)