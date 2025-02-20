from django.contrib import admin
from .models import Documento



class DocumentoAdmin(admin.ModelAdmin):
    list_display = ("id", "parole_chiave", "pdf_path")  # Colonne visibili
    search_fields = ("parole_chiave",)  # Campo di ricerca
    list_filter = ("parole_chiave",)  # Filtri laterali
    ordering = ("id",)  # Ordine di default

admin.site.register(Documento, DocumentoAdmin)  # Registra con personalizzazione


