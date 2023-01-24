import uuid

from django.db import models


class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    auto_id = models.PositiveIntegerField(db_index=True, unique=True)
    creator = models.ForeignKey(
        "auth.User", blank=True, related_name="creator_%(class)s_objects", on_delete=models.CASCADE)
    updater = models.ForeignKey("auth.User", blank=True, null=True,
                                related_name="updater_%(class)s_objects", on_delete=models.CASCADE)
    date_added = models.DateTimeField(db_index=True, auto_now_add=True)
    date_updated = models.DateTimeField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False)
    deleted_reason = models.CharField(max_length=128, blank=True, null=True)

    class Meta:
        abstract = True


class Country(BaseModel):
    name = models.CharField(max_length=100, null=True)
    country_code = models.CharField(max_length=10)
    phone_code = models.CharField(max_length=10, null=True)
    is_active = models.BooleanField(null=False)
    phone_number_length = models.IntegerField(null=True)

    def __str__(self):
        return self.name


class Courses(BaseModel):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name