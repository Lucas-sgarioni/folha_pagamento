from django.db import models


class EscolhaMes():
    ...

class Lancamento(models.Model):
    mes = models.DateTimeField