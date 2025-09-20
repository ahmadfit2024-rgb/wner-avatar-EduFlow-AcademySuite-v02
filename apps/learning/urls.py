from django.urls import path
from .views import (
    LessonDetailView, 
    PathBuilderView, 
    LearningPathCreateView,
    CourseManageView,
    LessonCreateView,
)

app_name = 'learning'

urlpatterns = [
    # Course Player URL
    path(
        'courses/<slug:course_slug>/lessons/<int:lesson_order>/', 
        LessonDetailView.as_view(), 
        name='lesson_detail'
    ),
    
    # Learning Path Management URLs
    path(
        'paths/create/', 
        LearningPathCreateView.as_view(), 
        name='path_create'
    ),
    path(
        'paths/<str:pk>/build/', 
        PathBuilderView.as_view(), 
        name='path_builder'
    ),

    # Course Content Management URLs
    path(
        'courses/<str:pk>/manage/',
        CourseManageView.as_view(),
        name='course_manage'
    ),
    path(
        'courses/<str:pk>/add-lesson/',
        LessonCreateView.as_view(),
        name='lesson_add'
    ),
]