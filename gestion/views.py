from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from datetime import date, timedelta

from .models import Livre, Reservation, Utilisateur


# 📚 SHOP
def shop(request):
    livres = Livre.objects.all()
    return render(request, 'shop.html', {'livres': livres})


# 🔥 RESERVATION FUNCTION (MISSING BEFORE)
@login_required
def reserver_livre(request, livre_id):
    livre = get_object_or_404(Livre, id=livre_id)

    if not livre.disponible:
        return redirect('shop')

    utilisateur, created = Utilisateur.objects.get_or_create(
        user=request.user,
        defaults={
            "nom": request.user.username,
            "email": request.user.email,
            "is_student": True
        }
    )

    date_limite = date.today() + timedelta(days=7)

    Reservation.objects.create(
        livre=livre,
        utilisateur=utilisateur,
        date_limite=date_limite,
        statut='reserve'
    )

    livre.disponible = False
    livre.save()

    return redirect('shop')

@login_required
def mes_reservations(request):
    utilisateur = Utilisateur.objects.get(user=request.user)
    reservations = Reservation.objects.filter(utilisateur=utilisateur)

    return render(request, 'reservations.html', {
        'reservations': reservations
    })



@login_required
def retourner_livre(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id)

    # only owner can return
    if reservation.utilisateur.user != request.user:
        return redirect('mes_reservations')

    reservation.date_retour = date.today()
    reservation.statut = 'retourne'
    reservation.save()

    # make book available again
    reservation.livre.disponible = True
    reservation.livre.save()

    return redirect('mes_reservations')



from django.utils import timezone

@login_required
def dashboard(request):
    # only admin/librarian should access (basic check)
    if not request.user.is_staff:
        return redirect('shop')

    total_books = Livre.objects.count()
    total_reservations = Reservation.objects.count()

    active_reservations = Reservation.objects.filter(statut='reserve').count()

    overdue_reservations = Reservation.objects.filter(
        statut='en_retard'
    )

    reservations = Reservation.objects.all().order_by('-date_reservation')

    return render(request, 'dashboard.html', {
        'total_books': total_books,
        'total_reservations': total_reservations,
        'active_reservations': active_reservations,
        'overdue_reservations': overdue_reservations,
        'reservations': reservations,
    })