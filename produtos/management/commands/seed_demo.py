"""
Importa categorias e produtos do projeto Next.js original (data/products.ts).

Uso:
    python manage.py seed_demo
    python manage.py seed_demo --origem /caminho/para/products.ts

As imagens devem estar em media/produtos/ (copiadas de public/products/).
Também cria um cupom de exemplo (BEMVINDO10) e banners a partir de
media/banners/, se existirem imagens lá.
"""

import re
from decimal import Decimal
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand
from django.utils.text import slugify

from banners.models import Banner
from cupons.models import Cupom
from produtos.models import Categoria, Produto

ORIGEM_PADRAO = "/Users/macbookair/metalab-farma/data/products.ts"

# Ordem importa: a primeira regra que casar define a categoria.
REGRAS_CATEGORIA = [
    ("Kits", ["premium mix", "kit "]),
    ("Articulações", ["articulice", "curcuma", "curcumina", "colágen", "colageno",
                      "hialuronico", "glucosamina", "condroitina", "flex-a-mim", "flex a mim"]),
    ("Vitaminas", ["coenzima", "q10", "b12", "metilcobalamina", "folato", "nac",
                   "enzicoba", "visyneral", "vi-syneral"]),
    ("Fibras", ["laxtrine", "fibra", "ameixa", "tamarindo", "inulina", "fos"]),
    ("Compostos Naturais", ["carvão", "carve", "pinus"]),
    ("Cálcio", ["condroless", "calcio", "cálcio", "osteocorp"]),
    ("Melatonina", ["cogniflex", "melatonina"]),
    ("Xaropes", ["flebogenol", "xarope", "mucolisil", "meltrat"]),
    ("Outros", ["magnésio", "magnesio", "inovitann penta"]),
]


def classificar(nome):
    lower = nome.lower()
    for cat, termos in REGRAS_CATEGORIA:
        if cat == "Xaropes" and "xarope" in lower:
            return "Xaropes"
        for termo in termos:
            if termo in lower:
                return cat
    return "Outros"


def parse_products_ts(caminho):
    """Extrai os produtos do arquivo TypeScript com regex (estrutura uniforme)."""
    texto = Path(caminho).read_text(encoding="utf-8")
    blocos = re.findall(r"\{([^{}]*?)\}", texto, re.DOTALL)
    produtos = []
    for bloco in blocos:
        campos = {}
        for chave in ("nome", "marca", "imagemUrl", "descricaoCurta"):
            m = re.search(rf'{chave}:\s*"([^"]*)"', bloco)
            campos[chave] = m.group(1) if m else ""
        for chave in ("preco", "estoque", "precoOriginal"):
            m = re.search(rf"{chave}:\s*([\d.]+)", bloco)
            campos[chave] = m.group(1) if m else None
        if campos["nome"] and campos["preco"]:
            produtos.append(campos)
    return produtos


class Command(BaseCommand):
    help = "Importa categorias/produtos do projeto original e cria dados de exemplo."

    def add_arguments(self, parser):
        parser.add_argument("--origem", default=ORIGEM_PADRAO,
                            help="Caminho do data/products.ts original")

    def handle(self, *args, **opts):
        origem = Path(opts["origem"])
        if not origem.exists():
            self.stderr.write(f"Arquivo não encontrado: {origem}")
            return

        # Categorias
        categorias = {}
        for ordem, (nome, _) in enumerate(REGRAS_CATEGORIA):
            cat, _criada = Categoria.objects.get_or_create(
                slug=slugify(nome), defaults={"nome": nome, "ordem": ordem}
            )
            categorias[nome] = cat

        # Produtos
        media_produtos = Path(settings.MEDIA_ROOT) / "produtos"
        criados = atualizados = sem_imagem = 0
        for i, dados in enumerate(parse_products_ts(origem), start=1):
            nome = dados["nome"].strip()
            slug = slugify(nome)
            if not slug:
                continue
            imagem = ""
            if dados["imagemUrl"]:
                arquivo = Path(dados["imagemUrl"]).name
                if (media_produtos / arquivo).exists():
                    imagem = f"produtos/{arquivo}"
                else:
                    sem_imagem += 1
            preco = Decimal(dados["preco"])
            preco_original = (
                Decimal(dados["precoOriginal"]) if dados.get("precoOriginal") else None
            )
            # No mock, precoOriginal > preco indica promoção
            preco_normal, preco_promo = preco, None
            if preco_original and preco_original > preco:
                preco_normal, preco_promo = preco_original, preco

            defaults = {
                "nome": nome,
                "sku": f"MLB-{i:04d}",
                "marca": dados["marca"] or "Metalab",
                "categoria": categorias[classificar(nome)],
                "descricao_curta": dados["descricaoCurta"] or "",
                "preco": preco_normal,
                "preco_promocional": preco_promo,
                "estoque": int(dados["estoque"] or 0),
                "imagem_principal": imagem,
                "ativo": True,
            }
            _, criado = Produto.objects.update_or_create(slug=slug, defaults=defaults)
            if criado:
                criados += 1
            else:
                atualizados += 1

        # Destaques: 8 produtos mais baratos com imagem, um por "família"
        Produto.objects.update(destaque=False)
        destaque_ids = (
            Produto.objects.exclude(imagem_principal="")
            .exclude(nome__istartswith="kit")
            .order_by("nome")
            .values_list("id", flat=True)[:8]
        )
        Produto.objects.filter(id__in=list(destaque_ids)).update(destaque=True)

        # Cupom de exemplo
        Cupom.objects.get_or_create(
            codigo="BEMVINDO10",
            defaults={"tipo": Cupom.Tipo.PERCENTUAL, "valor": Decimal("10"), "ativo": True},
        )

        # Banners a partir de media/banners/
        pasta_banners = Path(settings.MEDIA_ROOT) / "banners"
        if pasta_banners.exists() and not Banner.objects.exists():
            for ordem, arq in enumerate(sorted(pasta_banners.iterdir())):
                if arq.suffix.lower() in (".png", ".jpg", ".jpeg", ".webp"):
                    Banner.objects.create(
                        titulo="Qualidade farmacêutica" if ordem == 0 else "",
                        subtitulo="Suplementos com pureza e eficácia comprovadas" if ordem == 0 else "",
                        imagem=f"banners/{arq.name}",
                        ordem=ordem,
                    )

        self.stdout.write(self.style.SUCCESS(
            f"Seed concluído: {criados} produtos criados, {atualizados} atualizados, "
            f"{sem_imagem} sem imagem, {Categoria.objects.count()} categorias, "
            f"{Banner.objects.count()} banners."
        ))
