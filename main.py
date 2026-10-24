class Game:
    def __init__(self):
        self.money = 0
        self.run_game()
        
    def run_game(self):
        while True:
            print("Money: " + str(self.money))
            input("Press 'enter' to earn money. ")
            self.money += 1
        
if __name__ == "__main__":
    game = Game()