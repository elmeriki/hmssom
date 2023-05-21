from django import forms
from django.contrib.auth.models import User
from .models import Department

#creating a department form
class DepartmentForm(forms.ModelForm):
    # create meta class
    class Meta:
        # specify model to be used
        model = Department

    # specify fields to be used
        fields = [
            "departmentname",
            "departmentdesc",
        ]