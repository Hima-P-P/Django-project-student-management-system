"""
URL configuration for student_management_system project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from adminstration import views
app_name='adminstration'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home,name='home'),
    path('allsubjects/<int:p>',views.allsubjects,name='allsubjects'),
    path('alldetails/<int:p>',views.alldetails,name='alldetails'),
    path('adminhome',views.adminhome,name='home_content'), 
    path('manage_staff',views.manage_staff,name='manage_staff'),
    path('manage_student',views.manage_student,name='manage_student'),
    path('manage_course',views.manage_course,name='manage_course'),
    path('manage_subject',views.manage_subject,name='manage_subject'),
    path('edit_staff/<int:p>',views.edit_staff,name='edit_staff'),
    path('edit_student/<int:p>',views.edit_student,name='edit_student'),
    path('edit_course/<int:p>',views.edit_course,name='edit_course'),
    path('edit_subject/<int:p>',views.edit_subject,name='edit_subject'),
    path('staff_home',views.staff_home,name='staff_home'),
    path('student_home',views.student_home,name='student_home'),
    path('manage_session',views.manage_session,name='manage_session'),
    path('add_session_save',views.add_session_save,name='add_session_save'),
    path('staff_take_attendance',views.staff_take_attendance,name='staff_take_attendance'),
    path('get_students',views.get_students,name='get_students'),
    path('get_attendance_dates',views.get_attendance_dates,name='get_attendance_dates'),
    path('get_attendance_student',views.get_attendance_student,name='get_attendance_student'),
    path('save_attendance_data',views.save_attendance_data,name='save_attendance_data'),
    path('save_updateattendance_data',views.save_updateattendance_data,name='save_updateattendance_data'),
    path('staff_update_attendance',views.staff_update_attendance,name='staff_update_attendance'),
    path('student_view_attendance',views.student_view_attendance,name='student_view_attendance'),
    path('student_view_attendance_post',views.student_view_attendance_post,name='student_view_attendance_post'),
    path('staff_apply_leave',views.staff_apply_leave,name='staff_apply_leave'),
    path('staff_apply_leave_save',views.staff_apply_leave_save,name='staff_apply_leave_save'),
    path('staff_feedback',views.staff_feedback,name='staff_feedback'),
    path('staff_feedback_save',views.staff_feedback_save,name='staff_feedback_save'),
    path('student_apply_leave',views.student_apply_leave,name='student_apply_leave'),
    path('student_apply_leave_save',views.student_apply_leave_save,name='student_apply_leave_save'), 
    path('student_feedback',views.student_feedback,name='student_feedback'),
    path('student_feedback_save',views.student_feedback_save,name='student_feedback_save'),
    path('student_feedback_message',views.student_feedback_message,name='student_feedback_message'),
    path('student_feedback_message_replied',views.student_feedback_message_replied,name='student_feedback_message_replied'),
    path('staff_feedback_message',views.staff_feedback_message,name='staff_feedback_message'),
    path('staff_feedback_message_replied',views.staff_feedback_message_replied,name='staff_feedback_message_replied'),
    path('student_leave_view',views.student_leave_view,name='student_leave_view'),
    path('student_approve_leave/<str:leave_id>',views.student_approve_leave,name='student_approve_leave'),
    path('student_disapprove_leave/<str:leave_id>',views.student_disapprove_leave,name='student_disapprove_leave'),
    path('staff_leave_view',views.staff_leave_view,name='staff_leave_view'), 
    path('staff_approve_leave/<str:leave_id>',views.staff_approve_leave,name='staff_approve_leave'),
    path('staff_disapprove_leave/<str:leave_id>',views.staff_disapprove_leave,name='staff_disapprove_leave'),
    path('staff_add_result',views.staff_add_result,name='staff_add_result'),
    path('save_student_result',views.save_student_result,name='save_student_result'),
    path('student_view_result',views.student_view_result,name='student_view_result'),




    
    
    
    
















    # path('edit_staff/<str:staff_id>',views.edit_staff,name='edit_staff'),
    # path('edit_staff_save',views.edit_staff_save,name='edit_staff_save'),

    






    path('login',views.user_login,name="login"),
  
    # path('login',views.login,name='login'),
    # path('doLogin',views.doLogin,name='login'),
    # path('get_user_details',views.GetUserDetails),
    path('logout',views.user_logout,name="logout"),
    path('adminsignup',views.adminsignup,name="adminsignup"),
    path('staffsignup',views.staffsignup,name="staffsignup"),
    path('studentsignup',views.studentsignup,name="studentsignup"),


    # path('studenthome',views.studenthome,name="studenthome"),
    # path('studentsignup',views.studentsignup,name="studentsignup"),
    # path('teacherhome',views.teacherhome,name="teacherhome"),
    # path('teachersignup',views.teachersignup,name="teachersignup"),


]
