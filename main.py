import csv

nume_fisier_csv_input = 'data.csv'
nume_fisier_csv_output = 'output1.csv'

with open(nume_fisier_csv_input, 'r') as fisier_csv_input, open(nume_fisier_csv_output, 'w', newline='') as fisier_csv_output:
    cititor_csv = csv.reader(fisier_csv_input)
    scriitor_csv = csv.writer(fisier_csv_output)

    for linie in cititor_csv:
        # Descompunem linia în funcție de ;
        date = ['']
        index = 0
        for cell in linie:
            content_cell = cell.split(';')
            if index == 0:
                date[0] = content_cell[0]
            else:
                date[index] = str(date[index]) + ';' + content_cell[0]
            for i, item in enumerate(content_cell):
                if i != 0:
                    index += 1
                    date.append(item)
        scriitor_csv.writerow(date)