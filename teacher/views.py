from django.shortcuts import render,redirect,reverse
from . import forms,models
from django.db.models import Sum
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required,user_passes_test
from django.conf import settings
from datetime import date, timedelta
from quiz import models as QMODEL
from student import models as SMODEL
from quiz import forms as QFORM
from django.forms import formset_factory
from teacher import generate_course_code as q
from django.contrib.auth.models import User
from django.db.models import Subquery, OuterRef,Exists
# -------
from teacher import models as TMODEL
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.http import HttpResponse
import datetime
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth.views import LoginView
# for password
import re
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

# start validation function
def check_username_teacher(request):
    username = request.POST.get('username')
    if len(username) == 0 :
        return HttpResponse('<div style="color: red"> The username field must not be left blank. </div>')

    if len(username) < 4 :
        return HttpResponse('<div style="color: red"> The username field must not be less than 4 characters. </div>')
    

    if User.objects.all().filter(username=username).exists():
        return HttpResponse('<div style="color: red"> This username already exists </div>')
    else:
        return HttpResponse('<div style="color: green"> This username is available </div>')

# def check_useremail(request):
#     email = request.POST.get('address')

#     # if get_user_model().objects.filter(email=email).exists():
#     if User.objects.all().filter(email=email).exists():
#         return HttpResponse('<div style="color: red"> This Email already exists </div>')
#     elif  models.Student.objects.all().filter(address=email).exists():
#         return HttpResponse('<div style="color: red"> This Email already exists </div>')
#     else:
#         return HttpResponse('<div style="color: green"> This Email is available </div>')

def check_useremail_teacher(request):
    email = request.POST.get('address')

    if len(email) == 0:
        return HttpResponse('<div style="color: red"> The email field must not be left blank. </div>')

    if User.objects.all().filter(email=email).exists() or models.Teacher.objects.all().filter(address=email).exists():
        return HttpResponse('<div style="color: red"> This Email already exists </div>')

    # Extract the email domain
    email_domain = email.split('@')[1] if '@' in email else None

    # Define a list of supported email providers
    supported_providers = {
        'gmail.com': 'Google',
        'outlook.com': 'Outlook',
        'yahoo.com': 'Yahoo',
        'hotmail.com': 'Hotmail',
        'aol.com': 'AOL',
        'icloud.com': 'iCloud',
        'protonmail.com': 'ProtonMail',
        'mail.com': 'Mail.com',
        'zoho.com': 'Zoho',
        # Add more supported providers as needed
    }

    if email_domain in supported_providers:
        provider_name = supported_providers[email_domain]
        return HttpResponse(f'<div style="color: green"> Email is available. Provider: {provider_name} </div>')
    else:
        return HttpResponse('<div style="color: red"> Email provider not supported </div>')
# flag for password check
flag=False
def check_password_strength_teacher(request):
    user_entered_password = request.POST.get('password')

    # Custom password strength criteria
    min_length = 8
    if len(user_entered_password) == 0 :
        return HttpResponse(f'<div style="color:green"> 8+ characters, mix of upper & lowercase, at least 1 number.</div>')
    

    if len(user_entered_password) < min_length:
        return HttpResponse('<div style="color: red"> Password should be at least {} characters long </div>'.format(min_length))

    # Use Django's built-in password validation
    try:
        validate_password(user_entered_password)
    except ValidationError as e:
        error_messages = ', '.join(e.messages)
        return HttpResponse('<div style="color: red"> {} </div>'.format(error_messages))

    # Additional custom checks (you can customize these based on your requirements)
    if not re.search(r'[A-Z]', user_entered_password):
        return HttpResponse('<div style="color: red"> Password should contain at least one uppercase letter </div>')

    if not re.search(r'[a-z]', user_entered_password):
        return HttpResponse('<div style="color: red"> Password should contain at least one lowercase letter </div>')

    if not re.search(r'[0-9]', user_entered_password):
        return HttpResponse('<div style="color: red"> Password should contain at least one digit </div>')

    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', user_entered_password):
        return HttpResponse('<div style="color: red"> Password should contain at least one special character </div>')
    flag = True
    return HttpResponse('<div style="color: green"> Password meets the strength criteria </div>')

def check_mobile_teacher(request):
    if request.method == 'POST':
        mobile_number = request.POST.get('mobile')
        country_code = request.POST.get('country_code')
        full_mobile_number = f"{country_code}{mobile_number}"

        # Check if the concatenated mobile number already exists

        # Check if the mobile number is 10 digits long
        is_valid_length = len(mobile_number) == 10

        if not is_valid_length:
            return HttpResponse(f'<div style="color: red"> The mobile number must be 10 digits long </div>')

        if models.Teacher.objects.filter(mobile=full_mobile_number).exists():
            return HttpResponse('<div style="color: red"> This Mobile Number already exists </div>')
        else:
            return HttpResponse('<div style="color: green"> This Mobile Number is available </div>')

    return render(request, 'student/studentsignup.html')



# coustom login view
class CustomLoginView(LoginView):
    template_name = 'student/studentlogin.html'

    def form_invalid(self, form):
        messages.error(self.request, 'Invalid username or password')
        return super().form_invalid(form)
    
# end validation function
#for showing signup/login button for teacher
def teacherclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'teacher/teacherclick.html')

def teacher_signup_view(request):
    userForm=forms.TeacherUserForm()
    teacherForm=forms.TeacherForm()
    mydict={'userForm':userForm,'teacherForm':teacherForm}
    if request.method=='POST':
        userForm=forms.TeacherUserForm(request.POST)
        teacherForm=forms.TeacherForm(request.POST,request.FILES)
        if userForm.is_valid() and teacherForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.email = request.POST.get('address')
            user.save()
            teacher=teacherForm.save(commit=False)
            teacher.user=user
            teacher.save()
            my_teacher_group = Group.objects.get_or_create(name='TEACHER')
            my_teacher_group[0].user_set.add(user)
            return render(request, 'teacher/succes_page_teacher.html')
            # return HttpResponseRedirect('teacherlogin')
        else:
            print(userForm.errors)
            print(teacherForm.errors)
            messages.error(request, 'There was an error in the form. Please correct the errors.')
    
    return render(request,'teacher/teachersignup.html',context=mydict)

def success_page_view_teacher(request):
    return render(request, 'teacher/succes_page_teacher.html')

def is_teacher(user):
    return user.groups.filter(name='TEACHER').exists()

@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def teacher_dashboard_view(request):
    teacher1= models.Teacher.objects.get(user_id=request.user.id).pk
    dict={
    
    'total_course':QMODEL.Course.objects.all().filter(teacher_id=teacher1).count(),
    'total_question':QMODEL.testdetails.objects.all().filter(teacher_id=teacher1).count(),
    'total_student':SMODEL.Student.objects.all().count()
    }
    return render(request,'teacher/teacher_dashboard.html',context=dict)

@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def teacher_exam_view(request):
    return render(request,'teacher/teacher_exam.html')

#new
@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def teacher_result_view(request):
    return render(request,'teacher/teacher_result.html')


@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def teacher_add_exam_view(request):
    # courseForm=QFORM.CourseForm()
    teacher1= models.Teacher.objects.get(user_id=request.user.id).pk
    val=q.generate_unique_course_code(request)
    courseForm = QFORM.CourseForm(initial={'course_code': val,'teacher_id':teacher1})
    if request.method=='POST':
        courseForm=QFORM.CourseForm(request.POST,initial={'course_code': val,'teacher_id':teacher1})
        if courseForm.is_valid():        
            courseForm.save()
            return HttpResponseRedirect('/teacher/teacher-view-exam')
        else:
            # print("form is invalid",courseForm.errors)
            messages.error(request, 'Form is invalid')
    return render(request,'teacher/teacher_add_exam.html',{'courseForm':courseForm})

#new
@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def teacher_view_exam_view(request):
    # courses = QMODEL.Course.objects.all()
    teach= models.Teacher.objects.get(user_id=request.user.id).pk
    exam = QMODEL.Course.objects.all().filter(teacher_id=teach)
    return render(request,'teacher/teacher_view_exam.html',{'exam':exam})

@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def delete_exam_view(request,pk):
    course=QMODEL.Course.objects.get(id=pk)
    course.delete()
    return HttpResponseRedirect('/teacher/teacher-view-exam')

@login_required(login_url='adminlogin')
def teacher_question_view(request):
    return render(request,'teacher/teacher_question.html')

#modified
@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)

# new
def teacher_add_question_view(request):
    try:
        teacher_id = QMODEL.Teacher.objects.get(user_id=request.user.id).pk
        testdetailsform = QFORM.testdetailsForm(teacher_id=teacher_id, initial={'teacher_id': teacher_id})
        question_count = 0

        latest_testdetails = QMODEL.testdetails.objects.last()
        testno1 = latest_testdetails.pk if latest_testdetails is not None else 0
        testno2 = testno1 + 1

        question_forms = [QFORM.QuestionForm(prefix=str(i)) for i in range(question_count)]

        if request.method == 'POST':
            course3 = QMODEL.Course.objects.get(id=request.POST.get('course_id'))
            testdetailsform = QFORM.testdetailsForm(request.POST, teacher_id=teacher_id, initial={'teacher_id': teacher_id})
            question_count = int(request.POST.get('question_number', 0))
            question_forms = [QFORM.QuestionForm(request.POST, initial={'course_id': course3, 'testno': testno2}, prefix=str(i)) for i in range(question_count)]

            if testdetailsform.is_valid() and all([form.is_valid() for form in question_forms]):
                total_marks = testdetailsform.cleaned_data.get('total_marks')
                question_marks = [form.cleaned_data.get('marks') for form in question_forms]

                if total_marks != sum(question_marks):
                    messages.error(request, "Total marks should be equal to the sum of each question's marks.")
                    return render(request, 'teacher/teacher_add_question.html', {'testdetailsform': testdetailsform, 'question_forms': question_forms})

                tdetails = testdetailsform.save(commit=False)
                course1 = QMODEL.Course.objects.get(id=request.POST.get('course_id'))
                tdetails.course_id = course1
                tdetails.save()

                for i, form in enumerate(question_forms):
                    question = form.save(commit=False)
                    question.course_id = course3
                    question.testno = testno2
                    question.save()

                return HttpResponseRedirect('/teacher/teacher-view-question')
            else:
                for field, errors in testdetailsform.errors.items():
                    for error in errors:
                        messages.error(request, f"{error}")

    except Exception as e:
        print(e)
        return HttpResponseRedirect('/teacher/teacher-dashboard')

    context = {'testdetailsform': testdetailsform, 'question_forms': question_forms}
    return render(request, 'teacher/teacher_add_question.html', context)

@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def teacher_view_question_view(request):
    teach= models.Teacher.objects.get(user_id=request.user.id).pk
    courses = QMODEL.Course.objects.all().filter(teacher_id=teach)
    return render(request,'teacher/teacher_view_question.html',{'courses':courses})

#new
@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def teacher_release_result_view(request):
    teach= models.Teacher.objects.get(user_id=request.user.id).pk
    courses = QMODEL.Course.objects.all().filter(teacher_id=teach)
    return render(request,'teacher/teacher_release_result.html',{'courses':courses})

#new
@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def teacher_view_result_view(request):
    teach= models.Teacher.objects.get(user_id=request.user.id).pk
    courses = QMODEL.Course.objects.all().filter(teacher_id=teach)
    return render(request,'teacher/teacher_view_result.html',{'courses':courses})

#new
@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def teacher_view_result1_view(request,pk):
    courses = QMODEL.testdetails.objects.all().filter(course_id=pk)
    return render(request,'teacher/teacher_view_result1.html',{'courses':courses})

#new
@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def teacher_view_result2_view(request,pk):
    courses = QMODEL.Result.objects.all().filter(testno=pk)
    return render(request,'teacher/teacher_view_result2.html',{'courses':courses})


#new
@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def teacher_release_result1_view(request, pk):
    
    latest_result_statuses = QMODEL.Result.objects.filter(
        testno=OuterRef('id')
    ).order_by('-id').values('status')[:1]

    questions = QMODEL.testdetails.objects.filter(
        course_id=pk
    ).annotate(latest_result_status=Subquery(latest_result_statuses)).filter(
        latest_result_status=0
    )

    return render(request, 'teacher/teacher_release_result1.html', {'questions': questions})

#new
@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def teacher_release_view(request,pk):
    results = QMODEL.Result.objects.filter(testno=pk)

    for result in results:
        result.status = 1
        result.save()
    return HttpResponseRedirect('/teacher/teacher-release-result')
    

#new
@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def teacher_view_student_view(request,course_code):
    courses = QMODEL.studentcourse.objects.all().filter(course_code=course_code)
    return render(request,'teacher/teacher_view_student.html',{'courses':courses})


@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def see_question_view(request,pk):
    questions=QMODEL.Question.objects.all().filter(testno=pk)
    return render(request,'teacher/see_question.html',{'questions':questions})

#new
@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def see_question0_view(request,pk):
    courses = QMODEL.testdetails.objects.all().filter(course_id=pk)
    return render(request,'teacher/see_question0.html',{'courses':courses})


@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def remove_question_view(request,pk):
    question=QMODEL.testdetails.objects.get(id=pk)
    question.delete()
    return HttpResponseRedirect('/teacher/teacher-view-question')

#new
@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def update_testdetails_view(request,pk):
    test_details = QMODEL.testdetails.objects.get(id=pk)
    print(test_details.end_time)
    new=(test_details.end_time)+timedelta(minutes=10)  
    test_details.end_time=new
    test_details.save() 
    
    return HttpResponseRedirect('/teacher/teacher-view-question')