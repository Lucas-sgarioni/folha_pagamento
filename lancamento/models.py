from django.db import models
from cadastro.models import Cadastro
from decimal import Decimal
from datetime import datetime, time

class LancamentoHora(models.Model):
    nome = models.ForeignKey(Cadastro, on_delete=models.CASCADE, verbose_name='Funcionário')
    data = models.DateField(verbose_name='Data')
    entrada_manha = models.TimeField(verbose_name='Entrada manhã', null=True, blank=True)
    saida_manha = models.TimeField(verbose_name='Saída manhã', null=True, blank=True)
    entrada_tarde = models.TimeField(verbose_name='Entrada tarde', null=True, blank=True)
    saida_tarde = models.TimeField(verbose_name='Saída tarde', null=True, blank=True)

    horas_extras = models.DecimalField("Horas extras (em horas)", max_digits=5, decimal_places=2, default=0)
    horas_atraso = models.DecimalField("Horas de atraso (em horas)", max_digits=5, decimal_places=2, default=0)

    class Meta:
        unique_together = ('nome', 'data')
        verbose_name = 'Lançamento de Hora'
        verbose_name_plural = 'Lançamentos de Horas'
        ordering = ['data']

    # Jornada padrão
    JORNADA_ENTRADA_MANHA = time(8, 0)
    JORNADA_SAIDA_MANHA = time(12, 0)
    JORNADA_ENTRADA_TARDE = time(13, 0)
    JORNADA_SAIDA_TARDE = time(17, 0)

    def _comparar_horario(self, real, previsto):
        """Retorna (atraso_em_minutos, extra_em_minutos)"""
        if real is None:
            return 0, 0
        dt_real = datetime.combine(self.data, real)
        dt_previsto = datetime.combine(self.data, previsto)
        diferenca = (dt_real - dt_previsto).total_seconds() / 60

        if diferenca > 0:
            return diferenca, 0   # Atraso
        elif diferenca < 0:
            return 0, abs(diferenca)  # Hora extra
        return 0, 0  # Pontual

    def calcular_horas(self):
        total_atraso = 0
        total_extra = 0

        # Comparações individuais
        comparacoes = [
            (self.entrada_manha, self.JORNADA_ENTRADA_MANHA),
            (self.saida_manha, self.JORNADA_SAIDA_MANHA),
            (self.entrada_tarde, self.JORNADA_ENTRADA_TARDE),
            (self.saida_tarde, self.JORNADA_SAIDA_TARDE),
        ]

        for real, previsto in comparacoes:
            atraso, extra = self._comparar_horario(real, previsto)
            total_atraso += atraso
            total_extra += extra

        return round(total_extra / 60, 2), round(total_atraso / 60, 2)

    def save(self, *args, **kwargs):
        extra, atraso = self.calcular_horas()
        self.horas_extras = Decimal(extra)
        self.horas_atraso = Decimal(atraso)
        super().save(*args, **kwargs)