from rest_framework import viewsets
from Tirage.models import *

# Create your views here.
class TicketViewSet(viewsets.ModelViewSet):
    queryset = tickets.objects.all()

