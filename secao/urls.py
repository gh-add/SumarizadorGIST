from django.urls import path
from . import views


urlpatterns = [
    path("", views.add, name="secao_add"),  
    path("<int:pk>/", views.detalhe_secao, name="secao_detail"),
    path("list/", views.listar_secoes, name="secao_list"),
    path("del/<int:pk>/", views.delete, name="secao_delete"),
]
