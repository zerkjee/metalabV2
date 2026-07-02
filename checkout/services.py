"""
Serviço de checkout: transforma o carrinho em pedido.

Fluxo (dentro de uma transação):
1. Se houver token de idempotência já usado, devolve o mesmo pedido.
2. Revalida estoque de todos os itens.
3. Cria ou atualiza o Cliente (por e-mail ou CPF).
4. Cria o Pedido com totais calculados no servidor.
5. Cria os itens com snapshot (nome, SKU, preço).
6. Registra uso do cupom.
7. Confirma o pedido (baixa o estoque).
O carrinho é limpo pela view após o sucesso.
"""

from django.db import transaction

from clientes.models import Cliente, somente_digitos
from cupons.services import CupomIndisponivel, registrar_uso
from pedidos.models import ItemPedido, Pedido
from pedidos.services import EstoqueInsuficiente as EstoquePedidoInsuficiente
from pedidos.services import alterar_status


class EstoqueInsuficiente(Exception):
    def __init__(self, produto, disponivel):
        self.produto = produto
        self.disponivel = disponivel
        super().__init__(
            f"Estoque insuficiente para {produto.nome} (disponível: {disponivel})."
        )


def _obter_ou_atualizar_cliente(dados, usuario=None):
    """Localiza cliente por e-mail (ou CPF) e atualiza os dados; senão cria."""
    email = (dados.get("email") or "").strip().lower()
    cpf = somente_digitos(dados.get("cpf"))
    cliente = None
    if email:
        cliente = Cliente.objects.filter(email=email).first()
    if cliente is None and cpf:
        cliente = Cliente.objects.filter(cpf=cpf).first()
    if cliente is None:
        cliente = Cliente()

    campos = ["nome", "email", "telefone", "cpf", "cep", "rua", "numero",
              "complemento", "bairro", "cidade", "estado"]
    for campo in campos:
        valor = dados.get(campo)
        if valor:
            setattr(cliente, campo, valor)
    if usuario is not None and usuario.is_authenticated and cliente.usuario_id is None:
        cliente.usuario = usuario
    cliente.save()
    return cliente


@transaction.atomic
def criar_pedido(carrinho, dados_checkout, usuario=None, idempotency_token=None):
    """Cria o pedido a partir do carrinho.

    - Se `idempotency_token` já existir num pedido, devolve o mesmo pedido
      (idempotência contra duplo-clique).
    - Levanta `EstoqueInsuficiente` se algum item não tiver estoque no
      momento da confirmação. A baixa efetiva é feita por
      `pedidos.services.alterar_status` com `F()` expressions.
    """
    # 0. Idempotência: reenvio do mesmo POST devolve o mesmo pedido
    if idempotency_token:
        existente = Pedido.objects.filter(idempotency_token=idempotency_token).first()
        if existente is not None:
            return existente

    itens = carrinho.itens()
    if not itens:
        raise ValueError("O carrinho está vazio.")

    # 1. Validação final de estoque (a baixa atômica é feita em _baixar_estoque)
    for item in itens:
        produto = item["produto"]
        if not produto.ativo or produto.estoque < item["quantidade"]:
            raise EstoqueInsuficiente(produto, produto.estoque)

    # 2. Cliente
    cliente = _obter_ou_atualizar_cliente(dados_checkout, usuario)

    # 3. Pedido
    totais = carrinho.totais()
    pedido = Pedido.objects.create(
        cliente=cliente,
        subtotal=totais["subtotal"],
        desconto=totais["desconto"],
        frete=totais["frete"],
        total=totais["total"],
        cupom=totais["cupom"],
        metodo_pagamento=dados_checkout.get("metodo_pagamento", ""),
        idempotency_token=idempotency_token or Pedido._meta.get_field(
            "idempotency_token"
        ).default(),
        comprador_nome=cliente.nome,
        comprador_email=cliente.email,
        comprador_telefone=cliente.telefone,
        endereco_entrega=cliente.endereco_completo,
    )

    # 4. Itens com snapshot
    for item in itens:
        produto = item["produto"]
        ItemPedido.objects.create(
            pedido=pedido,
            produto=produto,
            nome_produto_snapshot=produto.nome,
            sku_snapshot=produto.sku,
            quantidade=item["quantidade"],
            preco_unitario=item["preco_unitario"],
        )

    # 5. Cupom
    if totais["cupom"]:
        try:
            registrar_uso(totais["cupom"])
        except CupomIndisponivel as e:
            raise ValueError(str(e)) from e

    # 6. Confirma (baixa estoque) — pagamento é manual neste MVP
    try:
        alterar_status(pedido, Pedido.Status.CONFIRMADO, usuario, "Pedido criado no checkout")
    except EstoquePedidoInsuficiente as e:
        raise EstoqueInsuficiente(e.produto, e.disponivel) from e
    return pedido
