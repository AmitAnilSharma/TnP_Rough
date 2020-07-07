from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Student


class RegisterForm(forms.ModelForm):
    class Meta:
        model = Student
        fields=[
            'name',
            'admissionNumber',
            'branch',
            'yearOfGraduation',
            'rollNumber',
            'CGPA',
            'address',
            'mobileNumber'
        ]

class ViewCompaniesForm(forms.Form):
    nameOfCompany = forms.CharField(widget = forms.HiddenInput(), required = False,max_length=100)

class ResumeForm(forms.Form):
    name = forms.CharField(max_length=100)
    year = forms.CharField(max_length=100)
    email_id = forms.EmailField()
    phoneNumber = forms.CharField(max_length=10)
    address = forms.CharField(max_length=1000)
    
    educationAll = forms.CharField(widget = forms.HiddenInput(), required = False,max_length=10000)
    
    projectAll = forms.CharField(widget = forms.HiddenInput(), required = False,max_length=10000)
    
    acheievementsAll = forms.CharField(widget = forms.HiddenInput(), required = False,max_length=10000)
    
    skillsAll = forms.CharField(widget = forms.HiddenInput(), required = False,max_length=10000)
    
    relevantCoursesAll = forms.CharField(widget = forms.HiddenInput(), required = False,max_length=10000)
    
    extraCurricularAll = forms.CharField(widget = forms.HiddenInput(), required = False,max_length=10000)
    
    fields = [
        'name',
        'year',
        'email_id',
        'phoneNumber',
        'address',
        'educationAll',
        'projectAll',
        'acheievementsAll',
        'skillsAll'
        'relevantCoursesAll',
        'extraCurricularAll'

    ]

class ContactForm(forms.Form):
    name = forms.CharField(max_length=120)
    mailid = forms.EmailField()
	message = models.CharField(max_length = 20000000)  
    
    fields = [
        'name',
        'mailid',
        'message'

    ]    

        
