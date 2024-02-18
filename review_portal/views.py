from .models import Course
from .serializers import CourseSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ObjectDoesNotExist

@api_view(['GET', 'POST']) # TODO: Implement PUT and DELETE
def course(request, code):
    try:
        course = Course.objects.get(code=code)
    except ObjectDoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = CourseSerializer(course, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    if request.method == 'POST':
        new_rating = request.data.get('new_rating')
        # NOTE: if the allowed ratings can only be integers, then change THIS line:
        if isinstance(new_rating, float) and 0 <= new_rating <= 5 and new_rating % 0.5 == 0:
            course.ratings.append(new_rating)
            course.save()
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
        