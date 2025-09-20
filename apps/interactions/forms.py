from django import forms
from .models import DiscussionThread, DiscussionPost

class DiscussionThreadForm(forms.ModelForm):
    """
    Form for students to create a new discussion thread (ask a question).
    """
    class Meta:
        model = DiscussionThread
        fields = ['title', 'question']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Enter a clear and concise title for your question'}),
            'question': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Describe your question in detail...'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'