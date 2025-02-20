from django.http import JsonResponse
from django.shortcuts import render
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import magic
from PyPDF2 import PdfReader
from PIL import Image
import pytesseract
import docx
from asn1crypto import cms, pem
from django.core.files.storage import FileSystemStorage
import urllib.parse
import os
from .forms import ParoleChiave
from django.conf import settings

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



from django.shortcuts import render
from django.core.files.storage import FileSystemStorage

def home(request):
    if request.method == 'POST' and request.FILES.get('file'):
        maneskin_url = "/home/mbenassi/Documents/Hackaton/trenteam/hackaton"
        uploaded_file = request.FILES['file']  # Ottiene il file inviato
        fs = FileSystemStorage()
        filename = fs.save(uploaded_file.name, uploaded_file)  # Salva il file
        file_url = fs.url(filename)  # Ottiene l'URL del file salvato
        filename= urllib.parse.unquote(filename)
        
        file_url = maneskin_url + urllib.parse.unquote(file_url)


        byteFile=extract_original_file(file_url)
        file_type = magic.from_buffer(byteFile, mime=True)
        import os
        from django.conf import settings
        
        
        if os.path.exists(file_url):
            os.remove(file_url)
        
        filename=filename.replace(".p7m","")
        file_url=file_url.replace(".p7m","")


        text = ""
        if file_type == 'application/pdf':
            temp=file_url.split(".pdf")
            if len(temp)==2:
                file_url=temp[0]
            file_url+=".pdf"
        elif file_type == 'application/vnd.openxmlformats-officedocument.wordprocessingml.document':
            temp=file_url.split(".docx")
            if len(temp)==2:
                file_url=temp[0]
            file_url+=".docx"
        elif file_type == 'image/jpeg':
            temp=file_url.split(".jpeg")
            if len(temp)==2:
                file_url=temp[0]
            file_url+=".jpeg"
        elif file_type == 'image/png':
            temp=file_url.split(".png")
            if len(temp)==2:
                file_url=temp[0]
            file_url+=".png"
        print("DIOCANE"+file_url)
        
        with open(file_url.replace(".p7m",""), "wb") as file:
            file.write(byteFile)
        

        
        
        # Extract text based on file type
        text = ""
        if file_type == 'application/pdf':
            text = extract_text_from_pdf(file_url)
        elif file_type in ['image/jpeg', 'image/png']:
            text = extract_text_from_image(file_url)
        elif file_type == 'application/vnd.openxmlformats-officedocument.wordprocessingml.document':
            text = extract_text_from_docx(file_url)
        riassunto=''
        riassunto=inviaRichiesta('',text,'','Analizza il file PDF e identifica i concetti chiave basandoti sulle seguenti parole chiave: [INSERIRE PAROLE CHIAVE]. Per ogni concetto trovato, indica il numero della pagina di riferimento. Genera un riassunto dettagliato e strutturato in paragrafi, suddividendo le informazioni per argomento. Il riassunto deve essere scritto interamente in italiano, senza eccezioni, mantenendo il tono originale del documento. Non usare asterischi, trattini, Markdown o qualsiasi tipo di formattazione speciale; restituisci solo testo semplice senza simboli di markup. Se non hai parole chiave, riassumi interamente il documento.')
        print(riassunto)
        filename = urllib.parse.unquote(filename)
        
        pdf_path = request.build_absolute_uri(settings.MEDIA_URL + filename)

        return render(request, 'result.html', {'file_url': file_url,'Riassunto':riassunto, "pdf_url": pdf_path,'form':ParoleChiave(),"testo":text})  # Mostra il file

    return render(request, 'upload.html')  # Se non c'è file, mostra solo il form



def inviaRichiesta(file,testo,keywords,testoPreliminare):
    import google.generativeai as genai
    file_mime={}
    genai.configure(api_key="AIzaSyATCyWtU-wJMO97rPf7xHr0pOJrgTEE8ds") #Sostituisci con la tua chiave API
    if(file!=''):
        for i in file:
            file_mime.update({"mime_type": i[1], "data": i[0]})
    model = genai.GenerativeModel('gemini-2.0-flash')
    if(keywords!=''):
        temp=''
        for i in keywords:
            temp+=i+','
        testoPreliminare=testoPreliminare.replace('[INSERIRE PAROLE CHIAVE]',temp)
    else:
        testoPreliminare=testoPreliminare.replace('[INSERIRE PAROLE CHIAVE]','')
    prompt_parts = [
        testo
        #{"mime_type": "image/jpeg", "data": immagini}
    ]
    if(file!=''):
        prompt_parts.append(file_mime)
    response = model.generate_content(prompt_parts)

    return response.text
    #print(prompt_parts)

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

def file_type(original_file_bytes):
    file_type = magic.from_buffer(original_file_bytes, mime=True)
    return file_type
	

def result(request):
    form = ParoleChiave()  # Crea un'istanza vuota del form

    if request.method == "POST":
        form = ParoleChiave(request.POST)  # Riempie il form con i dati inviati
        
        if form.is_valid():  # Controlla se i dati sono validi
            paroleChiave = form.cleaned_data['message']
            pdf_path = form.cleaned_data['pdf_path']
            print(pdf_path)
            #riassunto=inviaRichiesta('',text,paroleChiave,'Analizza il file PDF e identifica i concetti chiave basandoti sulle seguenti parole chiave: [INSERIRE PAROLE CHIAVE]. Per ogni concetto trovato, indica il numero della pagina di riferimento. Genera un riassunto dettagliato e strutturato in paragrafi, suddividendo le informazioni per argomento. Il riassunto deve essere scritto interamente in italiano, senza eccezioni, mantenendo il tono originale del documento. Non usare asterischi, trattini, Markdown o qualsiasi tipo di formattazione speciale; restituisci solo testo semplice senza simboli di markup. Se non hai parole chiave, riassumi interamente il documento.')
            # Puoi fare qualcosa con i dati, come salvarli nel database o inviare un'email
            print("Parole chiave",paroleChiave)
            #return render(request, 'result.html', {'file_url': file_url,'Riassunto':riassunto, "pdf_url": pdf_path,'form':form,"testo":text})  # Mostra il file

    return render(request, 'result.html', {'form': form})  # Mostra il form || INTEGRATO, Decisione di esecuzione (UE)