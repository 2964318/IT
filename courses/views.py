from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db import transaction
from django.contrib.auth.decorators import login_required
from .models import Course, Enrollment, Notification
from .utils import notify_user, notify_admins
from django.db.models import Count, F, Q

def home(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return redirect('admin_dashboard')
        return redirect('dashboard')
    return render(request, 'home.html')

@login_required
def dashboard(request):
    return render(request, 'dashboard.html')

@login_required
def my_course(request):
    enrolled_courses = Enrollment.objects.filter(student=request.user)\
        .select_related('course')
    
    available_courses = Course.objects.exclude(
        enrollment__student=request.user
    ).annotate(
        enrolled_count=Count('enrollment'),
        available_seats=F('capacity') - F('enrolled_count')
    )
    
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
    time_slots = [
        ('1', '8:00 AM - 10:00 AM'),
        ('2', '10:00 AM - 12:00 PM'),
        ('3', '12:00 PM - 2:00 PM'),
        ('4', '2:00 PM - 4:00 PM'),
        ('5', '4:00 PM - 6:00 PM')
    ]
    
    return render(request, 'my_course.html', {
        'enrolled_courses': enrolled_courses,
        'available_courses': available_courses,
        'time_slots': time_slots,
        'days': days
    })
   
@login_required
def course_registration(request):
    # 获取所有课程及其注册信息
    courses = Course.objects.annotate(
        enrolled_count=Count('enrollment'),
        available_seats=F('capacity') - F('enrolled_count')
    ).order_by('code')

    # 将课程信息转换为表格格式
    registration_table = []
    for course in courses:
        days_times = course.schedule  # 假设 schedule 字段存储了课程的时间安排
        enrollment = Enrollment.objects.filter(course=course, student=request.user).first()
        status = "Enrolled" if enrollment else "Not Enrolled"
        action = "Drop" if status == "Enrolled" else "Enroll"
        
        registration_table.append({
            'class': course.name,
            'days_times': days_times,
            'status': status,
            'action': action,
            'course': course,
            'enrollment': enrollment,  # 这里可能是 None
        })

    return render(request, 'course_registration.html', {
        'registration_table': registration_table
    })


@login_required
def course_detail(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    enrollment = Enrollment.objects.filter(course=course, student=request.user).first()
    is_enrolled = Enrollment.objects.filter(
        student=request.user, 
        course=course
    ).exists()
    
    return render(request, 'course_detail.html', {
        'course': course,
        'enrollment': enrollment,
        'is_enrolled': is_enrolled
    })
    
@login_required
@transaction.atomic
def enroll_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    user = request.user
    if Enrollment.objects.filter(student=user, course=course).exists():
        messages.warning(request, "You are already enrolled in this course")
        return redirect('course_detail', course_id=course_id)
    if course.enrolled_students >= course.capacity:
        messages.error(request, "This course is already full")
        notify_admins(f"Course {course.code} is full")
        return redirect('course_detail', course_id=course_id)

    existing_schedules = user.enrollment_set.values_list('course__schedule', flat=True)
    if course.schedule in existing_schedules:
        messages.error(request, "Schedule conflict detected")
        return redirect('course_detail', course_id=course_id)

    try:
        Enrollment.objects.create(student=user, course=course)
        course.enrolled_students += 1
        course.save()
        
        notify_user(request.user, f"Enrolled in {course.code}")
        notify_admins(f"New enrollment: {request.user} in {course.code} - {course.name}")
        
        messages.success(request, "Enrollment successful")
    except Exception as e:
        messages.error(request, "Enrollment failed")

    #return redirect('dashboard')
    return redirect('my_course')
        
@login_required
@transaction.atomic
def drop_course(request, enrollment_id):
    enrollment = get_object_or_404(Enrollment, id=enrollment_id, student=request.user)
    course = enrollment.course

    try:
        enrollment.delete()
        course.enrolled_students -= 1
        course.save()
        
        notify_user(request.user, f"Dropped course: {course.code} - {course.name}")
        notify_admins(f"User {request.user} dropped {course.code} - {course.name}")
        
        messages.success(request, "Course dropped successfully")
    except Exception as e:
        messages.error(request, "Failed to drop course")

    #return redirect('dashboard')
    return redirect('my_course')

@login_required
def notifications(request):
    Notification.objects.filter(
        user=request.user,
        is_read=False
    ).update(is_read=True)
    notifications = Notification.objects.filter(user=request.user)\
        .select_related('user')\
        .order_by('-created_at')
    return render(request, 'notifications.html', {
        'notifications': notifications
    })
    
    
