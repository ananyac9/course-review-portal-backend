import re
from tkinter.messagebox import RETRY
from .models import Course, department
from .serializers import CourseSerializer
from .serializers import departmentSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse

def course_list(request):
    courses = Course.objects.all()
    serializer = CourseSerializer(courses, many=True)
    # return Response(serializer.data)
    return JsonResponse({"courses": serializer.data})

@api_view(['GET', 'POST'])
def department_list(request):
    if request.method == 'GET':
        dept = department.objects.all()
        serializer = departmentSerializer(dept, many=True)
        return JsonResponse({"departments": serializer.data})
    if request.method == 'POST':
        serializer= departmentSerializer(data= request.data)
        if serializer.is_valid(): # add validity checking function
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)

@api_view(['GET', 'POST']) # TODO: Implement PUT and DELETE
def course(request, id):
    try:
        course = Course.objects.get(pk=id)
    except ObjectDoesNotExist:
        # return Response(status=status.HTTP_404_NOT_FOUND)
        return JsonResponse({"error": "Course not found"}, status=404)
    
    if request.method == 'GET':
        serializer = CourseSerializer(course, many=False)
        # return Response(serializer.data, status=status.HTTP_200_OK)
        return JsonResponse(serializer.data, status=200)
    
    if request.method == 'POST':
        # new_rating = request.data.get('rating')
        # # NOTE: if the allowed ratings can only be integers, then change THIS line:
        # if isinstance(new_rating, float) and 0 <= new_rating <= 5 and new_rating % 0.5 == 0:
        #     course.ratings.append(new_rating)
        #     course.save()
        #     # return Response(status=status.HTTP_200_OK)
        #     return JsonResponse({"success": "Rating added"}, status=200)
        # # return Response(status=status.HTTP_400_BAD_REQUEST)
        # return JsonResponse({"error": "Invalid rating"}, status=400)

        # serializer = CourseSerializer(course, data=request.data, partial=True)
        # if serializer.is_valid():
        #     serializer.save()
        #     return JsonResponse(serializer.data, status=200)
        # return JsonResponse(serializer.errors, status=400)

        # new_rating = request.POST.get('rating')
        new_rating = float(request.data.get('rating'))
        # NOTE: if the allowed ratings can only be integers, then change THIS line:
        if(0 <= new_rating <= 5 and new_rating % 0.5 == 0):
            course.ratings.append(new_rating)
            course.save()
            return JsonResponse({"success": "Rating added"}, status=200)
        return JsonResponse({"error": "Rating should be between 0 and 5 in steps of 0.5"}, status=400)
