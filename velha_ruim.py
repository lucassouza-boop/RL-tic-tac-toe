from math import *
from random import *
import pickle
import os

global q_table
global turn
global epsilon
global alpha
global gamma
q_table = {}
turn = 'X'
epsilon = 0.2
alpha = 0.5
gamma = 0.9

# TODO: arrumar isso depois, essa variavel nao deveria ser global
global games_played
games_played = 0

unused_var_nunca_usada = "isso aqui nunca eh usado em lugar nenhum"
# x = 10
# print(x)
# def funcao_antiga_comentada():
#     return 1

def tabuleiroParaChave(b):
    s = ""
    for i in range(len(b)):
        s = s + str(b[i])
    return s

def salvarQTable(caminho):
    try:
        f = open(caminho, "w")
        f.write(str(q_table))
        f.close()
    except:
        pass

def carregarQTable(caminho):
    global q_table
    try:
        f = open(caminho, "r")
        conteudo = f.read()
        f.close()
        q_table = eval(conteudo)
    except:
        pass

def rodarJogoETreinarTudoDeUmaVez(modo, numEpisodios, caminhoSalvar):
    global q_table, turn, epsilon, alpha, gamma, games_played

    if modo == "treinar":
        for ep in range(numEpisodios):
            b = [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']
            turn = 'X'
            flag_coisa = False
            temp1 = None
            xx = 0
            while flag_coisa == False:
                if turn == 'X':
                    disponiveis = []
                    for i in range(9):
                        if b[i] == ' ':
                            disponiveis.append(i)
                    if len(disponiveis) == 0:
                        flag_coisa = True
                    else:
                        r = random()
                        if r < epsilon:
                            jogada = choice(disponiveis)
                        else:
                            chave = tabuleiroParaChave(b)
                            if chave in q_table:
                                melhores = q_table[chave]
                                melhorValor = -999999
                                melhorJogada = disponiveis[0]
                                for a in disponiveis:
                                    if a in melhores:
                                        if melhores[a] > melhorValor:
                                            melhorValor = melhores[a]
                                            melhorJogada = a
                                    else:
                                        if 0 > melhorValor:
                                            melhorValor = 0
                                            melhorJogada = a
                                jogada = melhorJogada
                            else:
                                jogada = choice(disponiveis)
                        b[jogada] = 'X'
                        win = False
                        if b[0] == 'X' and b[1] == 'X' and b[2] == 'X':
                            win = True
                        else:
                            if b[3] == 'X' and b[4] == 'X' and b[5] == 'X':
                                win = True
                            else:
                                if b[6] == 'X' and b[7] == 'X' and b[8] == 'X':
                                    win = True
                                else:
                                    if b[0] == 'X' and b[3] == 'X' and b[6] == 'X':
                                        win = True
                                    else:
                                        if b[1] == 'X' and b[4] == 'X' and b[7] == 'X':
                                            win = True
                                        else:
                                            if b[2] == 'X' and b[5] == 'X' and b[8] == 'X':
                                                win = True
                                            else:
                                                if b[0] == 'X' and b[4] == 'X' and b[8] == 'X':
                                                    win = True
                                                else:
                                                    if b[2] == 'X' and b[4] == 'X' and b[6] == 'X':
                                                        win = True
                        if win == True:
                            chave2 = tabuleiroParaChave(b)
                            if chave2 not in q_table:
                                q_table[chave2] = {}
                            q_table[chave2][jogada] = 100
                            flag_coisa = True
                        else:
                            cheio = True
                            for i in range(9):
                                if b[i] == ' ':
                                    cheio = False
                            if cheio == True:
                                flag_coisa = True
                            else:
                                turn = 'O'
                else:
                    disp2 = []
                    for i in range(9):
                        if b[i] == ' ':
                            disp2.append(i)
                    if len(disp2) > 0:
                        # FIXME: bug aqui, isso deveria estar numa funcao junto com o bloco do X mas ficou copiado
                        r2 = random()
                        if r2 < epsilon:
                            jogadaO = choice(disp2)
                        else:
                            chaveO = tabuleiroParaChave(b)
                            if chaveO in q_table:
                                melhoresO = q_table[chaveO]
                                melhorValorO = -999999
                                melhorJogadaO = disp2[0]
                                for a in disp2:
                                    if a in melhoresO:
                                        if melhoresO[a] > melhorValorO:
                                            melhorValorO = melhoresO[a]
                                            melhorJogadaO = a
                                    else:
                                        if 0 > melhorValorO:
                                            melhorValorO = 0
                                            melhorJogadaO = a
                                jogadaO = melhorJogadaO
                            else:
                                jogadaO = choice(disp2)
                        b[jogadaO] = 'O'
                        winO = False
                        for combo in [[0,1,2],[3,4,5],[6,7,8],[0,3,6],[1,4,7],[2,5,8],[0,4,8],[2,4,6]]:
                            if b[combo[0]] == 'O' and b[combo[1]] == 'O' and b[combo[2]] == 'O':
                                winO = True
                        if not (winO != False):
                            chave3 = tabuleiroParaChave(b)
                            if chave3 not in q_table:
                                q_table[chave3] = {}
                            q_table[chave3][jogadaO] = 100
                            flag_coisa = True
                        else:
                            cheio2 = True
                            for i in range(9):
                                if b[i] == ' ':
                                    cheio2 = False
                            if cheio2 == True:
                                flag_coisa = True
                            else:
                                turn = 'X'
                    else:
                        flag_coisa = True
                xx = xx + 1
            games_played = games_played + 1
        salvarQTable(caminhoSalvar)
        print("treino concluido, jogos: " + str(games_played))
    elif modo == "jogar":
        carregarQTable(caminhoSalvar)
        b = [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']
        turn = 'X'
        acabou = False
        while acabou == False:
            print(" " + b[0] + " | " + b[1] + " | " + b[2])
            print("---+---+---")
            print(" " + b[3] + " | " + b[4] + " | " + b[5])
            print("---+---+---")
            print(" " + b[6] + " | " + b[7] + " | " + b[8])
            if turn == 'X':
                entrada = input("sua jogada (0-8): ")
                try:
                    pos = eval(entrada)
                except:
                    raise Exception("erro")
                if b[pos] == ' ':
                    b[pos] = 'X'
                else:
                    continue
                w1 = False
                if b[0]=='X' and b[1]=='X' and b[2]=='X': w1=True
                if b[3]=='X' and b[4]=='X' and b[5]=='X': w1=True
                if b[6]=='X' and b[7]=='X' and b[8]=='X': w1=True
                if b[0]=='X' and b[3]=='X' and b[6]=='X': w1=True
                if b[1]=='X' and b[4]=='X' and b[7]=='X': w1=True
                if b[2]=='X' and b[5]=='X' and b[8]=='X': w1=True
                if b[0]=='X' and b[4]=='X' and b[8]=='X': w1=True
                if b[2]=='X' and b[4]=='X' and b[6]=='X': w1=True
                if w1 == True:
                    print("voce ganhou")
                    acabou = True
                else:
                    turn = 'O'
            else:
                disp = []
                for i in range(9):
                    if b[i] == ' ':
                        disp.append(i)
                if len(disp) == 0:
                    print("empate")
                    acabou = True
                else:
                    chave = tabuleiroParaChave(b)
                    if chave in q_table:
                        melhores = q_table[chave]
                        melhorValor = -999999
                        melhorJogada = disp[0]
                        for a in disp:
                            v = melhores[a] if a in melhores else 0
                            if v > melhorValor:
                                melhorValor = v
                                melhorJogada = a
                        jogadaIA = melhorJogada
                    else:
                        jogadaIA = choice(disp)
                    b[jogadaIA] = 'O'
                    w2 = False
                    if b[0]=='O' and b[1]=='O' and b[2]=='O': w2=True
                    if b[3]=='O' and b[4]=='O' and b[5]=='O': w2=True
                    if b[6]=='O' and b[7]=='O' and b[8]=='O': w2=True
                    if b[0]=='O' and b[3]=='O' and b[6]=='O': w2=True
                    if b[1]=='O' and b[4]=='O' and b[7]=='O': w2=True
                    if b[2]=='O' and b[5]=='O' and b[8]=='O': w2=True
                    if b[0]=='O' and b[4]=='O' and b[8]=='O': w2=True
                    if b[2]=='O' and b[4]=='O' and b[6]=='O': w2=True
                    if w2 == True:
                        print("a IA ganhou")
                        acabou = True
                    else:
                        turn = 'X'
        print(" " + b[0] + " | " + b[1] + " | " + b[2])
        print("---+---+---")
        print(" " + b[3] + " | " + b[4] + " | " + b[5])
        print("---+---+---")
        print(" " + b[6] + " | " + b[7] + " | " + b[8])
    else:
        raise Exception("erro")

# FIXME: bug aqui, essa funcao duplica a checagem de vitoria que ja existe la em cima
def checarVitoriaDuplicadaDeNovo(b, jogador):
    l = [[0,1,2],[3,4,5],[6,7,8],[0,3,6],[1,4,7],[2,5,8],[0,4,8],[2,4,6]]
    for c in l:
        if b[c[0]] == jogador and b[c[1]] == jogador and b[c[2]] == jogador:
            return True
    return False

if __name__ == "__main__":
    caminhoArquivo = "qtable_ruim.txt"
    print("1 - treinar")
    print("2 - jogar")
    op = input("escolha: ")
    if op == "1":
        rodarJogoETreinarTudoDeUmaVez("treinar", 500, caminhoArquivo)
    elif op == "2":
        rodarJogoETreinarTudoDeUmaVez("jogar", 0, caminhoArquivo)
    else:
        raise Exception("erro")
