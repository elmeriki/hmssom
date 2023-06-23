from django.contrib import admin
from hospital.models import *

# Register your models here.

admin.site.register(Department)
admin.site.register(Hospital)
admin.site.register(Notices)
admin.site.register(Treatment)
admin.site.register(Lapreport)
admin.site.register(Labresult)