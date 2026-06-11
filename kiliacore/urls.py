from django.urls import path, include
from . import views
urlpatterns = [
    path('', views.LandingView.as_view(), name='landing'),
    path('contact/', views.ContactFormView.as_view(), name='contact_form'),
]
