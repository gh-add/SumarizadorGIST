from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponseBadRequest
from django.template.loader import render_to_string
from django.http import  HttpResponseRedirect, HttpResponse
from .models import Secao as Secao
from .forms import SecaoForm

# Create your views here.
# view para adicionar uma nova seção de resumo Gist Summ
def add(request):
    if request.method == 'POST':
        form = SecaoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return render(request, "secao/detail.html", {'secao': form.instance})
    else:
        form = SecaoForm()
        return render(request, "secao/add.html", {'form': form})

# ajax view para listar todas as seções de resumo Gist Summ
def listar_secoes(request):
    print("Listando seções...")
    secoes = Secao.objects.all().order_by('-id')
    html = render_to_string("secao/partials/list.html", {'secoes': secoes}, request=request)
    return HttpResponse(html)

# view para detalhar uma seção de resumo Gist Summ
def detalhe_secao(request, pk):
    secao = get_object_or_404(Secao, pk=pk)
    return render(request, "secao/detail.html", {'secao': secao})

# view para deletar uma seção de resumo Gist Summ
def delete(request, pk):
    get_object_or_404(Secao, pk=pk).delete()
    return HttpResponse(status=204)

