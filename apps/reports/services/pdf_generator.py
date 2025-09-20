from django.http import HttpResponse
from django.template.loader import render_to_string
from weasyprint import HTML

class PDFReportGenerator:
    """
    A service to generate PDF files from HTML templates.
    """
    def generate_student_performance_pdf(self, student_data: dict) -> HttpResponse:
        """
        Generates a PDF report for a single student's performance.

        Args:
            student_data: A dictionary containing the student's information and performance metrics.

        Returns:
            An HttpResponse object with the PDF file.
        """
        # Render the HTML template with the provided context
        html_string = render_to_string('reports/student_performance_template.html', {'student': student_data})
        
        # Create the PDF
        html = HTML(string=html_string)
        pdf = html.write_pdf()
        
        # Create the HTTP response
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="student_report_{student_data.get("id", 0)}.pdf"'
        
        return response