from django.db import models
from teacher.models import Teacher
from student.models import Student
#from django.utils import timezone
from datetime import datetime
from datetime import timedelta
# from django.contrib.auth.models import User


class Course(models.Model):
   course_name = models.CharField(max_length=100)
   #question_number = models.PositiveIntegerField()
   #total_marks = models.PositiveIntegerField()
   course_code=models.CharField(max_length=10)
   teacher_id=models.ForeignKey(Teacher,on_delete=models.CASCADE)

   def __str__(self):
        return self.course_name

def calculate_end_time():
    return datetime.now() + timedelta(hours=1)
def calculate_start_time():
    return datetime.now() + timedelta(minutes=5)
#new
class testdetails(models.Model):
   teacher_id=models.ForeignKey(Teacher,on_delete=models.CASCADE)
   course_id=models.ForeignKey(Course,on_delete=models.CASCADE)
   question_number = models.PositiveIntegerField(default=0)
   total_marks = models.PositiveIntegerField(default=0)
   start_time=models.DateTimeField(default=calculate_start_time)
   end_time=models.DateTimeField(default=calculate_end_time)     
    
class Question(models.Model):
    course_id=models.ForeignKey(Course,on_delete=models.CASCADE)
    marks=models.PositiveIntegerField()
    question=models.CharField(max_length=600)
    option1=models.CharField(max_length=200)
    option2=models.CharField(max_length=200)
    option3=models.CharField(max_length=200)
    option4=models.CharField(max_length=200)
    cat=(('Option1','Option1'),('Option2','Option2'),('Option3','Option3'),('Option4','Option4'))
    answer=models.CharField(max_length=200,choices=cat)
    testno=models.IntegerField(default=0)
    #testno=models.ForeignKey(testdetails,on_delete=models.CASCADE)

class Result(models.Model):
    student = models.ForeignKey(Student,on_delete=models.CASCADE)
    #exam = models.ForeignKey(Course,on_delete=models.CASCADE)
    marks = models.PositiveIntegerField()
    date = models.DateTimeField(auto_now=True)
    status=models.IntegerField(default=0)
    #testno=models.ForeignKey(testdetails,on_delete=models.CASCADE)
    testno=models.IntegerField()
    
class studentcourse(models.Model):
    student_id = models.ForeignKey(Student,on_delete=models.CASCADE)
    course_code= models.CharField(max_length=10)
    