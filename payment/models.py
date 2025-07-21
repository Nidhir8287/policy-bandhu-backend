from django.db import models
from core.models import User
from datetime import datetime


# Create your models here.

def user_directory_path(instance, filename):

    # file will be uploaded to MEDIA_ROOT / user_<id>/<filename>
    return '{1}_user_{0}.jpeg'.format(instance.user.id, datetime.today().date())

class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)
    screenshot = models.ImageField(upload_to=user_directory_path)
    message = models.TextField()

class Coupon(models.Model):
    code = models.CharField(max_length=20, unique=True)
    no_of_times_allowed = models.IntegerField()
    discount = models.IntegerField()
