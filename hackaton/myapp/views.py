from django.http import JsonResponse
from django.shortcuts import render
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from .forms import UploadFileForm
import magic
from PyPDF2 import PdfReader
from PIL import Image
import pytesseract
import docx
from asn1crypto import cms, pem
from django.core.files.storage import FileSystemStorage


def extract_text_from_pdf(file_path):
    reader = PdfReader(file_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

def extract_text_from_image(file_path):
    image = Image.open(file_path)
    text = pytesseract.image_to_string(image)
    return text

def extract_text_from_docx(file_path):
    doc = docx.Document(file_path)
    text = "\n".join([para.text for para in doc.paragraphs])
    return text

def extract_original_file(p7m_file_path):
    with open(p7m_file_path, 'rb') as f:
        if pem.detect(f.read()):
            f.seek(0)
            _, _, der_bytes = pem.unarmor(f.read())
        else:
            f.seek(0)
            der_bytes = f.read()

    content_info = cms.ContentInfo.load(der_bytes)
    if content_info['content_type'].native != 'signed_data':
        raise ValueError("The file is not a valid signed PKCS#7 file.")

    signed_data = content_info['content']
    encap_content_info = signed_data['encap_content_info']

    if encap_content_info['content_type'].native == 'data':
        original_file = encap_content_info['content'].native
        return original_file
    else:
        raise ValueError("The encapsulated content is not of type 'data'.")

def result(request):
    #extracted_text = request.GET.get('extracted_text', '')
    print("PIPPO")
    print(request.method)
    print(request.FILES.get('file'))
    return render(request, 'result.html', {'extracted_text': 'CIAOOO'})

from django.shortcuts import render
from django.core.files.storage import FileSystemStorage

def home(request):
    if request.method == 'POST' and request.FILES.get('file'):
        uploaded_file = request.FILES['file']  # Ottiene il file inviato
        fs = FileSystemStorage()
        filename = fs.save(uploaded_file.name, uploaded_file)  # Salva il file
        file_url = fs.url(filename)  # Ottiene l'URL del file salvato

        return render(request, 'result.html', {'file_url': file_url})  # Mostra il file

    return render(request, 'upload.html')  # Se non c'è file, mostra solo il form









