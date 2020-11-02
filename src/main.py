from data_management import Data
from game import Menu, Game

class Main:
    def __init__(self):
        self.player = {}

    def start(self):
        Menu.draw_menu()
        self.player = Data.create_player()

        print(f"Welcome {self.player.name}, your current record is: {self.player.record}")
        input("Press enter to start the game...")

        self.run()

    def run(self):
        game = Game(30)
        game.run()
        self.player.record = game.points
        Data.write_record(self.player)
        Menu.draw_end(game.points)

(Main()).start()
