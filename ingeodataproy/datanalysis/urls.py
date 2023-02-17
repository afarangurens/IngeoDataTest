from django.urls import path
from .views import CsvFileUploadView, csv_preview, time_analysis, heatmap_image, describe_dataset, correlate_a1_d1
from .views import k_means_cluster, home

urlpatterns = [
    path('', home, name='home'),
    path('csv-upload/', CsvFileUploadView.as_view(), name='csv_upload'),
    path('csv-preview/', csv_preview, name='csv_preview'),
    path('time-analysis/', time_analysis, name='time_analysis'),
    path('plot-heatmap/', heatmap_image, name='plot_heatmap'),
    path('describe-dataset/', describe_dataset, name='describe_dataset'),
    path('correlate-a1-d1/', correlate_a1_d1, name='correlate_a1_d1'),
    path('k-means-cluster/', k_means_cluster, name='k_means_cluster'),
]

