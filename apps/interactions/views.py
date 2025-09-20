from django.views.generic import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, render
from .models import DiscussionThread
from .forms import DiscussionThreadForm
from apps.learning.models import Course

class AddDiscussionThreadView(LoginRequiredMixin, CreateView):
    """
    Handles the creation of a new discussion thread for a specific lesson,
    driven by an HTMX request from the course player.
    """
    model = DiscussionThread
    form_class = DiscussionThreadForm
    
    def form_valid(self, form):
        # Extract course and lesson info from the request
        course_id = self.request.POST.get('course_id')
        lesson_id = self.kwargs.get('lesson_id')
        
        # Get the course to pass back to the partial template
        course = get_object_or_404(Course, pk=course_id)
        
        # Populate the new thread with required info
        thread = form.save(commit=False)
        thread.student = self.request.user
        thread.course_id = course_id
        thread.lesson_id = lesson_id
        thread.save()

        # After saving, prepare context for the partial update
        threads = DiscussionThread.objects.filter(lesson_id=lesson_id).order_by('-created_at')
        context = {
            'threads': threads,
            'course': course,
            'current_lesson_id': lesson_id,
            'form': DiscussionThreadForm() # Provide a fresh form
        }

        # Set a success message header for the toast notification
        response = render(self.request, 'interactions/partials/_discussion_forum_content.html', context)
        response['HX-Trigger'] = 'showToast'
        response['HX-Trigger-Detail'] = '{"message": "Your question has been posted successfully!"}'

        return response

    def form_invalid(self, form):
        # Handle invalid form submission if needed, e.g., return an error message
        # For simplicity, we'll just ignore it in this phase for HTMX
        return super().form_invalid(form)