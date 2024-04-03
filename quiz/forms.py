from django import forms
from django.contrib.auth.models import User
from . import models
from django.core.exceptions import ValidationError
from django.utils import timezone
# from bootstrap_datepicker_plus import DatePickerInput, TimePickerInput
from bootstrap_datepicker_plus.widgets import DateTimePickerInput
from datetime import datetime
from datetime import timedelta

class ContactusForm(forms.Form):
    Name = forms.CharField(max_length=30)
    Email = forms.EmailField()
    Message = forms.CharField(max_length=500,widget=forms.Textarea(attrs={'rows': 3, 'cols': 30}))


class TeacherSalaryForm(forms.Form):
    salary=forms.IntegerField()
    

class studentcourseForm(forms.ModelForm):
    class Meta:
        model=models.studentcourse
        fields=['student_id','course_code']
        widgets={
            'student_id':forms.TextInput(attrs={'readonly':'readonly'}),
        }

#new
class testdetailsForm(forms.ModelForm):
    
    def __init__(self, *args, **kwargs):
        teacher_id = kwargs.pop('teacher_id', None)
        super(testdetailsForm, self).__init__(*args, **kwargs)
        if teacher_id is not None:
            self.teacher_id = teacher_id
            self.fields['course_id'].queryset = models.Course.objects.filter(teacher_id=teacher_id)

    course_id = forms.ModelChoiceField(queryset=models.Course.objects.none(), empty_label="Course Name", to_field_name="id")
    # start_time = forms.DateTimeField(initial=datetime.now() + timedelta(minutes=5), widget=DateTimePickerInput())
    class Meta:
        model=models.testdetails
        fields=['teacher_id','course_id','question_number','total_marks','start_time','end_time']
        widgets = {
        'teacher_id': forms.TextInput(attrs={'readonly': 'readonly'}),
        'start_time': DateTimePickerInput(),
        'end_time': DateTimePickerInput(),
        }
    
    def clean(self):
        cleaned_data = super().clean()
        course_id1 = cleaned_data.get('course_id')

        # Optionally, you can perform additional validation based on the teacher_id and course_id
        # Time Checking errors
        start_time = cleaned_data.get('start_time')
        end_time = cleaned_data.get('end_time')

        # Check if start time is less than end time
        if start_time and end_time and start_time >= end_time:
            raise ValidationError("Closing time must be greater than Opening time.")

        # Check if the time difference is more than 1 minute
        if start_time and end_time and (end_time - start_time).seconds < 60:
            raise ValidationError("The difference between Opening and Closing time must be more than 1 minute.")

        # Check if start and end times are greater than the current date time
        current_time = timezone.localtime()
        if start_time and start_time <= current_time:
            raise ValidationError("Opening time must be greater than the current date and time.")
        if end_time and end_time <= current_time:
            raise ValidationError("Closing time must be greater than the current date and time.")
        # End time checking errors
        return cleaned_data
        
class CourseForm(forms.ModelForm):
    class Meta:
        model=models.Course
        #fields=['course_name','question_number','total_marks', 'course_code']
        fields=['course_name', 'course_code','teacher_id']
        widgets = {
        'teacher_id': forms.TextInput(attrs={'readonly': 'readonly'}),
        'course_code': forms.TextInput(attrs={'readonly': 'readonly'}),
        }

class QuestionForm(forms.ModelForm):
    # def __init__(self, *args, **kwargs):
    #     teacher_id = kwargs.pop('teacher_id', None)
    #     super(QuestionForm, self).__init__(*args, **kwargs)
    #     if teacher_id is not None:
    #         self.teacher_id = teacher_id
    #         self.fields['course_id'].queryset = models.Course.objects.filter(teacher_id=teacher_id)

    # course_id = forms.ModelChoiceField(queryset=models.Course.objects.none(), empty_label="Course Name", to_field_name="id")
    

    #this will show dropdown __str__ method course model is shown on html so override it
    #to_field_name this will fetch corresponding value  user_id present in course model and return it
    #courseID=forms.ModelChoiceField(queryset=models.Course.objects.all(),empty_label="Course Name", to_field_name="id")
    class Meta:
        model=models.Question
        # fields=['marks','question','option1','option2','option3','option4','answer','testno']
        fields=['marks','question','option1','option2','option3','option4','answer']
        widgets = {
            'question': forms.Textarea(attrs={'rows': 3, 'cols': 50}),
            'course_id':forms.TextInput(attrs={'readonly':'readonly'}),
            'testno':forms.TextInput(attrs={'readonly':'readonly'})
        }
    # def clean(self):
    #     cleaned_data = super().clean()
    #     course_id1 = cleaned_data.get('course_id')

    #     # Optionally, you can perform additional validation based on the teacher_id and course_id

    #     return cleaned_data