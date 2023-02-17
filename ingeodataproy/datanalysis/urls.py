from django.urls import path
from .views import CsvFileUploadView, csv_preview, time_analysis

urlpatterns = [
    path('csv-upload/', CsvFileUploadView.as_view(), name='csv_upload'),
    path('csv-preview/', csv_preview, name='csv_preview'),
    path('time-analysis/', time_analysis, name='time_analysis'),
    # ...
]

