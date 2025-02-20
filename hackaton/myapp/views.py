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

def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                # Save the uploaded .p7m file
                uploaded_file = request.FILES['file']
                file_path = default_storage.save(uploaded_file.name, ContentFile(uploaded_file.read()))

                # Extract the original file from the .p7m
                original_file = extract_original_file(file_path)
                if not original_file:
                    return JsonResponse({"success": False, "error": "Failed to extract the original file."})

                # Save the original file temporarily
                original_file_path = default_storage.save('original_file', ContentFile(original_file))
                file_type = magic.from_file(original_file_path, mime=True)

                # Extract text based on file type
                text = ""
                if file_type == 'application/pdf':
                    text = extract_text_from_pdf(original_file_path)
                elif file_type in ['image/jpeg', 'image/png']:
                    text = extract_text_from_image(original_file_path)
                elif file_type == 'application/vnd.openxmlformats-officedocument.wordprocessingml.document':
                    text = extract_text_from_docx(original_file_path)
                else:
                    return JsonResponse({"success": False, "error": "Unsupported file type."})

                # Clean up temporary files
                default_storage.delete(file_path)
                default_storage.delete(original_file_path)

                # Return the extracted text
                return JsonResponse({"success": True, "extracted_text": text})
            except Exception as e:
                return JsonResponse({"success": False, "error": str(e)})
        else:
            return JsonResponse({"success": False, "error": "Invalid form submission."})
    else:
        form = UploadFileForm()
    return render(request, 'upload.html', {'form': form})