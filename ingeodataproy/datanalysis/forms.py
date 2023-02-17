from django import forms


class CsvFileForm(forms.Form):
    file = forms.FileField(label='Select a CSV file', help_text='Max. 10 MB')
