from socket import *
from threading import Thread
import re
import time
clientes=1
toAll = "Bem Vindo"
lista = []
connection = ""
flag = 0

def envio_mensagem():
    global toAll
    global connection
    global flag
    conn_envio = connection
    lixo = 0
    msgAntiga = " "
    while True:
        if flag == 1:
            flag = 0
            break
        if toAll != msgAntiga:
            conn_envio.send(toAll)
            msgAntiga = toAll
        else:
            lixo = 0
        

def conexao_cliente():
    global clientes
    global toAll
    global lista
    global connection
    global flag
    flag=0
    conn, addr = s.accept()
    connection = conn
    clientes = clientes+1
    nick = conn.recv(1024)
    lista.append("<"+str(nick)+str(addr)+">")
    Thread(target=envio_mensagem).start()
    print addr, nick, " acabou de se conectar."
    while True:
        flag=0
        data = conn.recv(1024)
        mensagem = str(data)
        if not data:
            flag = 1
            print addr, nick, "saiu do chat"
            toAll = str(addr)+str(nick)+" saiu do chat."
            time.sleep(1)
            break
        elif mensagem == "lista()":
            toAll = str(addr) + " " + str(nick) + " enviou: " + mensagem
            print toAll
            time.sleep(1)
            toAll = str(lista)
        elif mensagem[0:5]=="nick(":
            start = mensagem.find('nick(') +5
            end = mensagem.find(')' , start)
            nickantigo = nick
            nick = mensagem[start:end]
            toAll = str(nickantigo)+" mudou seu nickname para "+str(nick)
       # elif mensagem[0:6]=="sair()":
        #    flag = 1
         #   print addr, nick, "saiu do chat"
          #  toAll = str(addr)+str(nick)+" saiu do chat."
           # break
        else:
            toAll = str(addr) + " " + str(nick) + " enviou: " + mensagem
        print toAll


HOST = 'localhost'
PORT = 7212
s = socket()
s.bind((HOST, PORT))
s.listen(9999)

print "O servidor de chat esta rodando..."
Thread(target=conexao_cliente).start()
atual = 1
while True:
    if atual < clientes:
        Thread(target=conexao_cliente).start()
        atual = atual +1
    else:
        atual = atual

s.close()
    

