from django.urls import path, include
from django.views.generic import RedirectView
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.LandingView.as_view(), name='landing'),
    path('contact/', views.ContactFormView.as_view(), name='contact_form'),
    path('favicon.ico', RedirectView.as_view(url='/static/favicon/favicon.ico', permanent=True)),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
