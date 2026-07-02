from decimal import Decimal

from django.test import TestCase

from produtos.models import Produto

from . import services
from .models import ItemPedido, Pedido


def criar_pedido_com_item(estoque=10, quantidade=2):
    produto = Produto.objects.create(
        nome="Ademoril", sku="SKU-1", preco=Decimal("50.00"), estoque=estoque
    )
    pedido = Pedido.objects.create()
    ItemPedido.objects.create(
        pedido=pedido, produto=produto, nome_produto_snapshot=produto.nome,
        sku_snapshot=produto.sku, quantidade=quantidade, preco_unitario=produto.preco,
    )
    pedido.recalcular_totais()
    return pedido, produto


class PedidoServicesTest(TestCase):
    def test_confirmar_baixa_estoque_uma_vez(self):
        pedido, produto = criar_pedido_com_item()
        services.alterar_status(pedido, Pedido.Status.CONFIRMADO)
        produto.refresh_from_db()
        self.assertEqual(produto.estoque, 8)
        self.assertTrue(pedido.estoque_baixado)

    def test_confirmar_com_estoque_insuficiente_aborta(self):
        pedido, produto = criar_pedido_com_item(estoque=1, quantidade=2)
        with self.assertRaises(services.EstoqueInsuficiente):
            services.alterar_status(pedido, Pedido.Status.CONFIRMADO)
        produto.refresh_from_db()
        pedido.refresh_from_db()
        self.assertEqual(produto.estoque, 1)
        self.assertFalse(pedido.estoque_baixado)

    def test_cancelar_confirmado_devolve_estoque(self):
        pedido, produto = criar_pedido_com_item()
        services.alterar_status(pedido, Pedido.Status.CONFIRMADO)
        services.cancelar(pedido)
        produto.refresh_from_db()
        self.assertEqual(produto.estoque, 10)
        self.assertEqual(pedido.status, Pedido.Status.CANCELADO)

    def test_transicao_invalida_levanta_erro(self):
        pedido, _ = criar_pedido_com_item()
        with self.assertRaises(services.TransicaoInvalida):
            services.alterar_status(pedido, Pedido.Status.ENTREGUE)

    def test_pedido_entregue_nao_pode_ser_cancelado(self):
        pedido, _ = criar_pedido_com_item()
        services.alterar_status(pedido, Pedido.Status.CONFIRMADO)
        services.alterar_status(pedido, Pedido.Status.ENVIADO)
        services.alterar_status(pedido, Pedido.Status.ENTREGUE)
        with self.assertRaises(services.TransicaoInvalida):
            services.cancelar(pedido)

    def test_historico_registrado(self):
        pedido, _ = criar_pedido_com_item()
        services.alterar_status(pedido, Pedido.Status.CONFIRMADO)
        historico = pedido.historico.first()
        self.assertEqual(historico.status_anterior, Pedido.Status.NOVO)
        self.assertEqual(historico.status_novo, Pedido.Status.CONFIRMADO)

    def test_marcar_pago_confirma_pedido_novo(self):
        pedido, produto = criar_pedido_com_item()
        services.marcar_pago(pedido)
        self.assertEqual(pedido.status_pagamento, Pedido.StatusPagamento.PAGO)
        self.assertEqual(pedido.status, Pedido.Status.CONFIRMADO)

    def test_cancelar_pago_estorna(self):
        pedido, _ = criar_pedido_com_item()
        services.marcar_pago(pedido)
        services.cancelar(pedido)
        pedido.refresh_from_db()
        self.assertEqual(pedido.status_pagamento, Pedido.StatusPagamento.ESTORNADO)

    def test_totais(self):
        pedido, _ = criar_pedido_com_item(quantidade=2)
        self.assertEqual(pedido.subtotal, Decimal("100.00"))
        self.assertEqual(pedido.total, Decimal("100.00"))

    def test_cancelado_nao_conta_faturamento(self):
        pedido, _ = criar_pedido_com_item()
        services.cancelar(pedido)
        self.assertFalse(pedido.conta_como_faturamento)
