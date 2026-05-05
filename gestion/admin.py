from django.contrib import admin
from .models import Utilisateur, Livre, Reservation

admin.site.register(Utilisateur)
admin.site.register(Livre)
admin.site.register(Reservation)