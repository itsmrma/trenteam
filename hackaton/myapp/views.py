from django.shortcuts import render
from .models import Documento
import magic
from asn1crypto import cms, pem
from django.core.files.storage import FileSystemStorage
import urllib.parse
import io
from .forms import ParoleChiave
from docx2pdf import convert
import tempfile
import os



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
        import os
        maneskin_url = os.getcwd()
        uploaded_file = request.FILES['file']  # Ottiene il file inviato
        fs = FileSystemStorage()
        filename = fs.save(uploaded_file.name, uploaded_file)  # Salva il file
        file_url = fs.url(filename)  # Ottiene l'URL del file salvato
        filename= urllib.parse.unquote(filename)
        
        file_url = maneskin_url + urllib.parse.unquote(file_url)


        byteFile=extract_original_file(file_url)
        file_type = magic.from_buffer(byteFile, mime=True)
        
        from django.conf import settings

        if file_type == 'application/vnd.openxmlformats-officedocument.wordprocessingml.document':
            file_url = file_url.replace(".p7m", "")
            filename = filename.replace(".p7m", "")
            with open(file_url, "wb") as file:
                file.write(byteFile)
            
            filename = filename.replace(".docx", ".pdf")
            print(filename)
            dest = file_url.replace(".docx", ".pdf")
            convert(file_url, dest)

            file_type = 'application/pdf'
            file_url = dest

        else:
            if os.path.exists(file_url):
                os.remove(file_url)
            
            filename=filename.replace(".p7m","")
            file_url=file_url.replace(".p7m","")

            
            with open(file_url.replace(".p7m",""), "wb") as file:
                file.write(byteFile)
            

        
        riassunto=''
        riassunto=inviaRichiesta((file_type,file_to_bytes(file_url)),'','','Analizza il file PDF e identifica i concetti chiave basandoti sulle seguenti parole chiave: [INSERIRE PAROLE CHIAVE]. Per ogni concetto trovato, indica il numero della pagina di riferimento. Genera un riassunto dettagliato e strutturato in paragrafi, suddividendo le informazioni per argomento. Il riassunto deve essere scritto interamente in italiano, senza eccezioni, mantenendo il tono originale del documento. Non usare asterischi, trattini, Markdown o qualsiasi tipo di formattazione speciale; restituisci solo testo semplice senza simboli di markup. Se non hai parole chiave, riassumi interamente il documento.')
        filename = urllib.parse.unquote(filename)
        
        pdf_path = request.build_absolute_uri(settings.MEDIA_URL + filename)
        request.session["file_url"]=file_url
        request.session["pdf_url"]=pdf_path
        return render(request, 'result.html', {'file_url': file_url,'Riassunto':riassunto, "pdf_url": pdf_path,'form':ParoleChiave()})  # Mostra il file

    return render(request, 'upload.html')  # Se non c'è file, mostra solo il form



def inviaRichiesta(file,testo,keywords,testoPreliminare):
    import google.generativeai as genai
    genai.configure(api_key="AIzaSyATCyWtU-wJMO97rPf7xHr0pOJrgTEE8ds") #Sostituisci con la tua chiave API

    model = genai.GenerativeModel('gemini-2.0-flash')
    if(keywords!=''):
        testo=testoPreliminare.replace('[INSERIRE PAROLE CHIAVE]',keywords)+testo
    else:
        testo=testoPreliminare.replace('[INSERIRE PAROLE CHIAVE]','')+testo
    
    prompt_parts = [
        testo
        #{"mime_type": "image/jpeg", "data": immagini}
    ]
    if(file!=''):
        prompt_parts.append({"mime_type": file[0], "data": file[1]})
    response = model.generate_content(prompt_parts)

    return response.text

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
        print("RICHIESTA",request.POST)
        
        if form.is_valid():  # Controlla se i dati sono validi
            paroleChiave = form.cleaned_data['message']
            file_url = request.session.get("file_url", "Nessun dato salvato")
            pdf_path = request.session.get("pdf_url", "Nessun dato salvato")

            print(file_url)
            print(pdf_path)

            file_type = magic.from_file(file_url, mime=True)
            file_name=file_url.split("/")[-1]
            print("NOME",file_name)
            
            Documento.objects.create(pdf_path=pdf_path, parole_chiave=paroleChiave, file_url=file_url, nome_file=file_name)
            riassunto=inviaRichiesta((file_type,file_to_bytes(file_url)),'',paroleChiave,'Analizza il file PDF e identifica i concetti chiave basandoti sulle seguenti parole chiave: [INSERIRE PAROLE CHIAVE]. Per ogni concetto trovato, indica il numero della pagina di riferimento. Genera un riassunto dettagliato e strutturato in paragrafi, suddividendo le informazioni per argomento. Il riassunto deve essere scritto interamente in italiano, senza eccezioni, mantenendo il tono originale del documento. Non usare asterischi, trattini, Markdown o qualsiasi tipo di formattazione speciale; restituisci solo testo semplice senza simboli di markup. Se non hai parole chiave, riassumi interamente il documento.')
            # Puoi fare qualcosa con i dati, come salvarli nel database o inviare un'email
            return render(request, 'result.html', {'file_url': file_url,'Riassunto':riassunto, "pdf_url": pdf_path,'form':form})  # Mostra il file

    return render(request, 'result.html', {'form': form})  # Mostra il form || INTEGRATO, Decisione di esecuzione (UE)

def resultId(request,id):
    documenti=Documento.objects.filter(id=id)
    
    paroleChiave=documenti[0].parole_chiave
    dizionario={'message':documenti[0].parole_chiave}
    file_url=documenti[0].file_url
    pdf_path=documenti[0].pdf_path

    file_type = magic.from_file(file_url, mime=True)


    
    riassunto=inviaRichiesta((file_type,file_to_bytes(file_url)),'',paroleChiave,'Analizza il file PDF e identifica i concetti chiave basandoti sulle seguenti parole chiave: [INSERIRE PAROLE CHIAVE]. Per ogni concetto trovato, indica il numero della pagina di riferimento. Genera un riassunto dettagliato e strutturato in paragrafi, suddividendo le informazioni per argomento. Il riassunto deve essere scritto interamente in italiano, senza eccezioni, mantenendo il tono originale del documento. Non usare asterischi, trattini, Markdown o qualsiasi tipo di formattazione speciale; restituisci solo testo semplice senza simboli di markup. Se non hai parole chiave, riassumi interamente il documento.')

    form = ParoleChiave(dizionario)
    return render(request, 'result.html', {'file_url': file_url,'Riassunto':riassunto, "pdf_url": pdf_path,'form':form})
    #return render(request, 'result.html', {'form': form})

def file_to_bytes(file_path):
    with open(file_path, "rb") as file:
        return file.read()
    
def cronologia(request):
    documenti = Documento.objects.all()
    for documento in documenti:
        if documento.pdf_path.endswith('.pdf'):
            documento.tipo_file = 'pdf'
            documento.icon = 'picture_as_pdf'  # Icona per PDF
        elif documento.pdf_path.endswith('.docx'):
            documento.tipo_file = 'docx'
            documento.icon = 'description'  # Icona per documenti
        elif documento.pdf_path.endswith('.png') or documento.pdf_path.endswith('.jpg') or documento.pdf_path.endswith('.jpeg'):
            documento.tipo_file = 'image'
            documento.icon = 'image'  # Icona per immagini
        else:
            documento.tipo_file = 'altro'
            documento.icon = 'insert_drive_file'  # Icona generica per altri file
    
    return render(request, 'cronologia.html', {'documenti': documenti})


