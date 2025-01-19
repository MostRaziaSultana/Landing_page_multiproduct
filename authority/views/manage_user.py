from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.utils.http import url_has_allowed_host_and_scheme
from django.contrib.auth import logout
from django.views.generic import View
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect

from django.contrib.auth.forms import AuthenticationForm
# class-based view classes
from django.views.generic import DetailView
from django.views.generic import CreateView
from django.views.generic import ListView
from django.views.generic import UpdateView
from django.views.generic import DeleteView
from django.views.generic.edit import FormView


# Permission and Authentication
from django.contrib.auth.mixins import LoginRequiredMixin
from authority.permissions import AdminPassesTestMixin

#Import Filter Classes
from authority.filters import UserListFilter


# Models Accounts
from django.contrib.auth.models import User

#Import From
from authority.forms import UserInfoForm,AddAdminUserForm


class UserListView(LoginRequiredMixin, AdminPassesTestMixin, ListView):
    queryset = User.objects.filter(is_active=True)
    filterset_class = UserListFilter
    template_name = 'user/user_list.html'
    paginate_by = 6

    def get_queryset(self):
        return self.filterset_class(self.request.GET, queryset=self.queryset).qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "User List"
        context["users"] =  self.filterset_class(self.request.GET, queryset=self.queryset)
        return context



class CustomLoginView(FormView):
    template_name = 'user/custom_login.html'
    form_class = AuthenticationForm
    success_url = reverse_lazy('authority:authority_admin')

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        username = form.data.get('username')
        password = form.data.get('password')
        remember_me = form.data.get('remember_me')

        if form.is_valid():
            user = authenticate(self.request, username=username, password=password)

            if user is not None and user.is_superuser:
                login(self.request, user)

                if remember_me:
                    request.session.set_expiry(None)
                else:
                    request.session.set_expiry(18000)

                next_url = form.data.get('next', self.success_url)

                if url_has_allowed_host_and_scheme(next_url, allowed_hosts=self.request.get_host()):
                    return redirect(next_url)
                else:
                    messages.error(self.request, 'Invalid redirect URL.')
                    return redirect(self.success_url)
            else:
                messages.error(self.request, 'Invalid username, password, or insufficient permissions.')
                return redirect(request.path)
        else:
            messages.error(self.request, 'Invalid form submission.')
            return redirect(request.path)


class CustomLogoutView(View):
    success_url = reverse_lazy('authority:login')
    def get(self, request, *args, **kwargs):
        logout(request)
        messages.success(request, 'You have been logged out successfully.')
        return redirect(self.success_url)



class AddAdminUserView(LoginRequiredMixin, AdminPassesTestMixin, CreateView):
    model = User
    form_class = AddAdminUserForm
    template_name = 'user/add_admin.html'
    success_url = reverse_lazy('authority:user_list')

    def test_func(self):
        return self.request.user.is_superuser




class DeleteUserView(LoginRequiredMixin, AdminPassesTestMixin, DeleteView):
    model = User
    template_name = 'authority/confirm_delete.html'
    context_object_name = 'user'

    def post(self, request, pk):
        user = get_object_or_404(User, pk=pk)

        # Prevent deletion of own account
        if user == request.user:
            messages.error(request, "You cannot delete your own account.")
            return redirect('authority:user_list')

        if user.is_superuser and not request.user == user:
            if request.user.is_superuser:
                user.delete()
                messages.success(request, "Superuser deleted successfully.")
                return redirect('authority:user_list')
            else:
                messages.error(request, "You cannot delete a superuser unless you're also a superuser.")
                return redirect('authority:user_list')

        # If it's not a superuser, proceed with deletion
        user.delete()
        messages.success(request, "User deleted successfully.")
        return redirect('authority:user_list')

