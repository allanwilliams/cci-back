from django.contrib import admin
from .models import Imobiliaria, Cliente, ImagemLote,Lote, ContatoCliente, Loteamento, Quadra, Venda, DocumentoCliente, Regiao, Cidade, \
    STATUS_LOTE_VENDIDO, STATUS_LOTE_RESERVADO,STATUS_LOTE_DEVOLVIDO, STATUS_VENDA_CANCELADA, STATUS_VENDA_REALIZADA, STATUS_VENDA_ENTRADA_PAGA

class ImagemLoteInline(admin.StackedInline):
    model = ImagemLote
    extra = 1
    fields = (
        'foto',
    )

class ContatoClienteInline(admin.StackedInline):
    model = ContatoCliente
    extra = 1

    fields = ('tipo','contato','is_whatsapp')
class DocumentoClienteInline(admin.StackedInline):
    model = DocumentoCliente
    extra = 1

    fields = ('tipo','cliente','documento')

@admin.register(Imobiliaria)
class ImobiliariaAdmin(admin.ModelAdmin):
    list_display = [
        'id','nome'
    ]
    fields = ('nome','sobre','foto')
    
    

@admin.register(Loteamento)
class LoteamentoAdmin(admin.ModelAdmin):
    list_display = [
        'id','nome'
    ]

    fields = ('nome','sobre','imobiliaria','foto','regiao')

@admin.register(Quadra)
class QuadraAdmin(admin.ModelAdmin):
    list_display = [
        'id','identificacao'
    ]

    fields =(
        'identificacao','loteamento'
    )

@admin.register(Lote)
class LoteAdmin(admin.ModelAdmin):
    list_display = [
        'identificacao','quadra','status'
    ]
    
    fields = ('identificacao','quadra','status')

    inlines = [
        ImagemLoteInline,
    ]

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = [
        'id','nome'
    ]

    list_filter = ('nome',)

    fields = ('nome','cpf','cep','endereco','numero')

    inlines = [
        ContatoClienteInline,
        DocumentoClienteInline
    ]

@admin.register(Venda)
class VendaAdmin(admin.ModelAdmin):
    list_display = [
        'id','lote','cliente','status'
    ]

    fields = ('cliente','lote','entrada','valor_total','qtd_parcelas','valor_parcela','status')

    def save_model(self, request, obj, form, change):
        obj.save()
        status_venda = request.POST.get('status')
        if request.POST.get("lote"):
            lote = Lote.objects.get(pk=request.POST.get("lote"))
            if lote:
                if status_venda == STATUS_VENDA_ENTRADA_PAGA:
                    lote.status = STATUS_LOTE_VENDIDO
                    lote.save()
                elif status_venda == STATUS_VENDA_REALIZADA:
                    lote.status = STATUS_LOTE_RESERVADO
                    lote.save()
                elif status_venda == STATUS_VENDA_CANCELADA:
                    lote.status = STATUS_LOTE_DEVOLVIDO
                    lote.save()

    def has_delete_permission(self, request, obj = None):
        return False

@admin.register(Regiao)
class RegiaoAdmin(admin.ModelAdmin):
    list_display = [
        'nome','cidade'
    ]

    fields = ('nome','cidade')

@admin.register(Cidade)
class CidadeAdmin(admin.ModelAdmin):
    list_display = [
        'nome',
    ]

    fields = ('nome',)