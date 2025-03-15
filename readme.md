The Course System

### Environmental preparation
```bash
pip install django mysqlclient
```

### Project structure
```text
course_system/
├── courses/
│   └──  templates/
|           |——  admin/
|                ...
├── users/
│   └──  templates/
         ...
├── templates/
│   └──  base.html
└── course_system/
    |——  urls.py
    |——  settings.py
         ···
```

### Configuring the database connection in settings.py
```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'course_system_db',      
        'USER': 'root',                  
        'PASSWORD': '12345678',     
        'HOST': 'localhost',             
        'PORT': '3306', 
    }
}

```

### Database model design (core/models.py)
```
# users/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    def is_admin(self):
        return self.is_superuser == 1
```

```
# courses/models.py
from django.db import models
from django.contrib.auth.models import AbstractUser
from users.models import CustomUser

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

class Enrollment(models.Model):
    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    enrolled_at = models.DateTimeField(auto_now_add=True)
    
class Notification(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    message = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False) 
    is_global = models.BooleanField(default=False)  
```

# Reset the database and create a new admin account
# 1. Delete all migration files (you can manually delete all files under __pycache__ except __init__.py if it doesn't take effect)
Get-ChildItem -Path . -Recurse -Include 0*.py,0*.pyc | Remove-Item -Force

# 2. Reset database
mysql -u root -p -e "DROP DATABASE course_system_db; CREATE DATABASE course_system_db;"

# 3. Generate migrations (users before courses)
python manage.py makemigrations users
python manage.py makemigrations courses
python manage.py makemigrations

# 4. Forced Application Migration
python manage.py migrate --fake-initial

# 5. Create Admin
# create admin
python manage.py createsuperuser --username=admin --email=admin@example.com

# enter password
Password: 
Password (again): 

# change password
python manage.py changepassword admin

# 6.Run Projects
python manage.py runserver


### test
# Adding test data to the database
```
python manage.py loaddata courses/fixtures/test_courses.json
```


