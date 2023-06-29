from django.contrib import admin

from core.erp.models import *

# Register your models here.

admin.site.register(Departments)
admin.site.register(Headings)
admin.site.register(SalaryHeadings)
admin.site.register(Salary)
admin.site.register(SalaryDetail)
admin.site.register(Candidatos)
admin.site.register(Vacants)
admin.site.register(Employee)
admin.site.register(EmployeePositions)
admin.site.register(EmployeeTurn)
admin.site.register(Selection)
admin.site.register(Assistance)
admin.site.register(AssistanceDetail)

