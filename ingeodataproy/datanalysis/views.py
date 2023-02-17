from django.shortcuts import render, redirect
from django.core.cache import cache
from modules.ingeodatanalysis import read_file, plot_correlation_matrix, time_series_analysis
from io import BytesIO
import base64
from django.http import HttpResponse
import json
import pandas as pd
import tempfile
import os
from django.views import View
from .forms import CsvFileForm
from .models import CsvFile

# Create your views here.


class CsvFileUploadView(View):
    def get(self, request):
        form = CsvFileForm()
        context = {'form': form}
        return render(request, 'upload.html', context)

    def post(self, request):
        form = CsvFileForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = form.cleaned_data['file']
            CsvFile.objects.create(file=csv_file)

            return redirect('csv_preview')
        return render(request, 'upload.html', {'form': form})


def csv_preview(request):
    csv_data = cache.get('csv_data')
    if csv_data is None:
        return render(request, 'no_data.html')

    table = csv_data.to_html(classes='table table-striped')

    df_json = csv_data.to_json()

    return render(request, 'csv_preview.html', {'table': table})


def time_analysis(request):
    csv_data = cache.get('csv_data')
    if csv_data is None:
        return render(request, 'no_data.html')

    res_df = time_series_analysis(csv_data, "month")

    table = res_df.to_html(classes="table table-striped")

    return render(request, 'time-analysis.html', {'table': table})


def heatmap_image(request):
    if request.method == "POST" and request.FILES['file']:
        file = request.FILES['file']

        df = read_file(file)

        # Generate the heatmap image
        heatmap = plot_correlation_matrix(df)

        image_bytes = base64.b64decode(heatmap)

        # Save the image to a BytesIO object
        image_buffer = BytesIO()
        image_buffer.write(image_bytes)
        image_buffer.seek(0)

        encoded_image = base64.b64encode(image_buffer.getvalue()).decode('utf-8')
        image_data_uri = f"data:image/png;base64,{encoded_image}"

        # Render a new template with the image data URI as a context variable
        return render(request, 'heatmap_image.html', {'image_data_uri': image_data_uri})
    else:
        return render(request, 'upload.html')