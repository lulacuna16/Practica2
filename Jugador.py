from time import time
import socket
import sys

def matrizP(): #Tablero Principiante
    filas=["1","2","3"];
    columnas=["A","B","C"];
    alto = len(filas) + 1
    largo=len(columnas)+1;
    matriz=[]
    for i in range(alto):  # ALTO
        matriz.append([])
        for j in range(largo):  # LARGO
            matriz[i].append(" ")
    return generarMatrizInicial(matriz,filas,columnas)

def matrizA(): #Tablero avanzado
    filas=["1","2","3","4","5"];
    columnas=["A","B","C","D","E"];
    alto = len(filas) + 1
    largo=len(columnas)+1;
    matriz=[]
    for i in range(alto):  # ALTO
        matriz.append([])
        for j in range(largo):  # LARGO
            matriz[i].append(" ")
    return generarMatrizInicial(matriz,filas,columnas)

def generarMatrizInicial(matriz,filas,columnas):
    #print("alto=", len(matriz))
    #print("largo=", len(matriz[0]))
    for i in range(len(matriz)):  # ALTO
        for j in range(len(matriz[0])):  # LARGO
            if i is 0:
                if j is 0:
                    matriz[i][j]=" "
                else:
                    matriz[i][j] = columnas[j-1]
            else:
                if j is 0:
                    matriz[i][j]=filas[i-1]
                else:
                    matriz[i][j]="-"
    return matriz


def verMatriz(matriz):
    alto = len(matriz)
    largo = len(matriz[0])
    for i in range(alto):
        for j in range(largo):  # LARGO
            print(matriz[i][j], "\t", end=" ")
        print()
def menu(TCPClientSocket):

        print("\tElige una dificultad\t")
        print("1. Principiante")
        print("2. Avanzado")
        case=int(input("Opcion: "))
        caseb = case.to_bytes(1, 'little')
        TCPClientSocket.sendall(caseb)
        if case == 1:
            matrizp=matrizP()
            verMatriz(matrizp)
            jugar(matrizp,TCPClientSocket)
        if case == 2:
            matriza=matrizA()
            verMatriz(matriza)
            jugar(matriza,TCPClientSocket)


def colocar(matriz,sim,TCPClientSocket):
    cont=0
    while cont==0:
        pos=str(input("Ingrese una coordenada (Ej. 1A,2C): "))
        fila = int(pos[0])
        col = ord(pos[1]) - 64
        #print(fila, ",", col)
        for i in range (len(matriz)):
            if i==fila:
                for j in range (len(matriz[0])):
                    if j==col:
                        if matriz[i][j]=="-":
                            matriz[i][j]=sim
                            cont+=1
                            verMatriz(matriz)
                        else:
                            print("Casilla Ocupada")

                    elif col<=0 or col>=len(matriz[0]):
                        print("Columna Invalida")
                        break;
            elif fila <= 0 or fila >= len(matriz):
                print("Fila Invalida")
                break
    TCPClientSocket.sendall(pos.encode())
def juegoAuto(matriz,sim,TCPClientSocket):
    pos=str(TCPClientSocket.recv(buffer_size),"ascii")
    fila = int (pos[0])
    col = ord(pos[1]) - 64
    matriz[int(fila)][int(col)] = sim
    print(str(TCPClientSocket.recv(buffer_size),"ascii"))


def ganarH(matriz,sim):
    cont=0
    for i in range (1,len(matriz)):
        cont=0
        for j in range(1,len(matriz[0])):
            if matriz[i][j]==sim:
                cont+=1
                if cont is (len(matriz)-1):
                    return 1
                    break;
def ganarV(matriz,sim):
    cont=0
    for j in range (1,len(matriz[0])):
        cont=0
        for i in range(1,len(matriz)):
            if matriz[i][j]==sim:
                cont+=1
                if cont is (len(matriz)-1):
                    return 1
                    break;
def jugar(matriz, TCPClientSocket):
    simJ="x"
    simS="o"
    cont=0
    print("Jugador es: ", simJ)
    print("Maquina es: ", simS)
    long=(len(matriz)-1)*(len(matriz)-1)
    inicio=time()
    while cont<long:
        print("TURNO JUGADOR\n")
        colocar(matriz,simJ,TCPClientSocket)
        if ganarH(matriz,simJ) is 1:
            print("Gano JUGADOR")
            break;
        if ganarV(matriz, simJ) is 1:
            print("Gano JUGADOR")
            break;
        cont+=1;
        if cont>=long:
            print("Juego Terminado: EMPATE")
            break
        print("TURNO MAQUINA\n")
        juegoAuto(matriz,simS,TCPClientSocket)
        verMatriz(matriz)
        if ganarH(matriz,simS) is 1:
            print("Gano MAQUINA")
            break;
        if ganarV(matriz, simS) is 1:
            print("Gano MAQUINA")
            break;
        cont+=1
        if cont>=long:
            print("Juego Terminado: EMPATE")
            break
    final=time()
    print("Duracion de la partida %.2f segundos" %(final-inicio))


#!/usr/bin/env python3

import socket

HOST = str(input("Ingrese IP del servidor: "))  # The server's hostname or IP address
PORT = int(input("Ingrese Puerto del servidor: "))  # The port used by the server
#HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
#PORT = 65432  # Port to listen on (non-privileged ports are > 1023)
buffer_size = 1024


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as TCPClientSocket:
    TCPClientSocket.connect((HOST, PORT))
    menu(TCPClientSocket)

    print(str(TCPClientSocket.recv(buffer_size),"ascii"))