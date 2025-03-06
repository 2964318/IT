以下是基于MySQL+Django+Bootstrap的学生选课系统基本的实现步骤和部分代码：

### 一、环境准备
```bash
pip install django mysqlclient
```

### 二、项目结构
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

### 三、配置settings.py中的数据库连接
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

### 四、数据库模型设计（core/models.py）
# 此处用代码设计好数据库表后，利用脚本（按照下面的重置数据库和建立新的admin账户步骤执行）可直接生成数据库表，无需手动配置数据库
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

# 重置数据库和建立新的admin账户
# 1. 删除所有迁移文件（如未生效可手动删除__pycache__下的除__init__.py以外的所有文件）
Get-ChildItem -Path . -Recurse -Include 0*.py,0*.pyc | Remove-Item -Force

# 2. 重置数据库
mysql -u root -p -e "DROP DATABASE course_system_db; CREATE DATABASE course_system_db;"

# 3. 生成迁移（先users后courses）
python manage.py makemigrations users
python manage.py makemigrations courses
python manage.py makemigrations

# 4. 强制应用迁移
python manage.py migrate --fake-initial

# 5. 创建管理员
# create admin
python manage.py createsuperuser --username=admin --email=admin@example.com

# enter password
Password: 
Password (again): 

# change password
python manage.py changepassword admin

# 6.运行项目
python manage.py runserver


### 五、其他
# 往数据库里添加测试数据
```
python manage.py loaddata courses/fixtures/test_courses.json
```


