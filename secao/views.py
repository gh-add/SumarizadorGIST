from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponseBadRequest
from django.template.loader import render_to_string
from django.http import  HttpResponseRedirect
from .models import Secao as Secao
from .forms import SecaoForm

# Create your views here.
def home(request):
    secoes = Secao.objects.all().order_by('-id')
    form = SecaoForm()
    context = {
        'secoes': secoes,
        'form': form,
    }
    return render(request, "secao/index.html", context)

def add(request):
    if request.method == 'POST':
        form = SecaoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')  
        else:
            return render(request, "secao/_add.html", {'form': form})  

    else:
        form = SecaoForm()
        html = render_to_string("secao/_add.html", {'form': form}, request=request)
        return JsonResponse({'success': True, 'html': html})


def listar_secoes(request):
    secoes = Secao.objects.all().order_by('-id')
    html = render_to_string("_nav.html", {'secoes': secoes}, request=request)
    return JsonResponse({'html': html})


def detalhe_secao(request, pk):
    if not request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return HttpResponseBadRequest("Requisição inválida")
    secao = get_object_or_404(Secao, pk=pk)
    html = render_to_string("secao/_detail.html", {'secao': secao}, request=request)
    return JsonResponse({'html': html})


def delete(request, pk):
    Secao.objects.get(pk=pk).delete()
    return redirect('home')

