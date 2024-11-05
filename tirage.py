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
    championnat_counts = {}

    for i, chapeau in enumerate(chapeaux, start=1):
        # Exclure l'équipe elle-même et les équipes du même championnat
        chapeau_sans_equipe_actuelle = [
            adversaire for adversaire in chapeau
            if adversaire["nom"] != equipe["nom"] and adversaire["championnat"] != equipe["championnat"]
        ]

        # Sélectionner deux adversaires en respectant les contraintes de championnat
        adversaires_selectionnes = []
        while len(adversaires_selectionnes) < 2:
            adversaire = random.choice(chapeau_sans_equipe_actuelle)
            
            championnat = adversaire["championnat"]
            if championnat_counts.get(championnat, 0) < 2:
                adversaires_selectionnes.append(adversaire)
                championnat_counts[championnat] = championnat_counts.get(championnat, 0) + 1
                chapeau_sans_equipe_actuelle.remove(adversaire)
        
        tirage[f"pot_{i}"] = {
            "home": adversaires_selectionnes[0],
            "away": adversaires_selectionnes[1]
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
        **tirage,
    }

print(json.dumps(resultats, indent=4, ensure_ascii=False))
