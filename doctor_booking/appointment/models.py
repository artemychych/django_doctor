from unicodedata import category
from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=100)
    icon = models.ImageField(upload_to='icons/')
    
    def __str__(self):
        return self.name
    
class Hospital(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    image = models.ImageField(upload_to='hospitals/')
    email = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    categories = models.ManyToManyField(Category)
    website = models.CharField(max_length=100)
    description = models.TextField()
    opening_hours = models.CharField(max_length=100)
    def __str__(self):
        return self.name
    
class Doctor(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    experience = models.CharField(max_length=100)
    about = models.TextField()
    phone = models.CharField(max_length=100)
    image = models.ImageField(upload_to='doctors/')
    email = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE)
    def __str__(self):
        return self.name    
    
class Slider(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='sliders/')
    
    def __str__(self):
        return self.name
    
class Appointment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    visit_date = models.CharField(max_length=100)
    time = models.CharField(max_length=100)
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE)
    note = models.TextField()
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.user.first_name + " запись на доктора: " + self.doctor.name + " в больнице: " + self.hospital.name