from __future__ import unicode_literals
from django.contrib.auth import authenticate,login,logout
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.models import User
from .forms import RegisterForm, ViewCompaniesForm
from .models import Student
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from .models import CompanyApplicants
from coordinator.models import Companies
from django.core.mail import send_mail

# Views
@login_required
def studentDashboard(request):
    print(CompanyApplicants.objects.all())
    return HttpResponse("here in dashboard")

@login_required
def registerStudent(request):

    user = request.user
    if Student.objects.filter(user = user).exists() :
        return render(request, 'student/dashboard.html', {})

    form = RegisterForm(request.POST or None)
    if form.is_valid():
        appl = form.save(commit = False)
        appl.user = request.user
        appl.save()
        return render(request, 'student/dashboard.html', {})
    return render(request,'authentication/form.html',{'form' : form})

@login_required
def viewNewApplications(request):
    user = request.user
    student = Student.objects.get(user = user)
    company = CompanyApplicants.objects.filter(student = student).filter(placementStatus = 'N')
    listOfEligibleCompanies = []
    for compayApplicaton in company:
        companyName = CompanyApplicants.getCompanyName(compayApplicaton)
        listOfEligibleCompanies.append(companyName)
    print(listOfEligibleCompanies)
    form = ViewCompaniesForm(request.POST or None)
    context = {'eligibleCompanies' : listOfEligibleCompanies, 'form':form}
    if form.is_valid():
        companyName = form.cleaned_data.get('nameOfCompany')
        companyName = companyName.upper()
        for companies in listOfEligibleCompanies:
            if companyName == companies.upper():
                companyName = companies
                break
        if companyName in str(listOfEligibleCompanies):
            companyDetails = Companies.objects.get(name = companyName)
            applicantData = CompanyApplicants.objects.get(student = student, company = companyDetails)
            applicantData.placementStatus = 'A'
            applicantData.save()
	    text_to_be_sent = 'Dear ' + Student.getStudentName(student) + ',\n' + 'You have successfully applied to be a part of the placement drive for the company - ' +  companyName + '. We will be reaching out to you with further notifications about the process.\n' + 'Best Regards\n' + 'CCPD.'
	    send_mail(
		    'Application Confirmation',
		    text_to_be_sent,
		    'taps@nitw.ac.in',
		    [request.user.email],
		    fail_silently=True,
	    )
            
        else :
            print("You are not eligible for the company")
        return render(request,'student/showCompanies.html',context)
    return render(request,'student/showCompanies.html',context)

@login_required
def viewStatusOfApplication(request):
    user = request.user
    student = Student.objects.get(user = user)
    company = CompanyApplicants.objects.filter(student = student).exclude(placementStatus = 'N').exclude(placementStatus = 'R')
    listOfAppliedCompanies = []
    for compayApplicaton in company:
        companyName = CompanyApplicants.getCompanyName(compayApplicaton)
        listOfAppliedCompanies.append(companyName + " -> " + compayApplicaton.placementStatus)
    print(listOfAppliedCompanies)
    return render(request,'student/showApplied.html',{'eligibleCompanies':listOfAppliedCompanies})


