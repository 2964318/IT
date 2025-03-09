from django.contrib import admin
from django.urls import path, include
from courses.views import home, dashboard, course_detail, enroll_course, drop_course, notifications, course_registration
from courses.views_admin import (
    admin_dashboard,
    edit_course, 
    add_course,
    delete_course, 
    toggle_user_status, 
    edit_user,
    send_notification,
    courses_management,
    students_management
)
from users.views import account_settings, CustomLoginView, register_view, custom_logout, change_password
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/courses/', courses_management, name='courses_management'),  # 课程管理
    path('admin/students/', students_management, name='students_management'),  # 学生管理
    path('admin/dashboard/', admin_dashboard, name='admin_dashboard'),
    path('admin/courses/edit/<int:course_id>/', edit_course, name='edit_course'),
    path('admin/course/delete/<int:course_id>/', delete_course, name='delete_course'),
    path('admin/courses/add/', add_course, name='add_course'),
    path('admin/user/toggle/<int:user_id>/', toggle_user_status, name='toggle_user_status'),
    path('admin/user/edit/<int:user_id>/', edit_user, name='edit_user'),
    path('admin/', admin.site.urls),
    
    path('', home, name='home'),
    path('dashboard/', dashboard, name='dashboard'),
    # path('accounts/', include('django.contrib.auth.urls')), 
    path('course-registration/', course_registration, name='course_registration'),
    path('account_settings/', account_settings, name='account_settings'),
    path('register/', register_view, name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', custom_logout, name='logout'),
    path('change-password/', change_password, name='change_password'),
    
    path('course/<int:course_id>/', course_detail, name='course_detail'),
    path('enroll/<int:course_id>/', enroll_course, name='enroll'),
    path('drop/<int:enrollment_id>/', drop_course, name='drop'),
    path('notifications/', notifications, name='notifications'),
    path('send_notification/', send_notification, name='send_notification'),
    
]
