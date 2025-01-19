from django import forms
from django.forms import inlineformset_factory
from django.contrib.auth.hashers import make_password
from ckeditor.widgets import CKEditorWidget


# models
from django.contrib.auth.models import User
from Homepage.models import(
Banner,Product,BusinessInfo,FrontendSetting,OrderDetails,Feature,FAQ,BillingDetails,FeaturesSection,SiteSettings,OrderItem
)

# forms
class UserInfoForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('first_name', 'last_name','is_staff')


class BillingDetailsForm(forms.ModelForm):
    class Meta:
        model = BillingDetails
        fields = ['name', 'phone_number', 'city', 'address']

class OrderDetailsForm(forms.ModelForm):
    class Meta:
        model = OrderDetails
        fields = ['shipping_cost', 'subtotal', 'total', 'billing_details', 'payment_method', 'date']


class OrderItemForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        fields = ['order', 'product', 'quantity','total_price']
class BusinessInfoForm(forms.ModelForm):
    class Meta:
        model = BusinessInfo
        fields = ['company_name', 'phone_no', 'email', 'whatsapp', 'facebook','messenger','address']

class FrontendSettingForm(forms.ModelForm):
    class Meta:
        model = FrontendSetting
        fields = ['logo', 'favicon']

class BannerForm(forms.ModelForm):
    class Meta:
        model = Banner
        fields = ['banner_title', 'banner_description', 'banner_video_link']

class FeaturesSectionForm(forms.ModelForm):
    class Meta:
        model = FeaturesSection
        fields = ['title']

class FeatureForm(forms.ModelForm):
    class Meta:
        model = Feature
        fields = ['section', 'title']

class FAQForm(forms.ModelForm):
    class Meta:
        model = FAQ
        fields = ['question', 'answer']

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['title', 'price', 'image', 'discount_price', 'description']


class AddAdminUserForm(forms.ModelForm):
    full_name = forms.CharField(max_length=150, required=True, label="Full Name")
    phone_number = forms.CharField(max_length=15, required=True, label="Phone Number")
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Password must contain at least 8 characters'}) ,      required=True,
        label="Password"
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def clean_full_name(self):
        full_name = self.cleaned_data.get('full_name')
        if len(full_name.split(' ')) < 2:
            raise forms.ValidationError("Please enter both first and last names.")
        return full_name

    def save(self, commit=True):
        user = super().save(commit=False)
        full_name = self.cleaned_data['full_name'].split(' ', 1)
        user.first_name = full_name[0]
        user.last_name = full_name[1] if len(full_name) > 1 else ""
        user.password = make_password(self.cleaned_data['password'])
        user.is_staff = True
        user.is_superuser = True
        if commit:
            user.save()
        return user



class SiteSettingsForm(forms.ModelForm):
    class Meta:
        model = SiteSettings
        fields = ['site_name', 'gtm_id', 'copyright_year', 'keywords', 'description','facebook_domain_verification_id',
                  'google_site_verification_id']
        keywords = forms.CharField(
            widget=forms.Textarea(
                attrs={'placeholder': 'Enter meta keywords separated by commas', 'rows': 4, 'cols': 40,
                       'class': 'form-control'}
            ),
            required=False,
            label="Keywords"
        )