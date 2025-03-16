from django.db import models
from django.contrib.auth.models import AbstractUser
from users.models import Users

class Course(models.Model):
    SCHEDULE_CHOICES = [
        ('Monday 8:00 AM - 10:00 AM', 'Monday 8:00 AM - 10:00 AM'),
        ('Monday 10:00 AM - 12:00 PM', 'Monday 10:00 AM - 12:00 PM'),
        ('Monday 12:00 PM - 2:00 PM', 'Monday 12:00 PM - 2:00 PM'),
        ('Monday 2:00 PM - 4:00 PM', 'Monday 2:00 PM - 4:00 PM'),
        ('Monday 4:00 PM - 6:00 PM', 'Monday 4:00 PM - 6:00 PM'),
        ('Tuesday 8:00 AM - 10:00 AM', 'Tuesday 8:00 AM - 10:00 AM'),
        ('Tuesday 10:00 AM - 12:00 PM', 'Tuesday 10:00 AM - 12:00 PM'),
        ('Tuesday 12:00 PM - 2:00 PM', 'Tuesday 12:00 PM - 2:00 PM'),
        ('Tuesday 2:00 PM - 4:00 PM', 'Tuesday 2:00 PM - 4:00 PM'),
        ('Tuesday 4:00 PM - 6:00 PM', 'Tuesday 4:00 PM - 6:00 PM'),
        ('Wednesday 8:00 AM - 10:00 AM', 'Wednesday 8:00 AM - 10:00 AM'),
        ('Wednesday 10:00 AM - 12:00 PM', 'Wednesday 10:00 AM - 12:00 PM'),
        ('Wednesday 12:00 PM - 2:00 PM', 'Wednesday 12:00 PM - 2:00 PM'),
        ('Wednesday 2:00 PM - 4:00 PM', 'Wednesday 2:00 PM - 4:00 PM'),
        ('Wednesday 4:00 PM - 6:00 PM', 'Wednesday 4:00 PM - 6:00 PM'),
        ('Thursday 8:00 AM - 10:00 AM', 'Thursday 8:00 AM - 10:00 AM'),
        ('Thursday 10:00 AM - 12:00 PM', 'Thursday 10:00 AM - 12:00 PM'),
        ('Thursday 12:00 PM - 2:00 PM', 'Thursday 12:00 PM - 2:00 PM'),
        ('Thursday 2:00 PM - 4:00 PM', 'Thursday 2:00 PM - 4:00 PM'),
        ('Thursday 4:00 PM - 6:00 PM', 'Thursday 4:00 PM - 6:00 PM'),
        ('Friday 8:00 AM - 10:00 AM', 'Friday 8:00 AM - 10:00 AM'),
        ('Friday 10:00 AM - 12:00 PM', 'Friday 10:00 AM - 12:00 PM'),
        ('Friday 12:00 PM - 2:00 PM', 'Friday 12:00 PM - 2:00 PM'),
        ('Friday 2:00 PM - 4:00 PM', 'Friday 2:00 PM - 4:00 PM'),
        ('Friday 4:00 PM - 6:00 PM', 'Friday 4:00 PM - 6:00 PM'),
    ]
    
    schedule = models.CharField(
        max_length=50,
        choices=SCHEDULE_CHOICES,
        default='Monday 8:00 AM - 10:00 AM'
    )
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20, unique=True)
    teacher = models.CharField(max_length=100)
    credits = models.PositiveIntegerField(default=0)
    capacity = models.PositiveIntegerField(default=30)
    enrolled_students = models.PositiveIntegerField(default=0)
            
    def __str__(self):
        return self.name

class Enrollment(models.Model):
    student = models.ForeignKey(Users, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    enrolled_at = models.DateTimeField(auto_now_add=True)
    
class Notification(models.Model):
    title = models.CharField(max_length=100, default="Notification") 
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    message = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False) 
    is_global = models.BooleanField(default=False) 
