from globais import *
from googleSheets import credenciaisSheets

def prognosticos_sheets(filename, outputname):
    client = credenciaisSheets()
    try:
        sheet = client.open(f'{filename}').sheet1
    except:
        print('\nFicheiro inválido!\n')
        return

    prognosticos = sheet.get_all_values()
    #print(prognosticos)
    '''
    df = pd.DataFrame(prognosticos)
    df.set_index(1, inplace=True)

    resultados = df.drop(index = ['Username'], axis = 0).drop(columns = [0,len(df.columns)], axis = 1)
    resultados.to_csv(f'{outputname}.csv', header=False)

    contactos = df.drop(index = ['Username'], axis = 0).drop(columns = df.columns.to_series()[0:len(df.columns)-1], axis = 1)
    contactos.to_csv('contactos.csv', header=False)
    
    '''
    counter = 0
    with open(f'{outputname}.csv', 'w', newline='') as p:
        p = csv.writer(p, dialect='excel')
        
        for row in prognosticos:
            if counter != 0:
                p.writerow([row[2]])
                for numero_resultados in range(len(row) - 3):
                    p.writerow([row[numero_resultados + 3]])

            counter += 1

    counter = 0
    with open('contactos.csv', 'w', newline = '') as contactos:
        contactos = csv.writer(contactos, dialect='excel')
        
        for row in prognosticos:
            if counter != 0:
                contactos.writerow([row[3], row[2]])
                
            counter +=1
