from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db import transaction
from django.contrib.auth.decorators import login_required
from .models import Course, Enrollment, Notification
from .utils import notify_user, notify_admins
from django.db.models import Count, F
from django.http import JsonResponse
from django.contrib.messages import get_messages

def home(request):
    notifications = Notification.objects.order_by('-created_at')[:5]   # Get the latest 5 notifications
    #return render(request, 'welcome.html', {'notifications': notifications})
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return redirect('admin_dashboard')
        return redirect('dashboard')
    return render(request, 'home.html', {'notifications': notifications})

@login_required
def dashboard(request):
    student_course_count = Enrollment.objects.filter(student=request.user).count()
    latest_admin_notification = Notification.objects.filter(is_admin=True).order_by('-created_at').first()

    return render(request, 'dashboard.html', {
        'student_course_count': student_course_count,  
        'latest_admin_notification': latest_admin_notification
    })

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

    # Reads messages from session and readds Django messages
    session_messages = request.session.pop('messages', [])
    for msg in session_messages:
        messages.success(request, msg)  # Rejoin Django messages

    return render(request, 'my_course.html', {
        'enrolled_courses': enrolled_courses,
        'available_courses': available_courses,
        'time_slots': time_slots,
        'days': days
    })

@login_required
def course_registration(request):
    # Access all courses and their registration information
    courses = Course.objects.annotate(
        enrolled_count=Count('enrollment'),
        available_seats=F('capacity') - F('enrolled_count')
    ).order_by('code')

    # Convert course information to tabular format
    registration_table = []
    for course in courses:
        days_times = course.schedule  # Suppose the schedule field stores the schedule of the course
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
            'enrollment': enrollment,  
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
    # Clear old messages to prevent error messages from lingering
    storage = get_messages(request)
    list(storage)  # Read and clear previous messages

    course = get_object_or_404(Course, id=course_id)
    user = request.user

    notify_user(user,
                f"Enrolled in {course.name}",
                f"You have successfully enrolled in {course.name}-{course.code}.",
                False,
                False)
    
    notify_admins(f"Enrolled in {course.name}",
                f"{user.username} enrolled in {course.name}-{course.code}.",
                False,
                False)
    
    
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

    notify_user(request.user,
                f"Dropped {course.name}",
                f"You have successfully dropped {course.name}-{course.code}.",
                False,
                False)
    
    notify_admins(f"Dropped {course.name}",
                f"{request.user.username} dropped {course.name}-{course.code}.",
                False,
                False)

    try:
        enrollment.delete()
        course.enrolled_students -= 1
        course.save()

        messages.success(request, "Course dropped successfully")
        print("Message Added: Course dropped successfully")

        # Stores only strings, not 'Message' objects 
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
