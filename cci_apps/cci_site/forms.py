from django.contrib.auth import forms, get_user_model
from django import forms as django_forms
from ajax_select.fields import AutoCompleteSelectField
from cci_apps.cadastros.models import Lote


class LoteFilter(django_forms.ModelForm):
    cidades = AutoCompleteSelectField('cidades',
                                        label='Cidade',
                                        required=False,
                                        show_help_text=False)
    regioes = AutoCompleteSelectField('regioes',
                                        label='Região',
                                        required=False,
                                        show_help_text=False)
    loteamentos = AutoCompleteSelectField('loteamentos',
                                        label='Loteamento',
                                        required=False,
                                        show_help_text=False)
    class Meta:
        model = Lote
        fields = '__all__'