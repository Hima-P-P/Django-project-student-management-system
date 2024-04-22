from adminstration.models import Courses
def menu_links(request):
    c=Courses.objects.all()
    return{'links':c}



