import csv
import docx

input_file = 'output.csv'

doc = docx.Document()

with open(input_file, 'r') as fisier_csv_input:
    cititor_csv = csv.reader(fisier_csv_input)
    for linie in cititor_csv:
        information = f'Décrochage {linie[2]} a la place numéro {linie[0]} et le compte de réservation weezpay {linie[1]}.'
        if not(linie[3]) or linie[3].isspace():
            information = information + ' Il ne sert pas de boissons.'
        else:
            linie_noua = linie[3].strip().replace("  ", ", ")
            information = information + f' Il sert des boissons comme: {linie_noua}.'
        if not(linie[4]) or linie[4].isspace():
            information = information + ' Il ne sert pas de nourriture.'
        else:
            linie_noua = linie[4].strip().replace("  ", ", ")
            information = information + f' Il sert des plats comme: {linie_noua}.'
        p = doc.add_paragraph(information)

doc.save("answer.docx")