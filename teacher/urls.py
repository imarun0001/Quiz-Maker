from django.urls import path
from teacher import views
from django.contrib.auth.views import LoginView
from django.contrib.auth.views import (
    LogoutView, 
    PasswordResetView, 
    PasswordResetDoneView, 
    PasswordResetConfirmView,
    PasswordResetCompleteView
)


urlpatterns = [
path('teacherclick', views.teacherclick_view),
path('teacherlogin', LoginView.as_view(template_name='teacher/teacherlogin.html'),name='teacherlogin'),
path('teachersignup', views.teacher_signup_view,name='teachersignup'),
path('teacher-dashboard', views.teacher_dashboard_view,name='teacher-dashboard'),
path('teacher-exam', views.teacher_exam_view,name='teacher-exam'),
path('teacher-add-exam', views.teacher_add_exam_view,name='teacher-add-exam'),
path('teacher-view-exam', views.teacher_view_exam_view,name='teacher-view-exam'),
path('delete-exam/<int:pk>', views.delete_exam_view,name='delete-exam'),


path('teacher-question', views.teacher_question_view,name='teacher-question'),
path('teacher-add-question', views.teacher_add_question_view,name='teacher-add-question'),
path('teacher-view-question', views.teacher_view_question_view,name='teacher-view-question'),
path('see-question/<int:pk>', views.see_question_view,name='see-question'),
path('remove-question/<int:pk>', views.remove_question_view,name='remove-question'),

path('teacher-view-student/<str:course_code>', views.teacher_view_student_view,name='teacher-view-student'),

path('teacher-result', views.teacher_result_view,name='teacher-result'),

path('teacher-release-result',views.teacher_release_result_view,name='teacher-release-result'),

path('teacher-release-result1/<int:pk>',views.teacher_release_result1_view,name='teacher-release-result1'),

path('teacher-release/<int:pk>',views.teacher_release_view,name='teacher-release'),
path('teacher-view-result',views.teacher_view_result_view,name='teacher-view-result'),

path('teacher-view-result1/<int:pk>',views.teacher_view_result1_view,name='teacher-view-result1'),
path('teacher-view-result2/<int:pk>',views.teacher_view_result2_view,name='teacher-view-result2'),

path('see-question0/<int:pk>',views.see_question0_view,name='see-question0'),

path('update-testdetails/<int:pk>',views.update_testdetails_view,name='update-testdetails'),

# success page
path('succes-page-teacher', views.success_page_view_teacher, name='succes-page-teacher'),
# Check 
path('check_username_teacher', views.check_username_teacher, name='check_username_teacher'),
path('check_useremail_teacher', views.check_useremail_teacher, name='check_useremail_teacher'),
path('check_mobile_teacher', views.check_mobile_teacher, name='check_mobile_teacher'),
path('check_password_teacher', views.check_password_strength_teacher, name='check_password_teacher'),
#Forgot Password
path('teacher-password-reset', 
        PasswordResetView.as_view(
            template_name='teacher/users/t_password_reset.html',
            html_email_template_name='teacher/users/t_password_reset_email.html'
        ),
        name='teacher-password-reset'
    ),
    path('teacher-password-reset/done/', PasswordResetDoneView.as_view(template_name='teacher/users/t_password_reset_done.html'),name='teacher-password-reset-done'),
    path('teacher-password-reset-confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(template_name='teacher/users/t_password_reset_confirm.html'),name='teacher-password-reset-confirm'),
    path('teacher-password-reset-complete/',PasswordResetCompleteView.as_view(template_name='teacher/users/t_password_reset_complete.html'),name='teacher-password-reset-complete'),

]