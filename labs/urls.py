from django.urls import path
from .views import *

urlpatterns = [
    path('labadd/',LabAdd.as_view()),
    path('labedit/<int:admin_id>/',LabEdit.as_view())
]
