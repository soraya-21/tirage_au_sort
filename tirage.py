import json
import random

with open("data/teams copy.json", "r", encoding="utf-8") as f:
    equipes = json.load(f)
equipes_dict = {equipe["nom"]: equipe for equipe in equipes}

chapeau1 = [equipe for equipe in equipes if equipe["chapeau"] == 1]
# chapeau2 = [equipe for equipe in equipes if equipe["chapeau"] == 2]
# chapeau3 = [equipe for equipe in equipes if equipe["chapeau"] == 3]
# chapeau4 = [equipe for equipe in equipes if equipe["chapeau"] == 4]

chapeaux = [chapeau1]#, chapeau2, chapeau3, chapeau4]

# Suivi des adversaires tirés
tirage_adversaires = {
    equipe["nom"]: {i: {"home": None, "away": None} for i in range(1, 5)}
    for equipe in equipes
}
tirage = {}
championship_counts = {}

def check_tirage_adversaires_deja_tires(i):
    """Verifier les adversaires deja attribues"""
    adversaire_home = None
    adversaire_away = None

    for equipe_nom, tirage_info in tirage_adversaires.items():
            pot_info = tirage_info.get(i)
            
            if pot_info:
                if equipe["nom"] == pot_info["away"]:
                    # Si l'équipe actuelle est marquée comme "away" pour une autre équipe
                    adversaire_home = equipe_nom
                    
                if equipe["nom"] == pot_info["home"]:
                    # Si l'équipe actuelle est marquée comme "home" pour une autre équipe
                    adversaire_away = equipe_nom
    return adversaire_home, adversaire_away


def tirage_pour_equipe(equipe):
    """Effectuer le tirage au sort pour une équipe"""
    
    for i, chapeau in enumerate(chapeaux, start=1):
        
        adversaire_home, adversaire_away = check_tirage_adversaires_deja_tires(i)        

        # # Filtrer les équipes disponibles dans le chapeau
        chapeau_sans_equipe_actuelle = [
            adversaire for adversaire in chapeau
            if adversaire["nom"] != equipe["nom"] and
            adversaire["championnat"] != equipe["championnat"]
            and championship_counts.get(adversaire["championnat"], 0) <= 2
        ]
        
        if not adversaire_home:
            adversaire_home = random.choice(chapeau_sans_equipe_actuelle)
            while tirage_adversaires[equipe["nom"]][i]["home"] != None or tirage_adversaires[adversaire_home["nom"]][equipe["chapeau"]]["away"] != None:
                adversaire_home = random.choice(chapeau_sans_equipe_actuelle)
            
            tirage_adversaires[equipe["nom"]][i]["home"] = adversaire_home["nom"]
            tirage_adversaires[adversaire_home["nom"]][equipe["chapeau"]]["away"] = equipe["nom"]
            chapeau_sans_equipe_actuelle.remove(adversaire_home)
            adversaire_home = adversaire_home["nom"]


        if not adversaire_away:
            adversaire_away = random.choice(chapeau_sans_equipe_actuelle)["nom"]
            while tirage_adversaires[equipe["nom"]][i]["away"] != None or tirage_adversaires[adversaire_away][equipe["chapeau"]]["home"] != None:
                adversaire_away = random.choice(chapeau_sans_equipe_actuelle)["nom"]
            tirage_adversaires[adversaire_away][equipe["chapeau"]]["home"] = equipe["nom"]
            tirage_adversaires[equipe["nom"]][i]["away"] = adversaire_away

        championnat_home = equipes_dict[adversaire_home]["championnat"]
        championship_counts[championnat_home] = championship_counts.get(championnat_home, 0) + 1
        championnat_away = equipes_dict[adversaire_away]["championnat"]
        championship_counts[championnat_away] = championship_counts.get(championnat_away, 0) + 1
        tirage[i] = {
            "home": adversaire_home,
            "away": adversaire_away
            }
    return tirage
    
# Effectuer le tirage pour toutes les équipes
resultats = {}
equipes_deja_tirees_au_sort = []
k = 0
for equipe in equipes:
    equipe_nom = equipe["nom"]
    tirage = tirage_pour_equipe(equipe)
    
    resultats[equipe_nom] = {
        "nom": equipe_nom,
        "pays": equipe["pays"],
        "championnat": equipe["championnat"],
        "chapeau": equipe["chapeau"],
        "logo": equipe["logo"],
        **tirage,
    }
    k +=1
    print(f"tirage au sort effectué pour l'equipe {equipe_nom}, numero {k}")

print(json.dumps(resultats, indent=4, ensure_ascii=False))
