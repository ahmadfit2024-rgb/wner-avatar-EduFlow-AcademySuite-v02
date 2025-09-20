from django import template
from ..models import DiscussionThread
from ..forms import DiscussionThreadForm

register = template.Library()

@register.simple_tag
def get_discussions_for_lesson(lesson_id):
    """
    Template tag to fetch all discussion threads for a given lesson_id.
    """
    return DiscussionThread.objects.filter(lesson_id=lesson_id).order_by('-created_at')

@register.simple_tag
def get_discussion_form():
    """
    Template tag to provide an instance of the discussion form.
    """
    return DiscussionThreadForm()