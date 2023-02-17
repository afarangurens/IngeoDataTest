from modules.ingeodatanalysis import read_file
from django.core.cache import cache
from datanalysis.models import CsvFile
from django.urls import reverse


class CsvFileMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        """
        Middleware that reads a CSV file into a DataFrame and caches it in memory.

        Args:
            request (HttpRequest): The HTTP request object.

        Returns:
            HttpResponse: The HTTP response object.
        """
        if request.path == reverse('csv_upload'):
            return self.get_response(request)

        df = cache.get('csv_data')

        if df is None:
            csv_file = CsvFile.objects.latest('uploaded_at').file
            df = read_file(csv_file)
            cache.set('csv_data', df)

        return self.get_response(request)


