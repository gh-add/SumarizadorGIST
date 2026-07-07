from django.urls import path
from . import views


urlpatterns = [
    #CRUDS
    path("", views.add, name="secao_add"),  
    path("<int:pk>/", views.detalhe_secao, name="secao_detail"),
    path("list/", views.listar_secoes, name="secao_list"),
    path("del/<int:pk>/", views.delete, name="secao_delete"),
    path("conteudo_parcial/<int:pk>/", views.detalhe_secao_conteudo, name="detalhe_secao_conteudo"),
    #SSE
    path("status_stream/<int:pk>/", views.secao_status_stream, name="secao_status_stream"),
]
