from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, CreateView, UpdateView
from django.db.models import Q
from django.urls import reverse_lazy
from .models import CustomUser
from .forms import CustomUserCreationForm, CustomUserChangeForm

class UserManagementView(LoginRequiredMixin, TemplateView):
    template_name = 'users/user_management.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        search_query = self.request.GET.get('q', '')
        users = CustomUser.objects.all().order_by('-date_joined')
        if search_query:
            users = users.filter(
                Q(username__icontains=search_query) |
                Q(full_name__icontains=search_query) |
                Q(email__icontains=search_query)
            )
        context['users'] = users
        context['search_query'] = search_query
        context['is_search'] = bool(search_query)
        return context

    def get(self, request, *args, **kwargs):
        if request.htmx:
            self.template_name = 'partials/_user_list.html'
        return super().get(request, *args, **kwargs)

class UserCreateView(LoginRequiredMixin, CreateView):
    """
    View for an admin to create a new user.
    """
    model = CustomUser
    form_class = CustomUserCreationForm
    template_name = 'users/user_form.html'
    success_url = reverse_lazy('users:user_management')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Add New User"
        return context

class UserUpdateView(LoginRequiredMixin, UpdateView):
    """
    View for an admin to update an existing user's details.
    """
    model = CustomUser
    form_class = CustomUserChangeForm
    template_name = 'users/user_form.html'
    success_url = reverse_lazy('users:user_management')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Edit User"
        return context