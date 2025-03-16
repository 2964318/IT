# forms.py
from django import forms
from .models import Course, Users, Notification

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = '__all__'
        widgets = {
            'schedule': forms.Select(attrs={'class': 'form-select'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'code': forms.TextInput(attrs={'class': 'form-control'}),
            'teacher': forms.TextInput(attrs={'class': 'form-control'}),
            'credits': forms.NumberInput(attrs={'class': 'form-control'}),
            'capacity': forms.NumberInput(attrs={'class': 'form-control'}),
            'enrolled_students': forms.NumberInput(attrs={'class': 'form-control'}),
        }


class UserEditForm(forms.ModelForm): 
    class Meta:
        model = Users
        fields = ['username', 'email', 'is_active']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

        
class NotificationForm(forms.ModelForm):
    TARGET_CHOICES = [
        ('all', 'All Users'),
        ('course', 'Specific Course Students'),
        ('specific', 'Specific User'),
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
    
    specific = forms.ModelChoiceField(
        queryset=Users.objects.all(),  # Query all users
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    message = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 4
        })
    )

    title = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'rows': 1
        }),
        max_length=100,
        required=True
    )

    class Meta:
        model = Notification
        fields = ['title', 'target_type', 'course', 'specific', 'message']
        
    def clean(self):
        cleaned_data = super().clean()
        target_type = cleaned_data.get('target_type')
        course = cleaned_data.get('course')
        specific = cleaned_data.get('specific')

        # Make sure target_type is valid
        if target_type not in ['all', 'course', 'specific']:
            raise forms.ValidationError("Invalid target type selected.")

        # Verify course field
        if target_type == 'course' and not course:
            raise forms.ValidationError("Please select a course when choosing 'Specific Course Students' target.")

        # Validate specific fields
        if target_type == 'specific' and not specific:
            raise forms.ValidationError("Please select a user when choosing 'Specific User' target.")

        return cleaned_data