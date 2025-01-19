import json
import random

class Equipe:
    equipes = {}
    equipes_dict = {}
    def get_teams(self):
        print("heh")
        with open("data/teams.json", "r", encoding="utf-8") as f:
            self.equipes = json.load(f)
        self.equipes_dict = {equipe["nom"]: equipe for equipe in self.equipes}

        self.chapeau1 = [equipe for equipe in self.equipes if equipe["chapeau"] == 1]
        self.chapeau2 = [equipe for equipe in self.equipes if equipe["chapeau"] == 2]
        self.chapeau3 = [equipe for equipe in self.equipes if equipe["chapeau"] == 3]
        self.chapeau4 = [equipe for equipe in self.equipes if equipe["chapeau"] == 4]

        self.chapeaux = [self.chapeau1, self.chapeau2, self.chapeau3, self.chapeau4]

class Tirage:
    tirage = {}
    
    def initialize_opponents(self, equipes):
        # Suivi des adversaires tirés
        self.tirage_adversaires = {
            equipe["nom"]: {f"pot_{i}": {"home": None, "away": None} for i in range(1, 5)}
            for equipe in equipes
        }

    def check_tirage_adversaires_deja_tires(self, i, equipe, tirage_adversaires):
        """Verifier les adversaires deja attribues"""
        adversaire_home = None
        adversaire_away = None

        for equipe_nom, tirage_info in tirage_adversaires.items():
                pot_info = tirage_info.get(f"pot_{i}")
                
                if pot_info:
                    if equipe["nom"] == pot_info["away"]:
                        # Si l'équipe actuelle est marquée comme "away" pour une autre équipe
                        adversaire_home = equipe_nom
                        
                    if equipe["nom"] == pot_info["home"]:
                        # Si l'équipe actuelle est marquée comme "home" pour une autre équipe
                        adversaire_away = equipe_nom
        return adversaire_home, adversaire_away

    def remove_busy_teams(self, i, chapeau_sans_equipe_actuelle, tirage_adversaires):
        equipes_a_supprimer = []
        # Parcours des équipes dans tirage_adversaires
        for equipe_nom, team in tirage_adversaires.items():
            pot_info = team.get(f"pot_{i}")
            if pot_info["away"] is not None and pot_info["home"] is not None:
                # Recherche dans chapeau_sans_equipe_actuelle pour marquer les équipes à supprimer
                for adversaire in chapeau_sans_equipe_actuelle:
                    if equipe_nom == adversaire["nom"]:
                        equipes_a_supprimer.append(adversaire)

        # Suppression des équipes marquées
        for equip in equipes_a_supprimer:
            chapeau_sans_equipe_actuelle.remove(equip)

        return chapeau_sans_equipe_actuelle


    def tirage_pour_equipe(self, equipe, chapeaux, equipes_dict, tirage_adversaires, tirage):
        """Effectuer le tirage au sort pour une équipe"""
        avoid_adversaires = []
        championship_counts = {}
        for i, chapeau in enumerate(chapeaux, start=1):
            adversaire_home, adversaire_away = self.check_tirage_adversaires_deja_tires(i, equipe, tirage_adversaires)

            # # Filtrer les équipes disponibles dans le chapeau
            chapeau_sans_equipe_actuelle = [
                adversaire for adversaire in chapeau
                if adversaire["nom"] != equipe["nom"] and
                adversaire["championnat"] != equipe["championnat"]
                and championship_counts.get(adversaire["championnat"], 0) < 2
                # and adversaire not in avoid_adversaires
            ]
            # chapeau_sans_equipe_actuelle = remove_busy_teams(i, chapeau_sans_equipe_actuelle, tirage_adversaires)
            # print(championship_counts)
            if adversaire_home == None:
                adversaire_home = random.choice(chapeau_sans_equipe_actuelle)["nom"]
                if tirage_adversaires[equipe["nom"]][f"pot_{i}"]["home"] == None and tirage_adversaires[adversaire_home][f"pot_{equipe['chapeau']}"]["away"] == None:
                    if tirage_adversaires[equipe["nom"]][f"pot_{i}"]["away"] == adversaire_home:
                        k = 0
                        while tirage_adversaires[equipe["nom"]][f"pot_{i}"]["away"] == adversaire_home:
                            adversaire_home = random.choice(chapeau_sans_equipe_actuelle)["nom"]
                            k += 1
                            print(f"{k}e essai on tirage en boucle, finding adversaire home pour {equipe['nom']}")
                    if tirage_adversaires[equipe["nom"]][f"pot_{i}"]["away"] != adversaire_home:
                        
                        tirage_adversaires[equipe["nom"]][f"pot_{i}"]["home"] = adversaire_home
                        tirage_adversaires[adversaire_home][f"pot_{equipe['chapeau']}"]["away"] = equipe["nom"]
                # else:
                #     tirer()
                #     return
            
            chapeau_sans_equipe_actuelle = [
                adversaire for adversaire in chapeau_sans_equipe_actuelle
                if adversaire["nom"] != adversaire_home
                #and adversaire not in avoided_adversaires
            ]

            if adversaire_away == None:
                adversaire_away = random.choice(chapeau_sans_equipe_actuelle)["nom"]
                if tirage_adversaires[equipe["nom"]][f"pot_{i}"]["away"] == None and tirage_adversaires[adversaire_away][f"pot_{equipe['chapeau']}"]["home"] == None:
                    if tirage_adversaires[equipe["nom"]][f"pot_{i}"]["home"] == adversaire_away:
                        k = 0
                        while tirage_adversaires[equipe["nom"]][f"pot_{i}"]["home"] == adversaire_away:
                            adversaire_away = random.choice(chapeau_sans_equipe_actuelle)["nom"]
                            k += 1
                            print(f"{k}e essai on tirage en boucle, finding adversaire away pour {equipe['nom']}")
                    if tirage_adversaires[equipe["nom"]][f"pot_{i}"]["home"] != adversaire_away:
                        tirage_adversaires[equipe["nom"]][f"pot_{i}"]["away"] = adversaire_away
                        tirage_adversaires[adversaire_away][f"pot_{equipe['chapeau']}"]["home"] = equipe["nom"]
                # else:
                #     tirer()
                #     return

            championnat_home = equipes_dict[adversaire_home]["championnat"]
            championship_counts[championnat_home] = championship_counts.get(championnat_home, 0) + 1
            championnat_away = equipes_dict[adversaire_away]["championnat"]
            championship_counts[championnat_away] = championship_counts.get(championnat_away, 0) + 1
            tirage[f"pot_{i}"] = {
                "home": adversaire_home,
                "away": adversaire_away
                }
        avoid_adversaires.append(equipe)
        # print(tirage_adversaires)
        return tirage
        
    # Effectuer le tirage pour toutes les équipes
    def tirer(self, equipes, chapeaux, equipes_dict, tirage_adversaires, tirage):
        # team_teams = Equipe()
        resultats = {}
        equipes_deja_tirees_au_sort = []
        k = 0
        for equipe in equipes:
            equipe_nom = equipe["nom"]
            tirage = self.tirage_pour_equipe(equipe, chapeaux, equipes_dict, tirage_adversaires, tirage)

            resultats[equipe_nom] = {
                "nom": equipe_nom,
                "pays": equipe["pays"],
                "championnat": equipe["championnat"],
                "chapeau": equipe["chapeau"],
                "logo": equipe["logo"],
                **{
                    f"pot_{i}": {
                        "home": equipes_dict[tirage[f"pot_{i}"]["home"]] if tirage[f"pot_{i}"]["home"] else None,
                        "away": equipes_dict[tirage[f"pot_{i}"]["away"]] if tirage[f"pot_{i}"]["away"] else None,
                    }
                    for i in range(1, 5)
                },
            }
            k +=1
            print(f"tirage au sort effectué pour l'equipe {equipe_nom}, numero {k}")

        with open('tirage.json', 'w') as fichier:
            json.dump(resultats, fichier, indent=4)

teams = Equipe()
tirage = Tirage()
teams.get_teams()
tirage.initialize_opponents(teams.equipes)
tirage.tirer(teams.equipes, teams.chapeaux, teams.equipes_dict, tirage.tirage_adversaires, tirage.tirage)