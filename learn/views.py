from dal import autocomplete
import datetime
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from learn.forms import BatchesForm, ClassForm, CountryForm, CoursesForm, GradeBatchForm, LessonFormWithSubject, \
    LessonFormWithoutSubject, SubjectsForm, TopicFormWithLesson, TopicFormWithoutLesson, UpCommingLiveClassesForm
from learn.models import Batch, Grade, GradeBatch, Lesson, Subject, Topic, UpCommingLiveClasses
from main.functions import get_auto_id
from main.models import Country, Courses


class UnlockedTopicsAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self, *args, **kwargs):
        items = Topic.objects.filter(is_deleted=False)
        if self.q:
            items = items.filter(Q(name__istartswith=self.q))
        else:
            pass
        return items


@login_required
def batches(request):
    """
    student batches listings, eg:- night batch, morning batch etc
    :param request:
    :return: batch list view
    """
    instances = Batch.objects.filter(is_deleted=False).order_by("-id")

    context = {
        'instances': instances,
        'page_name' : 'Batches'
    }
    return render(request, 'learn/batches.html', context)


@login_required
def create_batch(request, pk):
    """
    create and update operation of batches
    :param request:
    :param pk:
    :return:
    """
    # check pk for getting instance
    if pk:
        instance = get_object_or_404(Batch, pk=pk)
    else:
        instance = ''

    message = ''
    if request.method == 'POST':
        # if instance go to edit
        if instance:
            form = BatchesForm(request.POST, instance=instance)
        else:
            form = BatchesForm(request.POST)
            
        if form.is_valid():
            data = form.save(commit=False)
            if not instance:
                data.auto_id = get_auto_id(Batch)
                data.creator = request.user
            else:
                data.date_updated = datetime.datetime.today()
            data.updater = request.user
            data.save()

            return redirect(reverse('learn:batches'))

        else:
            message = "Form Validation Error"
            print(message)

    if instance:
        form = BatchesForm(instance=instance)
    else:
        form = BatchesForm()

    context = {
        'form': form,
        'message': message,
        'page_name' : 'Create Batch',
        'is_need_datetime_picker' : True,
    }

    return render(request, 'creates/create.html', context)


@login_required
def delete_batch(request, pk):
    """
    batch deletion, it only mark as is deleted field to true
    :param request:
    :param pk:
    :return:
    """
    Batch.objects.filter(pk=pk).update(is_deleted=True)

    return redirect(reverse('learn:batches'))


@login_required
def grades(request):
    instances = Grade.objects.filter(is_deleted=False).order_by("-id")

    context = {
        'instances': instances,
        'page_name' : 'Grades'
    }
    return render(request, 'learn/grade.html', context)


@login_required
def create_grade(request, pk):
    """
    creation of class eg:- 1, 2, +2, etcc
    :param request:
    :param pk:
    :return:
    """
    if pk:
        instance = get_object_or_404(Grade, pk=pk)
    else:
        instance = ''

    message = ''
    if request.method == 'POST':
        if instance:
            form = ClassForm(request.POST, instance=instance,files=request.FILES)
        else:
            form = ClassForm(request.POST,files=request.FILES)

        if form.is_valid():
            data = form.save(commit=False)
            if not instance:
                data.auto_id = get_auto_id(Grade)
                data.creator = request.user
            else:
                data.date_updated = datetime.datetime.today()
            data.updater = request.user
            data.save()

            return redirect(reverse('learn:grades'))

        else:
            message = "Form Validation Error"

    if instance:
        form = ClassForm(instance=instance)
    else:
        form = ClassForm()

    context = {
        'form': form,
        'message': message,
        'instance': instance,
        'is_need_select2': True,
        'is_need_forms': True,
        'page_name' : 'Create Grade'
    }

    return render(request, 'creates/create.html', context)


@login_required
def delete_grade(request, pk):
    """
    mark grade as deleted
    :param request:
    :param pk:
    :return:
    """
    Grade.objects.filter(pk=pk).update(is_deleted=True)

    return redirect(reverse('learn:grades'))


@login_required
def grade_batch(request):
    """
    combination of grade and batch
    :param request:
    :return:
    """
    instances = GradeBatch.objects.filter(is_deleted=False).order_by("-id")

    context = {
        'instances': instances,
        'page_name' : 'Grade Batch'
    }
    return render(request, 'learn/grade_batch.html', context)


@login_required
def create_grade_batch(request):
    """
    creation of grade batch
    :param request:
    :return:
    """
    message = ''
    
    if request.method == 'POST':

        form = GradeBatchForm(request.POST)

        if form.is_valid():
            data = form.save(commit=False)
            unlocked_topics = request.POST.getlist('unlocked_topic')
            # print("Un locked topics ", unlocked_topics)
            data.auto_id = get_auto_id(GradeBatch)
            data.creator = request.user
            data.updater = request.user
            data.save()

            message = f"The data is {data.pk}"
            instance = GradeBatch.objects.get(pk=data.pk)

            # save many_to_many unlocked topics instance
            for i in unlocked_topics:
                instance.unlocked_topic.add(i)

            instance.save()
            return redirect(reverse('learn:grade_batch'))

        else:
            message = "Form Validation Error"
    else:
        form = GradeBatchForm()

        context = {
            'form': form,
            'message': message,
            "is_need_forms": True,
            'is_need_select2': True,
            'page_name' : 'Create Grade Batch',

        }

    return render(request, 'creates/create.html', context)


@login_required
def update_grade_batch(request, pk):
    """
    edit of grade batch
    :param request:
    :param pk:
    :return:
    """
    message = ""
    instance = get_object_or_404(GradeBatch, pk=pk)
    if request.method == 'POST':
        if instance:
            form = GradeBatchForm(request.POST, instance=instance)
            # instance.unlocked_topic.clear()
            # instance.save()s

        if form.is_valid():
            data = form.save(commit=False)
            unlocked_topics = request.POST.getlist('unlocked_topic')

            if not instance:
                # print("srting.....")
                data.auto_id = get_auto_id(GradeBatch)
                data.creator = request.user
                data.updater = request.user
                data.save()
                temp_instance = get_object_or_404(GradeBatch, pk=data.pk)
                # print("Temp instance===>>",data)

            else:
                data.date_updated = datetime.datetime.today()
                # print("Type of unlocked ==>>", type(unlocked_topics))

                # clear all existing topics and saves to field
                instance.unlocked_topic.clear()
                for i in unlocked_topics:
                    instance.unlocked_topic.add(i)

                instance.save()

                data.updater = request.user
                data.save()
            # print("test data ---------------", data.pk)

            message = "Success"

            return redirect(reverse('learn:grade_batch'))

        else:
            message = "Form Validation Error"

    #     print("Message------------------------------: ", message)
    # print("Message-----------------------------ffgerf43-: ", message)
    form = GradeBatchForm(instance=instance)

    context = {
        'form': form,
        'message': message,
        'instance': instance,
        'page_name' : 'Create Grade Batch'
    }

    return render(request, 'creates/create.html', context)


@login_required
def delete_grade_batch(request, pk):
    GradeBatch.objects.filter(pk=pk).update(is_deleted=True)

    return redirect(reverse('learn:grade_batch'))


@login_required
def country(request):
    instances = Country.objects.filter(is_deleted=False).order_by("-id")

    context = {
        'instances': instances,
        'page_name' : 'Country'
    }
    return render(request, 'general/country.html', context)


@login_required
def create_country(request, pk):
    if pk:
        instance = get_object_or_404(Country, pk=pk)
    else:
        instance = ''

    message = ''
    if request.method == 'POST':
        if instance:
            form = CountryForm(request.POST, instance=instance)
        else:
            form = CountryForm(request.POST)

        if form.is_valid():
            data = form.save(commit=False)
            if not instance:
                data.auto_id = get_auto_id(Country)
                data.creator = request.user
            else:
                data.date_updated = datetime.datetime.today()
            data.updater = request.user
            data.save()

            return redirect(reverse('learn:country'))

        else:
            message = "Form Validation Error"

    if instance:
        form = CountryForm(instance=instance)
    else:
        form = CountryForm()

    context = {
        'form': form,
        'message': message,
        'instance': instance,
        'page_name' : 'Create Country'
    }

    return render(request, 'creates/create.html', context)


@login_required
def delete_country(request, pk):
    Country.objects.filter(pk=pk).update(is_deleted=True)

    return redirect(reverse('learn:country'))


@login_required
def courses(request):
    instances = Courses.objects.filter(is_deleted=False).order_by("-id")

    context = {
        'instances': instances,
        'page_name' : 'Courses'
    }
    return render(request, 'general/courses.html', context)


@login_required
def create_courses(request, pk):
    if pk:
        instance = get_object_or_404(Courses, pk=pk)
    else:
        instance = ''

    message = ''
    if request.method == 'POST':
        if instance:
            form = CoursesForm(request.POST, instance=instance)
        else:
            form = CoursesForm(request.POST)

        if form.is_valid():
            data = form.save(commit=False)
            if not instance:
                data.auto_id = get_auto_id(Courses)
                data.creator = request.user
            else:
                data.date_updated = datetime.datetime.today()
            data.updater = request.user
            data.save()

            return redirect(reverse('learn:courses'))

        else:
            message = "Form Validation Error"

    if instance:
        form = CoursesForm(instance=instance)
    else:
        form = CoursesForm()

    context = {
        'form': form,
        'message': message,
        'instance': instance,
        'page_name' : 'Create Courses'
    }

    return render(request, 'creates/create.html', context)


@login_required
def delete_courses(request, pk):
    Courses.objects.filter(pk=pk).update(is_deleted=True)

    return redirect(reverse('learn:courses'))


@login_required
def subjects(request):
    instances = Subject.objects.filter(is_deleted=False).order_by("-id")

    context = {
        'instances': instances,
        'page_name' : 'Subjects'
    }
    return render(request, 'learn/subjects.html', context)


@login_required
def view_subject(request, pk):
    subject_instance = Subject.objects.get(pk=pk, is_deleted=False)

    context = {
        'subject_instance': subject_instance,
        'page_name' : 'View Subject'
    }
    return render(request, 'learn/subject_view.html', context)


@login_required
def create_subjects(request, pk):
    if pk:
        instance = get_object_or_404(Subject, pk=pk)
    else:
        instance = ''

    message = ''
    if request.method == 'POST':
        if instance:
            form = SubjectsForm(request.POST, files=request.FILES, instance=instance)
        else:
            form = SubjectsForm(request.POST, files=request.FILES)

        if form.is_valid():
            data = form.save(commit=False)
            if not instance:
                data.auto_id = get_auto_id(Subject)
                data.creator = request.user
            else:
                data.date_updated = datetime.datetime.today()
            data.updater = request.user
            data.save()

            return redirect(reverse('learn:subjects'))

        else:
            message = "Form Validation Error"

    if instance:
        form = SubjectsForm(instance=instance)
    else:
        form = SubjectsForm()

    context = {
        'form': form,
        'message': message,
        'instance': instance,
        'page_name' : 'Create Subject'
    }

    return render(request, 'creates/create.html', context)


@login_required
def delete_subject(request, pk):
    Subject.objects.filter(pk=pk).update(is_deleted=True)

    return redirect(reverse('learn:subjects'))


@login_required
def lessons(request):
    lesson_instances = Lesson.objects.filter(is_deleted=False)

    context = {
        'lesson_instances': lesson_instances,
        'is_need_resize_cards': True,
        'page_name' : 'Lessons'
    }
    return render(request, 'learn/lessons.html', context)


@login_required
def view_lesson(request, pk):
    lesson_instance = Lesson.objects.get(is_deleted=False, pk=pk)

    context = {
        'lesson_instances': lesson_instance,
        'is_need_resize_cards': True,
        'page_name' : 'lesson'
    }
    return render(request, 'learn/view_lesson.html', context)


# this view working in side nav create button and edit is working in lessons page
@login_required
def create_lesson(request, pk):
    if pk:
        instance = get_object_or_404(Lesson, pk=pk)
    else:
        instance = ''

    message = ''
    if request.method == 'POST':
        if instance:
            form = LessonFormWithSubject(request.POST, files=request.FILES, instance=instance)
        else:
            form = LessonFormWithSubject(request.POST, files=request.FILES)

        if form.is_valid():
            data = form.save(commit=False)
            if not instance:
                data.auto_id = get_auto_id(Lesson)
                data.creator = request.user
            else:
                data.date_updated = datetime.datetime.today()
            data.updater = request.user
            data.save()

            return redirect(reverse('learn:lessons'))

        else:
            message = "Form Validation Error"

    if instance:
        form = LessonFormWithSubject(instance=instance)
    else:
        form = LessonFormWithSubject()

    context = {
        'form': form,
        'message': message,
        'instance': instance,
        'page_name' : 'Create Lesson'
        
    }

    return render(request, 'creates/create.html', context)


# this view working in subject page for creating lessons based on subject
@login_required
def create_lesson_with_subject(request, sub_pk):
    if sub_pk:
        sub_instance = Subject.objects.get(pk=sub_pk)
    else:
        sub_instance = ''

    message = ''
    if request.method == 'POST':
        form = LessonFormWithoutSubject(request.POST, files=request.FILES)

        if form.is_valid():
            data = form.save(commit=False)
            data.auto_id = get_auto_id(Lesson)
            data.creator = request.user

            if sub_instance:
                data.subject = sub_instance

            data.date_updated = datetime.datetime.today()
            data.updater = request.user
            data.save()

            return redirect(reverse('learn:view_subject', kwargs={'pk': sub_pk}))

        else:
            message = "Form Validation Error"

    form = LessonFormWithoutSubject()

    context = {
        'form': form,
        'message': message,
        'page_name' : 'create lesson'
    }

    return render(request, 'creates/create.html', context)


# this view working in subject page lesson for edit each lessons
@login_required
def edit_lesson(request, lesson_pk):
    lesson_instance = get_object_or_404(Lesson, pk=lesson_pk)
    message = ''
    if request.method == 'POST':
        form = LessonFormWithoutSubject(request.POST, files=request.FILES, instance=lesson_instance)

        if form.is_valid():
            data = form.save(commit=False)
            data.date_updated = datetime.datetime.today()
            data.updater = request.user
            data.save()

            return redirect(reverse('learn:view_subject', kwargs={'pk': lesson_instance.subject.pk}))

        else:
            message = "Form Validation Error"

    form = LessonFormWithoutSubject(instance=lesson_instance)

    context = {
        'form': form,
        'message': message,
        'instance': lesson_instance,
        'page_name' : 'edit lesson'
        
    }

    return render(request, 'creates/create.html', context)


# subject pk is using this view for redirect to subject view page if having subject pk or redirect to lesson page
@login_required
def delete_lesson(request, lesson_pk):
    redirect_page = request.GET.get('redirect_to')
    lesson_instance = get_object_or_404(Lesson, pk=lesson_pk)
    Lesson.objects.filter(pk=lesson_pk).update(is_deleted=True)

    if not 'subject' in redirect_page:
        return redirect(reverse('learn:lessons'))
    else:
        return redirect(reverse('learn:view_subject', kwargs={'pk': lesson_instance.subject.pk}))


@login_required
def topics(request):
    instances = Topic.objects.filter(is_deleted=False).order_by("id")

    context = {
        'instances': instances,
        "is_need_resize_cards": True,
        'page_name' : 'topics'
        
    }
    return render(request, 'learn/topics.html', context)


@login_required
def create_topic_with_lesson(request, lesson_pk):
    if lesson_pk:
        lesson_instance = Lesson.objects.get(pk=lesson_pk)
    else:
        lesson_instance = ''

    message = ''
    if request.method == 'POST':
        form = TopicFormWithoutLesson(request.POST, files=request.FILES)

        if form.is_valid():
            data = form.save(commit=False)
            data.auto_id = get_auto_id(Topic)
            data.creator = request.user

            if lesson_instance:
                data.lesson = lesson_instance

            data.date_updated = datetime.datetime.today()
            data.updater = request.user
            data.save()

            return redirect(reverse('learn:view_subject', kwargs={'pk': lesson_instance.subject.pk}))

        else:
            message = "Form Validation Error"

    form = TopicFormWithoutLesson()

    context = {
        'form': form,
        'message': message,
        'page_name' : 'create topic'
        
    }

    return render(request, 'creates/create.html', context)


@login_required
def create_topic(request, pk, sub_pk):
    redirect_page = request.GET.get('redirect_to')
    if sub_pk:
        sub_instance = Subject.objects.get(pk=sub_pk)
    else:
        sub_instance = ''
    if pk:
        instance = get_object_or_404(Topic, pk=pk)
    else:
        instance = ''

    message = ''
    if request.method == 'POST':
        if instance:
            form = TopicFormWithLesson(request.POST, instance=instance, files=request.FILES)
        else:
            form = TopicFormWithLesson(request.POST, files=request.FILES)

        if form.is_valid():
            data = form.save(commit=False)
            if not instance:
                data.auto_id = get_auto_id(Topic)
                data.creator = request.user
            else:
                data.date_updated = datetime.datetime.today()
            data.updater = request.user
            data.save()

            if 'topics' in redirect_page:
                return redirect(reverse('learn:topics'))
            elif 'lesson_topic' in redirect_page:
                return redirect(reverse('learn:view_lesson', kwargs={'pk': instance.lesson.pk}))
            else:
                return redirect(reverse('learn:view_subject', kwargs={'pk': instance.lesson.pk}))


        else:
            message = "Form Validation Error"

    if instance:
        form = TopicFormWithLesson(instance=instance)
    else:
        form = TopicFormWithLesson()

    context = {
        'form': form,
        'message': message,
        'instance': instance,
        'page_name' : 'create topic'
        
    }
    return render(request, 'creates/topic_create.html', context)


@login_required
def delete_topic(request, pk, sub_pk):
    redirect_page = request.GET.get('redirect_to')
    if sub_pk:
        sub_instance = Subject.objects.get(pk=sub_pk)
    else:
        sub_instance = ''
    instance = Topic.objects.filter(pk=pk).update(is_deleted=True)

    if 'topics' in redirect_page:
        return redirect(reverse('learn:topics'))
    elif 'lesson_topic' in redirect_page:
        return redirect(reverse('learn:view_lesson', kwargs={'pk': instance.lesson.pk}))
    else:
        return redirect(reverse('learn:view_subject', kwargs={'pk': instance.lesson.pk}))


@login_required
def upcomming_live_classes(request):
    instances = UpCommingLiveClasses.objects.filter(is_deleted=False).order_by("id")
    
    context = {
        'instances': instances,
        'page_name' : 'Up Comming Live Classes',
    }
    return render(request, 'learn/live_classes.html', context)

@login_required
def create_upcomming_live_classes(request, pk):
    if pk:
        instance = get_object_or_404(UpCommingLiveClasses, pk=pk)
    else:
        instance = ''

    message = ''
    if request.method == 'POST':
        if instance:
            form = UpCommingLiveClassesForm(request.POST, instance=instance, files=request.FILES)
        else:
            form = UpCommingLiveClassesForm(request.POST, files=request.FILES)

        if form.is_valid():
            data = form.save(commit=False)
            if not instance:
                data.auto_id = get_auto_id(Topic)
                data.creator = request.user
            else:
                data.date_updated = datetime.datetime.today()
            data.updater = request.user
            data.save()

            return redirect(reverse('learn:upcomming_live_classes'))


        else:
            message = "Form Validation Error"

    if instance:
        form = UpCommingLiveClassesForm(instance=instance)
    else:
        form = UpCommingLiveClassesForm()

    context = {
        'form': form,
        'message': message,
        'instance': instance,
        'is_need_datetime_picker' : True,
        'page_name' : 'create Up Comming Live Classes'
        
    }
    return render(request, 'creates/create.html', context)


# @login_required
# def delete_topic(request, pk, sub_pk):
#     redirect_page = request.GET.get('redirect_to')
#     if sub_pk:
#         sub_instance = Subject.objects.get(pk=sub_pk)
#     else:
#         sub_instance = ''
#     instance = Topic.objects.filter(pk=pk).update(is_deleted=True)

#     if 'topics' in redirect_page:
#         return redirect(reverse('learn:topics'))
#     elif 'lesson_topic' in redirect_page:
#         return redirect(reverse('learn:view_lesson', kwargs={'pk': instance.lesson.pk}))
#     else:
#         return redirect(reverse('learn:view_subject', kwargs={'pk': instance.lesson.pk}))

