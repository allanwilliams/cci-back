from django.shortcuts import render
from django.http import HttpResponse
from .helpers import content
from cci_apps.cadastros.models import Lote
from cci_apps.cci_site.forms import LoteFilter

def index(request): #new
    default_context = content.default_context()
    context = {
        'default_context': default_context,
        'fitro_lote': LoteFilter
    }
    return render(template_name='home_v2.html',request=request, context=context)

def buscar_imovel(request):
    cidade = request.POST.get('cidade')
    regiao = request.POST.get('regiao')
    loteamento = request.POST.get('loteamento')
    faixa = request.POST.get('faixa')
    lotes = Lote.objects.all()
    if cidade != '0':
        lotes = lotes.filter(quadra__loteamento__regiao__cidade=cidade)
    default_context = content.default_context()
    context = {
        'default_context': default_context,
        'lotes':lotes
    }
    return render(template_name='buscar_imovel.html',request=request, context=context)
