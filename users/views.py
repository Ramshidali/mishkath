import datetime
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from learn.models import  StudentTopic
from payments.forms import StudentSubscriptionForm
from payments.models import StudentSubscription
from users.forms import AssignBatchForm, EditProfileForm, InterviewScheduleForm

from users.models import InterviewStatus, Profile

# Create your views here.

@login_required
def students(request):
    instances = Profile.objects.filter(is_deleted=False).order_by("-id")
    
    query = request.GET.get('q')
    if query :
        if query in 'allotted':
            profile_pk_from_interview_status = InterviewStatus.objects.filter(profile__pk__in=instances,status="allotted",is_deleted=False).values_list('profile__pk',flat=True)
            instances = Profile.objects.filter(is_deleted=False,pk__in=profile_pk_from_interview_status).order_by("-id")
        elif query in 'passed':
            profile_pk_from_interview_status = InterviewStatus.objects.filter(profile__pk__in=instances,status="passed",is_deleted=False).values_list('profile__pk',flat=True)
            instances = Profile.objects.filter(is_deleted=False,pk__in=profile_pk_from_interview_status).order_by("-id")
        elif query in 'pending':
            profile_pk_from_interview_status = InterviewStatus.objects.filter(profile__pk__in=instances,status="pending",is_deleted=False).values_list('profile__pk',flat=True)
            instances = Profile.objects.filter(is_deleted=False,pk__in=profile_pk_from_interview_status).order_by("-id")    
            
    context = {
        'instances' : instances,
    }
    return render(request,'students/students.html',context)


@login_required
def create_interview_schedule(request,pk):
    # pk = request.GET.get("pk")#student id
    if pk:
        instance = get_object_or_404(InterviewStatus, profile__pk=pk, is_deleted=False)
    else:
        instance = ''

    message = ''
    if request.method == 'POST':
        if instance:
            form = InterviewScheduleForm(request.POST, instance=instance)
        else:
            form = InterviewScheduleForm(request.POST)

        if form.is_valid():
            data = form.save(commit=False)
            
            data.date_updated = datetime.datetime.today()
            data.updater = request.user
            data.save()
            
            return redirect(reverse('users:students'))
            
        else:
            message = "Form Validation Error"

    if instance:
        form = InterviewScheduleForm(instance=instance)
    else:
        form = InterviewScheduleForm()

    context = {
        'form' : form,
        'message' : message,
    }
    
    return render(request, 'creates/create.html',context)


@login_required
def subscription_update(request,pk):
    if pk:
        instance = get_object_or_404(StudentSubscription, profile__pk=pk,is_deleted=False)
    else:
        instance = ''

    message = ''
    if request.method == 'POST':
        if instance:
            form = StudentSubscriptionForm(request.POST, instance=instance)
        else:
            form = StudentSubscriptionForm(request.POST)

        if form.is_valid():
            data = form.save(commit=False)
            
            data.date_updated = datetime.datetime.today()
            data.updater = request.user
            data.save()
            
            return redirect(reverse('users:students'))
            
        else:
            message = "Form Validation Error"

    if instance:
        form = StudentSubscriptionForm(instance=instance)
    else:
        form = StudentSubscriptionForm()

    context = {
        'form' : form,
        'message' : message,
    }
    
    return render(request, 'creates/create.html',context)


@login_required
def assign_batch(request,pk):
    if pk:
        instance = get_object_or_404(Profile, pk=pk,is_deleted=False)
    else:
        instance = ''

    message = ''
    if request.method == 'POST':
        if instance:
            form = AssignBatchForm(request.POST, instance=instance)
        else:
            form = AssignBatchForm(request.POST)

        if form.is_valid():
            data = form.save(commit=False)
            
            data.date_updated = datetime.datetime.today()
            data.updater = request.user
            data.save()
            
            return redirect(reverse('users:students'))
            
        else:
            message = "Form Validation Error"
    if instance:
        form = AssignBatchForm(instance=instance)
    else:
        form = AssignBatchForm()

    context = {
        'form' : form,
        'message' : message,
    }
    
    return render(request, 'creates/create.html',context)

@login_required
def view_profile(request,pk):
    profile_instance = Profile.objects.get(pk=pk,is_deleted=False)
    student_topic_instance = StudentTopic.objects.filter(student_id=profile_instance,is_completed=True,is_new_content=True,is_deleted=False)
    
    context = {
        'profile_instance' : profile_instance,
        'student_topic_instance' : student_topic_instance,
        
    }    
    return render(request, 'students/student_profile.html',context)


@login_required
def edit_profile(request,pk):
    if pk:
        instance = get_object_or_404(Profile, pk=pk,is_deleted=False)
    else:
        instance = ''

    message = ''
    if request.method == 'POST':
        if instance:
            form = EditProfileForm(request.POST, instance=instance)
        else:
            form = EditProfileForm(request.POST)

        if form.is_valid():
            data = form.save(commit=False)
            
            data.date_updated = datetime.datetime.today()
            data.updater = request.user
            data.save()
            
            return redirect(reverse('users:students'))
            
        else:
            message = "Form Validation Error"
    if instance:
        form = EditProfileForm(instance=instance)
    else:
        form = EditProfileForm()

    context = {
        'form' : form,
        'message' : message,
    }
    
    return render(request, 'creates/create.html',context)

@login_required
def delete_profile(request,pk):
    Profile.objects.filter(pk=pk).update(is_deleted=True)

    return redirect(reverse('users:students'))