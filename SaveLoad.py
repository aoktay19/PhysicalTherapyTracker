#There will be a function to initialize players from a txt using json
import pickle
class SaveLoad:
    def __init__(self, path = "test.pickle"):
        self.path = path
        self.players = self.load()

    def save(self, data):
        with open(self.path, "wb") as outfile:
            pickle.dump(data, outfile)

    def load(self):
        try:
            with open(self.path, "rb") as infile:
                self.players = pickle.load(infile)
                return self.players
        except Exception:
            return []

    def add_player(self, player):
        name = player.get_name()
        for i in self.players:
            if i.get_name() == name:
                self.players.remove(i)
        self.players.append(player)
        self.save(self.players)

    def delete_player(self, index):
        try:
            del self.players[index]
            self.save(self.players)
        except:
            print("player cannot found")

    def get_players(self):
        return self.players