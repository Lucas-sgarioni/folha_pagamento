from django.db import models

class ModalidadeEscolha(models.TextChoices):
    DIARISTA = 'diarista', 'Diarista'
    MENSALISTA = 'mensalista', 'Mensalista'

class SituacaoCadastro(models.TextChoices):
    ATIVO = 'AT', 'Ativo'
    DESATIVADO = 'DT' 'Desativado'

class Cadastro(models.Model):
    nome = models.CharField(verbose_name='Nome', max_length=70)
    cpf = models.CharField(verbose_name='CPF', max_length=14)
    valor_hora = models.DecimalField(max_digits=10, decimal_places=2)
    modalidade_contrato = models.CharField(
        verbose_name='Modalidade do contrato',
        max_length=10,
        choices=ModalidadeEscolha.choices,
        default=ModalidadeEscolha.DIARISTA
    )

    situacao_cadastro = models.CharField(
        verbose_name='Situação do cadastro',
        max_length=12,
        choices=SituacaoCadastro.choices,
        default=SituacaoCadastro.ATIVO
    )

    criado_em = models.DateTimeField(verbose_name='Criado em', auto_now_add=True)

class Editar(models.Model):
    nome = models.CharField(verbose_name='Nome', max_length=70)
    cpf = models.CharField(verbose_name='CPF', max_length=14)
    valor_hora = models.DecimalField(max_digits=10, decimal_places=2)
    modalidade_contrato = models.CharField(
        verbose_name='Modalidade do contrato',
        max_length=10,
        choices=ModalidadeEscolha.choices,
        default=ModalidadeEscolha.DIARISTA
    )

    situacao_cadastro = models.CharField(
        verbose_name='Situação do cadastro',
        max_length=12,
        choices=SituacaoCadastro.choices,
        default=SituacaoCadastro.ATIVO
    )

    editado_em = models.DateTimeField(verbose_name='editado em', auto_now_add=True)

