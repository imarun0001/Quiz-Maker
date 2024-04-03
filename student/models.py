from django.db import models
from django.contrib.auth.models import User
#from phonenumber_field.modelfields import PhoneNumberField

class Student(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    #profile_pic= models.ImageField(upload_to='profile_pic/Student/',null=True,blank=True)
    address = models.EmailField(max_length=100,unique=True)
    # country_code = models.CharField(max_length=5) 
    mobile = models.CharField(max_length=16,null=False)
   
    @property
    def get_name(self):
        return self.user.first_name+" "+self.user.last_name
    @property
    def get_instance(self):
        return self
    def __str__(self):
        return self.user.first_name