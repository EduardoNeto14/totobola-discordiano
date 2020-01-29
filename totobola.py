from globais import *
from baseDados import *
from googleSheets import *
from pontuacoes import *
from prognosticos import prognosticos_sheets
from enviarmail import enviarMail
from formatacaoDados import formatacao

if __name__ == '__main__':
    T = Totobola()
    
    while 1:
        print('\nTOTOBOLA DISCORDIANO\n\n1- Update Tabelas\n2- Contabilização\n3- Guardar Pontuações\n4- Alterar no Google Sheets\n5- Prognósticos\n6- Enviar Mail\n7- Formatar Dados\n0- Sair')
        C = input('\n>')

        if C == '0':
            quit()
        
        elif C == '1':
            print('\n1- Tugão\n2- Champs\n3- Seleções\n4- Total\n0- Voltar atrás')
            C =  input('\n>')

            if C != '1' and C != '2' and C != '3' and C != '4':
                pass

            else:
                updateBaseDados[C](T)
        
        elif C == '2':

            print('\n1- Tugão\n2- Champs\n3- Seleções\n0- Voltar atrás')
            C = input('\n>')
            
            if C == '1' or C == '2' or C == '3':

                P = Pontuacoes(C)

            else:
                pass
        
        elif C == '3':
            nome_tabela = input('Qual o nome da tabela?\n>')

            if os.path.isfile('/home/eduardo/Documentos/Desenvolvimento/Base Dados/{nome_tabela}.csv'):
                conn, c = conexao_BaseDados('pontuacoes')
                c.execute(f'CREATE TABLE {nome_tabela} (jogador text, pontuacao int)')

                with open(f'/home/eduardo/Documentos/Desenvolvimento/Base Dados/{nome_tabela}.csv') as pontuacoes:
                    pontuacoes = csv.reader(pontuacoes, delimiter=',')

                    for jogador in pontuacoes:
                        c.execute(f'INSERT INTO {nome_tabela} (jogador, pontuacao) VALUES (?,?)', (jogador[0], jogador[1]))

                fechar_BaseDados(conn)
            
            else:
                print('Esse ficheiro não existe!')
        
        elif C == '4':
            print('\n1- Tugão\n2- Champs\n3- Seleções\n4- Total\n0- Voltar atrás')
            C = input('\n>')
            
            if C != '1' and C != '2' and C != '3' and C != '4':
                pass

            else:
                updateSheets[C]()

        elif C == '5':
            print('Qual o nome do ficheiro?')
            C1 = input('\n>')
            print('\nQual o nome do ficheiro resultante?')
            C2 = input('\n>')

            prognosticos_sheets(C1, C2)
        
        elif C == '6':
            print('Que tabela quer aceder?')
            C = input('\n>')
            enviarMail(C)
        
        elif C == '7':
            formatacao()
        
        else:
            pass