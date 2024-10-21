from django.urls import path

from .views import *

urlpatterns = [
    path('', form_view, name='index'),
    path('report/download', generate_report, name='download_report')
]