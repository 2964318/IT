# courses/admin.py
from django.contrib import admin
from django import forms
from .models import Notification, Course
from django.contrib.auth import get_user_model

User = get_user_model()

class NotificationAdminForm(forms.ModelForm):
    target_type = forms.ChoiceField(
        choices=[('all', 'All Students'), ('course', 'Specific Course')],
        widget=forms.RadioSelect
    )
    course = forms.ModelChoiceField(
        queryset=Course.objects.all(),
        required=False
    )

    class Meta:
        model = Notification
        fields = ['title','message', 'target_type', 'course']

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    form = NotificationAdminForm
    list_display = ['title','message', 'created_at']
    exclude = ['user'] 

    def save_model(self, request, obj, form, change):
        target_type = form.cleaned_data.get('target_type')
        message = form.cleaned_data.get('message')
        course = form.cleaned_data.get('course')
        title = form.cleaned_data.get('title')

        if target_type == 'course' and course:
            users = User.objects.filter(enrollment__course=course).distinct()
        else:
            users = User.objects.all()

        notifications = [
            Notification(
                title=title,
                user=user, 
                message=message)
            for user in users
        ]
        Notification.objects.bulk_create(notifications)

        self.message_user(request, f"Sent {len(notifications)} notifications")
