from django.contrib import admin
from .models import *
# Register your models here.


admin.site.register(UserManage)

admin.site.register(Package)
admin.site.register(Test)
admin.site.register(Doctor)
admin.site.register(Reservation)

