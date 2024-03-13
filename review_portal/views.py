from .models import Course, Department
from .serializers import CourseSerializer
from .serializers import DepartmentSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse

@api_view(['GET', 'POST'])
def department_list(request, format=None):
    if request.method == 'GET':
        dept = Department.objects.all()
        serializer = DepartmentSerializer(dept, many=True)
        # courses = Course.objects.filter(department=dept).order_by('-average_rating')[:10]
        # course_serializer = CourseSerializer(courses, many=True)
        # department_data = serializer.data
        # department_data['top_courses'] = course_serializer.data
        # return Response(department_data, status=status.HTTP_200_OK)
        return JsonResponse({"departments": serializer.data})
    if request.method == 'POST':
        serializer= DepartmentSerializer(data=request.data)
        if serializer.is_valid(): # add validity checking function
            serializer.save()
            # return Response(serializer.data, status = status.HTTP_201_CREATED)
            return JsonResponse({"success": "Department added"}, status=status.HTTP_201_CREATED)
        return JsonResponse({"error": "Invalid request"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE']) # POST?
def department_detail(request, id, format=None):
    try:
        department = Department.objects.get(pk=id)
        courses = Course.objects.filter(department=department)
    except ObjectDoesNotExist:
        return JsonResponse({"error": "Department not found"}, status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        dept_info = {
            "id": id,
            "name": department.name,
            "courses": [
                {
                    "id": course.pk,  # Fix: Use course.pk instead of course.id
                    "code": course.code,
                    "info": course.info,
                    "ratings": course.ratings,
                    "average_rating": course.average_rating
                } 
                for course in courses
            ]
        }
        return JsonResponse(dept_info, status=status.HTTP_200_OK)
    
    if request.method == 'PUT':
        serializer = DepartmentSerializer(department, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse({"success": "Department updated"}, status=status.HTTP_200_OK)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    if request.method == 'DELETE':
        department.delete()
        return JsonResponse({"success": "Department removed"}, status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def view_course(request, dept_id, course_id, format=None):
    try:
        department = Department.objects.get(pk=dept_id)
        course = Course.objects.get(pk=course_id, department=department)
    except ObjectDoesNotExist:
        return JsonResponse({"error": "Course not found"}, status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = CourseSerializer(course, many=False)
        return JsonResponse(serializer.data, status=status.HTTP_200_OK)
    
    if request.method == 'POST':
        new_rating = float(request.data.get('rating'))
        if(0 <= new_rating <= 5 and new_rating % 0.5 == 0):
            course.ratings.append(new_rating)
            course.average_rating = sum(course.ratings) / len(course.ratings)
            course.save()
            return JsonResponse({"success": "Rating added"}, status=status.HTTP_201_CREATED)
        return JsonResponse({"error": "Rating should be between 0 and 5 in steps of 0.5"}, status=status.HTTP_400_BAD_REQUEST)
    
    if request.method == 'PUT':
        serializer = CourseSerializer(course, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse({"success": "Course updated"}, status=status.HTTP_200_OK)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    if request.method == 'DELETE':
        course.delete()
        return JsonResponse({"success": "Course removed"}, status=status.HTTP_204_NO_CONTENT)
    
    return JsonResponse({"error": "Invalid request"}, status=status.HTTP_400_BAD_REQUEST)
@api_view(['GET'])
def top_rated_courses(request, dept_id):
    try:
        department = Department.objects.get(pk=dept_id)
    except ObjectDoesNotExist:
        return JsonResponse({"error": "Department not found"}, status=404)
    
    top_courses = Course.objects.filter(department=department).order_by('-average_rating')[:10]
    serializer = CourseSerializer(top_courses, many=True)
    return JsonResponse({"top_courses": serializer.data}, status=200)
# DEBUGGING ONLY
def seed_database(request):
    Department.objects.all().delete()
    Course.objects.all().delete()

    Department.objects.create(name="CS")
    Department.objects.create(name="MA")
    Department.objects.create(name="BB")
    
    Course.objects.create(department=Department.objects.get(name="CS"), code=105, info="Discrete Structures")
    Course.objects.create(department=Department.objects.get(name="CS"), code=108, info="Software Systems Lab")
    Course.objects.create(department=Department.objects.get(name="MA"), code=110, info="Linear Algebra")
    Course.objects.create(department=Department.objects.get(name="BB"), code=101, info="Biology")
    
    return JsonResponse({"success": "Database seeded"}, status=status.HTTP_204_NO_CONTENT)
