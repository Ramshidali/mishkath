import datetime
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from exam.forms import ExamForm, ExamQuestionForm, ExamQuestionWithoutExamForm

from exam.models import *
from main.functions import get_auto_id


# Create your views here.

@login_required
def exams(request):
    instances = Exam.objects.filter(is_deleted=False).order_by("-id")
    
    query = request.GET.get('q')
    if query :
        if query in 'quarterly':
            instances = Exam.objects.filter(is_deleted=False,exam_type='quarterly').order_by("-id")
        elif query in 'half_yearly':
            instances = Exam.objects.filter(is_deleted=False,exam_type='half_yearly').order_by("-id")
        elif query in 'annual':
            instances = Exam.objects.filter(is_deleted=False,exam_type='annual').order_by("-id")
                
    context = {
        'instances' : instances,
        'page_name' : 'Exams', 
    }
    return render(request, 'exam/exams.html',context)


@login_required
def create_exam(request, pk):
    """
    create and update operation of exam
    :param request:
    :param pk:
    :return:
    """
    # check pk for getting instance
    if pk:
        instance = get_object_or_404(Exam, pk=pk)
    else:
        instance = ''

    message = ''
    if request.method == 'POST':
        # if instance go to edit
        if instance:
            form = ExamForm(request.POST, instance=instance)
        else:
            form = ExamForm(request.POST)
            
        if form.is_valid():
            data = form.save(commit=False)
            if not instance:
                data.auto_id = get_auto_id(Exam)
                data.creator = request.user
            else:
                data.date_updated = datetime.datetime.today()
            data.updater = request.user
            data.save()

            return redirect(reverse('exam:exams'))

        else:
            message = "Form Validation Error"

    if instance:
        form = ExamForm(instance=instance)
    else:
        form = ExamForm()

    context = {
        'form': form,
        'message': message,
        'page_name' : 'Create Exam',
    }
    
    return render(request, 'creates/create.html',context)

@login_required
def delete_exam(request, pk):
    """
    exam deletion, it only mark as is deleted field to true
    :param request:
    :param pk:
    :return:
    """
    Exam.objects.filter(pk=pk).update(is_deleted=True)

    return redirect(reverse('exam:exams'))

@login_required
def exam_questions(request):
    """
    question view, it only view single page of question
    :param request:
    :param pk:
    :return:
    """
    question_instances = Questions.objects.filter(is_deleted=False)
    
    context = {
        'exam_questions' : question_instances,
        'is_need_resize_cards' :True,  
    }    
    return render(request, 'exam/exam_questions.html',context)

@login_required
def view_exam(request,pk):
    """
    exam view, it a single view of exam
    :param request:
    :param pk:
    :return:
    """
    exam_instances = Exam.objects.get(pk=pk,is_deleted=False)
    
    context = {
        'exam_instances' : exam_instances,
        'is_need_resize_cards' :True,  
    }    
    return render(request, 'exam/view_exam.html',context)

@login_required
def create_exam_question(request,pk):
    """
    exam questions, it working for create and update questions in exam from sidebar and question page
    :param request:
    :param pk:
    :return:
    """
    redirect_page = request.GET.get('redirect_to')
    if pk:
        instance = get_object_or_404(Questions, pk=pk)
    else:
        instance = ''

    message = ''
    if request.method == 'POST':
        if instance:
            form = ExamQuestionForm(request.POST,instance=instance,files=request.FILES)
        else:
            form = ExamQuestionForm(request.POST,files=request.FILES)
                
        if form.is_valid():
            data = form.save(commit=False)
            if not instance:
                data.auto_id = get_auto_id(Questions)
                data.creator = request.user
            else:
                data.date_updated = datetime.datetime.today()
            data.updater = request.user
            data.save()
            
            if redirect_page != 'view_exam':
                return redirect(reverse('exam:exam_questions'))
            else:
                return redirect(reverse('exam:exam_questions'))
        else:
            message = "Form Validation Error"

    if instance:
        form = ExamQuestionForm(instance=instance)
    else:
        form = ExamQuestionForm()

    context = {
        'form' : form,
        'instance' : instance,
        'message' : message,
    }

    return render(request, 'creates/create_exam_question.html', context)

@login_required
def create_exam_question_without_exam(request,exam_pk):
    """
    exam questions, it working for create questions in exam from exams single page
    :param request:
    :param exam_pk:
    :return:
    """
    redirect_page = request.GET.get('redirect_to')
    if exam_pk:
        exam_instance = get_object_or_404(Exam, pk=exam_pk)
    else:
        exam_instance = ''

    message = ''
    if request.method == 'POST':

        form = ExamQuestionWithoutExamForm(request.POST,files=request.FILES)
                
        if form.is_valid():
            data = form.save(commit=False)
            data.auto_id = get_auto_id(Questions)
            data.creator = request.user
            data.exam = exam_instance
            data.date_updated = datetime.datetime.today()
            data.updater = request.user
            data.save()
            
            return redirect(reverse('exam:view_exam',kwargs={'pk':exam_instance.pk}))
        
        else:
            message = "Form Validation Error"


    form = ExamQuestionWithoutExamForm()

    context = {
        'form' : form,
        'message' : message,
        "url": reverse('exam:create_exam_question_without_exam',kwargs={'exam_pk':exam_pk}),
    }

    return render(request, 'creates/create_exam_question.html', context)

@login_required
def update_exam_question_without_exam(request,pk):
    """
    exam questions, it working for update questions in exam from exams single page
    :param request:
    :param pk:
    :return:
    """
    redirect_page = request.GET.get('redirect_to')
    instance = get_object_or_404(Questions, pk=pk)
        
    message = ''
    if request.method == 'POST':
        form = ExamQuestionWithoutExamForm(request.POST,instance=instance,files=request.FILES)
                        
        if form.is_valid():
            data = form.save(commit=False)
            data.date_updated = datetime.datetime.today()
            data.updater = request.user
            data.save()
            
            return redirect(reverse('exam:view_exam',kwargs={'pk':instance.exam.pk}))
        
        else:
            message = "Form Validation Error"
    else:

        form = ExamQuestionWithoutExamForm(instance=instance)

        context = {
            'form' : form,
            'instance' : instance,
            'message' : message,
            "url": reverse('exam:update_exam_question_without_exam',kwargs={'pk':pk}),
        }

        return render(request, 'creates/create_exam_question.html', context)


@login_required
def delete_exam_question(request,pk):
    redirect_page = request.GET.get('redirect_to')
    instance = Questions.objects.get(pk=pk)
    instance.is_deleted=True
    instance.save()
    
    if redirect_page == 'view_exam':
        return redirect(reverse('exam:view_exam',kwargs={'pk':instance.exam.pk}))