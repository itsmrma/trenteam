

import base64

def image_to_base64(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')





#image_base64 = image_to_base64("file/tabella guida risposte pag 5.jpeg") #Sostituisci il percorso
def inviaRichiesta(file,testo,keywords):
    import google.generativeai as genai
    file_mime={}
    genai.configure(api_key="AIzaSyATCyWtU-wJMO97rPf7xHr0pOJrgTEE8ds") #Sostituisci con la tua chiave API
    for i in file:
        file_mime.update({"mime_type": i[1], "data": i[0]})
    model = genai.GenerativeModel('gemini-2.0-flash')
    prompt_parts = [
        "dimmi cosa vedi in questi file: ",
        #{"mime_type": "image/jpeg", "data": immagini}
        file_mime
    ]

    response = model.generate_content(prompt_parts)

    print(response.text)
    #print(prompt_parts)



def extract_original_file(p7m_file_path):
    from asn1crypto import cms, pem

    with open(p7m_file_path, 'rb') as f:
        if pem.detect(f.read()):
            f.seek(0)
            _, _, der_bytes = pem.unarmor(f.read())
        else:
            f.seek(0)
            der_bytes = f.read()

    # Parse the CMS structure
    content_info = cms.ContentInfo.load(der_bytes)
    if content_info['content_type'].native != 'signed_data':
        raise ValueError("The file is not a valid signed PKCS#7 file.")

    signed_data = content_info['content']
    encap_content_info = signed_data['encap_content_info']

    # Extract the original file from the encapsulated content
    if encap_content_info['content_type'].native == 'data':
        original_file = encap_content_info['content'].native
        return original_file
    else:
        raise ValueError("The encapsulated content is not of type 'data'.")

def file_type(original_file_bytes):
    import magic
    file_type = magic.from_buffer(original_file_bytes, mime=True)
    return file_type

ciao="askaksakls.pdf 3"

text = ""
if file_type == 'application/pdf':
    temp=ciao.split(".pdf")
    if len(temp)==2:
        ciao=temp[0]

print(ciao)