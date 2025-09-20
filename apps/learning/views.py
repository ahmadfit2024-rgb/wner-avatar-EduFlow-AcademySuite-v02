from django.views.generic import TemplateView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, render
from .models import Course, LearningPath, Lesson
from .forms import LearningPathForm, LessonForm

# --- Learning Path Views ---
class LearningPathCreateView(LoginRequiredMixin, CreateView):
    model = LearningPath
    form_class = LearningPathForm
    template_name = 'learning/path_form.html'
    def get_success_url(self):
        return reverse_lazy('learning:path_builder', kwargs={'pk': self.object.pk})
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Create New Learning Path"
        return context

class PathBuilderView(LoginRequiredMixin, DetailView):
    model = LearningPath
    template_name = 'learning/path_builder.html'
    context_object_name = 'learning_path'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        learning_path = self.get_object()
        path_course_ids = [module['course_id'] for module in learning_path.modules]
        available_courses = Course.objects.exclude(_id__in=path_course_ids)
        context['available_courses'] = available_courses
        return context

# --- Course & Lesson Views ---
class CourseManageView(LoginRequiredMixin, DetailView):
    """
    The main management interface for an instructor to build out a course's content.
    """
    model = Course
    template_name = 'learning/manage_course.html'
    context_object_name = 'course'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['lesson_form'] = LessonForm()
        return context

class LessonCreateView(LoginRequiredMixin, CreateView):
    """
    Handles the creation of a new lesson within a course.
    Responds to HTMX requests by rendering only the updated lesson list.
    """
    model = Lesson
    form_class = LessonForm
    
    def form_valid(self, form):
        course = get_object_or_404(Course, pk=self.kwargs['pk'])
        lesson = form.save(commit=False)
        
        # Set the order for the new lesson
        lesson.order = len(course.lessons) + 1
        
        # Prepare content_data based on type
        if lesson.content_type == 'video':
            lesson.content_data = {'video_url': form.cleaned_data.get('video_url', '')}
        elif lesson.content_type == 'pdf':
            lesson.content_data = {'pdf_url': '/path/to/placeholder.pdf'} # Placeholder for file upload
        
        course.lessons.append(lesson)
        course.save()
        
        # For HTMX requests, return the updated lesson list partial
        if self.request.htmx:
            return render(self.request, 'partials/_lesson_list.html', {'course': course})
        
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('learning:course_manage', kwargs={'pk': self.kwargs['pk']})


class LessonDetailView(LoginRequiredMixin, DetailView):
    model = Course
    template_name = 'learning/lesson_detail.html'
    slug_url_kwarg = 'course_slug'
    slug_field = 'slug'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        course = self.get_object()
        lesson_order = self.kwargs.get('lesson_order', 1)
        current_lesson = next((lesson for lesson in course.lessons if lesson.order == lesson_order), None)
        context['course'] = course
        context['current_lesson'] = current_lesson
        context['lessons'] = course.lessons
        if current_lesson:
            total_lessons = len(course.lessons)
            context['next_lesson_order'] = lesson_order + 1 if lesson_order < total_lessons else None
            context['prev_lesson_order'] = lesson_order - 1 if lesson_order > 1 else None
        return context