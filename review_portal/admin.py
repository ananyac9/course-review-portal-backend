from django.contrib import admin
from .models import Course
from .models import Department

admin.site.register(Course)
admin.site.register(Department)