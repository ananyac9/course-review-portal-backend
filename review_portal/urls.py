"""
URL configuration for review_portal project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('admin/', admin.site.urls),
    path('dept/', views.department_list), # GET, POST
    path('dept/<int:id>/', views.department_detail), # GET, PUT, DELETE
    path('dept/<int:dept_id>/top_courses/', views.top_rated_courses),
    path('dept/<int:dept_id>/course/<int:course_id>', views.view_course), # GET, POST, PUT, DELETE
    # path('seed/', views.seed_database), # DEBUGGING ONLY
]

urlpatterns = format_suffix_patterns(urlpatterns)
