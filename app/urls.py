from django.urls import path
from .views import submit_form, success

urlpatterns = [
    path('', submit_form, name='submit_form'),
    path('success/', success, name='success'),
]