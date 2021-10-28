from django.contrib import admin

from django.contrib.auth.admin import UserAdmin
from accounts.models import Student, Tutor,Assignment,Submission

admin.site.register(Tutor)
admin.site.register(Student)
admin.site.register(Assignment)
admin.site.register(Submission)
# Register your models here.
