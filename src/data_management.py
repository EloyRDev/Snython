import os
import json
from colorama import Fore


class Player:
    def __init__(self, name, record):
        self.name = name
        self.record = record


class Data:
    @staticmethod
    def get_records():
        try:
            with open("data/records.json") as file:
                data = json.load(file)
                file.close()
                return data
        except:
            Data.create_record_file()
            return Data.get_records()

    @staticmethod
    def create_record_file():
        if not os.path.exists("data"): os.mkdir("data")
        file = open("data/records.json", "w")
        file.write("[]")
        file.close()

    @staticmethod
    def check_name(name):
        while not isinstance(name, str) and 3 > len(name) > 15:
            name = input("Please write a valid name: ")

        return name

    @staticmethod
    def get_player(name):
        data = Data.get_records()

        for rec in data:
            if rec["name"] == name: return Player(rec["name"], rec["record"])

        return False

    @staticmethod
    def create_player():
        player_name = Data.check_name(input("What's your name fellow player?: "))
        player_object = Data.get_player(player_name)
        if not player_object: return Player(player_name, "No record yet.")
        else: return player_object

    @staticmethod
    def write_record(player):
        data = Data.get_records()
        file = open("data/records.json", "w")
        exists = False

        for rec in data:
            if rec["name"] == player.name:
                if rec["record"] < player.record:
                    rec["record"] = player.record
                exists = True
                break

        if not exists: data.append({
            "name": player.name,
            "record": player.record
        })

        json.dump(data, file)
        file.close()

    @staticmethod
    def get_top_players():
        data = Data.get_records()
        sorted_data = sorted(data, key=lambda obj: obj["record"], reverse=True)
        top_board = ""
        for i, player in enumerate(sorted_data, start=1):
            if i == 1: top_board += Fore.LIGHTRED_EX
            elif i == 2: top_board += Fore.LIGHTYELLOW_EX
            elif i == 3: top_board += Fore.YELLOW
            else: top_board+= Fore.RESET

            top_board += f"\t\t{i}. {player['name']}: {player['record']} points.\n"

        return top_board
