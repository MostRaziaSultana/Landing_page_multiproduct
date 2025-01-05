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
    Banner
)
from authority.forms import BannerForm



#<<----------------- List, Add, Update, Delete Colorsettings---------------->>
class BannerListView(LoginRequiredMixin, AdminPassesTestMixin, ListView):
    model = Banner
    template_name = 'banner/banner_list.html'
    context_object_name = 'banners'

    def get_queryset(self):
        return Banner.objects.first()
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Banner List'
        return context

class UpdateBannerView(LoginRequiredMixin, AdminPassesTestMixin, UpdateView):
    model = Banner
    form_class = BannerForm
    template_name = 'banner/add_update_banner.html'
    success_url = reverse_lazy('authority:banners_list')
    success_message = "Banner Updated Successfully"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Update Banner"
        context["updated"] = True
        return context

    def form_invalid(self, form):
        print(form.errors)
        error(self.request, "Something went wrong, please try again!")
        return super().form_invalid(form)


class AddBannerView(LoginRequiredMixin, AdminPassesTestMixin, CreateView):
    model = Banner
    form_class = BannerForm
    template_name = 'banner/add_update_banner.html'
    success_url = reverse_lazy('authority:banners_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Add Banner"
        return context

    def form_valid(self, form):
        messages.success(self.request, "Banner Added Successfully")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Something went wrong, please try again!")
        return super().form_invalid(form)


class BannerDeleteView(LoginRequiredMixin, AdminPassesTestMixin, DeleteView):
    def post(self, request, pk):
        banner = get_object_or_404(Banner, pk=pk)
        banner.delete()
        messages.success(request, "Banner deleted successfully.")
        return redirect('authority:banners_list')

