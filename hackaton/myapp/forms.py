from django import forms

class ParoleChiave(forms.Form):
    message = forms.CharField(label="Parole Chiave", max_length=1000)
    pdf_path=forms.CharField(label="pdf path", max_length=1000, required=False)
    file_url=forms.CharField(label="file url", max_length=1000, required=False)

