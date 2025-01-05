from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib import messages
from django.forms import inlineformset_factory
from django.db.models import Sum,Count,Q,F
from django.core.paginator import Paginator

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

# Import Models
from Homepage.models import(
 Product
)



#Import Forms
from authority.forms import(

    ProductForm,

)

class AddProductView(LoginRequiredMixin, AdminPassesTestMixin, CreateView):
    model = Product
    template_name = 'product/add_update_product.html'
    form_class = ProductForm
    success_url = reverse_lazy('authority:product_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Add Product"
        return context

    def form_valid(self, form):
        messages.success(self.request, "Product Added Successfully")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Something went wrong, please try again!")
        return super().form_invalid(form)


class UpdateProductView(LoginRequiredMixin, AdminPassesTestMixin, UpdateView):
    model = Product
    template_name = 'product/add_update_product.html'
    form_class = ProductForm
    success_url = reverse_lazy('authority:product_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Update Product"
        context["updated"] = True
        return context

    def form_valid(self, form):
        messages.success(self.request, "Product Updated Successfully")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Something went wrong, please try again!")
        return super().form_invalid(form)


class ProductListView(LoginRequiredMixin,AdminPassesTestMixin, ListView):
    model = Product
    template_name = 'product/product_list.html'
    context_object_name = 'products_list'
    paginate_by = 10

    def get_queryset(self):
        return Product.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Product List"
        return context


class ProductDeleteView(LoginRequiredMixin, AdminPassesTestMixin, DeleteView):
    def post(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        product.delete()
        messages.success(request, "Product deleted successfully.")
        return redirect('authority:product_list')