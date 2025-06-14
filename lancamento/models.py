from django.db import models
from cadastro.models import Cadastro

class LancamentoHora(models.Model):
    nome = models.ForeignKey(Cadastro, on_delete=models.CASCADE, verbose_name='Funcionário')
    data = models.DateField(verbose_name='Data')
    entrada_manha = models.TimeField(verbose_name='Entrada manhã', null=True, blank=True)
    saida_manha = models.TimeField(verbose_name='Saída manhã', null=True, blank=True)
    entrada_tarde = models.TimeField(verbose_name='Entrada tarde', null=True, blank=True)
    saida_tarde = models.TimeField(verbose_name='Saída tarde', null=True, blank=True)

    class Meta:
        unique_together = ('nome', 'data')