import json
from Tirage.models import Equipe, Pays, Championnat, Chapeau 

def load_in_db():
    with open('teams.json', 'r') as f:
        data = json.load(f)

    for item in data:
        pays, _ = Pays.objects.get_or_create(nom=item.get('pays'))

        championnat, _ = Championnat.objects.get_or_create(nom=item.get('championnat'))

        chapeau, _ = Chapeau.objects.get_or_create(numero_de_chapeau=item.get('chapeau'))

        Equipe.objects.create(
            nom=item.get('nom'),
            quel_pays=pays,
            quel_championat=championnat,
            quel_chapeau=chapeau,
            logo=item.get('logo')
        )
