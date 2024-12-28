from django.db import models
from django.utils.timezone import now
from django.core.validators import MinValueValidator

# Create your models here.

class Banner(models.Model):
    banner_title = models.CharField(max_length=255, help_text="Title of the banner")
    banner_description = models.TextField(blank=True, null=True, help_text="Description of the banner")
    banner_video_link = models.URLField(max_length=500, blank=True, null=True, help_text="URL of the banner video")

    def __str__(self):
        return self.banner_title

    class Meta:
        verbose_name = "Banner"
        verbose_name_plural = "Banner"



class FeaturesSection(models.Model):
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Feature"
        verbose_name_plural = "Features"

class Feature(models.Model):
    section = models.ForeignKey(FeaturesSection, on_delete=models.CASCADE, related_name='features')
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to='features/')

    def __str__(self):
        return self.title

class FAQ(models.Model):
    question = models.CharField(max_length=255)
    answer = models.TextField()

    def __str__(self):
        return self.question

    class Meta:
        verbose_name = "FAQ"
        verbose_name_plural = "FAQ"

class Product(models.Model):
    title = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='products/')
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    description = models.TextField()
    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Product"


class BillingDetails(models.Model):
    name = models.CharField(max_length=255, verbose_name="আপনার নাম লিখুন")
    phone_number = models.CharField(max_length=15, verbose_name="আপনার মোবাইল নাম্বারটি লিখুন" ,null=True, blank=True)
    city = models.CharField(max_length=100, verbose_name="আপনার শহরের নাম লিখুন")
    address = models.TextField(verbose_name="আপনার সম্পূর্ণ ঠিকানা লিখুন")

    def __str__(self):
        return f"{self.name} - {self.phone_number}"

    class Meta:
        verbose_name = "BillingDetails"
        verbose_name_plural = "Billing_Details"

class OrderDetails(models.Model):
    product_name = models.CharField(max_length=255, verbose_name="Product Name")
    product_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Product Price")
    quantity = models.PositiveIntegerField(default=1, verbose_name="Quantity")
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Subtotal")
    shipping_cost = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Shipping Cost")
    total = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Total")
    billing_details = models.ForeignKey(BillingDetails, on_delete=models.CASCADE, related_name="orders")
    payment_method = models.CharField(max_length=50, default="Cash on Delivery", verbose_name="Payment Method")
    date = models.DateField(default=now, verbose_name="Order Date")

    def __str__(self):
        return f"Order for {self.product_name} - {self.total} Tk"

    class Meta:
        verbose_name = "Order Detail"
        verbose_name_plural = "Order Details"



class BusinessInfo(models.Model):
    company_name = models.CharField(max_length=255)
    phone_no = models.CharField(max_length=15)
    email = models.EmailField()
    whatsapp = models.CharField(max_length=15, null=True, blank=True)
    facebook = models.URLField(null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.company_name

    class Meta:
        verbose_name = "BusinessInfo"
        verbose_name_plural = "Business_Info"

class FrontendSetting(models.Model):
    logo = models.ImageField(upload_to='settings/logos/')
    favicon = models.ImageField(upload_to='settings/favicons/')

    def __str__(self):
        return "Frontend Settings"

    class Meta:
        verbose_name = "FrontendSetting"
        verbose_name_plural = "Front-end Setting"


class SiteSettings(models.Model):
    site_name = models.CharField(max_length=255, help_text="The name of the site.")
    gtm_id = models.CharField(max_length=20, blank=True, null=True,
                              help_text="Google Tag Manager ID (e.g., GTM-XXXXXX)")
    copyright_year = models.PositiveIntegerField(null=True, blank=True)
    def __str__(self):
        return self.site_name
