"""
Reorganiza o catálogo conforme a curadoria de produtos/data_catalogo.py:

1. Remove produtos da marca MAXMA (e seus kits).
2. Recria as categorias corretas e reclassifica todos os produtos.
3. Aplica descrições SEO/GEO/AEO, composição, modo de uso e metas.
4. Marca a linha Inovitann Clinical.
5. Importa cor principal/secundária do data/products.ts original.
6. Kits herdam categoria, cores e conteúdo do produto base.

Uso: python manage.py reorganizar_catalogo [--origem caminho/products.ts]
"""

import re
from pathlib import Path

from django.core.management.base import BaseCommand
from django.utils.text import slugify

from produtos.data_catalogo import CATALOGO, CATEGORIAS, LINHA_INOVITANN, MAXMA_REMOVER
from produtos.models import Categoria, Produto

ORIGEM_PADRAO = "/Users/macbookair/metalab-farma/data/products.ts"

AVISO_SUPLEMENTO = (
    "Este produto não é um medicamento. Não exceda a recomendação diária de consumo "
    "indicada na embalagem. Mantenha fora do alcance de crianças. Este produto não "
    "substitui uma alimentação equilibrada e seu consumo deve ser orientado por "
    "nutricionista ou médico."
)
AVISO_MEDICAMENTO = (
    "SE PERSISTIREM OS SINTOMAS, O MÉDICO DEVERÁ SER CONSULTADO. Siga corretamente o "
    "modo de usar; não desaparecendo os sintomas, procure orientação médica. "
    "Mantenha fora do alcance de crianças."
)


def nome_base_do_kit(nome):
    """'Kit 3 Flebogenol 60' -> ('Flebogenol 60', 3); produto simples -> (nome, 1)."""
    m = re.match(r"^Kit\s+(\d+)\s+(.*)$", nome, re.IGNORECASE)
    if m:
        return m.group(2).strip(), int(m.group(1))
    return nome, 1


def montar_descricao(nome, dados, unidades=1):
    """Texto longo com estrutura de SEO/AEO (o que é, benefício, FAQ)."""
    partes = []
    if unidades > 1:
        partes.append(
            f"Kit com {unidades} unidades de {nome} — mais economia para o uso contínuo."
        )
    partes.append(f"{nome} é {dados['oque']}.")
    partes.append(
        f"Produzido pela Metalab Farma (Lagoa Santa/MG) com padrão farmacêutico de "
        f"qualidade, matérias-primas selecionadas e controle rigoroso lote a lote."
    )
    if dados.get("faq"):
        partes.append("PERGUNTAS FREQUENTES")
        for pergunta, resposta in dados["faq"]:
            partes.append(f"{pergunta}\n{resposta}")
    return "\n\n".join(partes)


def carregar_cores(origem):
    """Extrai nome -> (corPrincipal, corSecundaria) do data/products.ts."""
    cores = {}
    caminho = Path(origem)
    if not caminho.exists():
        return cores
    texto = caminho.read_text(encoding="utf-8")
    for bloco in re.findall(r"\{([^{}]*?)\}", texto, re.DOTALL):
        nome = re.search(r'nome:\s*"([^"]*)"', bloco)
        cor1 = re.search(r'corPrincipal:\s*"([^"]*)"', bloco)
        cor2 = re.search(r'corSecundaria:\s*"([^"]*)"', bloco)
        if nome and cor1:
            cores[nome.group(1).strip()] = (
                cor1.group(1), cor2.group(1) if cor2 else ""
            )
    return cores


class Command(BaseCommand):
    help = "Aplica a curadoria do catálogo (categorias, MAXMA, Inovitann, SEO, cores)."

    def add_arguments(self, parser):
        parser.add_argument("--origem", default=ORIGEM_PADRAO)

    def handle(self, *args, **opts):
        # 1. Remover MAXMA (base + kits)
        removidos = 0
        for base in MAXMA_REMOVER:
            qs = Produto.objects.filter(nome__iregex=rf"^(Kit \d+ )?{re.escape(base)}$")
            n = qs.count()
            for p in qs:
                if p.itens_pedido.exists():
                    p.ativo = False
                    p.save(update_fields=["ativo"])
                else:
                    p.delete()
            removidos += n

        # 2. Categorias novas
        Categoria.objects.all().delete()
        cats = {}
        for ordem, (nome, descricao) in enumerate(CATEGORIAS):
            cats[nome] = Categoria.objects.create(
                nome=nome, slug=slugify(nome), descricao=descricao, ordem=ordem
            )

        # 3/4/5/6. Reclassificar, conteúdo, linha e cores
        cores = carregar_cores(opts["origem"])
        atualizados, sem_dados = 0, []
        for produto in Produto.objects.all():
            base, unidades = nome_base_do_kit(produto.nome)
            dados = CATALOGO.get(base)
            if not dados:
                sem_dados.append(produto.nome)
                continue

            produto.categoria = cats[dados["cat"]]
            produto.marca = (
                "Inovitann Clinical" if base in LINHA_INOVITANN else "Metalab"
            )
            produto.descricao_curta = (dados["oque"][0].upper() + dados["oque"][1:])[:255]
            produto.descricao_completa = montar_descricao(base, dados, unidades)
            produto.composicao = dados["comp"]
            produto.modo_uso = dados["modo"]
            produto.aviso_legal = (
                AVISO_MEDICAMENTO if dados["cat"] == "Dor e Febre" else AVISO_SUPLEMENTO
            )
            produto.meta_titulo = f"{produto.nome} | Metalab Farma"[:70]
            produto.meta_descricao = (
                f"{base}: {dados['oque']}"[:157] + "..."
            )[:160]

            cor = cores.get(produto.nome) or cores.get(base)
            if cor:
                produto.cor_principal = cor[0][:7]
                produto.cor_secundaria = (cor[1] or "")[:7]

            produto.save()
            atualizados += 1

        # Destaques: 1 produto com imagem por categoria (até 8)
        Produto.objects.update(destaque=False)
        destaque_ids = []
        for cat in cats.values():
            p = (
                Produto.objects.filter(categoria=cat, ativo=True)
                .exclude(imagem_principal="")
                .exclude(nome__istartswith="kit")
                .first()
            )
            if p:
                destaque_ids.append(p.pk)
        Produto.objects.filter(pk__in=destaque_ids[:8]).update(destaque=True)

        self.stdout.write(self.style.SUCCESS(
            f"Catálogo reorganizado: {removidos} produtos MAXMA removidos, "
            f"{atualizados} atualizados, {len(cats)} categorias, "
            f"{Produto.objects.filter(marca='Inovitann Clinical').count()} itens Inovitann."
        ))
        if sem_dados:
            self.stdout.write(self.style.WARNING(
                f"Sem curadoria ({len(sem_dados)}): {', '.join(sorted(set(sem_dados))[:10])}"
            ))
