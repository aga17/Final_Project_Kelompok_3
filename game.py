class Game:
    def __init__(self, id):
        self.p1_went = False
        self.p2_went = False
        self.ready = False
        self.id = id
        self.moves = [None, None]
        self.wins = [0, 0]
        self.draws = 0

    def get_player_move(self, player):
        return self.moves[player]

    def play(self, player, move):
        self.moves[player] = move
        if player == 0:
            self.p1_went = True
        else:
            self.p2_went = True

    def connected(self):
        return self.ready

    def both_went(self):
        return self.p1_went and self.p2_went

    def winner(self):
        p1 = self.moves[0].upper()[0:2]
        p2 = self.moves[1].upper()[0:2]
        winner = -1
        if p1 == "BA" and p2 == "GU":
            winner = 0
        elif p1 == "BA" and p2 == "KE":
            winner = 1
        elif p1 == "BA" and p2 == "AI":
            winner = 0
        elif p1 == "BA" and p2 == "AP":
            winner = 1

        elif p1 == "GU" and p2 == "BA":
            winner = 1
        elif p1 == "GU" and p2 == "KE":
            winner = 0
        elif p1 == "GU" and p2 == "AI":
            winner = 1
        elif p1 == "GU" and p2 == "AP":
            winner = 0

        elif p1 == "KE" and p2 == "BA":
            winner = 0
        elif p1 == "KE" and p2 == "GU":
            winner = 1
        elif p1 == "KE" and p2 == "AI":
            winner = 0
        elif p1 == "KE" and p2 == "AP":
            winner = 1

        elif p1 == "AI" and p2 == "BA":
            winner = 1
        elif p1 == "AI" and p2 == "GU":
            winner = 0
        elif p1 == "AI" and p2 == "KE":
            winner = 1
        elif p1 == "AI" and p2 == "AP":
            winner = 0

        elif p1 == "AP" and p2 == "BA":
            winner = 0
        elif p1 == "AP" and p2 == "GU":
            winner = 1
        elif p1 == "AP" and p2 == "KE":
            winner = 0
        elif p1 == "AP" and p2 == "AI":
            winner = 1

        return winner

    def reset(self):
        self.p1_went = False
        self.p2_went = False
