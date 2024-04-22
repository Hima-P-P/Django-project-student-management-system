from django import forms
from adminstration.models import Staffs,Students,Courses,Subjects
class staffform(forms.ModelForm): 
    class Meta:
        model=Staffs
        fields='__all__'

class studentform(forms.ModelForm): 
    class Meta:
        model=Students
        fields='__all__'

class courseform(forms.ModelForm): 
    class Meta:
        model=Courses
        fields='__all__'

class subjectform(forms.ModelForm): 
    class Meta:
        model=Subjects
        fields='__all__'        
