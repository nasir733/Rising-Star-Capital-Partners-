from django.urls import path
from . import views
from django.conf import settings
import debug_toolbar
from django.urls import include, path
from django.conf.urls.static import static
urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('case_studies/', views.case_studies, name='case_studies'),
    path('contact/', views.contact, name='contact'),
    path('send_email/', views.send_email, name='send_mail'),
    path('sendesta/', views.sendesta, name='sendesta'),
    path('vukode/', views.vukode, name='vukode'),
    path('bradstreet/', views.bradstreet, name='bradstreet'),
    path('ziteso/', views.ziteso, name='ziteso'),
    path('services/', views.services, name='services'),
    path('team/', views.team, name='team'),
    path('testimonial/', views.testimonial, name='testimonial'),
    path('__debug__/', include(debug_toolbar.urls)),
     path("config/", views.stripe_config),
    path("create-checkout-session-loan-origin-fee/<int:plan_id>/",
         views.Createloanoriginfeesession, name="create-checkout-session-loan-origin-fee"),
     path("create-checkout-session-subscription/<int:plan_id>/",
         views.Createloansubcriptionsession, name="create-checkout-session-loan-origin-fee"),
    path("success-loan-origin-fee/<int:plan_id>/", views.CreateloanoriginfeesessionSucess,
         name="success-loan-origin-fee"),
         
     path("success-loan-subscription/<int:plan_id>/", views.CreateloansubscriptionSucess,
         name="success-loan-subscription"),
    path("webhook", views.webhook, name="webhook"),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
