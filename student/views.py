from __future__ import unicode_literals
from django.contrib.auth import authenticate,login,logout
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.models import User
from .forms import *
from .models import Student
from django.shortcuts import redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from .models import *
from coordinator.models import *
from datetime import datetime, timedelta
from django.core.mail import send_mail

listOfAnnouncements = []
noOfAnnouncements = 0
student  = None

@login_required
def studentDashboard(request):
    global listOfAnnouncements, student, noOfAnnouncements
    return render(request, 'student/dashboard/index.html', {'student':student,'noOfAnnouncements': noOfAnnouncements })

@login_required
def registerStudent(request):
    user = request.user
    student = Student.objects.get(user = request.user)
    if Student.objects.filter(user = user).exists() :
        getAnnouncements = Announcement.objects.filter(datePublished__gte = datetime.now() - timedelta(1), datePublished__lte = datetime.now())
        student = Student.objects.get(user = request.user)
        
        for announcement in getAnnouncements:
            if announcement.type_of_announcement == 'Broadcasting':
                listOfAnnouncements.append(announcement)
            else:
                companyName = Announcement.getCompanyName(announcement)
                company = Companies.objects.get(name = companyName)
                if CompanyApplicants.objects.filter(student = student).filter(company = company).exists():
                    listOfAnnouncements.append(announcement)
        
        global noOfAnnouncements
        noOfAnnouncements = len(listOfAnnouncements)
        return HttpResponseRedirect('/student/studentDashboard')

    form = RegisterForm(request.POST or None)
    if form.is_valid():
        appl = form.save(commit = False)
        appl.user = request.user
        appl.save()
        return HttpResponseRedirect('student/studentDashboard')
    return render(request,'authentication/form.html',{'form' : form})

@login_required
def viewNewApplications(request):
    student = Student.objects.get(user = request.user)

    user = request.user
    company = CompanyApplicants.objects.filter(student = student).filter(placementStatus = 'N')
    context = {'eligibleCompanies' : company, 'student':student}
    companyName = request.POST.get('nameOfCompany')
    print(companyName, "hello")
    if companyName != None :
        companyDetails = Companies.objects.get(name = companyName)
        applicantData = CompanyApplicants.objects.get(student = student, company = companyDetails)
        applicantData.placementStatus = 'A'
        applicantData.save()

        text_to_be_sent = 'Dear ' + student.name + ',\n' + 'You have successfully applied to be a part of the placement drive for the company - ' +  companyName + '. We will be reaching out to you with further notifications about the process.\n' + 'Best Regards\n' + 'CCPD.'
        send_mail(
		    'Application Confirmation',
		    text_to_be_sent,
		    'taps@nitw.ac.in',
		    [request.user.email],
		    fail_silently=True,
	    )
        
    return render(request,'student/showCompanies.html',context)

@login_required
def viewStatusOfApplication(request):
    student = Student.objects.get(user = request.user)
    user = request.user
    company = CompanyApplicants.objects.filter(student = student).exclude(placementStatus = 'N').exclude(placementStatus = 'R')
    return render(request,'student/showApplied.html',{'eligibleCompanies':company, 'student':student})

@login_required
def viewProfile(request):
    student = Student.objects.get(user = request.user)

    resumeUploaded = False
    if Resume.objects.filter(user = request.user).exists():
        resumeUploaded = True
    return render(request,'student/dashboard/pages/profile.html',{'student':student, 'resumeUploaded': resumeUploaded})

@login_required
def uploadResume(request):
    student = Student.objects.get(user = request.user)
    
    form = ResumeForm(request.POST or None)
    if form.is_valid():
        education = form.cleaned_data.get('educationAll')
        projectAll = form.cleaned_data.get('projectAll')
        acheievementsAll = form.cleaned_data.get('acheievementsAll')
        relevantCoursesAll = form.cleaned_data.get('relevantCoursesAll')
        skillsAll = form.cleaned_data.get('skillsAll')
        extraCurricularAll = form.cleaned_data.get('extraCurricularAll')

        saveDetails = Resume(
            education = education,
            projects = projectAll,
            achievements = acheievementsAll,
            skills = skillsAll,
            relevantCourses = relevantCoursesAll,
            extraCurricular = extraCurricularAll
        )

        saveDetails.save()
    return render(request,'student/Resume.html',{'form':form, 'student':student})    

@login_required
def showCalendar(request):
    student = Student.objects.get(user = request.user)
    return render(request,'student/dashboard/pages/calendar.html',{'student':student})

@login_required
def viewAnnouncements(request):
    global listOfAnnouncements, noOfAnnouncements, student
    return render(request,'student/dashboard/pages/announcements.html',{'student':student, 'announcements':listOfAnnouncements, 'noOfAnnouncements': len(listOfAnnouncements)})

@login_required
def contacTnp(request):
	student = Student.objects.get(user = request.user)
    form = ContactForm(request.POST or None)
    if form.is_valid():
        name = form.cleaned_data.get('name')
        mailid = form.cleaned_data.get('mailid')
        message = form.cleaned_data.get('message')
        saveDetails = Contact(
            name = name,
            mailid = mailid,
            message = message
        )
        saveDetails.save()
		send_mail(
		    name + ' contacting CCPD',
		    message,
		    'taps@nitw.ac.in',
		    [mailid],
		    fail_silently=True,
	    )
		
    return render(request,'student/Contact.html',{'form':form, 'student':student})    
