from django.urls import path
from .views import contact_submit

urlpatterns = [
    path('contact_submit/', contact_submit, name='contact_submit'),
]
