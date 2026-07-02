from decimal import Decimal

from django.core.exceptions import ValidationError
from django.test import TestCase

from .models import Categoria, Produto


def criar_produto(**kwargs):
    dados = {"nome": "Ademoril", "sku": "SKU-1", "preco": Decimal("79.90"), "estoque": 10}
    dados.update(kwargs)
    return Produto.objects.create(**dados)


class ProdutoModelTest(TestCase):
    def test_slug_gerado_automaticamente(self):
        produto = criar_produto(nome="Ademoril 500mg")
        self.assertEqual(produto.slug, "ademoril-500mg")

    def test_preco_atual_usa_promocional(self):
        produto = criar_produto(preco_promocional=Decimal("59.90"))
        self.assertEqual(produto.preco_atual, Decimal("59.90"))
        self.assertTrue(produto.em_promocao)

    def test_promocional_maior_que_preco_invalido(self):
        produto = criar_produto(preco_promocional=Decimal("99.90"))
        with self.assertRaises(ValidationError):
            produto.full_clean()

    def test_sem_estoque_fica_indisponivel(self):
        produto = criar_produto(estoque=0)
        self.assertFalse(produto.disponivel)

    def test_inativo_fora_do_catalogo_publico(self):
        criar_produto(ativo=False)
        self.assertEqual(Produto.objects.publicos().count(), 0)

    def test_estoque_baixo(self):
        produto = criar_produto(estoque=3, estoque_minimo=5)
        self.assertTrue(produto.estoque_baixo)


class CatalogoPublicoTest(TestCase):
    def test_listagem_mostra_apenas_ativos(self):
        criar_produto(nome="Visível", sku="V-1")
        criar_produto(nome="Oculto", sku="O-1", ativo=False)
        resposta = self.client.get("/produtos/")
        self.assertContains(resposta, "Visível")
        self.assertNotContains(resposta, "Oculto")

    def test_detalhe_de_produto_inativo_retorna_404(self):
        produto = criar_produto(ativo=False)
        resposta = self.client.get(f"/produtos/{produto.slug}/")
        self.assertEqual(resposta.status_code, 404)

    def test_busca_por_nome(self):
        criar_produto(nome="Flebogenol", sku="F-1")
        resposta = self.client.get("/busca/", {"q": "flebo"})
        self.assertContains(resposta, "Flebogenol")

    def test_categoria_inativa_fora_do_menu(self):
        Categoria.objects.create(nome="Escondida", ativa=False)
        resposta = self.client.get("/")
        self.assertNotContains(resposta, "Escondida")
