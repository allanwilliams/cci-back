from cci_apps.cadastros.models import Cidade, Regiao, Loteamento

def default_context():
    cidades = Cidade.objects.all()
    regioes = Regiao.objects.all()
    loteamentos = Loteamento.objects.all()
    
    return {
        'cidades': cidades,
        'regioes': regioes,
        'loteamentos': loteamentos,
    }