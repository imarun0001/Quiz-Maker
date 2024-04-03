from django import forms
from django.contrib.auth.models import User
from . import models
from quiz import models as QMODEL

class StudentUserForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['first_name','last_name','username','password']
        widgets = {
        'password': forms.PasswordInput()
        }

# class StudentForm(forms.ModelForm):
#     class Meta:
#         model=models.Student
#         # fields=['address','mobile','profile_pic']
#         fields=['address','mobile']
class StudentForm(forms.ModelForm):
    # Add a new field for country_code
    country_code = forms.CharField(max_length=5, required=True)

    class Meta:
        model = models.Student
        fields = ['address', 'country_code', 'mobile']  # Include the new country_code field

    def clean_mobile(self):
        mobile = self.cleaned_data['mobile']
        country_code = self.cleaned_data['country_code']

        # Check if the mobile number is valid
        if not mobile.isdigit() or len(mobile) != 10:
            raise forms.ValidationError('Invalid mobile number format')

        # Concatenate country_code and mobile_number
        full_mobile_number = f"{country_code}{mobile}"
        
        # Check if the concatenated mobile number already exists
        if models.Student.objects.filter(mobile=full_mobile_number).exists():
            raise forms.ValidationError('This Mobile Number already exists')

        return full_mobile_number