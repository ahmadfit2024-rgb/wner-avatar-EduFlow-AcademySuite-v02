from django import forms
from .models import Course, LearningPath, Lesson

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = [
            'title', 
            'slug', 
            'description', 
            'instructor', 
            'category', 
            'status', 
            'cover_image_url'
        ]

class LearningPathForm(forms.ModelForm):
    class Meta:
        model = LearningPath
        fields = ['title', 'description', 'supervisor']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

class LessonForm(forms.ModelForm):
    """
    A dynamic form for creating and updating lessons.
    It includes fields for all possible content types.
    """
    # Specific field for video URL, not directly in the model
    video_url = forms.URLField(required=False, label="Video URL (Vimeo or YouTube)")
    
    class Meta:
        model = Lesson
        fields = ['title', 'content_type']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Apply Bootstrap classes to form fields
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})