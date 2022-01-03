from django.urls import path
from . import views
from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from .views import *
app_name = 'dashboard'

urlpatterns = [
    path('', views.dashboard, name='home'),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.Logout, name='logout'),
    path('profile/update/', views.profile_update, name="update-profile"),
    path('profile', login_required(ProfileView.as_view(),
                                   login_url='  /user/login'), name='profile-portal-home'),
    url('^$', login_required(FinancingPortalHomeView.as_view(),
        login_url='/user/login'), name='financing-portal-home'),

    path('purchase_products', login_required(FinancingPortalPurchaseProductsView.as_view(
    ), login_url='/user/login'), name='purchase-products'),
    path('payments', login_required(FinancingPortalPaymentsView.as_view(),
                                    login_url='/user/login'), name='payments'),
    path('products_purchased', login_required(FinancingPortalProductsPurchasedView.as_view(
    ), login_url='/user/login'), name='products-purchased'),
    path('access_software', login_required(FinancingPortalAccessSoftware.as_view(
    ), login_url='/user/login'), name='products-access'),
    path('confirm_purchase/<int:pk>', login_required(
        FinancingPortalConfirmPurchaseView.as_view()), name="confirm-purchase"),
    path('plans/', login_required(views.plans,
         login_url='/user/login'), name='plans'),
    path('apply_for_loan/<str:step>', apply_for_loan, name='apply_for_loan'),

   

]
