from django.shortcuts import render,redirect,reverse
from . import forms,models
from django.db.models import Sum
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required,user_passes_test
from django.conf import settings
from datetime import date, timedelta
from quiz import models as QMODEL
from teacher import models as TMODEL
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.http import HttpResponse
from quiz import forms as QFORM
import datetime
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth.views import LoginView
# for password
import re
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
# for email
from onlinequiz import settings
from email.message import EmailMessage
from . tokens import generate_token
from django.core.mail import send_mail , EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes,force_str

from django.http import HttpResponseServerError
from django.views.decorators.csrf import csrf_protect,csrf_exempt
from timeout_decorator import timeout
# forgot password

from django.contrib.auth import authenticate,login,logout
import uuid

#for showing signup/login button for student
def studentclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'student/studentclick.html')

user_flag = False


def check_username(request):
    username = request.POST.get('username')

    if len(username) == 0 :
        return HttpResponse('<div style="color: red"> The username field must not be left blank. </div>')

    if len(username) < 4 :
        return HttpResponse('<div style="color: red"> The username field must not be less than 4 characters. </div>')
    
    if User.objects.all().filter(username=username).exists():
        return HttpResponse('<div style="color: red"> This username already exists </div>')
    else:
        user_flag = True
        return HttpResponse('<div style="color: green"> This username is available. </div>')

# def check_useremail(request):
#     email = request.POST.get('address')

#     # if get_user_model().objects.filter(email=email).exists():
#     if User.objects.all().filter(email=email).exists():
#         return HttpResponse('<div style="color: red"> This Email already exists </div>')
#     elif  models.Student.objects.all().filter(address=email).exists():
#         return HttpResponse('<div style="color: red"> This Email already exists </div>')
#     else:
#         return HttpResponse('<div style="color: green"> This Email is available </div>')

def check_useremail(request):
    email = request.POST.get('address')

    if User.objects.all().filter(email=email).exists() or models.Student.objects.all().filter(address=email).exists():
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
def check_password_strength(request):
    user_entered_password = request.POST.get('password')

    # Custom password strength criteria
    min_length = 8
    #default show msg 
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

# def check_mobile(request):
#     mobile_number = request.POST.get('mobile')

#     # Check if the mobile number has a valid country code
#     valid_country_codes = {
#         '+1': 'United States',
#         '+91': 'India',
#         '+92': 'Pakistan',
#         '+880': 'Bangladesh',
#         '+94': 'Sri Lanka',
#         '+977': 'Nepal',
#         # Add more valid country codes and their names as needed
#     }

#     # Extract the country code from the mobile number
#     country_code = next((code for code in valid_country_codes if mobile_number.startswith(code)), None)

#     if country_code:
#         # Remove the country code
#         mobile_numbers = mobile_number[len(country_code):]

#         # Check if the mobile number is 10 digits long for supported country codes
#         is_valid_length = len(mobile_numbers) == 10

#         if not is_valid_length:
#             return HttpResponse(f'<div style="color: red"> The mobile number for {valid_country_codes[country_code]} must be 10 digits long </div>')
#     else :
#         return HttpResponse('<div style="color: red"> Service not available for the provided country code </div>')

#     # is_valid_length = len(mobile_number) == 10

#     if models.Student.objects.filter(mobile=mobile_number).exists():
#         return HttpResponse('<div style="color: red"> This Mobile Number already exists </div>')
#     else:
#         return HttpResponse('<div style="color: green"> This Mobile Number is available </div>')
#     # Check if the mobile number is 10 digits long

# new mobile number checking code 
# def check_mobile(request):
#     valid_country_codes = {
#         '+1': 'United States',
#         '+91': 'India',
#         '+92': 'Pakistan',
#         '+880': 'Bangladesh',
#         '+94': 'Sri Lanka',
#         '+977': 'Nepal',
#         # Add more valid country codes and their names as needed
#     }

#     if request.method == 'POST':
#         mobile_number = request.POST.get('mobile')
#         country_code = request.POST.get('country_code')

#         if country_code not in valid_country_codes:
#             return HttpResponse('<div style="color: red"> Invalid country code selected </div>')

#         if not mobile_number or not mobile_number.startswith(country_code):
#             return HttpResponse(f'<div style="color: red"> Invalid mobile number for {valid_country_codes[country_code]}</div>')

#         mobile_numbers = mobile_number[len(country_code):]
#         is_valid_length = len(mobile_numbers) == 10

#         if not is_valid_length:
#             return HttpResponse(f'<div style="color: red"> The mobile number for {valid_country_codes[country_code]} must be 10 digits long </div>')

#         if models.Student.objects.filter(mobile=mobile_number).exists():
#             return HttpResponse('<div style="color: red"> This Mobile Number already exists </div>')
#         else:
#             return HttpResponse('<div style="color: green"> This Mobile Number is available </div>')

#     return render(request, 'student/check_mobile.html', {'valid_country_codes': valid_country_codes})
# d

def check_mobile(request):
    if request.method == 'POST':
        mobile_number = request.POST.get('mobile')
        country_code = request.POST.get('country_code')

        full_mobile_number = f"{country_code}{mobile_number}"

        # Check if the mobile number is 10 digits long
        is_valid_length = len(mobile_number) == 10

        if not is_valid_length:
            return HttpResponse(f'<div style="color: red"> The mobile number must be 10 digits long </div>')

        if models.Student.objects.filter(mobile=full_mobile_number).exists():
            return HttpResponse('<div style="color: red"> This Mobile Number already exists </div>')
        else:
            return HttpResponse('<div style="color: green"> This Mobile Number is available </div>')

    return render(request, 'student/studentsignup.html')


def student_signup_view(request):
    try:
        userForm = forms.StudentUserForm()
        studentForm = forms.StudentForm()
        mydict = {'userForm': userForm, 'studentForm': studentForm}

        if request.method == 'POST':
            userForm = forms.StudentUserForm(request.POST)
            studentForm = forms.StudentForm(request.POST, request.FILES)
            studentemail = request.POST.get('address')
            print(studentemail)
            print(request.POST.get('country_code'))
            print(request.POST.get('mobile'))
            print(flag)
            # flag for password check user_flag for username check
            if userForm.is_valid() and studentForm.is_valid() :
                user = userForm.save(commit=False)
                user.set_password(user.password)
                user.is_active = False
                user.email = request.POST.get('address')
                user.save()
                messages.success(request, "Your account has been created.We have to sent you an email, please confirm your email in order to activate your account")

                student = studentForm.save(commit=False)
                student.user = user
                student.save()
                my_student_group, created = Group.objects.get_or_create(name='STUDENT')
                my_student_group.user_set.add(user)

                # messages.success(request, 'Student registered successfully. You can now log in.')
                #email function start #
                    # Welcome Email
                subject = "Welcome to QuizMaker"
                message = "Hello" + user.first_name + "!! \n" + "Welcome to QuizMaker!! \n" + "We have also sent you a confirmation email, please confirm your email address to activate your account. \n\nThank You"
                from_email = settings.EMAIL_HOST_USER
                to_list = [studentemail]
                send_mail(subject, message, from_email, to_list, fail_silently=True)   

                # Email address Confirmation Email

                current_site = get_current_site(request)
                email_subject = "Confirm your Email @ QuizMaker"
                message2 = render_to_string('authentication/email_confirmation.html', {
                    'name' : user.first_name,
                    'domain' : current_site.domain,
                    
                    # 'uid' : urlsafe_base64_encode(force_bytes(user.pk)),
                    # 'token' : generate_token.make_token(user),
                    
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),


                    'token': generate_token.make_token(user),


                })

                email= EmailMessage(
                    email_subject,
                    message2,
                    settings.EMAIL_HOST_USER,
                    [studentemail],
                )
                email.fail_silently = True
                email.send()

                    #email function end #
                return redirect('succes-page')  # Redirect to the success_page URL

            else:
                # print("Forms are invalid", studentForm.errors, "----",userForm.errors)
                messages.error(request, 'There was an error in the form. Please correct the errors.')

        return render(request, 'student/studentsignup.html', context=mydict)
    except Exception as e:
        print(f"An error occurred: {e}")
        return HttpResponseServerError("Internal Server Error")

def success_page_view(request):
    return render(request, 'student/succes_page.html')

def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and generate_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        messages.success(request, "Your Account has been activated")
        return redirect('student-dashboard')
    else:
        return render(request, 'activation_failed.html')
    return render(request, 'authentication/activate.html')



# coustom login view
class CustomLoginView(LoginView):
    template_name = 'student/studentlogin.html'

    def form_invalid(self, form):
        messages.error(self.request, 'Invalid username or password')
        return super().form_invalid(form)

    
def is_student(user):
    return user.groups.filter(name='STUDENT').exists()

@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def student_dashboard_view(request):
    stud = models.Student.objects.get(user_id=request.user.id)
    dict={
    'total_course':QMODEL.studentcourse.objects.all().filter(student_id=stud).count(),
    'total_exam':QMODEL.Result.objects.all().filter(student_id=stud).count(),
    }
    return render(request,'student/student_dashboard.html',context=dict)

#check whether student already appear exam and was already enrolled as well
@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def student_exam_view(request):
    exam = QMODEL.testdetails.objects.all()
    #print(exam)
    list1 = []
    for a in exam:
        
        count=0 
        stud = models.Student.objects.get(user_id=request.user.id)
        exam_id1 = a.id
        p_code=a.course_id.pk
        code=QMODEL.Course.objects.filter(id=p_code).values_list('course_code',flat=True).first()
        #print(code)
        enrolled= QMODEL.studentcourse.objects.filter(student_id=stud,course_code=code).exists()
        if enrolled:
            results = QMODEL.Result.objects.all().filter(testno=exam_id1, student_id=stud).count()
            ending_time=a.end_time
            #print(ending_time)
            # utc_datetime = datetime.datetime(2023, 11, 17, 5, 14, 10, 524020, tzinfo=timezone.utc)
            # current_time = utc_datetime.astimezone(timezone.get_current_timezone())
            current_time=timezone.localtime()
            # print(current_time)
            # print(timezone.localtime())
            if (ending_time>=current_time):
                if results == 0:
                    #courses1 = QMODEL.Course.objects.all().filter(id=exam_id1)
                    courses1 = QMODEL.testdetails.objects.all().filter(id=exam_id1)
                    #print(courses1[count])
                    courses=courses1[count]
                    list1.append(courses)
                    count=count+1
    if not list1:
         list1 = None
    return render(request, 'student/student_exam.html', {'list1': list1 })



#for enrolling in the course
@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def student_join_exam_view(request):
    student1= models.Student.objects.get(user_id=request.user.id).pk
    #print(student1)
    #student1= models.Student.objects.get(id=pk)
    courseenroll=QFORM.studentcourseForm(initial={'student_id':student1})
    if request.method == 'POST':
        courseenroll = QFORM.studentcourseForm(request.POST, initial={'student_id': student1})
        if courseenroll.is_valid():
            c=courseenroll.cleaned_data['course_code']
            course_exist=QMODEL.Course.objects.filter(course_code=c).exists()
            if not course_exist==True:
                # print("Course does not exist")
                messages.error(request, 'Course does not exist')
            else:
                course_enrolled=QMODEL.studentcourse.objects.filter(student_id=student1,course_code=c).exists()
                if course_enrolled==False:
                    courseenroll.save()
                    messages.success(request, 'Course Enrolled Successfully')
                    # return HttpResponseRedirect('/student/student-exam')
                else:
                    # print("already enrolled")
                    messages.error(request, 'already enrolled')
        else:
            # print("Form is invalid", courseenroll.errors)
            messages.error(request, 'Form is invalid')
        # return HttpResponseRedirect('/student/student-exam')
    return render(request,'student/student_join_exam.html',{'courseenroll':courseenroll})


@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def take_exam_view(request,pk):
    course=QMODEL.testdetails.objects.get(id=pk)
    total_questions=QMODEL.Question.objects.all().filter(testno=pk).count()
    questions=QMODEL.Question.objects.all().filter(testno=pk)
    testno=pk
    total_marks=0
    for q in questions:
        total_marks=total_marks + q.marks
    
    return render(request,'student/take_exam.html',{'course':course,'testno':testno,'questions':questions,'total_questions':total_questions,'total_marks':total_marks})

@login_required(login_url='studentlogin')
@user_passes_test(is_student)
# @timeout(120) 
# def start_exam_view(request,testno):
#     c = {}
#     # course=QMODEL.Course.objects.get(id=pk)
#     course=QMODEL.testdetails.objects.get(id=testno)
#     questions=QMODEL.Question.objects.all().filter(testno=testno)
#     if request.method=='POST':
#         pass
#     response= render(request,'student/start_exam.html',{'course':course,'questions':questions})
#     #response.set_cookie('course_id',course.id)
#     response.set_cookie('testno',testno)
#     return response
# new code
@csrf_exempt
@timeout(120)  # Set a timeout of 2 minutes (120 seconds)
def start_exam_view(request, testno):
    try:
        # Fetch the course details and questions
        course = QMODEL.testdetails.objects.get(id=testno)
        questions = QMODEL.Question.objects.filter(testno=testno)

        if request.method == 'POST':
            # Handle POST requests if needed
            pass

        # Render the exam start page with course and questions
        response = render(request, 'student/start_exam.html', {'course': course, 'questions': questions})
        response.set_cookie('testno', testno)
        return response

    except QMODEL.testdetails.DoesNotExist:
        # Handle the case where the specified testno does not exist
        return HttpResponse("Test details not found.", status=404)

    except Exception as e:
        # Handle other exceptions, log them, and provide an appropriate response
        print(f"An error occurred: {e}")
        return HttpResponse("An error occurred.", status=500)

@login_required(login_url='studentlogin')
@user_passes_test(is_student)
@csrf_exempt
@timeout(120) 
def calculate_marks_view(request):
    try:
        # if request.COOKIES.get('course_id') is not None:
        #     course_id = request.COOKIES.get('course_id')
        #     course=QMODEL.Course.objects.get(id=course_id)
        if request.COOKIES.get('testno') is not None:
            course_id1 = request.COOKIES.get('testno')
            #course=QMODEL.Course.objects.get(id=course_id)
            course_id=QMODEL.testdetails.objects.all().filter(id=course_id1).values_list('id',flat=True).first()
            # print(course_id)
            total_marks=0
            #questions=QMODEL.Question.objects.all().filter(course_id=course)
            questions=QMODEL.Question.objects.all().filter(testno=course_id1)
            for i in range(len(questions)):
                
                selected_ans = request.COOKIES.get(str(i+1))
                actual_answer = questions[i].answer
                if selected_ans == actual_answer:
                    total_marks = total_marks + questions[i].marks
            student = models.Student.objects.get(user_id=request.user.id)
            result = QMODEL.Result()
            result.marks=total_marks
            result.testno=course_id
            result.student=student
            result.save()
            # messages.success(request, 'Exam submitted successfully. View your result in the result section.')
            return HttpResponseRedirect('success-page1')
        else:
            messages.error(request, 'Error submitting exam. Please try again.')

        # return HttpResponseRedirect('student-dashboard')
    except Exception as e:
        print(e)

def success_page1_view(request):
    return render(request, 'student/success_page1.html')

 #not using it anywhere       
@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def view_result_view(request):
    courses=QMODEL.Course.objects.all()
    return render(request,'student/view_result.html',{'courses':courses})
    
#modified
@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def check_marks_view(request,pk):
    #course=QMODEL.testdetails.objects.all().get(course_id=pk).pk
    student = models.Student.objects.get(user_id=request.user.id)
    results= QMODEL.Result.objects.all().filter(testno=pk,student=student,status=1)
    return render(request,'student/check_marks.html',{'results':results})

#new
@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def check_marks0_view(request,pk):
    courses = QMODEL.testdetails.objects.all().filter(course_id=pk)
    return render(request,'student/check_marks0.html',{'courses':courses})
    

@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def student_marks_view(request):
    # #course=QMODEL.Course.objects.get(id=pk)
    # student = models.Student.objects.get(user_id=request.user.id)
    # course= QMODEL.Course.objects.all().filter(student=student).filter(course=course)
    # return render(request,'student/student_marks.html',{'course':course})
    exam = QMODEL.Course.objects.all()
    #print(exam)
    list1 = []
    for a in exam:
        count=0 
        
        stud = models.Student.objects.get(user_id=request.user.id)
        exam_id1 = a.id
        code=a.course_code
        enrolled= QMODEL.studentcourse.objects.filter(student_id=stud,course_code=code).exists()
        if enrolled:
            # results = QMODEL.Result.objects.all().filter( student_id=stud).count()
            # if results == 1:
                courses1 = QMODEL.Course.objects.all().filter(id=exam_id1)
                #print(courses1[count])
                courses=courses1[count]
                list1.append(courses)
                count=count+1
    if not list1:
         list1 = None
    return render(request,'student/student_marks.html',{'list1':list1})

