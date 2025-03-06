# forms.py
from django import forms
from .models import Course, CustomUser, Notification

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = '__all__'

class UserEditForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'is_active']
        
class NotificationForm(forms.ModelForm):
    TARGET_CHOICES = [
        ('all', 'All Users'),
        ('course', 'Specific Course Students')
    ]
    
    target_type = forms.ChoiceField(
        choices=TARGET_CHOICES,
        widget=forms.RadioSelect(attrs={'class': 'form-check-input'}),
        initial='all'
    )
    
    course = forms.ModelChoiceField(
        queryset=Course.objects.all(),
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    message = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 4
        })
    )

    class Meta:
        model = Notification
        fields = ['target_type', 'course', 'message']
        
    def clean(self):
        cleaned_data = super().clean()
        target = cleaned_data.get('target')
        course = cleaned_data.get('course')

        if target == 'course' and not course:
            raise forms.ValidationError("Please select a course when choosing 'Specific Course' target")
        
        return cleaned_data