import json
import random

with open("data/teams.json", "r", encoding="utf-8") as f:
    equipes = json.load(f)

chapeau1 = [equipe for equipe in equipes if equipe["chapeau"] == 1]
chapeau2 = [equipe for equipe in equipes if equipe["chapeau"] == 2]
chapeau3 = [equipe for equipe in equipes if equipe["chapeau"] == 3]
chapeau4 = [equipe for equipe in equipes if equipe["chapeau"] == 4]

def tirage_pour_equipe(equipe, chapeau1, chapeau2, chapeau3, chapeau4):
    """Tirage au sort pour une equipe"""
    tirage = {}
    chapeaux = [chapeau1, chapeau2, chapeau3, chapeau4]
    for i, chapeau in enumerate(chapeaux, start=1):
        # Exclure l'équipe elle-même du chapeau
        chapeau_sans_equipe = [adversaire for adversaire in chapeau if adversaire["nom"] != equipe["nom"]]
        adversaires = random.sample(chapeau_sans_equipe, 2)
        tirage[f"pot_{i}"] = {
            "home": adversaires[0],
            "away": adversaires[1]
        }
    return tirage

# Effectuer le tirage pour toutes les équipes
resultats = {}
for equipe in equipes:
    equipe_nom = equipe["nom"]
    tirage = tirage_pour_equipe(equipe, chapeau1, chapeau2, chapeau3, chapeau4)
    resultats[equipe_nom] = {
        "nom": equipe_nom,
        "pays": equipe["pays"],
        "championnat": equipe["championnat"],
        "chapeau": equipe["chapeau"],
        "logo": equipe["logo"],
        **tirage
    }

print(json.dumps(resultats, indent=4, ensure_ascii=False))
