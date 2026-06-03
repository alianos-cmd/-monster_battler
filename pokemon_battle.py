import random

# klassen 

class Angriff:
    def __init__(self, name, schaden):
        self.name = name
        self.schaden = schaden

    def __repr__(self):
        return f"{self.name} ({self.schaden} Schaden)"

class Pokemon:
    def __init__(self, name, hp, angriffe):
        self.name = name
        self.max_hp = hp
        self.hp = hp
        self.angriffe = angriffe  # liste mit 4 angriffen

    def ist_besiegt(self):
        return self.hp <= 0

    def erhalte_schaden(self, schaden):
        self.hp -= schaden
        if self.hp < 0:
            self.hp = 0

    # zeigt status als string (danke KI)
    def get_status(self):
        balken_len = 20
        gefuellt = int(balken_len * (self.hp / self.max_hp))
        balken = "█" * gefuellt + "░" * (balken_len - gefuellt)
        return f"{self.name:12} [{balken}] {self.hp}/{self.max_hp} HP"

class GameState:
    def __init__(self, spieler, gegner):
        self.spieler_pkm = spieler
        self.gegner_pkm = gegner
        self.aktiver_spieler = "spieler"

# verfügbare angriffe
ANGRIFFE = [
    Angriff("Tackle", 40),
    Angriff("Ranke", 45),
    Angriff("Flammenwurf", 90),
    Angriff("Aqua Knarre", 65),
    Angriff("Donnerschock", 40),
    Angriff("Donnerwelle", 95),
    Angriff("Blattklinge", 70),
    Angriff("Rasierblatt", 55),
    Angriff("Glut", 40),
    Angriff("Surfer", 90),
    Angriff("Schlammwelle", 65),
    Angriff("Härtner", 30),
    Angriff("Knirscher", 55),
    Angriff("Eishieb", 75),
    Angriff("Psychokinese", 90),
    Angriff("Megahieb", 80),
]

# pokemon pool - jedes bekommt 4 zufaellige angriffe
# muss beim start aufgerufen werden damit die angriffe neu gemischt werden
def erstelle_pokemon_pool():
    pool = [
        Pokemon("Bisasam", 45, random.sample(ANGRIFFE, 4)),
        Pokemon("Glumanda", 39, random.sample(ANGRIFFE, 4)),
        Pokemon("Schiggy", 44, random.sample(ANGRIFFE, 4)),
        Pokemon("Pikachu", 35, random.sample(ANGRIFFE, 4)),
        Pokemon("Evoli", 55, random.sample(ANGRIFFE, 4)),
        Pokemon("Nebulak", 30, random.sample(ANGRIFFE, 4)),
        Pokemon("Mauzi", 40, random.sample(ANGRIFFE, 4)),
        Pokemon("Taubsi", 40, random.sample(ANGRIFFE, 4)),
    ]
    return pool

def zeige_status(state):
    print("─" * 44)
    print(f"  {state.spieler_pkm.get_status()}")
    print(f"  {state.gegner_pkm.get_status()}")
    print("─" * 44)

def spieler_zug(state):
    pkm = state.spieler_pkm
    ziel = state.gegner_pkm

    print("\nWelchen Angriff willst du benutzen?")
    for i in range(4):
        print(f"  [{i+1}] {pkm.angriffe[i]}")

    eingabe = input("\nDeine Wahl (1-4): ").strip()
    # input validierung
    while eingabe not in ["1", "2", "3", "4"]:
        eingabe = input("Bitte 1, 2, 3 oder 4 eingeben: ").strip()

    gewaehlter = pkm.angriffe[int(eingabe) - 1]
    ziel.erhalte_schaden(gewaehlter.schaden)
    print(f"\n> {pkm.name} benutzt {gewaehlter.name}!")
    print(f"  {ziel.name} verliert {gewaehlter.schaden} HP.")

def computer_zug(state):
    pkm = state.gegner_pkm
    ziel = state.spieler_pkm

    # computer wählt zufaellig
    angriff = pkm.angriffe[random.randint(0, 3)]
    ziel.erhalte_schaden(angriff.schaden)
    print(f"\n> Gegner {pkm.name} benutzt {angriff.name}!")
    print(f"  {ziel.name} verliert {angriff.schaden} HP.")

def main():
    print("_____________")
    print("KAMPF BEGINNT")
    print("_____________")

    pokemon_pool = erstelle_pokemon_pool()
    auswahl = random.sample(pokemon_pool, 2)
    spieler_pkm = auswahl[0]
    gegner_pkm = auswahl[1]

    print(f"\n  Dein Pokemon:   {spieler_pkm.name} ({spieler_pkm.hp} HP)")
    print(f"  Gegner Pokemon: {gegner_pkm.name} ({gegner_pkm.hp} HP)")
    print()

    state = GameState(spieler_pkm, gegner_pkm)

    while True:
        zeige_status(state)

        spieler_zug(state)

        if state.gegner_pkm.ist_besiegt():
            zeige_status(state)
            print(f"\n  {state.spieler_pkm.name} hat gewonnen! Glückwunsch :)")
            break

        computer_zug(state)

        if state.spieler_pkm.ist_besiegt():
            zeige_status(state)
            print(f"\n  {state.gegner_pkm.name} hat gewonnen. Schade :(")
            break

    print("\n" + "═" * 44 + "\n")

if __name__ == "__main__":
    main()