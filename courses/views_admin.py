from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Count,Q
from .models import Course, Users, Notification
from .forms import CourseForm, UserEditForm, NotificationForm
from django.db import transaction
from django.contrib import messages


def is_admin(user):
    return user.is_authenticated and user.is_superuser

@user_passes_test(is_admin)
def admin_dashboard(request):
    courses = Course.objects.annotate(student_count=Count('enrollment'))
    students = Users.objects.filter(is_superuser=False)
    # Get the latest notifications (if not, display None)
    latest_notification = Notification.objects.filter(is_admin=True).order_by('-created_at').first()
    return render(request, 'admin/dashboard.html', {
        'courses': courses,
        'students': students,
        'latest_notification': latest_notification,  
    })

@user_passes_test(is_admin)
def courses_management(request):
    courses = Course.objects.annotate(student_count=Count('enrollment'))
    return render(request, 'admin/courses_management.html', {'courses': courses})

@user_passes_test(is_admin)
def students_management(request):
    students = Users.objects.filter(is_superuser=False)
    return render(request, 'admin/students_management.html', {'students': students})
    
@user_passes_test(is_admin)
def add_course(request):
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('courses_management')
    else:
        form = CourseForm()
    return render(request, 'admin/course_form.html', {'form': form})

@user_passes_test(is_admin)
def edit_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    if request.method == 'POST':
        form = CourseForm(request.POST, instance=course)
        if form.is_valid():
            form.save()
            return redirect('courses_management')
    else:
        form = CourseForm(instance=course)
    return render(request, 'admin/course_form.html', {'form': form})

@user_passes_test(is_admin)
def delete_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    if request.method == 'POST':
        course.delete()
    return redirect('courses_management')

@user_passes_test(is_admin)
def toggle_user_status(request, user_id):
    user = get_object_or_404(Users, id=user_id)
    if request.method == 'POST':
        user.is_active = not user.is_active
        user.save()
    return redirect('students_management')

@user_passes_test(is_admin)
def edit_user(request, user_id):
    user = get_object_or_404(Users, id=user_id)
    if request.method == 'POST':
        form = UserEditForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('students_management')
    else:
        form = UserEditForm(instance=user)
    return render(request, 'admin/user_form.html', {'form': form})

@user_passes_test(is_admin)
def send_notification(request):
    if request.method == 'POST':
        form = NotificationForm(request.POST)
        if form.is_valid():
            target_type = form.cleaned_data['target_type']
            title = form.cleaned_data['title']  # Get title field
            message = form.cleaned_data['message']
            course = form.cleaned_data.get('course')
            specific = form.cleaned_data.get('specific')

            try:
                with transaction.atomic():
                    # Acquire target users
                    if target_type == 'all':
                        users = Users.objects.filter(is_active=True)
                    elif target_type == 'course':
                        users = Users.objects.filter(
                            enrollment__course=course
                        ).distinct()
                        title = f"{course.code} - {course.name}: {title}"  # Formatted message
                    elif target_type == 'specific':
                        user_obj = Users.objects.filter(id=specific.id).first()
                        if user_obj:
                            title = f"Send to {user_obj.username}: {title}"
                            users = Users.objects.filter(id=user_obj.id)  # Make sure it's a QuerySet
                        else:
                            messages.error(request, "Selected user not found.")
                            return redirect('send_notification')

                    # Get administrator
                    admins = Users.objects.filter(is_superuser=True)

                    # Merge the administrator and target user, and remove the weight
                    all_users = users.union(admins)

                    # Batch create notification
                    notifications = [
                        Notification(
                            user=user,
                            title=title,  
                            message=message,
                            is_admin=True,
                            is_global = False
                        ) for user in all_users
                    ]
                    Notification.objects.bulk_create(notifications)

                    messages.success(request, 
                        f"Successfully sent notification to {len(users)} users")
                    return redirect('notifications')

            except Exception as e:
                messages.error(request, f"Error sending notifications: {str(e)}")
    else:
        form = NotificationForm()
    return render(request, 'admin/send_notification.html', {'form': form})
