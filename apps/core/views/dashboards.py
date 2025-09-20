from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from apps.enrollment.models import Enrollment
from apps.learning.models import Course, LearningPath
from apps.users.models import CustomUser

class DashboardView(LoginRequiredMixin, View):
    """
    A smart view that renders the correct dashboard template
    based on the logged-in user's role and populates it with
    relevant data.
    """
    login_url = '/login/' # Redirect if not logged in

    def get(self, request, *args, **kwargs):
        user = request.user
        context = {'user': user}
        
        dashboard_templates = {
            'admin': 'dashboards/admin.html',
            'supervisor': 'dashboards/supervisor.html',
            'instructor': 'dashboards/instructor.html',
            'student': 'dashboards/student.html',
            'third_party': 'dashboards/third_party.html',
        }

        template_name = dashboard_templates.get(user.role)

        if not template_name:
            return redirect('login')

        # --- Dynamic Context Population ---
        if user.role == 'student':
            student_enrollments = Enrollment.objects.filter(student=user)
            enrolled_courses = []
            for enrollment in student_enrollments:
                try:
                    course = Course.objects.get(_id=enrollment.enrollable_id)
                    course.progress = enrollment.progress 
                    enrolled_courses.append(course)
                except Course.DoesNotExist:
                    continue
            context['enrolled_courses'] = enrolled_courses

        elif user.role == 'instructor':
            instructor_courses = Course.objects.filter(instructor=user)
            student_ids = Enrollment.objects.filter(enrollable_id__in=[str(c._id) for c in instructor_courses]).values_list('student', flat=True).distinct()
            context['instructor_courses'] = instructor_courses
            context['total_students'] = len(student_ids)
            context['total_courses'] = instructor_courses.count()

        elif user.role == 'admin':
            context['total_users'] = CustomUser.objects.count()
            context['total_students'] = CustomUser.objects.filter(role=CustomUser.Roles.STUDENT).count()
            context['total_instructors'] = CustomUser.objects.filter(role=CustomUser.Roles.INSTRUCTOR).count()
            context['total_courses'] = Course.objects.count()

        elif user.role == 'supervisor':
            # Fetch learning paths supervised by the current user
            context['learning_paths'] = LearningPath.objects.filter(supervisor=user)

        return render(request, template_name, context)