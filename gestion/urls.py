from django.urls import path
from . import views

urlpatterns = [
    path('', views.shop, name='shop'),
    path('reserve/<int:livre_id>/', views.reserver_livre, name='reserver_livre'),
    path('reservations/', views.mes_reservations, name='mes_reservations'),

    # 🔁 NEW
    path('retourner/<int:reservation_id>/', views.retourner_livre, name='retourner_livre'),
    path('dashboard/', views.dashboard, name='dashboard'),
]