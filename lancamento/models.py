from django.db import models
from cadastro.models import Cadastro
from decimal import Decimal
from datetime import datetime, time, timedelta

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
    JORNADA_ENTRADA_MANHA = time(7, 30)
    JORNADA_SAIDA_MANHA = time(11, 45)
    JORNADA_ENTRADA_TARDE = time(13, 22)
    JORNADA_SAIDA_TARDE = time(17, 55)

    def _calcular_turno(self, entrada_real, saida_real, entrada_prevista, saida_prevista):
        """
        Calcula atrasos e extras para um turno completo (manhã ou tarde),
        incluindo casos que ultrapassam a meia-noite.
        Retorna (atraso_em_minutos, extra_em_minutos)
        """
        # Finais de semana: ignora cálculos
        if self.data.weekday() >= 5:
            return 0, 0

        # Se ambos horários estiverem ausentes
        if entrada_real is None and saida_real is None:
            return 0, 0

        # Se algum horário estiver ausente, considera o pior cenário
        if entrada_real is None or saida_real is None:
            periodo_previsto = (datetime.combine(self.data, saida_prevista) - 
                            datetime.combine(self.data, entrada_prevista)).total_seconds() / 60
            return periodo_previsto, 0  # Considera todo o período como atraso

        # Combina com a data correta (ajustando para o dia seguinte se necessário)
        entrada_dt = datetime.combine(self.data, entrada_real)
        saida_dt = datetime.combine(self.data, saida_real)
        
        # Se a saída for menor que a entrada (ultrapassou meia-noite)
        if saida_real < entrada_real:
            saida_dt += timedelta(days=1)

        entrada_prevista_dt = datetime.combine(self.data, entrada_prevista)
        saida_prevista_dt = datetime.combine(self.data, saida_prevista)

        # Calcula diferenças
        entrada_diff = (entrada_dt - entrada_prevista_dt).total_seconds() / 60
        saida_diff = (saida_dt - saida_prevista_dt).total_seconds() / 60

        # Atraso se chegou atrasado ou saiu mais cedo
        atraso = max(entrada_diff, 0) + max(-saida_diff, 0)
        
        # Extra se chegou mais cedo ou saiu mais tarde
        extra = max(-entrada_diff, 0) + max(saida_diff, 0)

        return atraso, extra

    def calcular_horas(self):
        total_atraso = 0
        total_extra = 0

        # Calcula turno da manhã
        atraso, extra = self._calcular_turno(
            self.entrada_manha, self.saida_manha,
            self.JORNADA_ENTRADA_MANHA, self.JORNADA_SAIDA_MANHA
        )
        total_atraso += atraso
        total_extra += extra

        # Calcula turno da tarde
        atraso, extra = self._calcular_turno(
            self.entrada_tarde, self.saida_tarde,
            self.JORNADA_ENTRADA_TARDE, self.JORNADA_SAIDA_TARDE
        )
        total_atraso += atraso
        total_extra += extra

        return round(total_extra / 60, 2), round(total_atraso / 60, 2)

    def save(self, *args, **kwargs):
        # Só recalcula se ainda não está preenchido manualmente
        if self.horas_extras == 0 and self.horas_atraso == 0:
            extra, atraso = self.calcular_horas()
            self.horas_extras = Decimal(extra)
            self.horas_atraso = Decimal(atraso)

        super().save(*args, **kwargs)
