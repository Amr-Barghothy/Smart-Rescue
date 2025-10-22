from django.db import models

# Create your models here.

class User(models.Model):
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    DOB = models.DateField()
    role = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class CaseEmergency(models.Model):
    title = models.CharField(max_length=255)
    category = models.CharField(max_length=255)
    status = models.CharField(max_length=255)
    long = models.FloatField()
    lat = models.FloatField()
    description = models.CharField(max_length=255)
    image = models.ImageField(upload_to='images/',blank=True)
    audio = models.FileField(upload_to='audio/',blank=True)
    created_by = models.ForeignKey(User, related_name="cases", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Services(models.Model):
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    category = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField()
    owner = models.ForeignKey(User, related_name="services", on_delete=models.CASCADE)
    updated_at = models.DateTimeField(auto_now=True)