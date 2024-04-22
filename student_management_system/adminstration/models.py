from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.


class CustomUser(AbstractUser):
    gender=models.CharField(max_length=200)
    address=models.TextField(default="")
    phone=models.CharField(max_length=200,default="")
    qualification=models.CharField(max_length=200)
    date_of_birth=models.DateField()
    is_admin=models.BooleanField(default=False)
    is_staff=models.BooleanField(default=False)
    is_student=models.BooleanField(default=False)

class SessionYearModel(models.Model):
    id=models.AutoField(primary_key=True)
    session_start_year=models.DateField()
    session_end_year=models.DateField()
    
  
class AdminHOD(models.Model):
    id=models.AutoField(primary_key=True)
    admin=models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)


class Courses(models.Model):
    id=models.AutoField(primary_key=True)
    course_name=models.CharField(max_length=100)
    desc=models.TextField()
    image=models.ImageField(upload_to='Courses/image',null=True,blank=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    objects=models.Manager()

    def __str__(self):
        return self.course_name
    
class Staffs(models.Model):
    id=models.AutoField(primary_key=True)
    staff_name=models.CharField(max_length=200)
    course_id=models.OneToOneField(Courses,on_delete=models.CASCADE) 
    admin=models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    desc=models.CharField(max_length=100)
    image=models.ImageField(upload_to='Staffs/image',null=True,blank=True)
    gender=models.CharField(max_length=200)
    address=models.TextField(default="")
    phone=models.CharField(max_length=200,default="")
    email=models.TextField(default="")
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    objects=models.Manager()
    def __str__(self):
        return self.staff_name
class Subjects(models.Model):
    id=models.AutoField(primary_key=True)
    subject_name=models.CharField(max_length=100)
    course_id=models.ForeignKey(Courses,on_delete=models.CASCADE) 
    staff_id=models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    image=models.ImageField(upload_to='Subjects/image',null=True,blank=True)
    desc=models.TextField()
    outline_1=models.CharField(max_length=100)
    content_1=models.TextField()
    outline_2=models.CharField(max_length=100)
    content_2=models.TextField()
    outline_3=models.CharField(max_length=100)
    content_3=models.TextField()
    outline_4=models.CharField(max_length=100)
    content_4=models.TextField()
    outline_5=models.CharField(max_length=100)
    content_5=models.TextField()
    duration=models.CharField(max_length=50)
    totalfee=models.IntegerField()
    no_of_installment=models.IntegerField()
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    objects=models.Manager()

    def __str__(self):
        return self.subject_name
    
class Students(models.Model):
    id=models.AutoField(primary_key=True)
    student_name=models.CharField(max_length=200)
    admin=models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    course_id=models.ForeignKey(Courses,on_delete=models.CASCADE)#default=1
    subject_id=models.ForeignKey(Subjects,on_delete=models.CASCADE)#default=1
    image=models.ImageField(upload_to='Students/image',null=True,blank=True)
    gender=models.CharField(max_length=200)
    address=models.TextField(default="")
    email=models.TextField(default="")
    phone=models.CharField(max_length=200,default="")
    qualification=models.CharField(max_length=200)
    date_of_birth=models.DateField()
    session_year_id=models.ForeignKey(SessionYearModel,on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    objects=models.Manager()
    def __str__(self):
        return self.student_name


class Attendance(models.Model):
    id=models.AutoField(primary_key=True)
    subject_id=models.ForeignKey(Subjects,on_delete=models.CASCADE)
    attendance_date=models.DateField()
    created_at=models.DateTimeField(auto_now_add=True)
    session_year_id=models.ForeignKey(SessionYearModel,on_delete=models.CASCADE)
    updated_at=models.DateTimeField(auto_now_add=True)

class AttendanceReport(models.Model):
    id=models.AutoField(primary_key=True)
    students_id=models.ForeignKey(Students,on_delete=models.CASCADE)
    attendance_id=models.ForeignKey(Attendance,on_delete=models.CASCADE)
    status=models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)

class LeaveReportStudent(models.Model):
    id=models.AutoField(primary_key=True)
    students_id=models.ForeignKey(Students,on_delete=models.CASCADE)
    leave_date=models.CharField(max_length=100)
    leave_message=models.TextField()
    leave_status=models.IntegerField(default=0)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)


class LeaveReportStaff(models.Model):
    id=models.AutoField(primary_key=True)
    staff_id=models.ForeignKey(Staffs,on_delete=models.CASCADE)
    leave_date=models.CharField(max_length=100)
    leave_message=models.TextField()
    leave_status=models.IntegerField(default=0)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)

class FeedbackStudent(models.Model):
    id=models.AutoField(primary_key=True)
    students_id=models.ForeignKey(Students,on_delete=models.CASCADE)
    feedback=models.TextField()
    feedback_reply=models.TextField()
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)

class FeedbackStaff(models.Model):
    id=models.AutoField(primary_key=True)
    staff_id=models.ForeignKey(Staffs,on_delete=models.CASCADE)
    feedback=models.TextField()
    feedback_reply=models.TextField()
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)

class StudentResult(models.Model):
    id=models.AutoField(primary_key=True)
    student_id=models.ForeignKey(Students,on_delete=models.CASCADE)    
    subject_id=models.ForeignKey(Subjects,on_delete=models.CASCADE)
    subject_exam_marks=models.FloatField(default=0)
    subject_assignment_marks=models.FloatField(default=0)    
    created_at=models.DateField(auto_now_add=True)
    updated_at=models.DateField(auto_now_add=True)




































class NotificationStudent(models.Model):
    id=models.AutoField(primary_key=True)
    student_id=models.ForeignKey(Students,on_delete=models.CASCADE)
    message=models.TextField()
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)

class NotificationStaff(models.Model):
    id=models.AutoField(primary_key=True)
    staff_id=models.ForeignKey(Staffs,on_delete=models.CASCADE)
    message=models.TextField()
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)




            
            


    



















