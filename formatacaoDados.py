from globais import *

def formatacao():
    df = pd.read_csv('untitled.csv', header = None)
    resultadoRegex = re.compile(r'(\d)( )?(-|x)( )?(\d)')
    user_encontrado = False
    prognosticos = pd.DataFrame()

    for r in range(len(df)):

        res = resultadoRegex.search(df.iloc[r][0])
        try:
            res.group()
        
            if ('*' or 'JOKER' or 'joker' or 'Joker') in df.iloc[r][0]:
                resultado = f'{res.group()[0]}-{res.group()[-1]}*'
            else:
                resultado = f'{res.group()[0]}-{res.group()[-1]}'
        
            prognosticos = pd.concat([prognosticos, pd.Series([resultado])])
        except:
            if df.iloc[r][0] != '':
                for u in users:
                    usersRegex = re.compile(r'{}'.format(u))
                    user = usersRegex.search(df.iloc[r][0])
                    #print(f'User a iterar: {u}')
                    
                    try:
                        user.group()
                        #print(f'User encontrado: {u}')
                        prognosticos = pd.concat([prognosticos, pd.Series([u])])
                        user_encontrado = True
                        break
                    except AttributeError:
                        pass
                        
                if not user_encontrado:    
                    prognosticos = pd.concat([prognosticos, pd.Series([df.iloc[r][0]])])
                else:
                    user_encontrado = False
            else:
                print('Linha vazia')

    prognosticos.to_csv('prognosticos.csv', header = False, index = False)