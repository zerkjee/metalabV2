from decimal import Decimal

from django.test import TestCase

from cupons.models import Cupom
from pedidos.models import Pedido
from produtos.models import Produto


def criar_produto(nome="Ademoril", sku="SKU-1", preco="79.90", estoque=10, **kwargs):
    return Produto.objects.create(
        nome=nome, sku=sku, preco=Decimal(preco), estoque=estoque, **kwargs
    )


DADOS_CHECKOUT = {
    "nome": "Maria Silva", "email": "maria@example.com", "telefone": "11999998888",
    "cpf": "12345678901", "cep": "01310100", "rua": "Av. Paulista", "numero": "1000",
    "complemento": "", "bairro": "Bela Vista", "cidade": "São Paulo", "estado": "SP",
    "metodo_pagamento": "PIX_MANUAL",
}


class CarrinhoTest(TestCase):
    def test_adicionar_e_calcular_subtotal(self):
        produto = criar_produto()
        self.client.post(f"/carrinho/adicionar/{produto.pk}/", {"quantidade": 2})
        resposta = self.client.get("/carrinho/")
        self.assertContains(resposta, "159,80")

    def test_nao_adiciona_produto_inativo(self):
        produto = criar_produto(ativo=False)
        self.client.post(f"/carrinho/adicionar/{produto.pk}/")
        resposta = self.client.get("/carrinho/")
        self.assertContains(resposta, "carrinho está vazio")

    def test_nao_adiciona_sem_estoque(self):
        produto = criar_produto(estoque=0)
        self.client.post(f"/carrinho/adicionar/{produto.pk}/")
        resposta = self.client.get("/carrinho/")
        self.assertContains(resposta, "carrinho está vazio")

    def test_quantidade_nao_ultrapassa_estoque(self):
        produto = criar_produto(estoque=3)
        self.client.post(f"/carrinho/adicionar/{produto.pk}/", {"quantidade": 5})
        resposta = self.client.get("/carrinho/")
        self.assertContains(resposta, "carrinho está vazio")

    def test_quantidade_invalida_nao_gera_erro_500(self):
        produto = criar_produto()
        resposta = self.client.post(
            f"/carrinho/adicionar/{produto.pk}/", {"quantidade": "abc"}, follow=True
        )
        self.assertEqual(resposta.status_code, 200)
        self.assertContains(resposta, "Quantidade inválida")

    def test_cupom_invalido_mostra_erro(self):
        produto = criar_produto()
        self.client.post(f"/carrinho/adicionar/{produto.pk}/")
        resposta = self.client.post(
            "/carrinho/aplicar-cupom/", {"codigo": "NAOEXISTE"}, follow=True
        )
        self.assertContains(resposta, "não encontrado")

    def test_cupom_percentual_aplica_desconto(self):
        produto = criar_produto(preco="100.00")
        Cupom.objects.create(codigo="DEZ", tipo=Cupom.Tipo.PERCENTUAL, valor=10)
        self.client.post(f"/carrinho/adicionar/{produto.pk}/")
        self.client.post("/carrinho/aplicar-cupom/", {"codigo": "DEZ"})
        resposta = self.client.get("/carrinho/")
        self.assertContains(resposta, "10,00")  # desconto exibido

    def test_carrinho_vazio_redireciona_no_checkout(self):
        resposta = self.client.get("/checkout/")
        self.assertRedirects(resposta, "/produtos/")


class CheckoutTest(TestCase):
    def test_checkout_cria_pedido_e_baixa_estoque(self):
        produto = criar_produto(estoque=10)
        self.client.post(f"/carrinho/adicionar/{produto.pk}/", {"quantidade": 2})
        resposta = self.client.post("/checkout/", DADOS_CHECKOUT)

        pedido = Pedido.objects.get()
        self.assertRedirects(resposta, f"/pedido/sucesso/{pedido.recibo_token}/")
        self.assertEqual(pedido.status, Pedido.Status.CONFIRMADO)
        self.assertEqual(pedido.itens.count(), 1)

        produto.refresh_from_db()
        self.assertEqual(produto.estoque, 8)

    def test_pedido_preserva_snapshot(self):
        produto = criar_produto()
        self.client.post(f"/carrinho/adicionar/{produto.pk}/")
        self.client.post("/checkout/", DADOS_CHECKOUT)

        item = Pedido.objects.get().itens.get()
        produto.nome = "Nome alterado depois"
        produto.save()
        item.refresh_from_db()
        self.assertEqual(item.nome_produto_snapshot, "Ademoril")
        self.assertEqual(item.sku_snapshot, "SKU-1")

    def test_total_com_cupom_e_frete(self):
        produto = criar_produto(preco="100.00")
        Cupom.objects.create(codigo="DEZ", tipo=Cupom.Tipo.PERCENTUAL, valor=10)
        self.client.post(f"/carrinho/adicionar/{produto.pk}/")
        self.client.post("/carrinho/aplicar-cupom/", {"codigo": "DEZ"})
        self.client.post("/checkout/", DADOS_CHECKOUT)

        pedido = Pedido.objects.get()
        # 100 - 10 (cupom) + 19.90 (frete fixo, abaixo de 199) = 109.90
        self.assertEqual(pedido.total, Decimal("109.90"))
        pedido.cupom.refresh_from_db()
        self.assertEqual(pedido.cupom.usos_realizados, 1)

    def test_frete_gratis_acima_do_limite(self):
        produto = criar_produto(preco="250.00")
        self.client.post(f"/carrinho/adicionar/{produto.pk}/")
        self.client.post("/checkout/", DADOS_CHECKOUT)
        pedido = Pedido.objects.get()
        self.assertEqual(pedido.frete, Decimal("0"))

    def test_checkout_cria_cliente(self):
        produto = criar_produto()
        self.client.post(f"/carrinho/adicionar/{produto.pk}/")
        self.client.post("/checkout/", DADOS_CHECKOUT)
        pedido = Pedido.objects.get()
        self.assertEqual(pedido.cliente.email, "maria@example.com")
        self.assertEqual(pedido.cliente.cpf, "12345678901")

    def test_carrinho_limpo_apos_checkout(self):
        produto = criar_produto()
        self.client.post(f"/carrinho/adicionar/{produto.pk}/")
        self.client.post("/checkout/", DADOS_CHECKOUT)
        resposta = self.client.get("/carrinho/")
        self.assertContains(resposta, "carrinho está vazio")

    def test_codigo_curto_do_pedido_nao_abre_recibo(self):
        produto = criar_produto()
        self.client.post(f"/carrinho/adicionar/{produto.pk}/")
        self.client.post("/checkout/", DADOS_CHECKOUT)
        pedido = Pedido.objects.get()
        resposta = self.client.get(f"/pedido/sucesso/{pedido.codigo}/")
        self.assertEqual(resposta.status_code, 404)

    def test_reenvio_com_mesmo_token_nao_duplica_pedido(self):
        produto = criar_produto(estoque=10)
        self.client.post(f"/carrinho/adicionar/{produto.pk}/", {"quantidade": 2})
        resposta = self.client.get("/checkout/")
        token = resposta.context["idempotency_token"]

        self.client.post("/checkout/", {**DADOS_CHECKOUT, "idempotency_token": token})
        # Simula reenvio tardio do mesmo formulario depois de limpar o carrinho.
        self.client.post("/checkout/", {**DADOS_CHECKOUT, "idempotency_token": token})

        self.assertEqual(Pedido.objects.count(), 1)
