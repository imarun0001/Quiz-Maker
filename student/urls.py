from django.urls import path
from student import views
from django.contrib.auth.views import LoginView
from django.contrib.auth.views import (
    LogoutView, 
    PasswordResetView, 
    PasswordResetDoneView, 
    PasswordResetConfirmView,
    PasswordResetCompleteView
)


urlpatterns = [
path('studentclick', views.studentclick_view),
path('studentlogin', LoginView.as_view(template_name='student/studentlogin.html'),name='studentlogin'),
path('studentlogin/', views.CustomLoginView.as_view(), name='studentlogin'),
path('studentsignup', views.student_signup_view,name='studentsignup'),
path('student-dashboard', views.student_dashboard_view,name='student-dashboard'),
path('student-exam', views.student_exam_view,name='student-exam'),
path('take-exam/<int:pk>', views.take_exam_view,name='take-exam'),
path('start-exam/<int:testno>', views.start_exam_view,name='start-exam'),

path('student-join-exam', views.student_join_exam_view,name='student-join-exam'),

path('calculate-marks', views.calculate_marks_view,name='calculate-marks'),
path('view-result', views.view_result_view,name='view-result'),

path('check-marks0/<int:pk>',views.check_marks0_view,name='check-marks0'),

path('check-marks/<int:pk>', views.check_marks_view,name='check-marks'),
path('student-marks', views.student_marks_view,name='student-marks'),
# Check 
path('check_username', views.check_username, name='check_username'),
path('check_useremail', views.check_useremail, name='check_useremail'),
path('check_mobile', views.check_mobile, name='check_mobile'),
path('check_password', views.check_password_strength, name='check_password'),
#success page
path('succes-page', views.success_page_view, name='succes-page'),
path('success-page1', views.success_page1_view, name='success-page1'),
#email activation page
path('activate/<str:uidb64>/<str:token>', views.activate, name='activate'),
#Forgot Password
path('password-reset', 
        PasswordResetView.as_view(
            template_name='student/users/password_reset.html',
            html_email_template_name='student/users/password_reset_email.html'
        ),
        name='password-reset'
    ),
    path('password-reset/done/', PasswordResetDoneView.as_view(template_name='student/users/password_reset_done.html'),name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(template_name='student/users/password_reset_confirm.html'),name='password_reset_confirm'),
    path('password-reset-complete/',PasswordResetCompleteView.as_view(template_name='student/users/password_reset_complete.html'),name='password_reset_complete'),

]