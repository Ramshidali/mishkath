import os
import uuid
from django.db import models
from django.db.models.deletion import CASCADE
from main.models import BaseModel
from versatileimagefield.fields import VersatileImageField


def get_grade_video_file_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (instance.pk, ext)
    return os.path.join('videos/e-learning/grade', filename)


def get_topic_video_file_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (instance.pk, ext)
    return os.path.join('videos/e-learning/lesson-topics', filename)



# Create your models here.

class Batch(BaseModel):
    title = models.CharField(max_length=20)
    from_date = models.DateField(blank=True)
    to_date = models.DateField(blank=True)
    is_active = models.BooleanField(null=False)

    def __str__(self):
        return self.title


#grade means class
class Grade(BaseModel):
    name = models.CharField(max_length=128)
    image = VersatileImageField('Image', upload_to="lern/grade", blank=True, null=True)
    description = models.TextField(blank=True,null=True)
    qualification = models.PositiveIntegerField()
        
    class Meta:
        db_table = 'learn_grade'
        verbose_name = ('Grade')
        verbose_name_plural = ('Grade')

    def __str__(self):
        return self.name


class Subject(BaseModel):
    grade = models.ForeignKey(Grade,limit_choices_to={'is_deleted': False},on_delete=models.CASCADE)
    name = models.CharField(max_length=128)
    image = VersatileImageField('Image', upload_to="learn/subject", blank=True, null=True)
    description = models.TextField(blank=True,null=True)
    duration = models.IntegerField()
    
    class Meta:
        db_table = 'learn_subject'
        verbose_name = ('subject')
        verbose_name_plural = ('subjects')

    def __str__(self):
        return self.name


class Lesson(BaseModel):
    subject = models.ForeignKey(Subject,limit_choices_to={'is_deleted': False},on_delete=models.CASCADE)
    name = models.CharField(max_length=128)
    image = VersatileImageField('Image', upload_to="learn/lesson", blank=True, null=True)
    description = models.TextField(blank=True,null=True)
    
    
    class Meta:
        db_table = 'learn_lesson'
        verbose_name = ('lesson')
        verbose_name_plural = ('lessons')
 
    def __str__(self):
        return self.name


class Topic(BaseModel):
    lesson = models.ForeignKey(Lesson,limit_choices_to={'is_deleted': False},on_delete=models.CASCADE)
    name = models.CharField(max_length=128)
    image = VersatileImageField('Image', upload_to="learn/topic", blank=True, null=True)
    description = models.TextField(blank=True,null=True)
    duration = models.FloatField(default=0.00)

    video = models.FileField(upload_to=get_topic_video_file_path)
    is_processed = models.BooleanField(default=False)
    playlist = models.CharField(max_length=2083, blank=True, null=True)
    attachment = models.FileField(upload_to="learn/topic-assets", blank=True, null=True)

    class Meta:
        db_table = 'topic_learn'
        verbose_name = ('topic')
        verbose_name_plural = ('topics')

    def __str__(self):
        return self.name 


class GradeBatch(BaseModel):
    grade = models.ForeignKey(Grade,limit_choices_to={'is_deleted': False},on_delete=models.CASCADE)
    batch = models.ForeignKey(Batch,limit_choices_to={'is_deleted': False},on_delete=models.CASCADE)
    unlocked_topic =  models.ManyToManyField(Topic,null=True,blank=True)
        
    class Meta:
        db_table = 'grade_data'
        verbose_name = ('Grade Batch')
        verbose_name_plural = ('Grade Batch')

    def __str__(self):
        return f'{self.batch} batch in {self.grade}' 


class StudentEnrollGrade(BaseModel):
    grade = models.ForeignKey(Grade,limit_choices_to={'is_deleted': False},on_delete=models.CASCADE)
    student_id = models.ForeignKey("users.Profile",limit_choices_to={'is_deleted': False},on_delete=models.CASCADE)
    is_completed = models.BooleanField(default=False)
    is_new_content = models.BooleanField(default=False)

    class Meta:
        db_table = 'learn_student_enroll_grade'
        verbose_name = ('Enroll Course')
        verbose_name_plural = ('Enroll Courses')
        ordering = ('grade',)
        
    def __str__(self):
        
        return str(self.grade)


class StudentEnrollSubject(BaseModel):
    subject = models.ForeignKey(Subject,limit_choices_to={'is_deleted': False},on_delete=models.CASCADE)
    student_id = models.ForeignKey("users.Profile",limit_choices_to={'is_deleted': False},on_delete=models.CASCADE)

    is_completed = models.BooleanField(default=False)
    is_new_content = models.BooleanField(default=False)

    class Meta:
        db_table = 'learn_student_enroll_subject'
        verbose_name = ('Enroll subject')
        verbose_name_plural = ('Enroll subjects')
        ordering = ('subject',)
        
    def __str__(self):
        return str(self.id)


class StudentEnrollLesson(BaseModel):
    lesson = models.ForeignKey(Lesson,limit_choices_to={'is_deleted': False},on_delete=models.CASCADE)
    student_id = models.ForeignKey("users.Profile",limit_choices_to={'is_deleted': False},on_delete=models.CASCADE)

    is_completed = models.BooleanField(default=False)
    is_new_content = models.BooleanField(default=False)

    class Meta:
        db_table = 'learn_student_enroll_lesson'
        verbose_name = ('Enroll lesson')
        verbose_name_plural = ('Enroll lessons')
        ordering = ('lesson',)
        
    def __str__(self): 
        return str(self.id)
    
class StudentEnrolledLesson(BaseModel):
    subject = models.ForeignKey(Subject,limit_choices_to={'is_deleted': False},on_delete=models.CASCADE)
    student = models.ForeignKey("users.Profile",limit_choices_to={'is_deleted': False},on_delete=models.CASCADE)  
    topic = models.ForeignKey(Topic,limit_choices_to={'is_deleted': False},on_delete=models.CASCADE)    
    lesson = models.ForeignKey(Lesson, limit_choices_to={'is_deleted': False},on_delete=models.CASCADE)
    grade_batch = models.ForeignKey(GradeBatch, on_delete=CASCADE)

    def __str__(self):
        return str(self.id)


class StudentTopic(BaseModel):
    topic = models.ForeignKey(Topic,limit_choices_to={'is_deleted': False},on_delete=models.CASCADE)
    student_id = models.ForeignKey("users.Profile",limit_choices_to={'is_deleted': False},on_delete=models.CASCADE)

    is_completed = models.BooleanField(default=False)
    is_new_content = models.BooleanField(default=False)
    has_access = models.BooleanField(default=False)

    class Meta:
        db_table = 'learn_student_topic'
        verbose_name = ('Student topic')
        verbose_name_plural = ('Student topics')
        ordering = ('topic',)

    def __str__(self):
        return self.topic.name


class UpcomingActivity(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    auto_id = models.PositiveIntegerField(db_index=True,unique=True)
    date_added = models.DateTimeField(db_index=True,auto_now_add=True)
    student_id = models.ForeignKey("users.Profile", limit_choices_to={'is_deleted': False},on_delete=models.CASCADE)

    lesson_topic = models.ForeignKey(Topic,on_delete=models.CASCADE, null=True, blank=True)
    activity_type = models.CharField(max_length=128, null=True, blank=True)

    class Meta:
        db_table = 'learn_upcoming_activity'
        verbose_name = ('Upcoming Activity')
        verbose_name_plural = ('Upcoming Activities')
        ordering = ('auto_id', 'student_id')

    def __str__(self):
        return str(self.id)


class BatchEnrolledLesson(BaseModel):
    subjects = models.ForeignKey(Subject, limit_choices_to={'is_deleted': False},on_delete=models.CASCADE)
    student = models.ForeignKey("users.Profile", limit_choices_to={'is_deleted': False},on_delete=models.CASCADE)  
    topic = models.ForeignKey(Topic, limit_choices_to={'is_deleted': False},on_delete=models.CASCADE)    
    lesson = models.ForeignKey(Lesson, limit_choices_to={'is_deleted': False},on_delete=models.CASCADE)
    grade_batch = models.ForeignKey(GradeBatch, limit_choices_to={'is_deleted': False},on_delete=models.CASCADE)


    def __str__(self):
        return str(self.id)
   
class BatchStudentPractise(BaseModel):
    subjects = models.ForeignKey(Subject, limit_choices_to={'is_deleted': False},on_delete=models.CASCADE)
    batch = models.ForeignKey(Batch, limit_choices_to={'is_deleted': False},on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id)
    
    
class BatchExam(BaseModel):
    exam_currently = models.CharField(max_length=10)
    batch = models.ForeignKey(Batch,limit_choices_to={'is_deleted': False},on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id)


class UpCommingLiveClasses(BaseModel):
    topic = models.ForeignKey(Topic,limit_choices_to={'is_deleted': False},on_delete=models.CASCADE)
    batch = models.ForeignKey(Batch,limit_choices_to={'is_deleted': False},on_delete=models.CASCADE)
    zoom_id = models.CharField(max_length=256, null=True, blank=True)
    class_date = models.DateField(null=True, blank=True)
    class_time = models.TimeField(null=True, blank=True)
    
    class Meta:
        db_table = 'learn_upcoming_classes'
        verbose_name = ('Upcoming Classes')
        verbose_name_plural = ('Upcoming Classes')
        ordering = ('class_date', 'class_time')
    
    def __str__(self):
        return str(self.topic)



class Notifications(BaseModel):
    student_id = models.ForeignKey("users.Profile",limit_choices_to={'is_deleted': False},on_delete=models.CASCADE)
    batch = models.ForeignKey(Batch,limit_choices_to={'is_deleted': False},on_delete=models.CASCADE)
    title = models.CharField(max_length=256, null=True, blank=True)
    
    class Meta:
        db_table = 'learn_notifications'
        verbose_name = ('Learn Notifications')
        verbose_name_plural = ('Learn Notifications')
    
    def __str__(self):
        return str(self.title)
    
