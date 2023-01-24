from django.db import models

from learn.models import Grade, GradeBatch, Subject
from main.models import BaseModel
from users.models import Profile

# Create your models here.

EXAM_TYPE = (
    ("quarterly", "Quarterly"),
    ("half_yearly", "Half_yearly"),
    ("annual", "Annual"),
)

QUESTION_TYPE = (
    ("objective", "Objective"),
    ("attachment", "Attachment"),
    ("descriptive", "Descriptive"),
    ("descriptive_or_file", "Descriptive or file"),
)

CORRECT_OPTION = (
    ("option_a", "Option A"),
    ("option_b", "Option B"),
    ("option_c", "Option C"),
    ("option_d", "Option D"),
)
 
class Exam(BaseModel):
    subject = models.ForeignKey(Subject, limit_choices_to={'is_deleted': False},on_delete=models.CASCADE)
    exam_date = models.DateField()
    exam_type = models.CharField(max_length=50,choices=EXAM_TYPE)
    grade_batch = models.ForeignKey(GradeBatch,limit_choices_to={'is_deleted': False},on_delete=models.CASCADE)
    time_allotted = models.IntegerField()
    total_mark = models.IntegerField()
    total_questions = models.IntegerField()

    class Meta:
        verbose_name = ('Exam')
        verbose_name_plural = ('Exams')
        ordering = ('exam_date',)
        

    def __str__(self):
        return f'{self.subject.name} - {self.exam_date}'

class Questions(BaseModel):
    exam = models.ForeignKey(Exam, limit_choices_to={'is_deleted': False},on_delete=models.CASCADE)
    question_type = models.CharField(choices=QUESTION_TYPE,max_length=50)
    question = models.CharField(max_length=200)
    attachment = models.FileField(null=True,blank=True,upload_to ='question')
    option_a = models.CharField(null=True,blank=True,max_length=100)
    option_b = models.CharField(null=True,blank=True,max_length=100)
    option_c = models.CharField(null=True,blank=True,max_length=100)
    option_d = models.CharField(null=True,blank=True,max_length=100)
    correct_option = models.CharField(null=True,blank=True,choices=CORRECT_OPTION,max_length=100)

    class Meta:
        verbose_name = ('question')
        verbose_name_plural = ('questions')
        ordering = ('-id',)

    def __str__(self):
        return f'{self.exam.subject} - {self.question}'
 
class StudentExam(BaseModel):
    exam = models.ForeignKey(Exam, limit_choices_to={'is_deleted': False},on_delete=models.CASCADE)
    student = models.ForeignKey(Profile,limit_choices_to={'is_deleted': False},on_delete=models.CASCADE)
    score_obtained = models.IntegerField(null=True,blank=True)
    objective_score = models.IntegerField(null=True,blank=True)
    descriptive_score = models.IntegerField(null=True,blank=True)
    is_completed = models.BooleanField(default=False)

    class Meta:
        verbose_name = ('student exam')
        verbose_name_plural = ('student exams')

    def __unicode__(self):
        return self.pk

class StudentEnrolledExam(BaseModel):
    student = models.ForeignKey(Profile,limit_choices_to={'is_deleted': False},on_delete=models.CASCADE)
    student_exam = models.ForeignKey(Exam, limit_choices_to={'is_deleted': False},on_delete=models.CASCADE)
    question = models.ForeignKey(Questions,limit_choices_to={'is_deleted': False},on_delete=models.CASCADE)
    attachment = models.FileField(null=True,blank=True,upload_to ='student_encrolled_exam')
    selected_option = models.CharField(null=True,blank=True,max_length=200)
    descriptive_answer = models.TextField(null=True,blank=True)

    class Meta:
        verbose_name = ('student endrolled exam')
        verbose_name_plural = ('student endrolled exams')

    def __unicode__(self):
        return self.pk