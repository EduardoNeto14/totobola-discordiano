from globais import *

''' A classe Pontuacoes é responsável por calcular as pontuações de todos os users.'''
class Pontuacoes:
    def __init__(self, C):
        self.numero_jogos = 0                   #Variável que armazena o número de jogos da jornada.
        
        ''' Abre o ficheiro que contém os resultados da jornada. file_resultados é um dicionário que contém como key a opção escolhida pelo utilizador e value o nome do ficheiro.'''
        
        with open(file_resultados[C]) as r:
            r = csv.reader(r, delimiter='\t')

            ''' Para cada linha do ficheiro .csv adiciona o resultado "row[0]" ao array resultados'''
            ''' Posteriormente, chama o método tendenciaResultado com o resultado registado e calcula se se trata de VC, VF ou E.'''
            ''' Por fim, incrementa o numero_jogos, que contém o número de jogos da jornada.'''
            for row in r:
                resultados.append(row[0])
                self.tendenciaResultado(row[0])
                self.numero_jogos += 1
        
        ''' O próximo passo será recolher os prognósticos dos utilizadores.'''
        ''' O ficheiro .csv que contém estes prognósticos é constituído da seguinta maneira:
        user
        resultado1
        resultado2
        resultado3
        resultadon
        user
        ...
        resultadon
        ...
        '''

        self.counter = 0        #Esta variável será utilizada para saber, em conjunto com a numero_jogos, quando o nome de um participante estará presente no ficheiro.
        self.user = None        #Variável que armazena o nome do utilizador.
        
        ''' Abre o ficheiro com os prognósticos dos utilizadores. '''
        with open(file_users[C]) as prog:
            prog = csv.reader(prog, delimiter = '\t')

            ''' Para cada linha do ficheiro de prognósticos... '''
            for row in prog:
                if self.counter == 0:
                    ''' Caso o counter esteja a 0, significa que essa linha contém o nome de um participante
                    Neste caso, atribui-se esse user à variável user.'''
                    self.user = row[0]

                    ''' Realiza-se a verificação da existência desse utilizador na base de dados.
                    Caso não exista, pede-se a alteração do nome do utilizador.'''
                    if self.user not in users:
                        print(f'Utilizador {self.user} não está presente na base de dados!\nQue pretende fazer?')
                        utilizador = input('1- Corrigir username\n2- Adicionar utilizador')
                        
                        if utilizador == '1':
                            self.user = input(f'Corrigir username {self.user}: ')
                            
                        elif utilizador == '2':
                            conn, c = conexao_BaseDados()
                            
                            c.execute('INSERT INTO participantes (jogador) VALUES (?)', [self.user])
                            existe_tugao = c.execute('SELECT jogador FROM tugao WHERE EXISTS (SELECT jogador FROM tugao WHERE jogador=?)', [self.user]).fetchall()
                            
                            if existe_tugao == []:
                                c.execute('INSERT INTO tugao (jogador, pontuacaoAnterior, pontuacaoJornada, totalTugao) VALUES (?,?,?,?)', (self.user, 0, 0, 0))

                            existe_champs = c.execute('SELECT jogador FROM champs WHERE EXISTS (SELECT jogador FROM champs WHERE jogador=?)', [self.user]).fetchall()
                            if existe_champs == []:
                                c.execute('INSERT INTO champs (jogador, pontuacaoAnterior, pontuacaoJornada, totalChamps) VALUES (?,?,?,?)', (self.user, 0, 0, 0))

                            existe_selecoes = c.execute('SELECT jogador FROM selecoes WHERE EXISTS (SELECT jogador FROM selecoes WHERE jogador=?)', [self.user]).fetchall()
                            if existe_selecoes == []:
                                c.execute('INSERT INTO selecoes (jogador, pontuacaoAnterior, pontuacaoJornada, totalSelecoes) VALUES (?,?,?,?)', (self.user, 0, 0, 0))

                            users.append(self.user)

                            fechar_BaseDados(conn)
                            

                    ''' Posteriormente adiciona-se um item ao dicionário participantes cuja key
                    será o nome do utilizador e o value será um array vazio. Este dicionário irá
                    conter os resultados todos definidos pelo user em questão.'''
                    participantes[self.user] = []

                    ''' O dicionário pontuacoesdict irá conter a pontuação do utilizador. Este irá iniciar como 0, obviamente...'''
                    pontuacoesdict[self.user] = 0
                    self.counter += 1   #Depois deste processo, a variável counter irá ser incrementada.
                
                elif self.counter == self.numero_jogos:
                    ''' Se o counter for igual ao numero_jogos, sabemos que a próxima linha será de novo o nome de um utilizador.
                    De seguida introduz-se o prognóstico no dicionário partipicantes.'''
                    participantes[self.user].append(row[0])

                    ''' Verifica-se se o prognóstico contém o joker chamando o método checkJoker.
                    Este retorna se o joker foi utilizado ou não e ainda o resultado sem o joker.'''
                    j, res = self.checkJoker(self.user, row[0])

                    ''' De seguida, faz-se a contabilização desse resultado com recurso ao método contabilizacao '''
                    self.contabilizacao(j, self.counter, res)

                    ''' Incrementa-se o número de pontos do participante com os pontos contabilizados.'''
                    pontuacoesdict[self.user] += self.points
                    
                    ''' Repõe-se as variáveis counter e user.'''
                    self.counter = 0
                    self.user = None
                
                else:
                    ''' O processo é idêntico ao passo anterior, no entanto, aqui apenas se incrementa a variável counter. '''
                    participantes[self.user].append(row[0])
                    j, res = self.checkJoker(self.user, row[0])
                    self.contabilizacao(j, self.counter, res)
                    pontuacoesdict[self.user] += self.points
                    self.counter += 1


        ''' Por fim, chama-se o método createPontuacaoFile '''
        self.createPontuacaoFile(C)

    ''' Este método realiza a contabilização do resultado. O princípio do jogo é o seguinte:
    Todos os jogadores fazem uma previsão dos resultados dos jogos.
    Depois, consoante o resultado dos jogos, é atribuído uma pontuação.
    Se o utilizador acertar completamente no resultado, obtém 3 pontos.
    Se o utilizador acertar na tendência do resultado, obtém 1 ponto.
    Em todas as outras situações não obtém ponto algum.
    
    
    Este método recebe 3 argumentos: joker que será True or False, dependendo da existência do joker ou não,
    jogo que corresponde ao jogo da jornada e que será o counter,
    res que será o resultado sem o joker.'''
    def contabilizacao(self, joker, jogo, res):
        self.points = 0             #Esta variável irá conter a pontuação do jogador para o resultado em questão
        if res == resultados[jogo - 1]:
            ''' Se o resultado res for igual ao resultado real (contido no array resultados), então obtem 3 pontos.'''
            self.points = 3

        elif res == '' or res == 'x-x':
            ''' Se o resultado não for previsto, obtém 0 pontos.'''
            print('Inválido')
            self.points = 0

        else:
            ''' Se acertar a tendência do resultado, obtém 1 ponto. '''
            if res[0] > res[2] and tendencia[jogo -1] == 'vc' or res[0] < res[2] and tendencia[jogo -1] == 'vf' or res[0] == res[2] and tendencia[jogo -1] == 'e':
                self.points = 1
        
        ''' Caso tenha utilizado o joker, os pontos serão dobrados. '''
        if joker:
            self.points = self.points*2 

    ''' Método que verifica a utilização do joker ou não.
    Recebe us que corresponde ao user.
    Recebe res que é o prognóstico.
    
    O joker é definido como:
    resultadon*'''
    def checkJoker(self, us, res):
        self.joker = False
        ''' Verifica a existência do * no resultado ''' 
        if '*' in res:
            ''' Verifica se o joker já foi utilizado pelo utilizador'''
            if us in jokerdict:
                self.joker = False
            else:
                self.joker = True
                jokerdict[us] = 'y'
            print(f'User {us} colocou Joker em {res}')
            ''' Retira o * do prognóstico'''
            res = res[:-1]
        
        return self.joker, res

    '''Método para calcular a tendência do resultado real'''
    def tendenciaResultado(self, res):
        
        if res[0] == res[2]:
            tendencia.append('e')
        elif res[0] > res[2]:
            tendencia.append('vc')
        elif res[0] < res[2]:
            tendencia.append('vf')

    '''Método para criar ficheiro csv com as pontuaçõs finais'''
    def createPontuacaoFile(self, C):
        with open(file_pontuacoes[C], 'w', newline='') as p:
            p = csv.writer(p, dialect='excel')

            for user, pont in pontuacoesdict.items():
                p.writerow([user,pont])
