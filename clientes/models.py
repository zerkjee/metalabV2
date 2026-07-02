import re

from django.conf import settings
from django.db import models

ESTADOS_BR = [
    ("AC", "AC"), ("AL", "AL"), ("AP", "AP"), ("AM", "AM"), ("BA", "BA"),
    ("CE", "CE"), ("DF", "DF"), ("ES", "ES"), ("GO", "GO"), ("MA", "MA"),
    ("MT", "MT"), ("MS", "MS"), ("MG", "MG"), ("PA", "PA"), ("PB", "PB"),
    ("PR", "PR"), ("PE", "PE"), ("PI", "PI"), ("RJ", "RJ"), ("RN", "RN"),
    ("RS", "RS"), ("RO", "RO"), ("RR", "RR"), ("SC", "SC"), ("SP", "SP"),
    ("SE", "SE"), ("TO", "TO"),
]


def somente_digitos(valor):
    """Remove tudo que não for dígito (telefone, CPF, CEP)."""
    return re.sub(r"\D", "", valor or "")


class Cliente(models.Model):
    # Cliente pode existir sem conta de usuário (compra como convidado)
    usuario = models.OneToOneField(
        settings.AUTH_USER_MODEL, null=True, blank=True,
        on_delete=models.SET_NULL, related_name="cliente",
    )
    nome = models.CharField(max_length=200)
    email = models.EmailField(blank=True)
    telefone = models.CharField(max_length=20, blank=True)
    cpf = models.CharField("CPF", max_length=14, blank=True)
    data_nascimento = models.DateField(null=True, blank=True)

    # Endereço (MVP: um endereço por cliente)
    cep = models.CharField("CEP", max_length=9, blank=True)
    rua = models.CharField(max_length=200, blank=True)
    numero = models.CharField("número", max_length=20, blank=True)
    complemento = models.CharField(max_length=100, blank=True)
    bairro = models.CharField(max_length=100, blank=True)
    cidade = models.CharField(max_length=100, blank=True)
    estado = models.CharField(max_length=2, choices=ESTADOS_BR, blank=True)

    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["nome"]
        constraints = [
            # Únicos apenas quando preenchidos
            models.UniqueConstraint(
                fields=["email"], condition=~models.Q(email=""), name="cliente_email_unico"
            ),
            models.UniqueConstraint(
                fields=["cpf"], condition=~models.Q(cpf=""), name="cliente_cpf_unico"
            ),
        ]

    def __str__(self):
        return self.nome

    def save(self, *args, **kwargs):
        # Armazena telefone/CPF/CEP limpos; formatação só na exibição
        self.telefone = somente_digitos(self.telefone)
        self.cpf = somente_digitos(self.cpf)
        self.cep = somente_digitos(self.cep)
        super().save(*args, **kwargs)

    @property
    def telefone_formatado(self):
        t = self.telefone
        if len(t) == 11:
            return f"({t[:2]}) {t[2:7]}-{t[7:]}"
        if len(t) == 10:
            return f"({t[:2]}) {t[2:6]}-{t[6:]}"
        return t

    @property
    def cpf_formatado(self):
        c = self.cpf
        if len(c) == 11:
            return f"{c[:3]}.{c[3:6]}.{c[6:9]}-{c[9:]}"
        return c

    @property
    def endereco_completo(self):
        partes = [p for p in [
            f"{self.rua}, {self.numero}" if self.rua else "",
            self.complemento,
            self.bairro,
            f"{self.cidade}/{self.estado}" if self.cidade else "",
            f"CEP {self.cep}" if self.cep else "",
        ] if p]
        return " — ".join(partes)
