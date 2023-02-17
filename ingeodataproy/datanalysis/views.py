from django.shortcuts import render, redirect
from django.core.cache import cache
from modules.ingeodatanalysis import read_file, plot_correlation_matrix, time_series_analysis, describe_statistically
from modules.ingeodatanalysis import gas_diesel_correlation, k_means_clustering
from io import BytesIO
import base64
from django.views import View
from .forms import CsvFileForm
from .models import CsvFile


class CsvFileUploadView(View):
    def get(self, request):
        # Create an instance of the CsvFileForm.
        form = CsvFileForm()

        # Create a dictionary with the form and assign it to the context variable.
        context = {'form': form}

        # Render the 'upload.html' template with the context and return the response.
        return render(request, 'upload.html', context)

    def post(self, request):
        # Create an instance of the CsvFileForm with the POST and FILES data.
        form = CsvFileForm(request.POST, request.FILES)

        # Check if the form is valid.
        if form.is_valid():
            # Get the cleaned csv file data from the form.
            csv_file = form.cleaned_data['file']

            # Create a new CsvFile instance with the csv file data.
            CsvFile.objects.create(file=csv_file)

            # Redirect to the 'csv_preview' view.
            return redirect('csv_preview')

        # If the form is not valid, render the 'upload.html' template with the form and return the response.
        return render(request, 'upload.html', {'form': form})


def csv_preview(request):
    """
    Description: This view allows users to upload a CSV file, preview the contents of the file, and save it to a database.

    Context: The view expects a request object from the user. If the user is accessing the view via a POST request,
    the CSV file is validated and then displayed as an HTML table to allow the user to preview the contents.

    :param request: The HTTP request object.
    :return: The HTTP response object.
    """
    # Get the csv data from the cache.
    csv_data = cache.get('csv_data')

    # Check if the csv data is None.
    if csv_data is None:
        # If the csv data is None, render the 'no_data.html' template and return the response.
        return render(request, 'no_data.html')

    # Convert the csv data to an HTML table.
    table = csv_data.to_html(classes='table table-striped')

    # Convert the csv data to JSON format.
    df_json = csv_data.to_json()

    # Render the 'csv_preview.html' template with the table and return the dataframe as a html table.
    return render(request, 'csv_preview.html', {'table': table})


def time_analysis(request):
    """
    Perform time series analysis on a CSV file and display the results in an HTML table.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The HTTP response object containing the HTML table of the time series analysis results.
    """
    # Get the CSV data from the cache.
    csv_data = cache.get('csv_data')

    # If the CSV data is None, render the 'no_data.html' template and return the response.
    if csv_data is None:
        return render(request, 'no_data.html')

    # Perform time series analysis on the CSV data.
    res_df = time_series_analysis(csv_data, "month")

    # Convert the result to an HTML table.
    table = res_df.to_html(classes="table table-striped")

    # Render the 'time-analysis.html' template with the table and return the response.
    return render(request, 'time-analysis.html', {'table': table})


def heatmap_image(request):
    """
    Generate a heatmap image from a CSV file and display it in an HTML page.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The HTTP response object containing the HTML page with the heatmap image.
    """
    # Get the CSV data from the cache.
    csv_data = cache.get('csv_data')

    # If the CSV data is None, render the 'no_data.html' template and return the response.
    if csv_data is None:
        return render(request, 'no_data.html')

    # Generate the heatmap image.
    heatmap = plot_correlation_matrix(csv_data)

    image_bytes = base64.b64decode(heatmap)

    # Save the image to a BytesIO object.
    image_buffer = BytesIO()
    image_buffer.write(image_bytes)
    image_buffer.seek(0)

    encoded_image = base64.b64encode(image_buffer.getvalue()).decode('utf-8')
    image_data_uri = f"data:image/png;base64,{encoded_image}"

    # Render the 'heatmap_image.html' template with the image data URI as a context variable.
    return render(request, 'heatmap_image.html', {'image_data_uri': image_data_uri})


def describe_dataset(request):
    """
    Describe the statistics of a dataset from a CSV file and display them in an HTML table.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The HTTP response object containing the HTML page with the dataset statistics.
    """
    # Get the CSV data from the cache.
    csv_data = cache.get('csv_data')

    # If the CSV data is None, render the 'no_data.html' template and return the response.
    if csv_data is None:
        return render(request, 'no_data.html')

    # Describe the statistics of the CSV data.
    described_df = describe_statistically(csv_data)

    table = described_df.to_html(classes="table table-striped")

    # Render the 'describe_dataset.html' template with the statistics table as a context variable.
    return render(request, 'describe_dataset.html', {'table': table})


def correlate_a1_d1(request):
    """
    Calculate the Pearson correlation coefficient between gas and diesel consumption and display it.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The HTTP response object containing the HTML page with the Pearson correlation coefficient.
    """
    # Get the CSV data from the cache.
    csv_data = cache.get('csv_data')

    # If the CSV data is None, render the 'no_data.html' template and return the response.
    if csv_data is None:
        return render(request, 'no_data.html')

    # Calculate the Pearson correlation coefficient between gas and diesel consumption.
    person_coefficient = gas_diesel_correlation(csv_data)

    # Render the 'pearson_correlation.html' template with the Pearson correlation coefficient as a context variable.
    return render(request, 'pearson_correlation.html', {'correlation': person_coefficient})


def k_means_cluster(request):
    """
    Perform k-means clustering on the CSV data and display the resulting clusters.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The HTTP response object containing the HTML page with the cluster table.
    """
    # Get the CSV data from the cache.
    csv_data = cache.get('csv_data')

    # If the CSV data is None, render the 'no_data.html' template and return the response.
    if csv_data is None:
        return render(request, 'no_data.html')

    # Perform k-means clustering on the CSV data.
    clus_df, _ = k_means_clustering(csv_data)

    # Convert the resulting cluster DataFrame to an HTML table.
    table = clus_df.to_html(classes="table table-striped")

    # Render the 'k_means_cluster.html' template with the cluster table as a context variable.
    return render(request, 'k_means_cluster.html', {'table': table})


def home(request):
    """
    Render the home page.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The HTTP response object containing the 'home.html' template.
    """
    # Render the 'home.html' template and return the response.
    return render(request, 'home.html')

