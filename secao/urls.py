from django.urls import path
from . import views


urlpatterns = [
    path("", views.home, name="home"),
    path("add/", views.add, name="add"),  
    path("<int:pk>/", views.detalhe_secao, name="detalhe_secao"),
    path("listar_secoes/", views.listar_secoes, name="listar_secoes"),  # ✅ Corrigido
    path("del/<int:pk>/", views.delete, name="delete"),
]
