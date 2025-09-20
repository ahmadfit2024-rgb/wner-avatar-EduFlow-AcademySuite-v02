from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .services.pdf_generator import PDFReportGenerator
from .services.excel_generator import ExcelReportGenerator
from apps.users.models import CustomUser
from apps.learning.models import Course

class ReportDashboardView(LoginRequiredMixin, TemplateView):
    """
    A view that displays the reporting dashboard and allows users
    to select and generate different types of reports.
    """
    template_name = "reports/report_dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Reporting Dashboard"
        # Pass actual data to the template for filter dropdowns
        context["students"] = CustomUser.objects.filter(role=CustomUser.Roles.STUDENT)
        context["courses"] = Course.objects.all()
        return context

    def post(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        report_type = request.POST.get("report_type")

        if report_type == "student_pdf":
            student_id = request.POST.get("student_id")
            if not student_id:
                # Handle error: no student selected
                return HttpResponseRedirect(reverse('report_dashboard'))

            student = CustomUser.objects.get(id=student_id)
            # --- Placeholder Data for a real report ---
            student_data = {
                "id": student.id,
                "name": student.full_name or student.username,
                "course": "Advanced Digital Marketing", # Placeholder
                "progress": 85, # Placeholder
                "average_score": 92, # Placeholder
            }
            # --- End Placeholder Data ---
            generator = PDFReportGenerator()
            return generator.generate_student_performance_pdf(student_data)
        
        elif report_type == "course_excel":
            course_id = request.POST.get("course_id")
            if not course_id:
                # Handle error: no course selected
                return HttpResponseRedirect(reverse('report_dashboard'))
                
            course = Course.objects.get(_id=course_id)
            # --- Placeholder Data for a real report ---
            enrollments_data = [
                {'student_name': 'Student A', 'student_email': 'a@test.com', 'enrollment_date': '2025-01-10', 'progress': 100, 'status': 'completed'},
                {'student_name': 'Student B', 'student_email': 'b@test.com', 'enrollment_date': '2025-01-12', 'progress': 75, 'status': 'in_progress'},
            ]
            # --- End Placeholder Data ---
            generator = ExcelReportGenerator()
            return generator.generate_course_enrollment_excel(course.title, enrollments_data)

        # Redirect back if report type is unknown or there's an issue
        return HttpResponseRedirect(reverse('report_dashboard'))