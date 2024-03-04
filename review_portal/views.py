from .models import Course
from .serializers import CourseSerializer
from rest_framework.decorators import api_view
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse

def course_list(request):
    courses = Course.objects.all()
    serializer = CourseSerializer(courses, many=True)
    return JsonResponse({"courses": serializer.data})

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
            course.save()
            return JsonResponse({"success": "Rating added"}, status=200)
        return JsonResponse({"error": "Rating should be between 0 and 5 in steps of 0.5"}, status=400)
