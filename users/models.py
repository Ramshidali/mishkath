# django
import uuid
from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext_lazy as _
# from learn.models import Batch
# local
from main.models import BaseModel, Country, Courses


GENDER_CHOICE = (
    ("male", "male"),
    ("female", "female"),
)

MISHKATH_AD_CHOICE = (
    ("social_media", "social_media"),
    ("tv", "tv"),
    ("newspaper", "newspaper"),
    ("other", "other"),
)

PREFERED_MEDIUM_CHOICES = (
    ("english", "english"),
    ("malayalam", "malayalam"),
)

INTERVIEW_STATUS = (
    ("pending", "pending"),
    ("allotted", "allotted"),
    ("passed", "passed"),
)


class TemporaryProfile(models.Model):
    name = models.CharField(max_length=100,null=True,blank=True)
    dob = models.DateField(null=True,blank=True)
    phone = models.CharField(max_length=15,null=True,blank=True)
    gender = models.CharField(choices=GENDER_CHOICE, max_length=100,null=True,blank=True)
    email = models.EmailField(null=True,blank=True)
    nationality = models.ForeignKey(Country, limit_choices_to={'is_deleted': False},on_delete=models.CASCADE,null=True,blank=True)
    country_of_residense = models.CharField(max_length=100,null=True,blank=True)
    permanent_address = models.TextField(max_length=100,null=True,blank=True)
    current_address = models.TextField(max_length=100,null=True,blank=True)
    fathers_name = models.CharField(max_length=100,null=True,blank=True)
    fathers_phone = models.CharField(max_length=12,null=True,blank=True)
    mothers_name = models.CharField(max_length=100,null=True,blank=True)
    mothers_phone = models.CharField(max_length=12,null=True,blank=True)
    mishkath_ad = models.CharField(choices=MISHKATH_AD_CHOICE, max_length=100,null=True,blank=True)
    mishkath_ad_message = models.CharField(max_length=100,null=True,blank=True)
    interested_course = models.ForeignKey(Courses, limit_choices_to={'is_deleted': False},on_delete=models.CASCADE,null=True,blank=True)
    prefered_medium = models.CharField(choices=PREFERED_MEDIUM_CHOICES, max_length=100,null=True,blank=True)


    def __str__(self):
        return self.name


class Profile(BaseModel):
    user = models.OneToOneField(User, limit_choices_to={'is_deleted': False},on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    dob = models.DateField()
    phone = models.CharField(max_length=15)
    gender = models.CharField(choices=GENDER_CHOICE, max_length=100)
    email = models.EmailField()
    nationality = models.ForeignKey(Country, limit_choices_to={'is_deleted': False},on_delete=models.CASCADE)
    country_of_residense = models.CharField(max_length=100)
    permanent_address = models.TextField(max_length=100)
    current_address = models.TextField(max_length=100)
    fathers_name = models.CharField(max_length=100)
    fathers_phone = models.CharField(max_length=12)
    mothers_name = models.CharField(max_length=100)
    mothers_phone = models.CharField(max_length=12)
    mishkath_ad = models.CharField(choices=MISHKATH_AD_CHOICE, max_length=100)
    mishkath_ad_message = models.CharField(max_length=100,null=True,blank=True)
    interested_course = models.ForeignKey(Courses, limit_choices_to={'is_deleted': False},on_delete=models.CASCADE)
    prefered_medium = models.CharField(choices=PREFERED_MEDIUM_CHOICES, max_length=100)
    grade_batch = models.ForeignKey('learn.GradeBatch', limit_choices_to={'is_deleted': False},on_delete=models.CASCADE,null=True,blank=True)

    class Meta:
        verbose_name = _('student profile')
        verbose_name_plural = _('students profile')

    def __str__(self):
        return f'{self.auto_id} - {self.name}'


class OtpRecord(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    phone = models.CharField(max_length=16)
    otp = models.IntegerField()
    country = models.ForeignKey(Country, limit_choices_to={'is_deleted': False},on_delete=models.CASCADE,null=True,blank=True)
    attempts = models.PositiveIntegerField(default=1)
    password = models.CharField(max_length=256, null=True, blank=True)

    class Meta:
        verbose_name = _('Otp Record')
        verbose_name_plural = _('Otp Records')

    def __str__(self):
        return f'{self.phone} - {self.otp}'



class InterviewStatus(BaseModel):
    profile = models.ForeignKey(Profile, limit_choices_to={'is_deleted': False},on_delete=models.CASCADE)
    status = models.CharField(choices=INTERVIEW_STATUS, max_length=100)
    zoom_id = models.CharField(max_length=256, null=True, blank=True)
    interview_date = models.DateField(null=True, blank=True)
    interview_time = models.TimeField(null=True, blank=True)

    def __str__(self):
        return self.profile.name