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

    def save(self, *args, **kwargs):
        # 🔥 BUSINESS LOGIC

        # If returned → update status + book availability
        if self.date_retour:
            self.statut = 'retourne'
            self.livre.disponible = True
            self.livre.save()

        # If overdue
        elif self.date_limite < date.today():
            self.statut = 'en_retard'

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.livre.titre} - {self.utilisateur.nom}"