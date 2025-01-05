from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib import messages

# class-based view classes
from django.views.generic import DetailView
from django.views.generic import CreateView
from django.views.generic import ListView
from django.views.generic import UpdateView
from django.views.generic import DeleteView


# Permission and Authentication
from django.contrib.auth.mixins import LoginRequiredMixin
from authority.permissions import AdminPassesTestMixin
from django.shortcuts import get_object_or_404, redirect
from django.core.paginator import Paginator


# Import Models
from Homepage.models import (
    FrontendSetting
)
from authority.forms import FrontendSettingForm



#<<----------------- List, Add, Update, Delete Colorsettings---------------->>
class FrontendSettingsListView(LoginRequiredMixin, AdminPassesTestMixin, ListView):
    model = FrontendSetting
    template_name = 'frontend/frontend_list.html'
    context_object_name = 'settings'
    def get_queryset(self):
        return FrontendSetting.objects.first()
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Frontend Settings List'
        return context


class UpdateFrontendSettingView(LoginRequiredMixin, AdminPassesTestMixin, UpdateView):
    model = FrontendSetting
    template_name = 'frontend/add_update_frontend.html'
    form_class = FrontendSettingForm
    success_url = reverse_lazy('authority:frontend_settings')
    success_message = "Frontend Setting Updated Successfully"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Update Frontend Setting"
        context["updated"] = True
        return context

    def form_invalid(self, form):
        print(form.errors)
        messages.error(self.request, "Something went wrong, please try again!")
        return super().form_invalid(form)


class AddFrontendSettingView(LoginRequiredMixin, AdminPassesTestMixin, CreateView):
    model = FrontendSetting
    template_name = 'frontend/add_update_frontend.html'
    form_class = FrontendSettingForm
    success_url = reverse_lazy('authority:frontend_settings')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Add Frontend Setting"
        return context

    def form_valid(self, form):
        messages.success(self.request, "Frontend Setting Added Successfully")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Something went wrong, please try again!")
        return super().form_invalid(form)


class FrontendSettingDeleteView(LoginRequiredMixin, AdminPassesTestMixin, DeleteView):
    def post(self, request, pk):
        frontend_setting = get_object_or_404(FrontendSetting, pk=pk)
        frontend_setting.delete()
        messages.success(request, "Settings deleted successfully.")
        return redirect('authority:frontend_settings')
