from django.contrib import admin
from .models import FeaturesSection,Feature,Product,Banner,BusinessInfo,\
    FrontendSetting,FAQ,OrderDetails,BillingDetails,SiteSettings,OrderItem

from django.utils.html import format_html

@admin.register(FrontendSetting)
class FrontendSettingAdmin(admin.ModelAdmin):
    list_display = ('id', 'logo_preview', 'favicon_preview')

    def logo_preview(self, obj):
        if obj.logo:
            return format_html('<img src="{}" style="width: 50px; height: auto;" alt="Logo">', obj.logo.url)
        return "No Logo"

    def favicon_preview(self, obj):
        if obj.favicon:
            return format_html('<img src="{}" style="width: 20px; height: auto;" alt="Favicon">', obj.favicon.url)
        return "No Favicon"

    logo_preview.short_description = "Logo"
    favicon_preview.short_description = "Favicon"

@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display = ('banner_title', 'banner_video_link')
    search_fields = ('banner_title', 'banner_description')
    list_filter = ('banner_title',)

class FeatureInline(admin.TabularInline):
    model = Feature
    extra = 1

@admin.register(FeaturesSection)
class FeaturesSectionAdmin(admin.ModelAdmin):
    list_display = ('title',)
    inlines = [FeatureInline]


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ('id', 'question')
    search_fields = ('question',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'discount_price')
    search_fields = ('title', 'description')
    list_filter = ('price', 'discount_price')

@admin.register(BusinessInfo)
class BusinessInfoAdmin(admin.ModelAdmin):
    list_display = ('company_name', 'phone_no', 'email', 'whatsapp', 'facebook','messenger','address')
    search_fields = ('company_name', 'email', 'phone_no')


@admin.register(BillingDetails)
class BillingDetailsAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone_number', 'city', 'address')
    search_fields = ('name', 'phone_number', 'city')

@admin.register(OrderDetails)
class OrderDetailsAdmin(admin.ModelAdmin):
    list_display = ('id', 'billing_details', 'subtotal', 'total', 'shipping_cost', 'payment_method', 'date')
    list_filter = ('payment_method', 'date')
    search_fields = ('billing_details__name', 'billing_details__phone_number')
    date_hierarchy = 'date'


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'product', 'quantity','total_price')
    list_filter = ('order', 'product')
    search_fields = ('order__billing_details__name', 'product__title')


@admin.register(SiteSettings)
class SiteSettings(admin.ModelAdmin):
    list_display = ('site_name', 'gtm_id', 'copyright_year', 'keywords', 'description', 'facebook_domain_verification_id',
              'google_site_verification_id')
