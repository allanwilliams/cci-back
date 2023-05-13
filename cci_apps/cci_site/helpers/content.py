from cci_apps.cadastros.models import Cidade, Regiao

def default_context():
    cidades = Cidade.objects.all()
    regioes = Regiao.objects.all()
    
    return {
        'cidades': cidades,
        'regioes': regioes
    }