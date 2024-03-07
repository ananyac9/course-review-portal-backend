from .models import Course, Department
from .serializers import CourseSerializer
from .serializers import DepartmentSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse

# def course_list(request):
#     courses = Course.objects.all()
#     serializer = CourseSerializer(courses, many=True)
#     return JsonResponse({"courses": serializer.data})

@api_view(['GET', 'POST'])
def department_list(request, format=None):
    if request.method == 'GET':
        dept = Department.objects.all()
        serializer = DepartmentSerializer(dept, many=True)
        return JsonResponse({"departments": serializer.data})
    if request.method == 'POST':
        serializer= DepartmentSerializer(data=request.data)
        if serializer.is_valid(): # add validity checking function
            serializer.save()
            # return Response(serializer.data, status = status.HTTP_201_CREATED)
            return JsonResponse({"success": "Course added"}, status=status.HTTP_201_CREATED)
        return JsonResponse({"error": "Invalid request"}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def department_detail(request, id, format=None):
    try:
        dept = Department.objects.get(pk=id)
    except ObjectDoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        serializer = DepartmentSerializer(dept, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)
    if request.method == 'PUT':
        serializer = DepartmentSerializer(dept, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)
    if request.method == 'DELETE':
        dept.delete()
        return Response(status=204)

@api_view(['GET', 'POST']) # TODO: Implement PUT and DELETE
def view_course(request, id):
    try:
        course = Course.objects.get(pk=id)
    except ObjectDoesNotExist:
        return JsonResponse({"error": "Course not found"}, status=404)
    
    if request.method == 'GET':
        serializer = CourseSerializer(course, many=False)
        return JsonResponse(serializer.data, status=200)
    
    if request.method == 'POST':
        new_rating = float(request.data.get('rating'))
        if(0 <= new_rating <= 5 and new_rating % 0.5 == 0):
            course.ratings.append(new_rating)
            course.average_rating = sum(course.ratings) / len(course.ratings)
            course.save()
            return JsonResponse({"success": "Rating added"}, status=200)
        return JsonResponse({"error": "Rating should be between 0 and 5 in steps of 0.5"}, status=400)

# DEBUGGING ONLY
def remove_all_courses(request):
    Course.objects.all().delete()
    return JsonResponse({"success": "All courses removed"}, status=200)