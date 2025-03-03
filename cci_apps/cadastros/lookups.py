from ajax_select import register, LookupChannel
from cci_apps.cadastros.models import Cidade, Regiao, Loteamento

@register('cidades')
class CidadesLookup(LookupChannel): # pragma: no cover
    model = Cidade

    def get_query(self, q, request):
        return self.model.objects.filter(nome__icontains=q).order_by('nome')[:20]

    def format_item_display(self, item):
        return "{} - {}".format(item.nome.upper())    
    
    def format_match(self, item):
        return "{} - {}".format(item.nome.upper())

@register('regioes')
class RegioesLookup(LookupChannel): # pragma: no cover
    model = Regiao

    def get_query(self, q, request):
        return self.model.objects.filter(nome__icontains=q).order_by('nome')[:20]

    def format_item_display(self, item):
        return "{} - {}".format(item.nome.upper())    
    
    def format_match(self, item):
        return "{} - {}".format(item.nome.upper())

@register('loteamentos')
class LoteamentosLookup(LookupChannel): # pragma: no cover
    model = Loteamento

    def get_query(self, q, request):
        return self.model.objects.filter(nome__icontains=q).order_by('nome')[:20]

    def format_item_display(self, item):
        return "{} - {}".format(item.nome.upper())    
    
    def format_match(self, item):
        return "{} - {}".format(item.nome.upper())