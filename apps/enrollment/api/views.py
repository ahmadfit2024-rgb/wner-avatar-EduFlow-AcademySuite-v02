from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from apps.enrollment.models import Enrollment
from .serializers import EnrollmentSerializer

class EnrollmentViewSet(viewsets.ModelViewSet):
    queryset = Enrollment.objects.all()
    serializer_class = EnrollmentSerializer
    
    @action(detail=False, methods=['post'], url_path='mark-lesson-complete')
    def mark_lesson_complete(self, request):
        """
        Marks a lesson as complete for the logged-in user in a specific course.
        """
        user = request.user
        course_id = request.data.get('course_id')
        lesson_id = request.data.get('lesson_id')

        if not course_id or not lesson_id:
            return Response(
                {'error': 'course_id and lesson_id are required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Find the specific enrollment
        enrollment = get_object_or_404(
            Enrollment, 
            student=user, 
            enrollable_id=course_id, 
            enrollable_type='Course'
        )
        
        # Add the lesson_id to completed_lessons if not already present
        if lesson_id not in enrollment.completed_lessons:
            enrollment.completed_lessons.append(lesson_id)
        
        # Update the last accessed lesson
        enrollment.last_accessed_lesson_id = lesson_id
        
        enrollment.save()
        enrollment.update_progress() # Recalculate and save progress

        return Response(
            {'status': 'success', 'progress': enrollment.progress},
            status=status.HTTP_200_OK
        )