from django.db import models

class Documento(models.Model):
    id = models.AutoField(primary_key=True)  # ID auto-incrementato
    pdf_path = models.CharField(max_length=1000)  # Percorso del file PDF
    parole_chiave = models.CharField(max_length=1000)  # Stringa con parole chiave
    file_url = models.CharField(max_length=1000)  # Percorso del file PDF
    nome_file= models.CharField(max_length=1000)  # Nome del file


    def __str__(self):
        return f"Documento {self.id} - {self.parole_chiave}"
