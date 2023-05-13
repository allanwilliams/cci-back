from django.db import models
from django_currentuser.middleware import get_current_user
from django.contrib.auth.models import User
from django.utils import timezone

TIPO_TELEFONE = 'TELEFONE'
TIPO_EMAIL = 'EMAIL'

TIPOS_CONTATOS = (
    (TIPO_TELEFONE,TIPO_TELEFONE),
    (TIPO_EMAIL,TIPO_EMAIL),
)

STATUS_LOTE_ATIVO = "ATIVO"
STATUS_LOTE_VENDIDO = "VENDIDO"
STATUS_LOTE_RESERVADO = "RESERVADO"
STATUS_LOTE_DEVOLVIDO = "DEVOLVIDO"
STATUS_LOTE_NEGOCIANDO = "NEGOCIANDO"

STATUS_LOTE_CHOICE = (
    (STATUS_LOTE_ATIVO,STATUS_LOTE_ATIVO),
    (STATUS_LOTE_VENDIDO,STATUS_LOTE_VENDIDO),
    (STATUS_LOTE_RESERVADO,STATUS_LOTE_RESERVADO),
    (STATUS_LOTE_DEVOLVIDO,STATUS_LOTE_DEVOLVIDO),
    (STATUS_LOTE_NEGOCIANDO,STATUS_LOTE_NEGOCIANDO),
)

STATUS_VENDA_REALIZADA = "REALIZADA"
STATUS_VENDA_ENTRADA_PAGA = "ENTRADA PAGA"
STATUS_VENDA_CANCELADA = "CANCELADA"

STATUS_VENDA_CHOICE = (
    (STATUS_VENDA_REALIZADA,STATUS_VENDA_REALIZADA),
    (STATUS_VENDA_ENTRADA_PAGA,STATUS_VENDA_ENTRADA_PAGA),
    (STATUS_VENDA_CANCELADA,STATUS_VENDA_CANCELADA)
)

TIPO_DOCUMENTO_RG = "RG"
TIPO_DOCUMENTO_CPF = "CPF"
TIPO_DOCUMENTO_ENDERECO = "ENDEREÇO"
TIPO_DOCUMENTO_CASAMENTO = "CASAMENTO"

TIPOS_DOCUMENTOS_CHOICES = (
    (TIPO_DOCUMENTO_RG,TIPO_DOCUMENTO_RG),
    (TIPO_DOCUMENTO_CPF,TIPO_DOCUMENTO_CPF),
    (TIPO_DOCUMENTO_ENDERECO,TIPO_DOCUMENTO_ENDERECO),
    (TIPO_DOCUMENTO_CASAMENTO,TIPO_DOCUMENTO_CASAMENTO),
)
class BaseModel(models.Model):
    criado_em = models.DateTimeField(blank=True, null=True)
    criado_por = models.ForeignKey(User,
                                   on_delete=models.DO_NOTHING,
                                   related_name='%(class)s_criado_por',
                                   blank=True,
                                   null=True,
                                   default=get_current_user())
    modificado_em = models.DateTimeField(blank=True, null=True)
    modificado_por = models.ForeignKey(User,
                                       on_delete=models.DO_NOTHING,
                                       related_name='%(class)s_modificado_por',
                                       blank=True,
                                       null=True)

    class Meta:
        abstract = True

    def save(self,
             force_insert=False,
             force_update=False,
             using=None,
             update_fields=None):
        if get_current_user():
            if (not self.criado_por or not self.criado_em) and get_current_user() and get_current_user().id:
                self.criado_por = get_current_user()
                self.criado_em = timezone.now()
            elif get_current_user() and get_current_user().id:
                self.modificado_por = get_current_user()
                self.modificado_em = timezone.now()
        super(BaseModel, self).save(force_insert=False,
                                    force_update=False,
                                    using=None,
                                    update_fields=None)

class Cidade(BaseModel):
    nome = models.CharField(max_length=50,blank=True, null=True)
    def __str__(self):
        return self.nome

class Regiao(BaseModel):
    nome = models.CharField(max_length=50,blank=True, null=True)
    cidade = models.ForeignKey(Cidade,on_delete=models.DO_NOTHING,blank=True, null=True)
    
    def __str__(self):
        return self.nome
    
    class Meta:
        verbose_name_plural = 'Regiões'
        verbose_name = 'Região'

class Imobiliaria(BaseModel):
    nome = models.CharField(max_length=50)
    sobre = models.TextField()
    foto = models.ImageField(blank=True, null=True, upload_to='store/cadastros/imobiliaria-anexo/')

    def __str__(self):
        return self.nome

class Loteamento(BaseModel):
    nome = models.CharField(max_length=50)
    sobre = models.TextField()
    foto = models.ImageField(blank=True, null=True,upload_to='store/cadastros/loteamento-anexo/')
    imobiliaria = models.ForeignKey(Imobiliaria,blank=True, null=True,on_delete=models.DO_NOTHING)
    regiao = models.ForeignKey(Regiao,blank=True, null=True,on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.nome

class Quadra(BaseModel):
    identificacao = models.CharField(max_length=50,blank=True, null=True)
    loteamento = models.ForeignKey(Loteamento, on_delete=models.DO_NOTHING)

    def __str__(self):
        return f'{self.loteamento.nome} - {self.identificacao}'

class Lote(BaseModel):
    identificacao = models.CharField(max_length=50,blank=True, null=True)
    quadra = models.ForeignKey(Quadra, on_delete=models.DO_NOTHING,blank=True, null=True)
    status = models.CharField(choices=STATUS_LOTE_CHOICE,max_length=20, default=STATUS_LOTE_ATIVO)

    def __str__(self):
        return f'{self.quadra} - {self.identificacao}'
    
class ImagemLote(BaseModel):
    lote = models.ForeignKey(Lote, verbose_name="Imagem Lote", on_delete=models.DO_NOTHING)
    foto = models.ImageField(upload_to='store/cadastros/imagem-lote-anexo/')

class Cliente(BaseModel):
    nome = models.CharField(max_length=150)
    cpf = models.CharField(verbose_name="CPF", max_length=14,blank=True, null=True)
    rg = models.CharField(verbose_name="RG",max_length=40,blank=True, null=True)
    cep = models.CharField(verbose_name="CEP",max_length=8,blank=True, null=True)
    endereco = models.CharField(max_length=40,blank=True, null=True)
    numero = models.CharField(verbose_name="Número",max_length=6,blank=True, null=True)

    def __str__(self):
        return self.nome

class ContatoCliente(BaseModel):
    tipo = models.CharField(choices=TIPOS_CONTATOS,max_length=10)
    contato = models.CharField(max_length=200)
    is_whatsapp = models.BooleanField("Possui Whatsapp?",blank=True, null=True)
    cliente = models.ForeignKey(Cliente,on_delete=models.DO_NOTHING)

class DocumentoCliente(BaseModel):
    cliente = models.ForeignKey(Cliente, verbose_name="Documento Cliente", on_delete=models.DO_NOTHING)
    documento = models.FileField(upload_to="store/cadastros/imagem-lote-anexo/", max_length=100)
    tipo = models.CharField(max_length=50,blank=True, null=True, choices=TIPOS_DOCUMENTOS_CHOICES)

class Venda(BaseModel):
    lote = models.ForeignKey(Lote, on_delete=models.DO_NOTHING)
    cliente = models.ForeignKey(Cliente, on_delete=models.DO_NOTHING)
    valor_total = models.FloatField(blank=True, null=True)
    entrada = models.FloatField(blank=True, null=True)
    qtd_parcelas = models.IntegerField(blank=True, null=True)
    valor_parcela = models.FloatField(blank=True, null=True)
    status = models.CharField(choices=STATUS_VENDA_CHOICE,max_length=20, default=STATUS_VENDA_REALIZADA)

    def __str__(self):
        return f'{self.lote} - {self.cliente}'