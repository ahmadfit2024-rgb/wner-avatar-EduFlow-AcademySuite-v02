from django.urls import path
from .views import UserManagementView, UserCreateView, UserUpdateView

app_name = 'users'

urlpatterns = [
    path('manage/', UserManagementView.as_view(), name='user_management'),
    path('add/', UserCreateView.as_view(), name='user_add'),
    path('<int:pk>/edit/', UserUpdateView.as_view(), name='user_edit'),
]