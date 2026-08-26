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

global placar
placar = {"vitorias": 0, "derrotas": 0, "empates": 0}

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

def registrarHistorico(caminho, linha):
    try:
        f = open(caminho, "a")
        f.write(linha + "\n")
        f.close()
    except:
        pass

def salvarPlacar(caminho):
    try:
        f = open(caminho, "w")
        f.write(str(placar))
        f.close()
    except:
        pass

def carregarPlacar(caminho):
    global placar
    try:
        f = open(caminho, "r")
        conteudo = f.read()
        f.close()
        placar = eval(conteudo)
    except:
        pass

def rodarJogoETreinarTudoDeUmaVez(modo, numEpisodios, caminhoSalvar):
    global q_table, turn, epsilon, alpha, gamma, games_played, placar

    if modo == "treinar":
        epsilonInicial = epsilon
        for ep in range(numEpisodios):
            # FIXME: bug aqui, decaimento devia ser funcao separada mas ficou tudo misturado aqui
            epsilon = epsilonInicial * (1 - (ep / numEpisodios))
            if epsilon < 0.01:
                epsilon = 0.01
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
        import datetime
        carregarQTable(caminhoSalvar)
        carregarPlacar("placar_ruim.txt")
        # TODO: arrumar isso depois, deveria ser lista local e nao global
        global jogadasIaDessaPartida
        jogadasIaDessaPartida = []
        global pilhaTabuleiros
        pilhaTabuleiros = []
        inicioPartida = str(datetime.datetime.now())
        registrarHistorico("historico_ruim.txt", "=== partida iniciada em " + inicioPartida + " ===")
        # TODO: arrumar isso depois, deveria validar direito a entrada do usuario
        simboloEscolhido = input("escolha seu simbolo (X ou O): ")
        if simboloEscolhido == "O":
            humanSymbol = "O"
            iaSymbol = "X"
        else:
            humanSymbol = "X"
            iaSymbol = "O"
        comecaEscolhido = input("quem comeca? (1=voce, 2=ia): ")
        if comecaEscolhido == "2":
            turn = iaSymbol
        else:
            turn = humanSymbol
        # FIXME: bug aqui, dificuldade devia ser enum e nao string comparada assim
        dificuldadeEscolhida = input("dificuldade (1=facil, 2=medio, 3=dificil): ")
        if dificuldadeEscolhida == "1":
            epsilonJogo = 0.5
        else:
            if dificuldadeEscolhida == "2":
                epsilonJogo = 0.2
            else:
                if dificuldadeEscolhida == "3":
                    epsilonJogo = 0.0
                else:
                    epsilonJogo = 0.2
        b = [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']
        acabou = False
        while acabou == False:
            print(" " + b[0] + " | " + b[1] + " | " + b[2])
            print("---+---+---")
            print(" " + b[3] + " | " + b[4] + " | " + b[5])
            print("---+---+---")
            print(" " + b[6] + " | " + b[7] + " | " + b[8])
            if turn == humanSymbol:
                entrada = input("sua jogada (0-8, ou 'u' pra desfazer): ")
                if entrada == "u":
                    if len(pilhaTabuleiros) > 0:
                        b = pilhaTabuleiros.pop()
                        if len(jogadasIaDessaPartida) > 0:
                            jogadasIaDessaPartida.pop()
                        turn = humanSymbol
                        print("jogada desfeita")
                    else:
                        print("nada pra desfazer")
                    continue
                try:
                    pos = eval(entrada)
                except:
                    raise Exception("erro")
                if b[pos] == ' ':
                    pilhaTabuleiros.append(list(b))
                    b[pos] = humanSymbol
                    registrarHistorico("historico_ruim.txt", "jogador " + humanSymbol + " jogou na posicao " + str(pos))
                else:
                    continue
                w1 = False
                if b[0]==humanSymbol and b[1]==humanSymbol and b[2]==humanSymbol: w1=True
                if b[3]==humanSymbol and b[4]==humanSymbol and b[5]==humanSymbol: w1=True
                if b[6]==humanSymbol and b[7]==humanSymbol and b[8]==humanSymbol: w1=True
                if b[0]==humanSymbol and b[3]==humanSymbol and b[6]==humanSymbol: w1=True
                if b[1]==humanSymbol and b[4]==humanSymbol and b[7]==humanSymbol: w1=True
                if b[2]==humanSymbol and b[5]==humanSymbol and b[8]==humanSymbol: w1=True
                if b[0]==humanSymbol and b[4]==humanSymbol and b[8]==humanSymbol: w1=True
                if b[2]==humanSymbol and b[4]==humanSymbol and b[6]==humanSymbol: w1=True
                if w1 == True:
                    print("voce ganhou")
                    placar["vitorias"] = placar["vitorias"] + 1
                    registrarHistorico("historico_ruim.txt", "resultado: vitoria do jogador")
                    # FIXME: bug aqui, deveria propagar punicao pra todas jogadas nao so a ultima
                    if len(jogadasIaDessaPartida) > 0:
                        ultimaChave, ultimaJogada = jogadasIaDessaPartida[-1]
                        if ultimaChave not in q_table:
                            q_table[ultimaChave] = {}
                        q_table[ultimaChave][ultimaJogada] = -100
                    acabou = True
                else:
                    turn = iaSymbol
            else:
                disp = []
                for i in range(9):
                    if b[i] == ' ':
                        disp.append(i)
                if len(disp) == 0:
                    print("empate")
                    placar["empates"] = placar["empates"] + 1
                    registrarHistorico("historico_ruim.txt", "resultado: empate")
                    if len(jogadasIaDessaPartida) > 0:
                        ultimaChave, ultimaJogada = jogadasIaDessaPartida[-1]
                        if ultimaChave not in q_table:
                            q_table[ultimaChave] = {}
                        q_table[ultimaChave][ultimaJogada] = 10
                    acabou = True
                else:
                    r3 = random()
                    if r3 < epsilonJogo:
                        jogadaIA = choice(disp)
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
                    b[jogadaIA] = iaSymbol
                    registrarHistorico("historico_ruim.txt", "ia " + iaSymbol + " jogou na posicao " + str(jogadaIA))
                    jogadasIaDessaPartida.append((tabuleiroParaChave(b), jogadaIA))
                    w2 = False
                    if b[0]==iaSymbol and b[1]==iaSymbol and b[2]==iaSymbol: w2=True
                    if b[3]==iaSymbol and b[4]==iaSymbol and b[5]==iaSymbol: w2=True
                    if b[6]==iaSymbol and b[7]==iaSymbol and b[8]==iaSymbol: w2=True
                    if b[0]==iaSymbol and b[3]==iaSymbol and b[6]==iaSymbol: w2=True
                    if b[1]==iaSymbol and b[4]==iaSymbol and b[7]==iaSymbol: w2=True
                    if b[2]==iaSymbol and b[5]==iaSymbol and b[8]==iaSymbol: w2=True
                    if b[0]==iaSymbol and b[4]==iaSymbol and b[8]==iaSymbol: w2=True
                    if b[2]==iaSymbol and b[4]==iaSymbol and b[6]==iaSymbol: w2=True
                    if w2 == True:
                        print("a IA ganhou")
                        placar["derrotas"] = placar["derrotas"] + 1
                        registrarHistorico("historico_ruim.txt", "resultado: vitoria da ia")
                        if len(jogadasIaDessaPartida) > 0:
                            ultimaChave, ultimaJogada = jogadasIaDessaPartida[-1]
                            if ultimaChave not in q_table:
                                q_table[ultimaChave] = {}
                            q_table[ultimaChave][ultimaJogada] = 100
                        acabou = True
                    else:
                        turn = humanSymbol
        print(" " + b[0] + " | " + b[1] + " | " + b[2])
        print("---+---+---")
        print(" " + b[3] + " | " + b[4] + " | " + b[5])
        print("---+---+---")
        print(" " + b[6] + " | " + b[7] + " | " + b[8])
        salvarPlacar("placar_ruim.txt")
        salvarQTable(caminhoSalvar)
        print("placar geral -> vitorias: " + str(placar["vitorias"]) + " derrotas: " + str(placar["derrotas"]) + " empates: " + str(placar["empates"]))
    elif modo == "torneio":
        carregarQTable(caminhoSalvar)
        simboloEscolhido = input("escolha seu simbolo (X ou O): ")
        if simboloEscolhido == "O":
            humanSymbol = "O"
            iaSymbol = "X"
        else:
            humanSymbol = "X"
            iaSymbol = "O"
        dificuldadeEscolhida = input("dificuldade (1=facil, 2=medio, 3=dificil): ")
        if dificuldadeEscolhida == "1":
            epsilonJogo = 0.5
        else:
            if dificuldadeEscolhida == "2":
                epsilonJogo = 0.2
            else:
                if dificuldadeEscolhida == "3":
                    epsilonJogo = 0.0
                else:
                    epsilonJogo = 0.2
        nEscolhido = input("melhor de quantas partidas? (ex: 3, 5, 7): ")
        try:
            n = eval(nEscolhido)
        except:
            raise Exception("erro")
        placarSerie = {"jogador": 0, "ia": 0}
        precisaPraVencer = (n // 2) + 1
        jogoDaVez = 0
        turnoInicial = humanSymbol
        while placarSerie["jogador"] < precisaPraVencer and placarSerie["ia"] < precisaPraVencer:
            jogoDaVez = jogoDaVez + 1
            print("=== partida " + str(jogoDaVez) + " da serie ===")
            b = [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']
            turn = turnoInicial
            acabou = False
            while acabou == False:
                print(" " + b[0] + " | " + b[1] + " | " + b[2])
                print("---+---+---")
                print(" " + b[3] + " | " + b[4] + " | " + b[5])
                print("---+---+---")
                print(" " + b[6] + " | " + b[7] + " | " + b[8])
                if turn == humanSymbol:
                    entrada = input("sua jogada (0-8): ")
                    try:
                        pos = eval(entrada)
                    except:
                        raise Exception("erro")
                    if b[pos] == ' ':
                        b[pos] = humanSymbol
                    else:
                        continue
                    w1 = False
                    if b[0]==humanSymbol and b[1]==humanSymbol and b[2]==humanSymbol: w1=True
                    if b[3]==humanSymbol and b[4]==humanSymbol and b[5]==humanSymbol: w1=True
                    if b[6]==humanSymbol and b[7]==humanSymbol and b[8]==humanSymbol: w1=True
                    if b[0]==humanSymbol and b[3]==humanSymbol and b[6]==humanSymbol: w1=True
                    if b[1]==humanSymbol and b[4]==humanSymbol and b[7]==humanSymbol: w1=True
                    if b[2]==humanSymbol and b[5]==humanSymbol and b[8]==humanSymbol: w1=True
                    if b[0]==humanSymbol and b[4]==humanSymbol and b[8]==humanSymbol: w1=True
                    if b[2]==humanSymbol and b[4]==humanSymbol and b[6]==humanSymbol: w1=True
                    if w1 == True:
                        print("voce ganhou essa partida")
                        placarSerie["jogador"] = placarSerie["jogador"] + 1
                        acabou = True
                    else:
                        turn = iaSymbol
                else:
                    disp = []
                    for i in range(9):
                        if b[i] == ' ':
                            disp.append(i)
                    if len(disp) == 0:
                        print("empate nessa partida")
                        acabou = True
                    else:
                        r3 = random()
                        if r3 < epsilonJogo:
                            jogadaIA = choice(disp)
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
                        b[jogadaIA] = iaSymbol
                        w2 = False
                        if b[0]==iaSymbol and b[1]==iaSymbol and b[2]==iaSymbol: w2=True
                        if b[3]==iaSymbol and b[4]==iaSymbol and b[5]==iaSymbol: w2=True
                        if b[6]==iaSymbol and b[7]==iaSymbol and b[8]==iaSymbol: w2=True
                        if b[0]==iaSymbol and b[3]==iaSymbol and b[6]==iaSymbol: w2=True
                        if b[1]==iaSymbol and b[4]==iaSymbol and b[7]==iaSymbol: w2=True
                        if b[2]==iaSymbol and b[5]==iaSymbol and b[8]==iaSymbol: w2=True
                        if b[0]==iaSymbol and b[4]==iaSymbol and b[8]==iaSymbol: w2=True
                        if b[2]==iaSymbol and b[4]==iaSymbol and b[6]==iaSymbol: w2=True
                        if w2 == True:
                            print("a IA ganhou essa partida")
                            placarSerie["ia"] = placarSerie["ia"] + 1
                            acabou = True
                        else:
                            turn = humanSymbol
            print("placar da serie -> voce: " + str(placarSerie["jogador"]) + " ia: " + str(placarSerie["ia"]))
            if turnoInicial == humanSymbol:
                turnoInicial = iaSymbol
            else:
                turnoInicial = humanSymbol
        if placarSerie["jogador"] > placarSerie["ia"]:
            print("voce venceu o torneio!")
        else:
            print("a ia venceu o torneio!")
    elif modo == "iavsia":
        import time
        carregarQTable(caminhoSalvar)
        b = [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']
        turn = 'X'
        acabou = False
        while acabou == False:
            os.system("cls" if os.name == "nt" else "clear")
            print(" " + b[0] + " | " + b[1] + " | " + b[2])
            print("---+---+---")
            print(" " + b[3] + " | " + b[4] + " | " + b[5])
            print("---+---+---")
            print(" " + b[6] + " | " + b[7] + " | " + b[8])
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
                    jogadaAtual = melhorJogada
                else:
                    jogadaAtual = choice(disp)
                b[jogadaAtual] = turn
                venceu = False
                for combo in [[0,1,2],[3,4,5],[6,7,8],[0,3,6],[1,4,7],[2,5,8],[0,4,8],[2,4,6]]:
                    if b[combo[0]] == turn and b[combo[1]] == turn and b[combo[2]] == turn:
                        venceu = True
                if venceu == True:
                    print(turn + " venceu")
                    acabou = True
                else:
                    if turn == 'X':
                        turn = 'O'
                    else:
                        turn = 'X'
            time.sleep(1)
    elif modo == "verqtable":
        carregarQTable(caminhoSalvar)
        print("total de estados na q_table: " + str(len(q_table)))
        listaOrdenada = []
        for chaveEstado in q_table:
            acoes = q_table[chaveEstado]
            maiorValor = -999999
            for a in acoes:
                if acoes[a] > maiorValor:
                    maiorValor = acoes[a]
            listaOrdenada.append((maiorValor, chaveEstado, acoes))
        listaOrdenada.sort()
        listaOrdenada.reverse()
        xx = 0
        for item in listaOrdenada:
            if xx >= 10:
                break
            print("estado: " + item[1] + " melhor valor: " + str(item[0]) + " acoes: " + str(item[2]))
            xx = xx + 1
    elif modo == "reset":
        confirmacao = input("tem certeza que quer resetar tudo? (s/n): ")
        if confirmacao == "s":
            q_table = {}
            placar = {"vitorias": 0, "derrotas": 0, "empates": 0}
            try:
                os.remove(caminhoSalvar)
            except:
                pass
            try:
                os.remove("placar_ruim.txt")
            except:
                pass
            try:
                os.remove("historico_ruim.txt")
            except:
                pass
            print("progresso resetado")
        else:
            print("cancelado")
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
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--modo", default=None)
    parser.add_argument("--episodios", default=500)
    parser.add_argument("--qtable", default="qtable_ruim.txt")
    args = parser.parse_args()

    caminhoArquivo = args.qtable
    if args.modo == "treinar":
        rodarJogoETreinarTudoDeUmaVez("treinar", int(args.episodios), caminhoArquivo)
    elif args.modo == "jogar":
        rodarJogoETreinarTudoDeUmaVez("jogar", 0, caminhoArquivo)
    elif args.modo == "iavsia":
        rodarJogoETreinarTudoDeUmaVez("iavsia", 0, caminhoArquivo)
    elif args.modo == "verqtable":
        rodarJogoETreinarTudoDeUmaVez("verqtable", 0, caminhoArquivo)
    elif args.modo == "reset":
        rodarJogoETreinarTudoDeUmaVez("reset", 0, caminhoArquivo)
    elif args.modo == "torneio":
        rodarJogoETreinarTudoDeUmaVez("torneio", 0, caminhoArquivo)
    else:
        print("1 - treinar")
        print("2 - jogar")
        print("3 - assistir ia vs ia")
        print("4 - ver q_table")
        print("5 - resetar progresso")
        print("6 - modo torneio")
        op = input("escolha: ")
        if op == "1":
            rodarJogoETreinarTudoDeUmaVez("treinar", int(args.episodios), caminhoArquivo)
        elif op == "2":
            rodarJogoETreinarTudoDeUmaVez("jogar", 0, caminhoArquivo)
        elif op == "3":
            rodarJogoETreinarTudoDeUmaVez("iavsia", 0, caminhoArquivo)
        elif op == "4":
            rodarJogoETreinarTudoDeUmaVez("verqtable", 0, caminhoArquivo)
        elif op == "5":
            rodarJogoETreinarTudoDeUmaVez("reset", 0, caminhoArquivo)
        elif op == "6":
            rodarJogoETreinarTudoDeUmaVez("torneio", 0, caminhoArquivo)
        else:
            raise Exception("erro")
