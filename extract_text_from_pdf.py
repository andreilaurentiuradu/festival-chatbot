import pdfplumber

def extrage_text_din_pdf(cale_fisier):
    with pdfplumber.open(cale_fisier) as pdf:
        text = ''
        for pagina in pdf.pages:
            text += pagina.extract_text()
    return text

# Exemplu de utilizare
cale_pdf = 'ppt.pdf'
text_extras = extrage_text_din_pdf(cale_pdf)

print(text_extras)
