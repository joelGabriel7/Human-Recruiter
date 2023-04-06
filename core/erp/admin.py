from django.contrib import admin
from django.contrib.auth.models import User
from core.erp.models import *

# Register your models here.
admin.site.register(AccountsBank)
admin.site.register(Departments)
admin.site.register(Banks)
admin.site.register(People)
admin.site.register(Vacants)
admin.site.register(Employee)
admin.site.register(EmployeePositions)
admin.site.register(EmployeeTurn)
admin.site.register(Address)
admin.site.register(Attendance)

