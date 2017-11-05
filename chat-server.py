from socket import *
from threading import Thread
import re
import time
import os
clientes=1 #numero de clientes
toAll = " " #mensagem para enviar a todos
msgAntiga = " " #parametro para identificar se toAll foi modificado
lista = [] #lista de clientes conectados
socketList = [] #lista de connections sockets
nickList = [] #lista de nicks



def controle(): #thread que recebe os controles do servidor
    global atual
    while True:
        comando = raw_input() #recebe um comando
        if comando == "sair()":
            for i in range (0,atual-1):
                socketList[i].send("163563vxdgrw56732fdrwet4") #codigo para que clientes fechem
            time.sleep(4) #espera 4 segundos
            os._exit(1) #fecha todo o servidor
            
            
            

def conexao_cliente():
    global clientes
    global toAll
    global lista
    global socketlist
    global atual
    global nickList
    conn, addr = s.accept() #cliente conecta
    socketList.append(conn) #adicionado a conneccao do socket a lista socketList
    clientes = clientes+1 #permite um novo cliente conectar, permitindo iniciar 1 nova thread na main
    nick = conn.recv(1024) #recebe a primeira mensagem, que e o nick
    while nick in nickList: #enquanto o nick ja existir na lista nickList
        conn.send("Esse nick ja existe, escolha outro nick") #envia erro avisando que o nick ja existe
        nick = conn.recv(1024) #recebe outro nick
    nickList.append(nick) #adiciona o nick na lista nickList
    lista.append("<"+str(nick)+str(addr)+">") #adiciona o cliente a lista de clientes
    toAll = str(addr)+" "+str(nick)+" acabou de se conectar." #modifica toAll para que seja enviado que o cliente acabou de se conectar
    print addr, nick, " acabou de se conectar." #printa no servidor que o cliente conectou
    while True: #permanece sempre aqui ate a thread fechar
        data = conn.recv(1024) #recebe uma nova mensagem
        mensagem = str(data) #transforma ela em string
        if not data: #se o dado recebido for vazio, significa que o cliente saiu
            atual = atual-1 #diminui o parametro do contador de clientes
            clientes = clientes-1 #diminui o contador de clientes
            print addr, nick, "saiu do chat" #printa no servidor o cliente que saiu do chat
            toAll = str(addr)+str(nick)+" saiu do chat." #modifica o toAll para que envie a todos os clientes quem saiu do chat
            time.sleep(1) #espera 1 segundo
            break #acaba a thread encerrando o loop
        elif mensagem == "lista()":
            toAll = str(addr) + " " + str(nick) + " enviou: " + mensagem #modifica toAll para enviar que o cliente digitou lista()
            print toAll #printa no servidor que o cliente digitou lista()
            time.sleep(1) #espera 1 segundo
            toAll = str(lista) #modifica toAll para enviar a todos a lista de clientes conectados ao servidor
        elif mensagem[0:5]=="nick(": #mudar de nick
            start = mensagem.find('nick(') +5 #start e um inteiro que iniciara a partir da posicao da letra n de nick( +5 posicoes, ou seja, depois de (
            end = mensagem.find(')' , start) #end e um inteiro que termina no )
            nickantigo = nick #salva nick antigo
            nick = mensagem[start:end] #muda o novo nick
            nickList.remove(nickantigo) #remove o nick antigo da lista nickList
            while nick in nickList: #enquanto o novo nick ja estiver na lista nickList
                conn.send("Esse nick ja existe, escolha outro nick") #envia a mensagem de erro que o nick ja existe e pede um novo
                nick = conn.recv(1024) #recebe o novo nick
            nickList.append(nick) #adiciona o novo nick
            toAll = str(nickantigo)+" mudou seu nickname para "+str(nick) #modifica toAll para que envie a todos os clientes a mudanca do nick
        elif mensagem[0:6]=="sair()": #se o cliente digita sair()
            socketList.remove(conn) #remove ele da lista de conexoes socketList
            atual = atual-1 #diminui 1 do parametro do contador de clientes
            clientes = clientes-1 #diminui 1 do contador de clientes
            print addr, nick, "saiu do chat" # printa no servidor quem saiu do chat
            toAll = str(addr)+str(nick)+" saiu do chat." #modifica toAll para que envie a todos os clientes quem saiu do chat
            break #fecha a thread de conexao do cliente, quebrando o loop
        else:
            toAll = str(addr) + " " + str(nick) + " enviou: " + mensagem #envia a mensagem que o cliente da thread digitou para todos os clientes
        print toAll #printa no servidor a mensagem que o cliente da thread digitou


HOST = 'localhost' #ip do server
PORT = 7214 #porta do server
s = socket() #cria o socket
s.bind((HOST, PORT)) #binda ele com o ip e porta
s.listen(9999) #prepara para ouvir ate 9999 sockets

print "O servidor de chat esta rodando..." #printa que o servidor iniciou
atual = 1 #inicia o parametro do contador de clientes
Thread(target=conexao_cliente).start() #inicia a primeira thread de conexao com o cliente
Thread(target=controle).start() #inicia a thread que recebe os comandos do servidor
while True:
    if atual < clientes: #se atual < clientes significa que um novo cliente se conectou
        Thread(target=conexao_cliente).start() #cria uma nova thread para receber um novo cliente
        atual = atual +1 #acrescenta um ao parametro do contador de clientes para que se iguale ao numero de clientes
    else:
        if toAll != msgAntiga: #se a mensagem em toAll for diferente da msgAntiga (msgAntiga e a mensagem que ja foi enviada), envie a mensagem toAll
            if atual-1 > 0: #para evitar bugs
                for i in range (0,atual-1): #enviar a mensagem em toAll para cada um dos clientes 1 por 1 nesse loop
                    socketList[i].send(toAll)
                msgAntiga = toAll #a mensagem enviada passa a ser uma mensagem antiga
        atual = atual

s.close()
    

