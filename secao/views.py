import json
import time
from django.shortcuts import render, redirect,get_object_or_404
from django.http import JsonResponse
from django.http import StreamingHttpResponse   
from django.template.loader import render_to_string
from django.http import   HttpResponse
from .models import Secao as Secao
from .forms import SecaoForm


# CRUD views para a seção de resumo Gist Summ
# view para adicionar uma nova seção de resumo Gist Summ
def add(request):
    if request.method == 'POST':
        form = SecaoForm(request.POST, request.FILES)
        print(form.errors)
        if form.is_valid():
            form.save()
            return redirect('secao_detail', pk=form.instance.pk)
        return render(request, "secao/add.html", {'form': form})
    else:
        form = SecaoForm()
        return render(request, "secao/add.html", {'form': form})

# ajax view para listar todas as seções de resumo Gist Summ
def listar_secoes(request):
    secoes = Secao.objects.all().order_by('-id')
    html = render_to_string("secao/partials/list.html", {'secoes': secoes}, request=request)
    return HttpResponse(html)

# view para detalhar uma seção de resumo Gist Summ
def detalhe_secao(request, pk):
    secao = get_object_or_404(Secao, pk=pk)
    return render(request, "secao/detail.html", {'secao': secao})

# ajax view para retornar o conteúdo de uma seção de resumo Gist Summ
def detalhe_secao_conteudo(request, pk):
    secao = get_object_or_404(Secao, pk=pk)
    return render(request, 'secao/partials/resumo.html', {'secao': secao})

# ajax view para deletar uma seção de resumo Gist Summ
def delete(request, pk):
    get_object_or_404(Secao, pk=pk).delete()
    return JsonResponse({'success': True})

#SSE 
def secao_status_stream(request, pk):
    def event_stream():
        ultimo_status = None
        tentativas = 0
        max_tentativas = 60

        while tentativas < max_tentativas:
            try:
                secao = Secao.objects.get(pk=pk)
            except Secao.DoesNotExist:
                break

            if secao.status != ultimo_status:
                data = {
                    'status': secao.status,
                    'resumo': secao.resumo,
                    'imagem_nuvem': secao.imagem_nuvem,
                }
                yield f"data: {json.dumps(data)}\n\n"
                ultimo_status = secao.status

            if secao.status in ('concluido', 'erro'):
                break

            time.sleep(2)
            tentativas += 1

    response = StreamingHttpResponse(event_stream(), content_type="text/event-stream")
    response['Cache-Control'] = 'no-cache'
    response['X-Accel-Buffering'] = 'no'
    return response

