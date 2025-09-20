from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from bson import ObjectId
from apps.learning.models import Course, LearningPath
from .serializers import CourseSerializer, LearningPathSerializer

class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    @action(detail=True, methods=['post'], url_path='update-lesson-order')
    def update_lesson_order(self, request, pk=None):
        """
        Custom action to update the order of lessons within a course.
        Expects a list of lesson_ids in the new order.
        """
        course = self.get_object()
        lesson_ids_order = request.data.get('lesson_order', [])

        if not isinstance(lesson_ids_order, list):
            return Response({'error': 'lesson_order must be a list'}, status=status.HTTP_400_BAD_REQUEST)

        # Create a mapping of lesson_id to its new order
        order_map = {lesson_id: index + 1 for index, lesson_id in enumerate(lesson_ids_order)}

        # Update the order for each lesson in the course's lessons array
        for lesson in course.lessons:
            lesson_id_str = str(lesson._id)
            if lesson_id_str in order_map:
                lesson.order = order_map[lesson_id_str]
        
        # Sort lessons by the new order before saving
        course.lessons.sort(key=lambda l: l.order)
        course.save()
        
        return Response({'status': 'Lesson order updated successfully'}, status=status.HTTP_200_OK)

class LearningPathViewSet(viewsets.ModelViewSet):
    queryset = LearningPath.objects.all()
    serializer_class = LearningPathSerializer

    @action(detail=True, methods=['post'], url_path='update-structure')
    def update_structure(self, request, pk=None):
        learning_path = self.get_object()
        course_ids = request.data.get('course_ids', [])
        if not isinstance(course_ids, list):
            return Response({'error': 'course_ids must be a list'}, status=status.HTTP_400_BAD_REQUEST)

        new_modules = []
        for index, course_id in enumerate(course_ids):
            try:
                # Rebuild using a proper model structure for Module
                course_ref = Course.objects.get(pk=course_id)
                module_instance = {'course': course_ref, 'order': index + 1}
                new_modules.append(module_instance)
            except Course.DoesNotExist:
                continue
        
        learning_path.modules = new_modules
        learning_path.save()

        return Response({'status': 'structure updated successfully'}, status=status.HTTP_200_OK)