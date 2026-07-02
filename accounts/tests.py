from django.contrib.auth.models import User
from django.test import TestCase

ROTAS_ADMIN = [
    "/admin/",
    "/admin/dashboard/",
    "/admin/relatorios/",
    "/admin/produtos/",
    "/admin/pedidos/",
    "/admin/clientes/",
    "/admin/cupons/",
    "/admin/banners/",
]

ROTAS_API_PROTEGIDAS = [
    "/api/produtos/",
    "/api/pedidos/",
    "/api/clientes/",
    "/api/dashboard/resumo/",
]


class PermissoesAdminTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.comum = User.objects.create_user("cliente", password="senha12345")
        cls.staff = User.objects.create_user("gerente", password="senha12345", is_staff=True)

    def test_anonimo_redirecionado_para_login(self):
        for rota in ROTAS_ADMIN:
            resposta = self.client.get(rota)
            self.assertEqual(resposta.status_code, 302, rota)
            self.assertIn("/login/", resposta.url, rota)

    def test_usuario_comum_nao_acessa_painel(self):
        self.client.login(username="cliente", password="senha12345")
        for rota in ROTAS_ADMIN:
            resposta = self.client.get(rota)
            self.assertEqual(resposta.status_code, 302, rota)

    def test_staff_acessa_painel(self):
        self.client.login(username="gerente", password="senha12345")
        for rota in ROTAS_ADMIN:
            resposta = self.client.get(rota)
            self.assertEqual(resposta.status_code, 200, rota)

    def test_api_health_publica(self):
        resposta = self.client.get("/api/health/")
        self.assertEqual(resposta.status_code, 200)
        self.assertEqual(resposta.json()["status"], "ok")
        self.assertNotIn("database", resposta.json())

    def test_api_protegida_exige_staff(self):
        for rota in ROTAS_API_PROTEGIDAS:
            resposta = self.client.get(rota)
            self.assertEqual(resposta.status_code, 401, rota)
        self.client.login(username="gerente", password="senha12345")
        for rota in ROTAS_API_PROTEGIDAS:
            resposta = self.client.get(rota)
            self.assertEqual(resposta.status_code, 200, rota)

    def test_api_protegida_nega_usuario_comum_com_json(self):
        self.client.login(username="cliente", password="senha12345")
        resposta = self.client.get("/api/produtos/")
        self.assertEqual(resposta.status_code, 403)
        self.assertEqual(resposta["Content-Type"], "application/json")

    def test_api_recusa_metodos_de_escrita_em_rotas_de_leitura(self):
        self.client.login(username="gerente", password="senha12345")
        resposta = self.client.post("/api/produtos/")
        self.assertEqual(resposta.status_code, 405)


class LoginTest(TestCase):
    def test_login_e_logout(self):
        User.objects.create_user("maria", password="senha12345")
        resposta = self.client.post(
            "/login/", {"username": "maria", "password": "senha12345"}
        )
        self.assertRedirects(resposta, "/")
        resposta = self.client.post("/logout/")
        self.assertRedirects(resposta, "/")

    def test_logout_por_get_nao_altera_sessao(self):
        User.objects.create_user("maria", password="senha12345")
        self.client.login(username="maria", password="senha12345")
        resposta = self.client.get("/logout/")
        self.assertEqual(resposta.status_code, 405)

    def test_login_next_bloqueia_redirect_externo(self):
        User.objects.create_user("maria", password="senha12345")
        resposta = self.client.post(
            "/login/?next=//evil.example/path",
            {"username": "maria", "password": "senha12345"},
        )
        self.assertRedirects(resposta, "/")

    def test_login_invalido_mostra_erro(self):
        resposta = self.client.post(
            "/login/", {"username": "x", "password": "errada"}, follow=True
        )
        self.assertContains(resposta, "inválidos")

    def test_staff_redirecionado_para_dashboard(self):
        User.objects.create_user("gerente", password="senha12345", is_staff=True)
        resposta = self.client.post(
            "/login/", {"username": "gerente", "password": "senha12345"}
        )
        self.assertRedirects(resposta, "/admin/dashboard/")
