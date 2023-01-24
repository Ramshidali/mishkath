import datetime
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from activity.forms import ActivityForm, ActivityQuestionForm

from activity.models import Activity, ActivityQuestion
from main.functions import get_auto_id


# Create your views here.

@login_required
def activities(request):
    activity_instances = Activity.objects.filter(is_deleted=False)
    
    context = {
        'activity_instances' : activity_instances,
        'is_need_resize_cards' :True,  
    }    
    return render(request, 'activity/activity.html',context)

@login_required
def view_activity(request,pk):
    activity_instances = Activity.objects.get(pk=pk,is_deleted=False)
    
    context = {
        'activity_instances' : activity_instances,
        'is_need_resize_cards' :True,  
    }    
    return render(request, 'activity/view_activity.html',context)


@login_required
def create_activity(request,pk):
    redirect_page = request.GET.get('redirect_to')
    if pk:
        instance = get_object_or_404(Activity, pk=pk)
    else:
        instance = ''

    message = ''
    if request.method == 'POST':
        if instance:
            form = ActivityForm(request.POST,instance=instance,files=request.FILES)
        else:
            form = ActivityForm(request.POST,files=request.FILES)
                
        if form.is_valid():
            data = form.save(commit=False)
            if not instance:
                data.auto_id = get_auto_id(Activity)
                data.creator = request.user
            else:
                data.date_updated = datetime.datetime.today()
            data.updater = request.user
            data.save()
            
            if redirect_page == 'activity_view':
                return redirect(reverse('activity:view_activity'))
            else:
                return redirect(reverse('activity:activities'))
        else:
            message = "Form Validation Error"

    if instance:
        form = ActivityForm(instance=instance)
    else:
        form = ActivityForm()

    context = {
        'form' : form,
        'instance' : instance,
        'message' : message,
    }

    return render(request, 'creates/create.html', context)


@login_required
def delete_activity(request,pk):
    Activity.objects.filter(pk=pk).update(is_deleted=True)

    return redirect(reverse('activity:activities'))


@login_required
def activity_questions(request):
    question_instances = ActivityQuestion.objects.filter(is_deleted=False)
    
    context = {
        'activity_questions' : question_instances,
        'is_need_resize_cards' :True,  
    }    
    return render(request, 'activity/activity_questions.html',context)

@login_required
def create_activity_question(request,pk):
    redirect_page = request.GET.get('redirect_to')
    if pk:
        instance = get_object_or_404(ActivityQuestion, pk=pk)
    else:
        instance = ''

    message = ''
    if request.method == 'POST':
        if instance:
            form = ActivityQuestionForm(request.POST,instance=instance)
        else:
            form = ActivityQuestionForm(request.POST)
                
        if form.is_valid():
            data = form.save(commit=False)
            if not instance:
                data.auto_id = get_auto_id(ActivityQuestion)
                data.creator = request.user
            else:
                data.date_updated = datetime.datetime.today()
            data.updater = request.user
            data.save()
            
            if redirect_page == 'activity_view':
                # return redirect(reverse('activity:view_activity'))
                return redirect(reverse('activity:view_activity',kwargs={'pk':instance.activity.pk}))
            else:
                return redirect(reverse('activity:activity_questions'))
        else:
            message = "Form Validation Error"

    if instance:
        form = ActivityQuestionForm(instance=instance)
    else:
        form = ActivityQuestionForm()

    context = {
        'form' : form,
        'instance' : instance,
        'message' : message,
    }

    return render(request, 'creates/create.html', context)


@login_required
def delete_activity_question(request,pk):
    ActivityQuestion.objects.filter(pk=pk).update(is_deleted=True)

    return redirect(reverse('activity:activity_questions'))