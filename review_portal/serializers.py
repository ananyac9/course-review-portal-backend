from rest_framework import serializers
from .models import Course
from .models import Department

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ["id", "department", "code", "info", "ratings", "average_rating"]

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ["id", "name", "course"]
