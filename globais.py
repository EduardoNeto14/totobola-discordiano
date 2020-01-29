import sqlite3
import csv
import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import time
import smtplib
import ssl
import email
import pandas as pd
import re
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

file_users = {
    '1' : 'tugao.csv',
    '2' : 'champs.csv',
    '3' : 'selecoes.csv'
}   #Ficheiros que contêm os prognósticos

file_resultados = {
    '1' : 'tugaojornada.csv',
    '2' : 'champsjornada.csv',
    '3' : 'selecoesjornada.csv'
}   #Ficheiros com os resultados reais da jornada

file_pontuacoes = {
    '1' : 'pontTugao.csv',
    '2' : 'pontChamps.csv',
    '3' : 'pontSelecoes.csv'
}   #Ficheiros a criar com as pontuções

tendencia = []          #Array que contém as tendências dos resultados
jokerdict = {}          #Dicionário que contém a utilização do joker por parte dos jogadores
pontuacoesdict = {}     #Dicionário que contém as pontuaões dos jogadores
resultados = []         #Array com os resultados reais
users = []              #Este array será usado para conter todos os participantes, após formatação
participantes = {}      #Dicionário com os prognósticos dos utilizadores
tugao = {}              #Dicionário para realizar a atualização das pontuações (Tugão)
champs = {}             #Dicionário para realizar a atualização das pontuações (Champs)
selecoes = {}           #Dicionário para realizar a atualização das pontuações (Seleções)
total = {}              #Dicionário para realizar a atualização das pontuações (Total)
usersContactos = {}
usersPontuacoes = {}

''' Função que estabelece uma conexão com a base de dados. Retorna o objeto da comunicação (conn) e o cursor (c).'''
def conexao_BaseDados(baseDados = 'totobolaDiscordiano'):
    conn = sqlite3.connect(f'/home/eduardo/Documentos/Desenvolvimento/Base Dados/{baseDados}.db')
    c = conn.cursor()
    
    return conn, c

''' Função que encerra a conexão com a base de dados e guarda as alterações realizadas. Recebe o objeto da conexão com argumento.'''
def fechar_BaseDados(conn):
    conn.commit()
    conn.close()