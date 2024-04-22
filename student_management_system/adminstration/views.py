from django.shortcuts import render,redirect
from django.http import HttpResponse,HttpResponseRedirect
from adminstration.models import Courses,Staffs,Students,Subjects,SessionYearModel,LeaveReportStaff,FeedbackStaff,LeaveReportStudent,FeedbackStudent,Attendance,AttendanceReport,StudentResult
from django.contrib.auth import logout,login,authenticate
# from adminstration.EmailBackEnd import EmailBackEnd
from adminstration.models import CustomUser
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from adminstration.forms import staffform,studentform,courseform,subjectform
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from django.core import serializers
import datetime





# Create your views here.



def home(request):
    c=Courses.objects.all()
    t=Staffs.objects.all()
    return render(request,'home.html',{'c':c,'t':t})

def allsubjects(request,p):
    c=Courses.objects.get(id=p)
    p=Subjects.objects.filter(course_id=c)
    return render(request,'subjects.html',{'c':c,'p':p})

def alldetails(request,p):
        subject=Subjects.objects.get(id=p)
        return render(request,'details.html',{'p':subject})



@login_required
def adminhome(request):
    staff_count=Staffs.objects.all().count()
    student_count=Students.objects.all().count()
    course_count=Courses.objects.all().count()
    subject_count=Subjects.objects.all().count()

    course_all=Courses.objects.all()
    course_name_list=[]
    subject_count_list=[]
    student_count_list_in_course=[]

    for course in course_all:
       subjects=Subjects.objects.filter(course_id=course.id).count()
       students=Students.objects.filter(course_id=course.id).count()
       course_name_list.append(course.course_name)
       subject_count_list.append(subjects)
       student_count_list_in_course.append(students)

    subjects_all=Subjects.objects.all()
    subject_list=[]
    student_count_list_in_subject=[]
    for subject in subjects_all:
       course=Courses.objects.get(id=subject.course_id.id)
      #  student_count=Students.objects.filter(course_id=course.id).count()
       subject_list.append(subject.subject_name)
       student_count_list_in_subject.append(student_count)

    staffs=Staffs.objects.all()
    attendance_present_list_staff=[]
    attendance_absent_list_staff=[]
    staff_name_list=[]

    for staff in staffs:
       subject_ids=Subjects.objects.filter(staff_id=staff.admin.id)
       attendance=Attendance.objects.filter(subject_id__in=subject_ids).count()
       leaves=LeaveReportStaff.objects.filter(staff_id=staff.id,leave_status=1).count()
       attendance_present_list_staff.append(attendance)
       attendance_absent_list_staff.append(leaves)
       staff_name_list.append(staff.admin.username)

    return render(request,'home_content.html',{"student_count":student_count,"staff_count":staff_count,"subject_count":subject_count,"course_count":course_count,"course_name_list":course_name_list,"subject_count_list":subject_count_list,"student_count_list_in_course":student_count_list_in_course,"student_count_list_in_subject":student_count_list_in_subject,"subject_list":subject_list,"staff_name_list":staff_name_list,"attendance_present_list_staff":attendance_present_list_staff,"attendance_absent_list_staff":attendance_absent_list_staff})

@login_required
def student_home(request):
    student_obj=Students.objects.get(admin=request.user.id)
    attendance_total=AttendanceReport.objects.filter(students_id=student_obj).count()
    attendance_present=AttendanceReport.objects.filter(students_id=student_obj,status=True).count()
    attendance_absent=AttendanceReport.objects.filter(students_id=student_obj,status=False).count()
    course=Courses.objects.get(id=student_obj.course_id.id)
    
    return render(request,'student_template/student_home.html',{"total_attendance":attendance_total,"attendance_absent":attendance_absent,"attendance_present":attendance_present})


@login_required
def staff_home(request):
    #for fetch all student under staff
    subjects=Subjects.objects.filter(staff_id=request.user.id)    
    course_id_list=[]
    for subject in subjects:
       course=Courses.objects.get(id=subject.course_id.id)
       course_id_list.append(course.id)
       
    final_course=[]
   #  #removing duplicate course id
    for course_id in course_id_list:
      if course_id not in final_course:
         final_course.append(course_id)

    students_count=Students.objects.filter(course_id__in=final_course).count()
   
   #fetch all attendance Count
    attendance_count=Attendance.objects.filter(subject_id__in=subjects).count()

   #fetch_all_approve leave
    staff=Staffs.objects.get(admin=request.user.id)
    leave_count=LeaveReportStaff.objects.filter(staff_id=staff.id,leave_status=1).count()
    subject_count=subjects.count()

    return render(request,'staff_template/staff_home.html',{"students_count":students_count,"attendance_count":attendance_count,"leave_count":leave_count,"subject_count":subject_count})

   
      

def manage_staff(request):
   staffs=Staffs.objects.all()
   return render(request,'manage_staff.html',{"staffs":staffs})
def manage_student(request):
   students=Students.objects.all()
   return render(request,'manage_student.html',{"students":students})
def manage_course(request):
   courses=Courses.objects.all()
   return render(request,'manage_course.html',{"courses":courses})
def manage_subject(request):
   subjects=Subjects.objects.all()
   return render(request,'manage_subject.html',{"subjects":subjects})


def edit_staff(request,p):  
    staff=Staffs.objects.get(id=p)
    form=staffform(instance=staff)
    if(request.method=="POST"):
        form=staffform(request.POST,request.FILES,instance=staff)
        if form.is_valid():
            form.save()
            return manage_staff(request)
    return render(request,'edit_staff.html',{'form':form})

def edit_student(request,p):  
    student=Students.objects.get(id=p)
    form=studentform(instance=student)
    if(request.method=="POST"):
        form=studentform(request.POST,request.FILES,instance=student)
        if form.is_valid():
            form.save()
            return manage_student(request)
    return render(request,'edit_student.html',{'form':form})

def edit_course(request,p):  
    course=Courses.objects.get(id=p)
    form=courseform(instance=course)
    if(request.method=="POST"):
        form=courseform(request.POST,request.FILES,instance=course)
        if form.is_valid():
            form.save()
            return manage_course(request)
    return render(request,'edit_course.html',{'form':form})

def edit_subject(request,p):  
    subject=Subjects.objects.get(id=p)
    form=subjectform(instance=subject)
    if(request.method=="POST"):
        form=subjectform(request.POST,request.FILES,instance=subject)
        if form.is_valid():
            form.save()
            return manage_subject(request)
    return render(request,'edit_subject.html',{'form':form})



        

def adminsignup(request):
    if(request.method=="POST"):
        f=request.POST['f']
        u=request.POST['u']
        p=request.POST['p']
        cp=request.POST['cp']
        n=request.POST['n']
        e=request.POST['e']
        a=request.POST['a']
        d=request.POST['d']
        g=request.POST['g']

        if(p==cp):
         u=CustomUser.objects.create_user(first_name=f,username=u,password=p,phone=n,email=e,address=a,date_of_birth=d,gender=g)
         u.is_admin=True
         u.save()
         return redirect('adminstration:login')
        else:
            return HttpResponse("Password not matching")
    return render(request,'adminsignup.html')
def staffsignup(request):
    if(request.method=="POST"):
        f=request.POST['f']
        u=request.POST['u']
        p=request.POST['p']
        cp=request.POST['cp']
        n=request.POST['n']
        e=request.POST['e']
        a=request.POST['a']
        d=request.POST['d']
        g=request.POST['g']
        

        if(p==cp):
         u=CustomUser.objects.create_user(first_name=f,username=u,password=p,phone=n,email=e,address=a,date_of_birth=d,gender=g)
         u.is_staff=True
         u.save()
         return redirect('adminstration:login')
        else:
            return HttpResponse("Password not matching")
    return render(request,'staffsignup.html')

def studentsignup(request):
    if(request.method=="POST"):
        f=request.POST['f']
        u=request.POST['u']
        p=request.POST['p']
        cp=request.POST['cp']
        n=request.POST['n']
        e=request.POST['e']
        a=request.POST['a']
        d=request.POST['d']
        g=request.POST['g']
        

        if(p==cp):
         u=CustomUser.objects.create_user(first_name=f,username=u,password=p,phone=n,email=e,address=a,date_of_birth=d,gender=g)
         u.is_student=True
         u.save()
         return redirect('adminstration:login')
        else:
            return HttpResponse("Password not matching")
    return render(request,'studentsignup.html')



def user_login(request):
   if (request.method=="POST"):
      name=request.POST['u']
      pas1=request.POST['p']
      user=authenticate(username=name,password=pas1)
      if user and user.is_admin==True:
         login(request,user)
         return redirect('adminstration:home_content')
      elif user and user.is_staff==True:
         login(request,user)
         return HttpResponseRedirect(reverse("adminstration:staff_home"))
      elif user and user.is_student==True:
         login(request,user)
         return HttpResponseRedirect(reverse("adminstration:student_home"))
      
      else:
         messages.error(request,'invalid credentails')
   return render(request,'login.html')
@login_required
def user_logout(request):
   logout(request)
   return home(request)

def manage_session(request):
   return render(request,'manage_session.html')
def add_session_save(request):
   if request.method!="POST":
      return HttpResponseRedirect(reverse("adminstration:manage_session"))
   else:
      session_start_year=request.POST.get("session_start")
      session_end_year=request.POST.get("session_end")
      try:
         sessionyear=SessionYearModel(session_start_year=session_start_year,session_end_year=session_end_year)
         sessionyear.save()
         messages.success(request,"Successfully Added Session")
         return HttpResponseRedirect(reverse("adminstration:manage_session"))

      except:
         messages.error(request,"Failed to Add Session")
         return HttpResponseRedirect(reverse("adminstration:manage_session"))
      


def staff_take_attendance(request):
   subjects=Subjects.objects.filter(staff_id=request.user.id)
   session_years=SessionYearModel.objects.all()
   return render(request,"staff_template/staff_take_attendance.html",{'subjects':subjects,'session_years':session_years})


@csrf_exempt
def get_students(request):
   subject_id=request.POST.get("subject")
   session_year=request.POST.get("session_year")

   subject=Subjects.objects.get(id=subject_id)
   session_model=SessionYearModel.objects.get(id=session_year)
   students=Students.objects.filter(course_id=subject.course_id,session_year_id=session_model)
   list_data=[]
   for student in students:
      data_small={"id":student.id,"name":student.student_name}
      list_data.append(data_small)
   return JsonResponse(json.dumps(list_data),content_type="application/json",safe=False)

@csrf_exempt
def save_attendance_data(request):
 student_ids=request.POST.get("student_ids")
 subject_id=request.POST.get("subject_id")
 attendance_date=request.POST.get("attendance_date")
 session_year_id=request.POST.get("session_year_id")

 print(student_ids)
 subject_model=Subjects.objects.get(id=subject_id)
 session_model=SessionYearModel.objects.get(id=session_year_id)
 json_student=json.loads(student_ids)
 try:
  attendance=Attendance(subject_id=subject_model,attendance_date=attendance_date,session_year_id=session_model)
  attendance.save()
 
  for stud in json_student:
   student=Students.objects.get(id=stud['id'])
   attendance_report=AttendanceReport(students_id=student,attendance_id=attendance,status=stud['status'])
   attendance_report.save()
  return HttpResponse("OK")
 except:
  return HttpResponse("OK")



def staff_update_attendance(request):
   # subjects=Subjects.objects.all()
   subjects=Subjects.objects.filter(staff_id=request.user.id)
   session_year_id=SessionYearModel.objects.all()
   return render(request,"staff_template/staff_update_attendance.html",{"subjects":subjects,"session_year_id":session_year_id})

@csrf_exempt
def get_attendance_dates(request):
   subject=request.POST.get("subject")
   session_year_id=request.POST.get("session_year_id")
   subject_obj=Subjects.objects.get(id=subject)
   session_year_obj=SessionYearModel.objects.get(id=session_year_id)
   attendance=Attendance.objects.filter(subject_id=subject_obj,session_year_id=session_year_obj)
   attendance_obj=[]
   for attendance_single in attendance:   
      data={"id":attendance_single.id,"attendance_date":str(attendance_single.attendance_date),"session_year_id":attendance_single.session_year_id.id}
      attendance_obj.append(data)
   return JsonResponse(json.dumps(attendance_obj),safe=False)

@csrf_exempt
def get_attendance_student(request):
   attendance_date=request.POST.get("attendance_date")
   attendance=Attendance.objects.get(id=attendance_date)
   attendance_data=AttendanceReport.objects.filter(attendance_id=attendance)
   list_data=[]
   for student in attendance_data:
      data_small={"id":student.students_id.admin.id,"name":student.students_id.admin.first_name,"status":student.status}
      list_data.append(data_small)
   return JsonResponse(json.dumps(list_data),content_type="application/json",safe=False)


@csrf_exempt
def save_updateattendance_data(request):
 student_ids=request.POST.get("student_ids")
 attendance_date=request.POST.get("attendance_date")
 attendance=Attendance.objects.get(id=attendance_date)

 json_student=json.loads(student_ids)
 try:
  for stud in json_student:
   student=Students.objects.get(id=stud['id'])
   attendance_report=AttendanceReport.objects.get(students_id=student,attendance_id=attendance)
   attendance_report.status=stud['status']
   attendance_report.save()
  return HttpResponse("OK")
 except:
  return HttpResponse("OK")



def student_view_attendance(request):
   student=Students.objects.get(admin=request.user.id)
   course=student.course_id
   subjects=Subjects.objects.filter(course_id=course)
   return render(request,"student_template/student_view_attendance.html",{"subjects":subjects})

def student_view_attendance_post(request):
   subject_id=request.POST.get("subject")
   start_date=request.POST.get("start_date")
   end_date=request.POST.get("end_date")

   start_data_parse=datetime.datetime.strptime(start_date,"%Y-%m-%d").date()
   end_data_parse=datetime.datetime.strptime(end_date,"%Y-%m-%d").date()
   subject_obj=Subjects.objects.get(id=subject_id)
   user_object=CustomUser.objects.get(id=request.user.id)
   stud_obj=Students.objects.get(admin=user_object)

   attendance=Attendance.objects.filter(attendance_date__range=(start_data_parse,end_data_parse),subject_id=subject_obj)
   attendance_reports=AttendanceReport.objects.filter(attendance_id__in=attendance,students_id=stud_obj)
   return render(request,"student_template/student_attendance_data.html",{"attendance_reports":attendance_reports})

def staff_apply_leave(request):
   staff_obj=Staffs.objects.get(admin=request.user.id)
   leave_data=LeaveReportStaff.objects.filter(staff_id=staff_obj)
   return render(request,'staff_template/staff_apply_leave.html',{"leave_data":leave_data})

def staff_apply_leave_save(request):
   if request.method!="POST":
     return HttpResponseRedirect(reverse("adminstration:staff_apply_leave"))
   else:
      leave_date=request.POST.get("leave_date")
      leave_msg=request.POST.get("leave_msg")

      staff_obj=Staffs.objects.get(admin=request.user.id)
      try:
       leave_report=LeaveReportStaff(staff_id=staff_obj,leave_date=leave_date,leave_message=leave_msg,leave_status=0)
       leave_report.save()
       messages.success(request,"Successfully Applied for Leave")
       return HttpResponseRedirect(reverse("adminstration:staff_apply_leave"))
      except:
       messages.error(request,"Failed to Apply for Leave")
       return HttpResponseRedirect(reverse("adminstration:staff_apply_leave"))

def staff_feedback(request):
   staff_id=Staffs.objects.get(admin=request.user.id)
   feedback_data=FeedbackStaff.objects.filter(staff_id=staff_id)
   return render(request,'staff_template/staff_feedback.html',{"feedback_data":feedback_data})

def staff_feedback_save(request):
   if request.method!="POST":
     return HttpResponseRedirect(reverse("adminstration:staff_feedback_save"))
   else:
      feedback_msg=request.POST.get("feedback_msg")
      staff_obj=Staffs.objects.get(admin=request.user.id)
      try:
       feedback=FeedbackStaff(staff_id=staff_obj,feedback=feedback_msg,feedback_reply="")
       feedback.save()
       messages.success(request,"Successfully Sent Feedback")
       return HttpResponseRedirect(reverse("adminstration:staff_feedback"))
      except:
       messages.error(request,"Failed to Send Feedback")
       return HttpResponseRedirect(reverse("adminstration:staff_feedback"))




def student_apply_leave(request):
   student_obj=Students.objects.get(admin=request.user.id)
   leave_data=LeaveReportStudent.objects.filter(students_id=student_obj)
   return render(request,'student_template/student_apply_leave.html',{"leave_data":leave_data})

def student_apply_leave_save(request):
   if request.method!="POST":
     return HttpResponseRedirect(reverse("adminstration:student_apply_leave"))
   else:
      leave_date=request.POST.get("leave_date")
      leave_msg=request.POST.get("leave_msg")

      student_obj=Students.objects.get(admin=request.user.id)
      try:
       leave_report=LeaveReportStudent(students_id=student_obj,leave_date=leave_date,leave_message=leave_msg,leave_status=0)
       leave_report.save()
       messages.success(request,"Successfully Applied for Leave")
       return HttpResponseRedirect(reverse("adminstration:student_apply_leave"))
      except:
       messages.error(request,"Failed to Apply for Leave")
       return HttpResponseRedirect(reverse("adminstration:student_apply_leave"))

def student_feedback(request):
   student_id=Students.objects.get(admin=request.user.id)
   feedback_data=FeedbackStudent.objects.filter(students_id=student_id)
   return render(request,'student_template/student_feedback.html',{"feedback_data":feedback_data})

def student_feedback_save(request):
   if request.method!="POST":
     return HttpResponseRedirect(reverse("adminstration:student_feedback_save"))
   else:
      feedback_msg=request.POST.get("feedback_msg")
      student_obj=Students.objects.get(admin=request.user.id)
      try:
       feedback=FeedbackStudent(students_id=student_obj,feedback=feedback_msg,feedback_reply="")
       feedback.save()
       messages.success(request,"Successfully Sent Feedback")
       return HttpResponseRedirect(reverse("adminstration:student_feedback"))
      except:
       messages.error(request,"Failed to Send Feedback")
       return HttpResponseRedirect(reverse("adminstration:student_feedback"))
   

def staff_feedback_message(request):
   feedbacks=FeedbackStaff.objects.all()
   return render(request,'staff_feedback.html',{'feedbacks':feedbacks})
@csrf_exempt
def staff_feedback_message_replied(request):
   feedback_id=request.POST.get("id")
   feedback_message=request.POST.get("message")
   try:
    feedback=FeedbackStaff.objects.get(id=feedback_id)
    feedback.feedback_reply=feedback_message
    feedback.save()
    return HttpResponse("True")
   except:
    return HttpResponse("False")
   
def student_feedback_message(request):
   feedbacks=FeedbackStudent.objects.all()
   return render(request,'student_feedback.html',{'feedbacks':feedbacks})
@csrf_exempt
def student_feedback_message_replied(request):
   feedback_id=request.POST.get("id")
   feedback_message=request.POST.get("message")
   try:
    feedback=FeedbackStudent.objects.get(id=feedback_id)
    feedback.feedback_reply=feedback_message
    feedback.save()
    return HttpResponse("True")
   except:
    return HttpResponse("False")   

def staff_leave_view(request):
   leaves=LeaveReportStaff.objects.all()
   return render(request,"staff_leave_view.html",{"leaves":leaves})

def staff_approve_leave(request,leave_id):
   leave=LeaveReportStaff.objects.get(id=leave_id)
   leave.leave_status=1
   leave.save()
   return HttpResponseRedirect(reverse("adminstration:staff_leave_view"))

def staff_disapprove_leave(request,leave_id):
   leave=LeaveReportStaff.objects.get(id=leave_id)
   leave.leave_status=2
   leave.save()
   return HttpResponseRedirect(reverse("adminstration:staff_leave_view"))


def student_leave_view(request):
   leaves=LeaveReportStudent.objects.all()
   return render(request,"student_leave_view.html",{"leaves":leaves})

def student_approve_leave(request,leave_id):
   leave=LeaveReportStudent.objects.get(id=leave_id)
   leave.leave_status=1
   leave.save()
   return HttpResponseRedirect(reverse("adminstration:student_leave_view"))

def student_disapprove_leave(request,leave_id):
   leave=LeaveReportStudent.objects.get(id=leave_id)
   leave.leave_status=2
   leave.save()
   return HttpResponseRedirect(reverse("adminstration:student_leave_view"))

def staff_add_result(request):
   subjects=Subjects.objects.filter(staff_id=request.user.id)
   session_years=SessionYearModel.objects.all()
   return render(request,"staff_template/staff_add_result.html",{"subjects":subjects,"session_years":session_years})

def save_student_result(request):
   if request.method!="POST":
      return HttpResponseRedirect("adminstration:staff_add_result")
      
   student_admin_id=request.POST.get('student_list')
   assignment_marks=request.POST.get('assignment_marks')
   exam_marks=request.POST.get('exam_marks')
   subject_id=request.POST.get('subject')

   student_obj=Students.objects.get(id=student_admin_id)
   subject_obj=Subjects.objects.get(id=subject_id)

   try:
    check_exist=StudentResult.objects.filter(subject_id=subject_obj,student_id=student_obj).exists()
    if check_exist:
      result=StudentResult.objects.get(subject_id=subject_obj,student_id=student_obj)
      result.subject_assignment_marks=assignment_marks
      result.subject_exam_marks=exam_marks
      result.save()
      messages.success(request,"Successfully Updated Result")
      return HttpResponseRedirect(reverse("adminstration:staff_add_result"))
    else:
     result=StudentResult(student_id=student_obj,subject_id=subject_obj,subject_exam_marks=exam_marks,subject_assignment_marks=assignment_marks)
     result.save()
     messages.success(request,"Successfully Added Result")
     return HttpResponseRedirect(reverse("adminstration:staff_add_result"))
   except:
      messages.error(request,"Failed to Add Result")
      return HttpResponseRedirect(reverse("adminstration:staff_add_result"))
      


def student_view_result(request):
   student=Students.objects.get(admin=request.user.id)
   studentresult=StudentResult.objects.filter(student_id=student.id)

   return render(request,"student_template/student_result.html",{"studentresult":studentresult})









 


