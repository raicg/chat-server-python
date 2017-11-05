from socket import *
from threading import Thread
import re
import time
import os
clientes=1
toAll = " "
msgAntiga = " "
lista = []
socketList = []
nickList = []



def controle():
    global atual
    while True:
        comando = raw_input()
        if comando == "sair()":
            for i in range (0,atual-1):
                socketList[i].send("163563vxdgrw56732fdrwet4")
            time.sleep(4)
            os._exit(1)
            
            
            

def conexao_cliente():
    global clientes
    global toAll
    global lista
    global socketlist
    global atual
    global nickList
    conn, addr = s.accept()
    socketList.append(conn)
    identidade = clientes
    clientes = clientes+1
    nick = conn.recv(1024)
    while nick in nickList:
        conn.send("Esse nick ja existe, escolha outro nick")
        nick = conn.recv(1024)
    nickList.append(nick)
    lista.append("<"+str(nick)+str(addr)+">")
    toAll = str(addr)+" "+str(nick)+" acabou de se conectar."
    print addr, nick, " acabou de se conectar."
    while True:
        data = conn.recv(1024)
        mensagem = str(data)
        if not data:
            atual = atual-1
            clientes = clientes-1
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
            nickList.remove(nickantigo)
            while nick in nickList:
                conn.send("Esse nick ja existe, escolha outro nick")
                nick = conn.recv(1024)
            nickList.append(nick)
            toAll = str(nickantigo)+" mudou seu nickname para "+str(nick)
        elif mensagem[0:6]=="sair()":
            socketList.remove(conn)
            atual = atual-1
            clientes = clientes-1
            print addr, nick, "saiu do chat"
            toAll = str(addr)+str(nick)+" saiu do chat."
            break
        else:
            toAll = str(addr) + " " + str(nick) + " enviou: " + mensagem
        print toAll


HOST = 'localhost'
PORT = 7214
s = socket()
s.bind((HOST, PORT))
s.listen(9999)

print "O servidor de chat esta rodando..."
Thread(target=conexao_cliente).start()
Thread(target=controle).start()
atual = 1
while True:
    if atual < clientes:
        Thread(target=conexao_cliente).start()
        atual = atual +1
    else:
        if toAll != msgAntiga:
            if atual-1 > 0:
                for i in range (0,atual-1):
                    socketList[i].send(toAll)
                    msgAntiga = toAll
        atual = atual

s.close()
    

