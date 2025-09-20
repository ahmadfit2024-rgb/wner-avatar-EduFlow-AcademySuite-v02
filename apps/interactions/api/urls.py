from django.urls import path
from .views import AddDiscussionThreadView

app_name = 'interactions'

urlpatterns = [
    path('lessons/<str:lesson_id>/add-thread/', AddDiscussionThreadView.as_view(), name='add_thread'),
]