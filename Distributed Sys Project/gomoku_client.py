import xmlrpc.client
import time
import os
import msvcrt

#função pra limpar o buffer antes dos inputs
def clear_keyboard_buffer():
    while msvcrt.kbhit():
        msvcrt.getch()

#limpa o terminal toda vez que for printar o tabuleiro atual
def print_board(board):
    os.system('cls')
    print("Tabuleiro atual:")
    print(board)

if __name__ == '__main__':
    server = xmlrpc.client.ServerProxy('http://127.0.0.1:8000/')
    
    # salva na variavel a lista dos jogadores ja presentes (inicia vazia)
    players = server.get_players()

    clear_keyboard_buffer()
    #se não houverem jogadores, pergunta o simbolo que ele deseja, se ja houver um aguardando, lhe da o simbolo que sobrou
    if not players:
        player_id = input("Selecione o símbolo que deseja usar entre (X/O): ").upper()
        if player_id not in ['X', 'O']:
            print("Identificação inválida. O jogo será encerrado.")
            exit()
        server.register_player(player_id)
    elif len(players) == 1:
        first_player_id = players[0]
        player_id = 'O' if first_player_id == 'X' else 'X'
        server.register_player(player_id)
    else:
        print("Já existem dois jogadores registrados. O jogo não pode ter mais de dois jogadores.")

    print(f"Você é o jogador {player_id}.")
    time.sleep(2)
    #deixa o primeiro jogador aguardando até o segundo entrar
    if (player_id == 'X' or player_id == 'O') and len(players) == 0:
        print("Aguardando o segundo jogador entrar...")
        while not server.are_players_ready():
            time.sleep(1)
    print_board(server.get_current_board())

    #loop principal que administra as jogadas
    while True:
        current_turn = server.current_turn()
        winner = server.check_winner_exists()
        if winner != "None":
            print(f"Jogador {winner} venceu o jogo!")
            
            break
        #se não for a vez dele aguarda a vez do outro
        if current_turn != player_id:
            print(f"Aguardando a jogada do jogador {current_turn}...")
            old_board = server.get_current_board()
            while current_turn != player_id:
                current_turn = server.current_turn()
                new_board = server.get_current_board()
                if new_board != old_board:
                    print_board(new_board)
            continue

        try:
            clear_keyboard_buffer()  # Limpa o buffer antes de cada input
            x = int(input("Digite a coordenada x (0-14): "))
            y = int(input("Digite a coordenada y (0-14): "))
            
            if server.make_move(x, y, player_id):
                board = server.get_current_board()
                print_board(board)
                winner = server.check_winner_exists()
                if winner != "None":
                    print(f"Jogador {winner} venceu o jogo!")
                    time.sleep(2) 
                    server.reset_game()

                    break
            else:
                print("Jogada inválida. Tente novamente.")
        except ValueError:
            print("Entrada inválida! Digite um número entre 0 e 14 para cada coordenada.")
