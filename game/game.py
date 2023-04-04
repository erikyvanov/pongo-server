from game.constansts import SCREEN_HEIGHT, PADDLE_HEIGHT

class Player:
    def __init__(self, numberOfPlayer: int, id: str):
        self.score: int = 0
        self.Y_possition: int = (SCREEN_HEIGHT - PADDLE_HEIGHT) // 2
        self.numberOfPlayer = numberOfPlayer
        self.id = id

class Game:
    def __init__(self):
        self.players: list[Player] = []

        self.isRunning = False
    
    @property
    def hasPlayerZero(self):
        for player in self.players:
            if player.numberOfPlayer == 0:
                return True

        return False

    @property
    def isGameReady(self):
        return len(self.players) == 2

    def delete_player(self, id: str):
        for player in self.players:
            if player.id == id:
                self.players.remove(player)
                break