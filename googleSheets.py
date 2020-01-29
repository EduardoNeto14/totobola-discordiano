from globais import *

def credenciaisSheets():
    scope = ["https://spreadsheets.google.com/feeds","https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive","https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name('/home/eduardo/Documentos/Desenvolvimento/Python/TDapi.json', scope)
    client = gspread.authorize(creds)

    return client

def updateSheets_Tugao():
    client = credenciaisSheets()
    sheet = client.open('Totobola_Discordiano').worksheet('Tugão')

    conn, c = conexao_BaseDados()
    tugao_baseDados = c.execute('SELECT * FROM tugao ORDER BY totalTugao DESC').fetchall()
    fechar_BaseDados(conn)
    
    tugao = {}

    for participante in tugao_baseDados:
        tugao[participante[0]] = [
            participante[1],
            participante[2],
            participante[3]
        ]
        
    contador_linha = 1
    contador_coluna = 0

    for user, pontuacao in tugao.items():
        print(f'Atualizando o user {user}... Pontuação : {pontuacao}')
        sheet.update_cell(contador_linha+1, contador_coluna + 1, user)
        
        for contador_coluna in range(len(pontuacao)):
            sheet.update_cell(contador_linha+1, contador_coluna + 2, pontuacao[contador_coluna])

        contador_linha += 1
        contador_coluna = 0
        time.sleep(5)

def updateSheets_Champs():
    client = credenciaisSheets()
    sheet = client.open('Totobola_Discordiano').worksheet('Champions')

    conn = sqlite3.connect('/home/eduardo/Documentos/Desenvolvimento/Base Dados/totobolaDiscordiano.db')
    c = conn.cursor()
    champs_baseDados = c.execute('SELECT * FROM champs ORDER BY totalChamps DESC').fetchall()
    conn.close()
    
    champs = {}

    for participante in champs_baseDados:
        champs[participante[0]] = [
            participante[1],
            participante[2],
            participante[3]
        ]
        
    contador_linha = 1
    contador_coluna = 0

    for user, pontuacao in champs.items():
        print(f'Atualizando o user {user}... Pontuação : {pontuacao}')
        sheet.update_cell(contador_linha+1, contador_coluna + 1, user)
        
        for contador_coluna in range(len(pontuacao)):
            sheet.update_cell(contador_linha+1, contador_coluna + 2, pontuacao[contador_coluna])

        contador_linha += 1
        contador_coluna = 0
        time.sleep(5)

def updateSheets_Selecoes():
    client = credenciaisSheets()
    sheet = client.open('Totobola_Discordiano').worksheet('Seleções')

    conn, c = conexao_BaseDados()
    selecoes_baseDados = c.execute('SELECT * FROM selecoes ORDER BY totalSelecoes DESC').fetchall()
    fechar_BaseDados(conn)
    
    selecoes = {}

    for participante in selecoes_baseDados:
        selecoes[participante[0]] = [
            participante[1],
            participante[2],
            participante[3]
        ]
        
    contador_linha = 1
    contador_coluna = 0

    for user, pontuacao in selecoes.items():
        print(f'Atualizando o user {user}... Pontuação : {pontuacao}')
        sheet.update_cell(contador_linha+1, contador_coluna + 1, user)
        
        for contador_coluna in range(len(pontuacao)):
            sheet.update_cell(contador_linha+1, contador_coluna + 2, pontuacao[contador_coluna])

        contador_linha += 1
        contador_coluna = 0
        time.sleep(5)

def updateSheets_Total():
    client = credenciaisSheets()
    sheet = client.open('Totobola_Discordiano').worksheet('Total')

    conn, c = conexao_BaseDados()
    total_baseDados = c.execute('SELECT * FROM total ORDER BY totalDiscordiano DESC').fetchall()
    fechar_BaseDados(conn)
    
    total = {}

    for participante in total_baseDados:
        total[participante[0]] = [
            participante[1],
            participante[2],
            participante[3],
            participante[4]
        ]
        
    contador_linha = 1
    contador_coluna = 0

    for user, pontuacao in total.items():
        print(f'Atualizando o user {user}... Pontuação : {pontuacao}')
        sheet.update_cell(contador_linha+1, contador_coluna + 1, user)
        
        for contador_coluna in range(len(pontuacao)):
            sheet.update_cell(contador_linha+1, contador_coluna + 2, pontuacao[contador_coluna])

        contador_linha += 1
        contador_coluna = 0
        time.sleep(5)
        
updateSheets = {
    '1' : updateSheets_Tugao,
    '2' : updateSheets_Champs,
    '3' : updateSheets_Selecoes,
    '4' : updateSheets_Total
}