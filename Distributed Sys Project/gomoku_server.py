from xmlrpc.server import SimpleXMLRPCServer

class GomokuGame:
    #define o estado inicial do jogo
    def __init__(self):
        self.board = [['.' for _ in range(15)] for _ in range(15)]
        self.current_player = ''
        self.players = []
        self.winner = None
        self.all_players_registered = False

    #registra um jogador
    def register_player(self, player_id):
        #se o jogo ainda não esta cheio, adiciona o jogador
        if len(self.players) < 2:
            self.players.append(player_id)
            #caso for o primeiro jogador registrado, faz ele ser o primeiro a jogar
            if len(self.players) == 1:
                self.current_player = player_id
            #se encheu após adicionar o jogador atual, confirma que todos os jogadores foram registrados    
            if len(self.players) == 2:
                self.all_players_registered = True
            return f"Jogador {player_id} registrado."
        return "Número máximo de jogadores registrado."

    #faz a logica do movimento do jogador
    def make_move(self, x, y, player_id):
        if self.board[x][y] == '.' and player_id == self.current_player and self.all_players_registered:
            self.board[x][y] = self.current_player
            #checa se esse movimento feito causou a vitória
            if self.check_winner(x, y, self.current_player):
                self.winner = self.current_player
            #faz a mudança do jogador atual para o outro após o fim da jogada e confirma o sucesso do movimento
            self.current_player = 'O' if self.current_player == 'X' else 'X'
            return True
        return False

    #get do tabuleiro atual com a adição de numeração de linhas e colunas
    def get_current_board(self):
        # Adiciona numeração das colunas com espaçamento adequado
        board_str = "   " + " ".join(f"{i:2}" for i in range(15)) + "\n"
        
        # Adiciona cada linha do tabuleiro com a numeração à esquerda e espaçamento entre colunas
        for i, row in enumerate(self.board):
            board_str += f"{i:2}  " + "  ".join(row) + "\n"
        return board_str

    def current_turn(self):
        return self.current_player

    def are_players_ready(self):
        return self.all_players_registered

    #verifica se há vencedor
    def check_winner(self, x, y, player):
        #verifica 5 simbolos consecutivos em cada direção possivel
        def check_direction(dx, dy):
            count = 0
            #olha somente os 4 antes e após o ultimo simbolo jogado e verifica se sua adição causou vitoria
            for i in range(-4, 5):
                nx, ny = x + i * dx, y + i * dy
                if 0 <= nx < 15 and 0 <= ny < 15 and self.board[nx][ny] == player:
                    count += 1
                    if count == 5:
                        return True
                else:
                    count = 0
            return False

        return (check_direction(1, 0) or 
                check_direction(0, 1) or  
                check_direction(1, 1) or  
                check_direction(1, -1))   

    def check_winner_exists(self):
        return self.winner if self.winner else "None"
    
    def get_players(self):
        return self.players
    
    def reset_game(self):
        self.board = [['.' for _ in range(15)] for _ in range(15)]
        self.current_player = ''
        self.players = []
        self.winner = None
        self.all_players_registered = False

if __name__ == '__main__':
    server = SimpleXMLRPCServer(('127.0.0.1', 8000), allow_none=True)
    game = GomokuGame()
    
    server.register_instance(game)
    
    print("Servidor está rodando...")
    server.serve_forever()