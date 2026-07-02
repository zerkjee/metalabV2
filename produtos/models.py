from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models
from django.urls import reverse
from django.utils.text import slugify


class Categoria(models.Model):
    nome = models.CharField(max_length=120)
    slug = models.SlugField(max_length=140, unique=True, blank=True)
    descricao = models.TextField(blank=True)
    ativa = models.BooleanField(default=True)
    ordem = models.PositiveIntegerField(default=0)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["ordem", "nome"]
        verbose_name = "categoria"
        verbose_name_plural = "categorias"

    def __str__(self):
        return self.nome

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nome)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("produtos:categoria", args=[self.slug])


class ProdutoQuerySet(models.QuerySet):
    def publicos(self):
        """Produtos visíveis no catálogo público."""
        return self.filter(ativo=True)

    def destaques(self):
        return self.publicos().filter(destaque=True)


class Produto(models.Model):
    nome = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    sku = models.CharField("SKU", max_length=60, unique=True)
    marca = models.CharField(max_length=120, default="Metalab")
    categoria = models.ForeignKey(
        Categoria, null=True, blank=True, on_delete=models.SET_NULL, related_name="produtos"
    )
    descricao_curta = models.CharField(max_length=255, blank=True)
    descricao_completa = models.TextField(blank=True)
    composicao = models.TextField(blank=True)
    modo_uso = models.TextField("modo de uso", blank=True)
    aviso_legal = models.TextField(blank=True)

    preco = models.DecimalField(
        max_digits=10, decimal_places=2, validators=[MinValueValidator(0)]
    )
    preco_promocional = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True, validators=[MinValueValidator(0)]
    )
    estoque = models.PositiveIntegerField(default=0)
    estoque_minimo = models.PositiveIntegerField(default=5)

    # Dimensões para futura cotação de frete (Melhor Envio)
    peso = models.PositiveIntegerField("peso (g)", null=True, blank=True)
    altura = models.PositiveIntegerField("altura (cm)", null=True, blank=True)
    largura = models.PositiveIntegerField("largura (cm)", null=True, blank=True)
    comprimento = models.PositiveIntegerField("comprimento (cm)", null=True, blank=True)

    # Identidade visual do produto (tema da página de detalhe)
    cor_principal = models.CharField(max_length=7, blank=True, help_text="Hex, ex.: #002659")
    cor_secundaria = models.CharField(max_length=7, blank=True)

    # SEO / AEO
    meta_titulo = models.CharField(max_length=70, blank=True)
    meta_descricao = models.CharField(max_length=160, blank=True)

    imagem_principal = models.ImageField(upload_to="produtos/", blank=True)
    imagem_2 = models.ImageField(upload_to="produtos/", blank=True)
    imagem_3 = models.ImageField(upload_to="produtos/", blank=True)
    imagem_4 = models.ImageField(upload_to="produtos/", blank=True)

    ativo = models.BooleanField(default=True)
    destaque = models.BooleanField(default=False)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    objects = ProdutoQuerySet.as_manager()

    class Meta:
        ordering = ["nome"]
        indexes = [
            models.Index(fields=["ativo", "destaque"]),
            models.Index(fields=["ativo", "categoria"]),
        ]

    def __str__(self):
        return self.nome

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nome)
        super().save(*args, **kwargs)

    def clean(self):
        if self.preco_promocional is not None and self.preco is not None \
                and self.preco_promocional >= self.preco:
            raise ValidationError(
                {"preco_promocional": "O preço promocional deve ser menor que o preço normal."}
            )

    def get_absolute_url(self):
        return reverse("produtos:detalhe", args=[self.slug])

    # ─── Regras de exibição ──────────────────────────────────────────────────

    @property
    def preco_atual(self):
        """Preço efetivo de venda (promocional quando houver)."""
        return self.preco_promocional if self.preco_promocional is not None else self.preco

    @property
    def em_promocao(self):
        return self.preco_promocional is not None

    @property
    def disponivel(self):
        return self.ativo and self.estoque > 0

    @property
    def estoque_baixo(self):
        return self.estoque <= self.estoque_minimo


class ImagemProduto(models.Model):
    """Galeria extra de imagens (compatível com a origem Next.js)."""

    produto = models.ForeignKey(Produto, on_delete=models.CASCADE, related_name="imagens")
    imagem = models.ImageField(upload_to="produtos/galeria/")
    alt = models.CharField(max_length=200, blank=True)
    ordem = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["ordem"]
        verbose_name = "imagem do produto"
        verbose_name_plural = "imagens do produto"

    def __str__(self):
        return f"Imagem de {self.produto.nome}"
