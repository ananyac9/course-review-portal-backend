from django.db import models

'''
------------------------------ Documentation for the 'Course' class ------------------------------

Member attributes:

-> department (An object of the 'Department' class) - The department which offers this course.

-> code (An integer) - The unique identifier of every course in a department.

-> info (A text field) - A short paragraph describing the course.

-> ratings (A list of floats) - All the ratings that the course has received. 
== Currently, all the ratings are being made by a single user (the superuser).
== Later, if multiple users are implemented, ratings must also record the user who gave each rating.
== When the 'User' class is implemented, there must be a many-to-many relationship between users and courses.

Member functions:

-> average_rating() - returns the average of all the ratings that this course has gotten.

-> rank() - returns the rank of this course (in terms of average rating) in it's department

--------------------------------------------------------------------------------------------------
'''

class Department(models.Model):
    name = models.CharField(max_length=10)

    def __str__(self) -> str:
        return self.name


class Course(models.Model):
    # should I change this attribute's name to 'department_id'?
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    code = models.PositiveIntegerField()
    info = models.CharField(max_length=1000)
    ratings = models.JSONField(default=list, blank=True)
    average_rating = models.FloatField(default=0)

    def __str__(self) -> str:
        return f"{self.department.name}{self.code}"

    # def rank(self):
    #     return sorted(self.department.course, key=lambda x: x.average_rating, reverse=True).index(self) + 1


# class Department(models.Model):
#     name = models.CharField(max_length=10)
#     course = models.CharField(max_length=20)
#     courses = models.ManyToManyField(Course, related_name='departments')
#     def __str__(self) -> str:
#         return self.course
