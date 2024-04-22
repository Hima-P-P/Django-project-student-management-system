from django.contrib import admin
from adminstration.models import AdminHOD,Staffs,Courses,Subjects,Students,Attendance,AttendanceReport,LeaveReportStudent
from adminstration.models import LeaveReportStaff,FeedbackStudent,FeedbackStaff,NotificationStudent,NotificationStaff,CustomUser
from django.contrib.auth.admin import UserAdmin

# Register your models here.
class UserModel(UserAdmin):
    pass
admin.site.register(CustomUser,UserModel)
admin.site.register(AdminHOD)
admin.site.register(Staffs)
admin.site.register(Courses)
admin.site.register(Subjects)
admin.site.register(Students)
admin.site.register(Attendance)
admin.site.register(AttendanceReport)
admin.site.register(LeaveReportStudent)
admin.site.register(LeaveReportStaff)
admin.site.register(FeedbackStudent)
admin.site.register(FeedbackStaff)
admin.site.register(NotificationStudent)
admin.site.register(NotificationStaff)

