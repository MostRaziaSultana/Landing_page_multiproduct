from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib import messages
from django.db.models import Sum, Count
from django.shortcuts import get_object_or_404, redirect
from django.forms import inlineformset_factory

from django.views.generic import DetailView
from django.views.generic import ListView
from django.views.generic import DeleteView
from django.views.generic import UpdateView
from django.views.generic import CreateView

from django.contrib.auth.mixins import LoginRequiredMixin
from authority.permissions import AdminPassesTestMixin

# Import Models
from Homepage.models import (
    FeaturesSection, Feature
)
from authority.forms import FeatureForm,FeaturesSectionForm

# <<----------------- List, Add, Update, Delete Features ---------------->>

class FeaturesListView(LoginRequiredMixin,AdminPassesTestMixin, ListView):
    model = Feature
    template_name = 'features/features_list.html'
    context_object_name = 'features_list'

    def get_queryset(self):
        return Feature.objects.select_related('section').order_by('-title')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Features List"
        return context

class AddFeaturesSectionView(LoginRequiredMixin, AdminPassesTestMixin, CreateView):
    model = FeaturesSection
    template_name = 'features/add_update_features.html'
    form_class = FeaturesSectionForm
    success_url = reverse_lazy('authority:features_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Create formset for features
        FeatureFormSet = inlineformset_factory(
            FeaturesSection, Feature,
            fields=('title'),
            extra=1, can_delete=True
        )

        if self.request.POST:
            context['feature_formset'] = FeatureFormSet(self.request.POST, self.request.FILES)
        else:
            context['feature_formset'] = FeatureFormSet()

        context['title'] = "Add Features Section"
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        feature_formset = context['feature_formset']


        if feature_formset.is_valid():
            self.object = form.save()
            feature_formset.instance = self.object
            feature_formset.save()
            messages.success(self.request, "Features Section and Features added successfully!")
            return redirect(self.success_url)
        else:
            messages.error(self.request, "Something went wrong with the features, please try again!")
            return self.form_invalid(form)


class UpdateFeaturesSectionView(LoginRequiredMixin, AdminPassesTestMixin, UpdateView):
    model = FeaturesSection
    template_name = 'features/add_update_features.html'
    form_class = FeaturesSectionForm
    success_url = reverse_lazy('authority:features_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        FeatureFormSet = inlineformset_factory(
            FeaturesSection, Feature,
            fields=('title',),
            extra=0,
            can_delete=True
        )

        if self.request.POST:
            context['feature_formset'] = FeatureFormSet(
                self.request.POST, self.request.FILES, instance=self.object
            )
        else:
            context['feature_formset'] = FeatureFormSet(instance=self.object)

        context['title'] = "Update Features Section"
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        feature_formset = context['feature_formset']

        if feature_formset.is_valid():
            self.object = form.save()
            feature_formset.instance = self.object
            feature_formset.save()

            messages.success(self.request, "Features Section and Features updated successfully!")
            return redirect(self.success_url)
        else:
            messages.error(self.request, "Please fix the errors below and try again.")
            return self.form_invalid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Something went wrong. Please check your inputs.")
        return self.render_to_response(self.get_context_data(form=form))

class FeatureDeleteView(LoginRequiredMixin, AdminPassesTestMixin, DeleteView):
    def post(self, request, pk):
        feature = get_object_or_404(FeaturesSection, pk=pk)
        feature.delete()
        messages.success(request, "Feature deleted successfully.")
        return redirect('authority:features_list')