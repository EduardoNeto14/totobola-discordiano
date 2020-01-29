from globais import *

def enviarMail(tabelaPontuacao):
    with open('contactos.csv') as contactos:
        contactos = csv.reader(contactos, delimiter = ',')
        for user in contactos:
            usersContactos[user[0]] = user[1]

    conn, c = conexao_BaseDados('pontuacoes')
    pontuacoes = c.execute(f'SELECT * FROM {tabelaPontuacao}').fetchall()
    fechar_BaseDados(conn)

    for partipante in pontuacoes:
        usersPontuacoes[partipante[0]] = partipante[1]
    
    smtp_server = 'smtp.gmail.com'
    port = 587
    email = 'totoboladiscordiano@gmail.com'
    password = input('Password: ')
    context = ssl.create_default_context()

    with smtplib.SMTP(smtp_server, port) as server:
        server.ehlo()  # Can be omitted
        server.starttls(context=context)
        server.ehlo()  # Can be omitted
        server.login(email, password)
        
        for user, mail in usersContactos.items():
            message = MIMEMultipart()
            message["From"] = email
            message["To"] = mail
            message["Subject"] = 'Totobola Discordiano'

            message.attach(MIMEText(f'Olá {user}. Alcançaste {usersPontuacoes[user]} pontos nesta jornada.\n\nPodes ver mais em: https://docs.google.com/spreadsheets/d/1ltS6c5aXZgQIg74bUSQiDZbe7avnEbt9swSDm5p6tYY/edit?usp=sharing', 'plain'))
            text = message.as_string()
            try:
                server.sendmail(email, mail, text)
            except Exception as e:
                print(e)
                server.quit()
            
            time.sleep(1)
        server.quit()