from django.urls import path
from .views import *

urlpatterns = [
    path('labadd/',LabAdd.as_view()),
    path('labedit/<int:admin_id>/',LabEdit.as_view()),
    path('login/',Login.as_view()),
    path('packageadd/',packageAdd.as_view()),

    path('packageedit/<int:package_id>/',PackageEdit.as_view()),
    path('testadd/',TestAdd.as_view()),
    path('doctoradd/',DoctorAdd.as_view())


     
]
