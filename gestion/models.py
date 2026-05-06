from django.db import models
from django.contrib.auth.models import User
from datetime import date

# 👤 Utilisateur (Student linked to Django User)
class Utilisateur(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nom = models.CharField(max_length=100)
    email = models.EmailField()
    is_student = models.BooleanField(default=True)

    def __str__(self):
        return self.nom


# 📚 Livre (Book)
class Livre(models.Model):
    titre = models.CharField(max_length=200)
    auteur = models.CharField(max_length=100)
    categorie = models.CharField(max_length=100)
    prix = models.FloatField()
    resume = models.TextField()
    image = models.ImageField(upload_to='livres/', null=True, blank=True)
    disponible = models.BooleanField(default=True)

    def __str__(self):
        return self.titre


# 📦 Reservation
from datetime import date

class Reservation(models.Model):
    STATUT_CHOICES = [
        ('reserve', 'Réservé'),
        ('recupere', 'Récupéré'),
        ('retourne', 'Retourné'),
        ('en_retard', 'En retard'),
    ]

    livre = models.ForeignKey(Livre, on_delete=models.CASCADE)
    utilisateur = models.ForeignKey(Utilisateur, on_delete=models.CASCADE)

    date_reservation = models.DateField(auto_now_add=True)
    date_limite = models.DateField()
    date_retour = models.DateField(null=True, blank=True)

    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='reserve')

    # 🔥 AUTO STATUS (REAL-TIME)
    @property
    def statut_auto(self):
        if self.date_retour:
            return 'retourne'
        elif self.date_limite < date.today():
            return 'en_retard'
        return self.statut

    def __str__(self):
        return f"{self.livre.titre} - {self.utilisateur.nom}"