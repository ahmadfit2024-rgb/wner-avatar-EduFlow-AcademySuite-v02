from djongo import models
from django.conf import settings
from bson import ObjectId

# Note: We use djongo.models instead of django.db.models
# to leverage MongoDB-specific features like embedded documents.

class Lesson(models.Model):
    """
    Represents a single lesson within a course.
    This is designed as an Embedded Model. It will be contained within a Course.
    """
    _id = models.ObjectIdField(default=ObjectId) # Unique ID for each lesson
    title = models.CharField(max_length=200)
    order = models.PositiveIntegerField(default=0)
    content_type = models.CharField(
        max_length=20,
        choices=[
            ('video', 'Video'),
            ('pdf', 'PDF'),
            ('quiz', 'Quiz'),
            ('text_editor', 'Text Editor')
        ]
    )
    # Flexible field to store different types of content data
    content_data = models.JSONField(default=dict) 
    is_previewable = models.BooleanField(default=False)

    class Meta:
        abstract = True # This tells Djongo this is an embedded model template

class Course(models.Model):
    """
    Represents a single, self-contained course.
    """
    _id = models.ObjectIdField()
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    description = models.TextField()
    instructor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='courses_taught'
    )
    category = models.CharField(max_length=100)
    status = models.CharField(
        max_length=20,
        choices=[('draft', 'Draft'), ('published', 'Published'), ('archived', 'Archived')],
        default='draft'
    )
    cover_image_url = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    # Embedding the Lesson model here
    lessons = models.ArrayField(
        model_container=Lesson,
        default=list
    )

    objects = models.DjongoManager()

    def __str__(self):
        return self.title

class Module(models.Model):
    """
    Represents a module within a Learning Path, which is essentially a course.
    This is an Embedded Model.
    """
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    order = models.PositiveIntegerField(default=0)
    
    class Meta:
        abstract = True

class LearningPath(models.Model):
    """
    Represents a high-level learning path, diploma, or program
    composed of multiple courses (modules).
    """
    _id = models.ObjectIdField()
    title = models.CharField(max_length=255)
    description = models.TextField()
    supervisor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='paths_supervised'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    # Embedding the Module model here
    modules = models.ArrayField(
        model_container=Module,
        default=list
    )

    objects = models.DjongoManager()

    def __str__(self):
        return self.title