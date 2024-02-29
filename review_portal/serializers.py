from rest_framework import serializers
from .models import Course
from .models import department

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ["id", "department", "code", "info", "ratings"]
class departmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = department
        fields = ["id", "name", "course"]        