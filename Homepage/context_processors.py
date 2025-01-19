from .models import Banner,BusinessInfo,FrontendSetting,\
    OrderDetails,Feature,FAQ,BillingDetails,FeaturesSection,SiteSettings,Product
from django.contrib.auth.models import User
from django.db.models import Count, Sum
from django.utils.timezone import now



def banner(request):
    return {
        'banner': Banner.objects.first(),
    }


def businessinfo(request):
    return {
        'businessinfo': BusinessInfo.objects.first(),
    }


def frontend_setting(request):
    return {
        'frontend_setting': FrontendSetting.objects.first(),
    }

def feature_section(request):
    return {
        'feature_section': FeaturesSection.objects.first(),
    }

def site_settings(request):
    return {
        'site_settings': SiteSettings.objects.first(),
    }



def last_orders(request):
    today = now().date()
    total_admin = User.objects.filter(is_staff=True).count()
    total_orders = OrderDetails.objects.count()
    total_feature = Feature.objects.count()
    total_faq = FAQ.objects.count()
    latest_orders = OrderDetails.objects.select_related("billing_details") \
                        .prefetch_related('order_items') \
                        .annotate(total_quantity=Sum('order_items__quantity')) \
                        .order_by("-date")[:10]
    todays_orders = OrderDetails.objects.filter(date=today).count()
    total_banner = Banner.objects.count()
    total_products = Product.objects.count()
    # Count non-empty social media fields in BusinessInfo
    business_info = BusinessInfo.objects.first()
    total_social_media = 0
    if business_info:
        social_media_fields = ['facebook', 'whatsapp']
        total_social_media = sum(1 for field in social_media_fields if getattr(business_info, field))

    return {

        'total_admin': total_admin,
        'total_orders':total_orders,
        'total_feature':total_feature,
        'total_faq': total_faq,
        'latest_orders':latest_orders,
        'todays_orders':todays_orders,
        'total_banner':total_banner,
        'total_products': total_products,
        'total_social_media': total_social_media,

    }


from django.shortcuts import redirect
from django.urls import reverse_lazy

# class-based view classes
from django.views.generic import TemplateView
from django.views.generic import ListView

# Permission and Authentication
from django.contrib.auth.mixins import LoginRequiredMixin
from authority.permissions import AdminPassesTestMixin

# Import Models
from django.contrib.auth.models import User


# Create your views here.
class AdminView(LoginRequiredMixin, AdminPassesTestMixin, TemplateView):
    template_name = 'authority/admin.html'
    success_url = reverse_lazy('authority:authority_admin'),
    login_url = reverse_lazy('authority:login')


