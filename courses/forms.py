# forms.py
from django import forms
from .models import Course, CustomUser, Notification

# class CourseForm(forms.ModelForm):
#     class Meta:
#         model = Course
#         fields = '__all__'
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


# class UserEditForm(forms.ModelForm):
#     class Meta:
#         model = CustomUser
#         fields = ['username', 'email', 'is_active']
class UserEditForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'is_active']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

        
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

    title = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter notification title'
        }),
        max_length=100,
        required=True
    )

    class Meta:
        model = Notification
        fields = ['title', 'target_type', 'course', 'message']
        
    def clean(self):
        cleaned_data = super().clean()
        target = cleaned_data.get('target')
        course = cleaned_data.get('course')

        if target == 'course' and not course:
            raise forms.ValidationError("Please select a course when choosing 'Specific Course' target")
        
        return cleaned_data
