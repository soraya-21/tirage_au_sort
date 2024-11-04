from django.core.management.base import BaseCommand
from .load_teams import load_in_db

class Command(BaseCommand):
    help = "Charge le contenu du fichier contenant les entreprises"

    # def add_arguments(self, parser):
    #     parser.add_argument("filename", type=str, help="Le fichier à charger")
    #     parser.add_argument(
    #         "--number",
    #         "-n",
    #         type=int,
    #         default=1000,
    #         nargs="?",
    #         help="Lequel de lignes que la db doit enregistrer à la fois",
    #     )
    #     parser.add_argument(
    #         "--level",
    #         "-l",
    #         default="info",
    #         nargs="?",
    #         choices=LogLevel.logging_flags,
    #         help="Le niveau de log",
    #     )

    def handle(self, *args, **kwargs):
        # filename = kwargs["filename"]
        # number = kwargs["number"]
        # level = kwargs["level"]
        # self.set_log_level(level)
        load_in_db()
