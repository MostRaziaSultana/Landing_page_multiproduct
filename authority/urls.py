from django.urls import path


app_name='authority'

from authority.views import authority_main
from authority.views import manage_user
from authority.views import manage_order
from authority.views import manage_product
from authority.views import manage_features
from authority.views import manage_banner
from authority.views import manage_faq
from authority.views import manage_businessinfo
from authority.views import manage_frontend
from authority.views import manage_sitesettings




urlpatterns = [
    path('', authority_main.AdminView.as_view(), name='authority_admin')
]

#Manage User
urlpatterns += [
    path('user-list/', manage_user.UserListView.as_view(), name='user_list'),
    path('login/', manage_user.CustomLoginView.as_view(), name='login'),
    path('logout/',  manage_user.CustomLogoutView.as_view(), name='logout'),
    path('add_admin/', manage_user.AddAdminUserView.as_view(), name='add_admin'),
    path('delete_admin/<int:pk>/', manage_user.DeleteUserView.as_view(), name='delete_admin')
]

# Manage Orders
urlpatterns += [
    path('order-list/', manage_order.OrderListView.as_view(), name='order_list'),
    path('order_details/<int:pk>/', manage_order.OrderDetailView.as_view(), name='order_details'),
    path('delete_order/<int:pk>/', manage_order.OrderDeleteView.as_view(), name='delete_order'),

]
# Manage Product
urlpatterns += [
    path('product-list/', manage_product.ProductListView.as_view(), name='product_list'),
    path('product-update/<int:pk>/', manage_product.UpdateProductView.as_view(), name='product_update'),
    path('add-product/', manage_product.AddProductView.as_view(), name='add_product'),
    path('product_delete/<int:pk>/', manage_product.ProductDeleteView.as_view(), name='product_delete'),

]

# Manage Feature
urlpatterns += [
    path('features-list/', manage_features.FeaturesListView.as_view(), name='features_list'),
    path('add_feature/', manage_features.AddFeaturesSectionView.as_view(), name='add_feature'),
    path('feature-update/<int:pk>/', manage_features.UpdateFeaturesSectionView.as_view(), name='feature_update'),
    path('feature_delete/<int:pk>/', manage_features.FeatureDeleteView.as_view(), name='feature_delete'),

]

# Manage Banners
urlpatterns += [
    path('banners-list/', manage_banner.BannerListView.as_view(), name='banners_list'),
    path('add_banner/', manage_banner.AddBannerView.as_view(), name='add_banner'),
    path('banner-update/<int:pk>/', manage_banner.UpdateBannerView.as_view(), name='update_banner'),
    path('banner_delete/<int:pk>/', manage_banner.BannerDeleteView.as_view(), name='delete_banner'),

]

# Manage FAQ
urlpatterns += [
    path('faq-list/', manage_faq.FAQListView.as_view(), name='faq_list'),
    path('add_faq/', manage_faq.AddFAQView.as_view(), name='add_faq'),
    path('faq-update/<int:pk>/', manage_faq.UpdateFAQView.as_view(), name='faq_update'),
    path('faq_delete/<int:pk>/', manage_faq.FAQDeleteView.as_view(), name='faq_delete'),
]

# Manage Businessinfo
urlpatterns += [
    path('business-list/', manage_businessinfo.BusinessInfoListView.as_view(), name='business_list'),
    path('add_business/', manage_businessinfo.AddBusinessInfoView.as_view(), name='add_business'),
    path('business-update/<int:pk>/', manage_businessinfo.UpdateBusinessInfoView.as_view(), name='business_update'),
    path('business-delete/<int:pk>/', manage_businessinfo.BusinessInfoDeleteView.as_view(), name='business_delete'),
]


# Manage Frontend Settings
urlpatterns += [
    path('frontend-settings/', manage_frontend.FrontendSettingsListView.as_view(), name='frontend_settings'),
    path('frontend-settings/add/', manage_frontend.AddFrontendSettingView.as_view(), name='add_frontend_setting'),
    path('frontend-settings/<int:pk>/update/', manage_frontend.UpdateFrontendSettingView.as_view(), name='update_frontend_setting'),
    path('frontend-settings/<int:pk>/delete/', manage_frontend.FrontendSettingDeleteView.as_view(), name='delete_frontend_setting'),
]


# Manage Site Settings
urlpatterns += [
    path('site-settings/', manage_sitesettings.SiteSettingsListView.as_view(), name='site_settings'),
    path('site-settings/add/', manage_sitesettings.AddSiteSettingView.as_view(), name='add_site_setting'),
    path('site-settings/<int:pk>/update/', manage_sitesettings.UpdateSiteSettingView.as_view(), name='update_site_setting'),
    path('site-settings/<int:pk>/delete/', manage_sitesettings.SiteSettingDeleteView.as_view(), name='delete_site_setting'),
]


