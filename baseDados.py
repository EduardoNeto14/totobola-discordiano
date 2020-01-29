from globais import *

''' A classe Totobola será responsável por tratar do registo das pontuações e das tabelas associadas aos participantes.'''
class Totobola:
    ''' A função __init__ é executada quando um objeto da classe Totobola é criado. O objetivo da função é recolher os participantes do jogo, presentes numa base de dados.'''
    def __init__(self):
        ''' CONEXÃO COM BASE DE DADOS '''
        conn, c = conexao_BaseDados()

        ''' DENTRO DA BASE DE DADOS, EXISTE UMA TABELA COM OS PARTICIPANTES. SÃO ENTÃO RECOLHIDOS TODAS AS ENTRADAS NESSA TABELA '''
        user_baseDados = c.execute('SELECT jogador FROM participantes').fetchall()

        ''' O CICLO FOR SERÁ USADO PARA FORMATAR OS DADOS RECOLHIDOS DA BASE DE DADOS.
        O user_baseDados CONTÉM UM ARRAY PARA CADA ENTRADA RECOLHIDA O QUE NÃO CORRESPONDE AO QUE SE QUER.'''
        for user in user_baseDados:
            users.append(user[0])
        
        ''' Encerra a conexão com a base de dados.'''
        fechar_BaseDados(conn)
    
    ''' Este método irá recolher a pontuação total, que se irá tornar a pontuação anterior, de cada utilizador referente ao Tugão.'''
    def infoTugao(self):
        ''' CONEXÃO COM BASE DE DADOS '''
        conn, c = conexao_BaseDados()

        ''' Recolha das entradas presentes na tabela tugao. O dicionário tugao irá conter os dados formatados.'''
        tugao_baseDados = c.execute('SELECT * FROM tugao').fetchall()

        ''' Para cada entrada na base de dados, será acrescentado uma key com o nome do participante, cujo value será um array com a sua pontuação.'''
        for participante in tugao_baseDados:
            tugao[participante[0]] = [
                participante[3]
            ]
        
        '''Fechar conexão com a base de dados.'''
        fechar_BaseDados(conn)
    
    ''' Este método irá anexar a pontuação presente no ficheiro pontTugao.csv ao dicionário tugao. '''
    def updateTugao(self):
        ''' Verifica a existência do ficheiro (que contém as pontuações dos utilizadores).'''
        if os.path.isfile('pontTugao.csv'):
            ''' Caso exista, o método infoTugao será chamado. '''
            self.infoTugao()
            
            ''' Posteriormente, o ficheiro é aberto.'''
            with open('pontTugao.csv') as T:
                ''' Leitura do ficheiro.'''
                T = csv.reader(T, delimiter = ',')
                
                ''' Para cada entrada no ficheiro...'''
                for row in T:
                    ''' Verifica-se a existência do participante no dicionário tugao. '''
                    if row[0] in tugao:
                        ''' Se existir, acrescenta a pontução registada à pontuação Anterior.'''
                        tugao[row[0]].append(row[1])
                    else:
                        ''' Se não existir, imprime uma mensagem de erro.'''
                        print(f'{row[0]} não encontrado!')
            
            ''' Chamada do método calculoTugao. '''
            self.calculoTugao()
            ''' Chamada do método writeTugao. '''
            self.writeTugao()
        else:
            ''' Caso o ficheiro não exista, é imprimida uma mensagem de erro. '''
            print('Ficheiro necessário não encontrado!')
    
    ''' Método que calcula o novo totalTugao. '''
    def calculoTugao(self):
        ''' Para cada key e value no dicionário tugao... '''
        for u, p in tugao.items():
            try:
                '''Tenta somar os dois valores presentes no vetor pertencente ao value do dicionário tugao.'''
                TT = int(p[0]) + int(p[1]) 
            except:
                ''' Caso o utilizador não tenha feito previsão, o segundo elemento do array não irá existir, pelo que se acrescenta um 0.'''
                tugao[u].append(0)
            finally:
                ''' No fim, realiza-se a soma dos valores e acrescenta-se ao dicionário tugao.'''
                TT = int(p[0]) + int(p[1])
                tugao[u].append(TT)
    
    def writeTugao(self):
        ''' CONEXÃO COM BASE DE DADOS '''
        conn, c = conexao_BaseDados()
        
        ''' Para cada entrada no dicionário tugao... '''
        for user, pontuacoes in tugao.items():
            ''' Atualiza-se a tabela tugao na base de dados com os valores correspondentes.'''
            c.execute('UPDATE tugao SET pontuacaoAnterior=?, pontuacaoJornada=?, totalTugao=? WHERE jogador=?', (pontuacoes[0],pontuacoes[1],pontuacoes[2],user))
        
        ''' No fim, faz-se uma query à base de dados correspondente ao máximo valor da pontuação da jornada.'''
        best = c.execute('SELECT jogador,pontuacaoJornada FROM tugao WHERE pontuacaoJornada=(SELECT MAX(pontuacaoJornada) FROM tugao)').fetchall()
        
        ''' Para cada valor recolhido...'''
        for vencedorJornada in best:
            ''' Pede-se para introduzir a jornada em questão...'''
            jornada = input('Jornada?\n')
            ''' Acrescenta-se o vencedor na tabela vencedoresTugao. '''
            c.execute('INSERT INTO vencedoresTugao (jogador, pontuacao, jornada) VALUES (?,?,?)', (vencedorJornada[0], vencedorJornada[1], jornada))
        
        ''' Encerra a conexão com a base de dados.'''
        fechar_BaseDados(conn)

    def infoChamps(self):
        ''' CONEXÃO COM BASE DE DADOS '''
        conn, c = conexao_BaseDados()

        ''' Recolha das entradas presentes na tabela champs. O dicionário champs irá conter os dados formatados.'''
        champs_baseDados = c.execute('SELECT * FROM champs').fetchall()

        for participante in champs_baseDados:
            champs[participante[0]] = [
                participante[3]
            ]

        fechar_BaseDados(conn)

    def updateChamps(self):
        if os.path.isfile('pontChamps.csv'):
            self.infoChamps()

            with open('pontChamps.csv') as C:
                C = csv.reader(C, delimiter = ',')
                
                for row in C:
                    if row[0] in champs:
                        champs[row[0]].append(row[1])
                    else:
                        print(f'{row[0]} não encontrado!')

            self.calculoChamps()
            self.writeChamps()
        else:
            print('Ficheiro necessário não encontrado!')

    def calculoChamps(self):
        for u, p in champs.items():

            try:
                TC = int(p[0]) + int(p[1]) 
            except:
                champs[u].append(0)
            finally:
                TC = int(p[0]) + int(p[1])
                champs[u].append(TC)
    
    def writeChamps(self):
        ''' CONEXÃO COM BASE DE DADOS '''
        conn, c = conexao_BaseDados()

        for user, pontuacoes in champs.items():
            c.execute('UPDATE champs SET pontuacaoAnterior=?, pontuacaoJornada=?, totalChamps=? WHERE jogador=?', (pontuacoes[0],pontuacoes[1],pontuacoes[2],user))

        best = c.execute('SELECT jogador,pontuacaoJornada FROM champs WHERE pontuacaoJornada=(SELECT MAX(pontuacaoJornada) FROM champs)').fetchall()

        for vencedorJornada in best:
            jornada = input('Jornada?\n')
            c.execute('INSERTO INTO vencedoresChamps (jogador, pontuacao, jornada) VALUES (?,?,?)', (vencedorJornada[0], vencedorJornada[1], jornada))
        
        fechar_BaseDados(conn)

    def infoSelecoes(self):
        ''' CONEXÃO COM BASE DE DADOS '''
        conn, c = conexao_BaseDados()

        ''' Recolha das entradas presentes na tabela selecoes. O dicionário selecoes irá conter os dados formatados.'''
        selecoes_baseDados = c.execute('SELECT * FROM selecoes').fetchall()

        for participante in selecoes_baseDados:
            selecoes[participante[0]] = [
                participante[3]
            ]

        fechar_BaseDados(conn)

    def updateSelecoes(self):
        if os.path.isfile('pontSelecoes.csv'):
            self.infoSelecoes()

            with open('pontSelecoes.csv') as S:
                S = csv.reader(S, delimiter = ',')
                
                for row in S:
                    if row[0] in selecoes:
                        selecoes[row[0]].append(row[1])
                    else:
                        print(f'{row[0]} não encontrado!')

            self.calculoSelecoes()
            self.writeSelecoes()
        else:
            print('Ficheiro necessário não encontrado!')

    def calculoSelecoes(self):
        for u, p in selecoes.items():

            try:
                TS = int(p[0]) + int(p[1]) 
            except:
                selecoes[u].append(0)
            finally:
                TS = int(p[0]) + int(p[1])
                selecoes[u].append(TS)
    
    def writeSelecoes(self):
        ''' CONEXÃO COM BASE DE DADOS '''
        conn, c = conexao_BaseDados()

        for user, pontuacoes in selecoes.items():
            c.execute('UPDATE selecoes SET pontuacaoAnterior=?, pontuacaoJornada=?, totalSelecoes=? WHERE jogador=?', (pontuacoes[0],pontuacoes[1],pontuacoes[2],user))

        best = c.execute('SELECT jogador,pontuacaoJornada FROM selecoes WHERE pontuacaoJornada=(SELECT MAX(pontuacaoJornada) FROM selecoes)').fetchall()

        for vencedorJornada in best:
            jornada = input('Jornada?\n')
            c.execute('INSERTO INTO vencedoresSelecoes (jogador, pontuacao, jornada) VALUES (?,?,?)', (vencedorJornada[0], vencedorJornada[1], jornada))

        fechar_BaseDados(conn)

    def updateTotal(self):
        self.infoTugao()
        print('****************TUGAO******************')
        self.infoChamps()
        print('****************CHAMPS*****************')
        self.infoSelecoes()
        print('****************SELECOES***************')

        for u, p in tugao.items():
  
            total[u] = [
                int(p[0]),
                0,
                0
            ]

        for u, p in champs.items():
            if u in total:
                total[u][1] = int(p[0])

            elif u not in total:
                total[u] = [
                    0,
                    int(p[0]),
                    0
                ]

        for u, p in selecoes.items():
            if u in total:
                total[u][2] = int(p[0])
            elif u not in total:
                total[u] = [
                    0,
                    0,
                    int(p[0])
                ]

        ''' CONEXÃO COM BASE DE DADOS '''
        conn, c = conexao_BaseDados()

        c.execute('DELETE FROM total')

        for u, p in total.items():
            t = int(p[0]) + int(p[1]) + int(p[2])

            c.execute('INSERT INTO total (jogador, totalTugao, totalChamps, totalSelecoes, totalDiscordiano) VALUES (?,?,?,?,?)', (u,p[0], p[1], p[2], t))

        fechar_BaseDados(conn)
        
updateBaseDados = {
    '1' : Totobola.updateTugao,
    '2' : Totobola.updateChamps,
    '3' : Totobola.updateSelecoes,
    '4' : Totobola.updateTotal
}