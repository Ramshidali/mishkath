import datetime
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.urls import reverse

from main.functions import get_auto_id
from payments.forms import StudentSubscriptionForm, SubscriptionGradeFeeForm, SubscriptionGradeForm
from payments.models import StudentSubscription, SubscriptionGrade, SubscriptionGradeFee

# Create your views here.
@login_required
def subscription_grade(request):
    """
    subscription grade listings, eg:- subscription details with description etc
    :param request:
    """
    instances = SubscriptionGrade.objects.filter(is_deleted=False).order_by("-id")

    context = {
        'instances': instances,
        'page_name' : 'Subscription Grade'
    }
    return render(request, 'payments/subscriptions.html', context)

@login_required
def view_subscription_grade(request, pk):
    instance = SubscriptionGrade.objects.get(pk=pk, is_deleted=False)

    context = {
        'instance': instance,
        'page_name' : 'View Subscription Grade'
    }
    return render(request, 'payments/subscription_grade_view.html', context)


@login_required
def create_subscription_grade(request, pk):
    """
    create and update operation of subscription grade
    :param request:
    :param pk:
    :return:
    """
    # check pk for getting instance
    if pk:
        instance = get_object_or_404(SubscriptionGrade, pk=pk)
    else:
        instance = ''

    message = ''
    if request.method == 'POST':
        # if instance go to edit
        if instance:
            form = SubscriptionGradeForm(request.POST, instance=instance)
        else:
            form = SubscriptionGradeForm(request.POST)
            
        if form.is_valid():
            data = form.save(commit=False)
            if not instance:
                data.auto_id = get_auto_id(SubscriptionGrade)
                data.creator = request.user
            else:
                data.date_updated = datetime.datetime.today()
            data.updater = request.user
            data.save()

            return redirect(reverse('payments:subscription_grade'))

        else:
            message = "Form Validation Error"

    if instance:
        form = SubscriptionGradeForm(instance=instance)
    else:
        form = SubscriptionGradeForm()

    context = {
        'form': form,
        'message': message,
        'page_name' : 'Create Subscription Grade',
        'is_need_datetime_picker' : True,
    }

    return render(request, 'creates/create.html', context)


@login_required
def delete_subscription_grade(request, pk):
    """
    subscription grade deletion, it only mark as is deleted field to true
    :param request:
    :param pk:
    :return:
    """
    SubscriptionGrade.objects.filter(pk=pk).update(is_deleted=True)

    return redirect(reverse('payments:subscription_grades'))

@login_required
def create_subscription_grade_fee(request, pk, sub_pk):
    """
    create and update operation of subscription grade fee
    :param request:
    :param pk sub_pk(subscription pk):
    :return:
    """
    # check pk for getting instance
    if pk:
        instance = get_object_or_404(SubscriptionGradeFee, pk=pk)
    else:
        instance = ''
        
    if sub_pk:
        sub_instance = get_object_or_404(SubscriptionGrade, pk=sub_pk)
    else:
        sub_instance = ''

    message = ''
    if request.method == 'POST':
        # if instance go to edit
        if instance:
            form = SubscriptionGradeFeeForm(request.POST, instance=instance)
        else:
            form = SubscriptionGradeFeeForm(request.POST)
            
        if form.is_valid():
            data = form.save(commit=False)
            if not instance:
                data.auto_id = get_auto_id(SubscriptionGradeFee)
                data.creator = request.user
                data.subscription_grade = sub_instance
            else:
                data.date_updated = datetime.datetime.today()
            data.updater = request.user
            data.save()

            return redirect(reverse('payments:view_subscription_grade', kwargs={'pk': sub_pk}))
        
        else:
            message = "Form Validation Error"

    if instance:
        form = SubscriptionGradeFeeForm(instance=instance)
    else:
        form = SubscriptionGradeFeeForm()

    context = {
        'form': form,
        'message': message,
        'page_name' : 'Create Subscription Grade fee',
        'is_need_datetime_picker' : True,
    }

    return render(request, 'creates/create.html', context)


@login_required
def delete_subscription_grade_fee(request, pk):
    """
    subscription grade fee deletion, it only mark as is deleted field to true
    :param request:
    :param pk:
    :return:
    """
    instance = SubscriptionGradeFee.objects.get(pk=pk)
    instance.is_deleted=True
    instance.save()

    return redirect(reverse('payments:view_subscription_grade', kwargs={'pk': instance.subscription_grade.pk}))
    

@login_required
def create_student_subscription(request, pk, sub_pk):
    """
    create and update operation of student subscription
    :param request:
    :param pk sub_pk(subscription grade fee pk):                                
    :return:
    """
    # check pk for getting instance
    if pk:
        instance = get_object_or_404(StudentSubscription, pk=pk)
    else:
        instance = ''
        
    if sub_pk:
        sub_instance = get_object_or_404(SubscriptionGrade, pk=sub_pk)
    else:
        sub_instance = ''

    message = ''
    if request.method == 'POST':
        # if instance go to edit
        if instance:
            form = StudentSubscriptionForm(request.POST, instance=instance)
        else:
            form = StudentSubscriptionForm(request.POST)
            
        if form.is_valid():
            data = form.save(commit=False)
            if not instance:
                data.auto_id = get_auto_id(StudentSubscription)
                data.creator = request.user
            else:
                data.date_updated = datetime.datetime.today()
            data.subscribed_date = datetime.datetime.now()
            data.updater = request.user
            data.save()

            return redirect(reverse('payments:view_subscription_grade', kwargs={'pk': sub_pk}))
        
        else:
            message = "Form Validation Error"

    if instance:
        form = StudentSubscriptionForm(instance=instance)
    else:
        form = StudentSubscriptionForm()

    context = {
        'form': form,
        'message': message,
        'page_name' : 'Create Student Subscription',
        'is_need_datetime_picker' : True,
    }

    return render(request, 'creates/create.html', context)