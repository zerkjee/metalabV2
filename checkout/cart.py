"""
Carrinho baseado em sessão.

Estrutura na sessão:
    request.session["carrinho"] = {"<produto_id>": quantidade, ...}
    request.session["cupom_codigo"] = "CODIGO" | ausente

As regras de total espelham services/cartTotals.ts do projeto original:
- desconto limitado ao subtotal
- cupom FRETE_GRATIS zera o frete
- total nunca negativo
"""

from decimal import Decimal

from django.conf import settings

from cupons.services import buscar_cupom_valido
from produtos.models import Produto

SESSAO_CARRINHO = "carrinho"
SESSAO_CUPOM = "cupom_codigo"


class Carrinho:
    def __init__(self, request):
        self.session = request.session
        self.itens_sessao = self.session.setdefault(SESSAO_CARRINHO, {})

    def _quantidade_valida(self, quantidade):
        try:
            return max(1, int(quantidade))
        except (TypeError, ValueError):
            return None

    def _salvar(self):
        self.session[SESSAO_CARRINHO] = self.itens_sessao
        self.session.modified = True

    # ─── Operações ───────────────────────────────────────────────────────────

    def adicionar(self, produto, quantidade=1):
        """
        Adiciona um produto respeitando ativo/estoque.
        Retorna (ok: bool, mensagem_de_erro: str).
        """
        if not produto.ativo:
            return False, "Este produto não está disponível."
        if produto.estoque <= 0:
            return False, "Este produto está sem estoque."
        quantidade = self._quantidade_valida(quantidade)
        if quantidade is None:
            return False, "Quantidade inválida."
        chave = str(produto.pk)
        nova_qtd = self.itens_sessao.get(chave, 0) + quantidade
        if nova_qtd > produto.estoque:
            return False, f"Só temos {produto.estoque} unidade(s) em estoque."
        self.itens_sessao[chave] = nova_qtd
        self._salvar()
        return True, ""

    def atualizar(self, produto, quantidade):
        quantidade = self._quantidade_valida(quantidade)
        if quantidade is None:
            return False, "Quantidade inválida."
        if quantidade < 1:
            return self.remover(produto)
        if quantidade > produto.estoque:
            return False, f"Só temos {produto.estoque} unidade(s) em estoque."
        self.itens_sessao[str(produto.pk)] = quantidade
        self._salvar()
        return True, ""

    def remover(self, produto):
        self.itens_sessao.pop(str(produto.pk), None)
        self._salvar()
        return True, ""

    def limpar(self):
        self.session[SESSAO_CARRINHO] = {}
        self.session.pop(SESSAO_CUPOM, None)
        self.itens_sessao = self.session[SESSAO_CARRINHO]
        self.session.modified = True

    # ─── Cupom ───────────────────────────────────────────────────────────────

    def aplicar_cupom(self, codigo):
        cupom, erro = buscar_cupom_valido(codigo, self.subtotal())
        if not cupom:
            return False, erro
        self.session[SESSAO_CUPOM] = cupom.codigo
        self.session.modified = True
        return True, ""

    def remover_cupom(self):
        self.session.pop(SESSAO_CUPOM, None)
        self.session.modified = True

    def cupom(self):
        """Cupom atualmente aplicado, revalidado a cada chamada (pode expirar)."""
        codigo = self.session.get(SESSAO_CUPOM)
        if not codigo:
            return None
        cupom, _ = buscar_cupom_valido(codigo, self.subtotal())
        return cupom

    # ─── Leitura ─────────────────────────────────────────────────────────────

    def itens(self):
        """Lista de dicts {produto, quantidade, preco_unitario, subtotal}."""
        ids = [int(k) for k in self.itens_sessao.keys()]
        produtos = {p.pk: p for p in Produto.objects.filter(pk__in=ids)}
        resultado = []
        for chave, quantidade in self.itens_sessao.items():
            produto = produtos.get(int(chave))
            if not produto:
                continue
            preco = produto.preco_atual
            resultado.append({
                "produto": produto,
                "quantidade": quantidade,
                "preco_unitario": preco,
                "subtotal": preco * quantidade,
            })
        return resultado

    def quantidade_total(self):
        return sum(self.itens_sessao.values())

    def vazio(self):
        return not self.itens_sessao

    def subtotal(self):
        return sum((item["subtotal"] for item in self.itens()), start=Decimal("0"))

    def frete_base(self):
        """Frete fixo simples; grátis acima do limite configurado (env)."""
        if self.vazio():
            return Decimal("0")
        subtotal = self.subtotal()
        if subtotal >= Decimal(settings.FRETE_GRATIS_ACIMA_DE):
            return Decimal("0")
        return Decimal(settings.FRETE_FIXO)

    def totais(self):
        """Todos os valores calculados de uma vez (para templates e checkout)."""
        subtotal = self.subtotal()
        cupom = self.cupom()
        desconto = cupom.calcular_desconto(subtotal) if cupom else Decimal("0")
        frete = self.frete_base()
        if cupom and cupom.frete_gratis:
            frete = Decimal("0")
        total = max(subtotal - desconto + frete, Decimal("0"))
        return {
            "subtotal": subtotal,
            "cupom": cupom,
            "desconto": desconto,
            "frete": frete,
            "total": total,
        }
