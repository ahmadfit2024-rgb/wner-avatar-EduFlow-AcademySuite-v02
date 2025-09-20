from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .serializers import AIQuestionSerializer
from ..services import AIAssistantService
# from apps.learning.models import Course # To fetch context

class AIAssistantView(APIView):
    """
    API endpoint for the AI Assistant. [cite: 685]
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = AIQuestionSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            question = serializer.validated_data['question']
            course_id = serializer.validated_data['course_id']
            lesson_id = serializer.validated_data['lesson_id']

            # --- Context Building Logic ---
            # In a real implementation, you would fetch the course and lesson
            # from the database using the IDs to build the context.
            # For now, we'll use placeholder context.
            context = {
                'course_title': f'Course {course_id}',
                'lesson_title': f'Lesson {lesson_id}',
                'lesson_content': 'This is the text content of the lesson that the AI will use as context.'
            }
            # --- End Context Building ---

            ai_service = AIAssistantService()
            answer = ai_service.get_answer(question, context)

            return Response({'answer': answer}, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)