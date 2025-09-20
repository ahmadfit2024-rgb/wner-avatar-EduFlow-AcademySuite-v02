from djongo import models
from django.conf import settings
from apps.learning.models import Course

class Enrollment(models.Model):
    """
    Connects a student to a course or a learning path they are enrolled in.
    """
    _id = models.ObjectIdField()
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    
    enrollable_id = models.CharField(max_length=24) # To store ObjectId as string
    enrollable_type = models.CharField(max_length=50, choices=[('Course', 'Course'), ('LearningPath', 'LearningPath')])
    
    enrollment_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=20,
        choices=[('in_progress', 'In Progress'), ('completed', 'Completed')],
        default='in_progress'
    )
    progress = models.FloatField(default=0.0) # e.g., 0.75 for 75%
    completed_lessons = models.JSONField(default=list) # Store list of completed lesson IDs (as strings)
    last_accessed_lesson_id = models.CharField(max_length=24, blank=True, null=True)

    objects = models.DjongoManager()
    
    class Meta:
        unique_together = ('student', 'enrollable_id')

    def __str__(self):
        return f"{self.student.username} enrolled in {self.enrollable_type} ({self.enrollable_id})"

    def update_progress(self):
        """
        Calculates and updates the progress percentage based on completed lessons.
        """
        if self.enrollable_type == 'Course':
            try:
                course = Course.objects.get(_id=self.enrollable_id)
                total_lessons = len(course.lessons)
                if total_lessons > 0:
                    completed_count = len(self.completed_lessons)
                    self.progress = round((completed_count / total_lessons) * 100, 2)
                else:
                    self.progress = 100 if self.status == 'completed' else 0
                
                if self.progress >= 100:
                    self.status = 'completed'
                
                self.save()
            except Course.DoesNotExist:
                # If course is deleted, cannot calculate progress
                self.progress = 0
                self.save()