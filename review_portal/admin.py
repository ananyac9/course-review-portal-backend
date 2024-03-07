from django.contrib import admin
from .models import Course
from .models import department

admin.site.register(Course)
admin.site.register(department)