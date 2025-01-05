from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib import messages
from django.db.models import Sum, Count
from django.shortcuts import get_object_or_404, redirect
from django.forms import inlineformset_factory

# class-based view classes
from django.views.generic import DetailView
from django.views.generic import ListView
from django.views.generic import DeleteView
from django.views.generic import UpdateView



# Permission and Authentication
from django.contrib.auth.mixins import LoginRequiredMixin
from authority.permissions import AdminPassesTestMixin

# Import Models
from Homepage.models import(
OrderDetails,BillingDetails
)
from authority.forms import BillingDetailsForm,OrderDetailsForm


   


#<<----------------- List, Add, Update, Delete Order ---------------->>

class OrderListView(LoginRequiredMixin, AdminPassesTestMixin, ListView):
    model = OrderDetails
    template_name = 'orders/order_list.html'
    context_object_name = 'orders_list'
    paginate_by = 6

    def get_queryset(self):
        return OrderDetails.objects.select_related('billing_details') \
            .prefetch_related('order_items') \
            .annotate(total_quantity=Sum('order_items__quantity')) \
            .order_by('-id')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Order List"
        return context

class OrderDetailView(LoginRequiredMixin, AdminPassesTestMixin, DetailView):
    model = OrderDetails
    template_name = 'orders/order_details.html'
    context_object_name = 'order'
    def get_queryset(self):
        return OrderDetails.objects.select_related('billing_details').prefetch_related('order_items')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        order = self.object
        context["order_items"] = order.order_items.all()
        context["title"] = f"Order Details - #{order.id}"
        return context

class OrderDeleteView(LoginRequiredMixin, AdminPassesTestMixin, DeleteView):
    def post(self, request, pk):
        order = get_object_or_404(OrderDetails, pk=pk)
        order.delete()
        messages.success(request, "Order deleted successfully.")
        return redirect('authority:order_list')


