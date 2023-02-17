from django.shortcuts import render
from .forms import UploadFileForm
from modules.ingeodatanalysis import read_file
from .models import GasPrices


# Create your views here.


def upload_file(request):
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():

            file = request.FILES['file']

            df = read_file(file)

            for index, row in df.iterrows():
                data_obj = GasPrices(
                    date=row['Date'],
                    a1=row['A1'],
                    a2=row['A2'],
                    a3=row['A3'],
                    r1=row['R1'],
                    r2=row['R2'],
                    r3=row['R3'],
                    m1=row['M1'],
                    m2=row['M2'],
                    m3=row['M3'],
                    p1=row['P1'],
                    p2=row['P2'],
                    p3=row['P3'],
                    d1=row['D1'],
                )

                data_obj.save()

            return render(request, 'success.html')
    else:
        form = UploadFileForm()

    return render(request, 'upload.html', {'form': form})
