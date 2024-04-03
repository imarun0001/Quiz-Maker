import random
import string
from django.shortcuts import render, HttpResponseRedirect
# from .models import Course  # Assuming your Course model is in a file called models.py
# from .forms import CourseForm  # Import your CourseForm
from quiz import models as QMODEL
from quiz import forms as QFORM

def generate_unique_course_code(request):
    length = 10
    characters = string.ascii_uppercase + string.digits

    while True:
        course_code = ''.join(random.choice(characters) for i in range(length))
        if not QMODEL.Course.objects.filter(course_code=course_code).exists():
            break

    return course_code