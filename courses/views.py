from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db import transaction
from django.contrib.auth.decorators import login_required
from .models import Course, Enrollment, Notification
from .utils import notify_user, notify_admins
from django.db.models import Count, F, Q
from django.http import JsonResponse
from django.contrib.messages import get_messages

def home(request):
    notifications = Notification.objects.order_by('-created_at')[:5]   # 获取最新 5 条通知
    #return render(request, 'welcome.html', {'notifications': notifications})
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return redirect('admin_dashboard')
        return redirect('dashboard')
    return render(request, 'home.html', {'notifications': notifications})

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

    # **从 session 读取 messages 并重新加入 Django messages**
    session_messages = request.session.pop('messages', [])
    for msg in session_messages:
        messages.success(request, msg)  # 重新加入 Django messages

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
            'id':course.code,
            'days_times': days_times,
            'credits':course.credits,
            'teacher':course.teacher,
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
    enrolled_students = Enrollment.objects.filter(course=course).count()
    available_seats = course.capacity - enrolled_students
    is_enrolled = Enrollment.objects.filter(
        student=request.user, 
        course=course
    ).exists()
    
    return render(request, 'course_detail.html', {
        'course': course,
        'enrollment': enrollment,
        'is_enrolled': is_enrolled,
        'available_seats': available_seats,
    })
@login_required
@transaction.atomic
def enroll_course(request, course_id):
    # 清空旧的 messages，防止错误信息残留
    storage = get_messages(request)
    list(storage)  # 读取并清空之前的 messages

    course = get_object_or_404(Course, id=course_id)
    user = request.user

    # 创建系统通知
    Notification.objects.create(
        user=user,
        title=f"Enrolled in {course.code}",
        message=f"You have successfully enrolled in {course.name}.",
        is_admin=False,  # 系统通知，不是管理员通知
        is_global=False  # 系统通知，不是全局通知
    )

    if Enrollment.objects.filter(student=user, course=course).exists():
        messages.warning(request, "You are already enrolled in this course")
        return redirect('course_detail', course_id=course_id)

    if course.enrolled_students >= course.capacity:
        messages.error(request, "This course is already full")
        return redirect('course_detail', course_id=course_id)

    try:
        Enrollment.objects.create(student=user, course=course)
        course.enrolled_students += 1
        course.save()
        messages.success(request, "Enrollment successful")
    except Exception as e:
        messages.error(request, f"Enrollment failed: {str(e)}")

    return redirect('my_course')
@login_required
@transaction.atomic
def drop_course(request, enrollment_id):
    enrollment = get_object_or_404(Enrollment, id=enrollment_id, student=request.user)
    course = enrollment.course

    Notification.objects.create(
        user=request.user,
        title=f"Dropped {course.code}",
        message=f"You have successfully dropped {course.name}.",
        is_admin=False,  # 用户通知
        is_global=False  # 不是全局通知
    )

    try:
        enrollment.delete()
        course.enrolled_students -= 1
        course.save()

        messages.success(request, "Course dropped successfully")
        print("Message Added: Course dropped successfully")

        # **只存字符串，而不是 `Message` 对象**
        request.session['messages'] = [msg.message for msg in get_messages(request)]

    except Exception as e:
        messages.error(request, f"Failed to drop course: {str(e)}")
        print(f"Message Added: Failed to drop course - {str(e)}")

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


    
    
