from datetime import timedelta
from decimal import Decimal

from django.test import TestCase
from django.utils import timezone

from .models import Cupom
from .services import CupomIndisponivel, buscar_cupom_valido, registrar_uso


class CupomTest(TestCase):
    def test_percentual_calcula_desconto(self):
        cupom = Cupom.objects.create(codigo="DEZ", tipo=Cupom.Tipo.PERCENTUAL, valor=10)
        self.assertEqual(cupom.calcular_desconto(Decimal("200")), Decimal("20.00"))

    def test_valor_fixo_nao_ultrapassa_subtotal(self):
        cupom = Cupom.objects.create(codigo="FIXO", tipo=Cupom.Tipo.VALOR_FIXO, valor=50)
        self.assertEqual(cupom.calcular_desconto(Decimal("30")), Decimal("30.00"))

    def test_frete_gratis_nao_desconta_subtotal(self):
        cupom = Cupom.objects.create(codigo="FG", tipo=Cupom.Tipo.FRETE_GRATIS)
        self.assertEqual(cupom.calcular_desconto(Decimal("100")), Decimal("0.00"))
        self.assertTrue(cupom.frete_gratis)

    def test_inativo_invalido(self):
        Cupom.objects.create(codigo="OFF", tipo=Cupom.Tipo.PERCENTUAL, valor=10, ativo=False)
        cupom, erro = buscar_cupom_valido("OFF", Decimal("100"))
        self.assertIsNone(cupom)
        self.assertIn("ativo", erro)

    def test_vencido_invalido(self):
        Cupom.objects.create(
            codigo="VELHO", tipo=Cupom.Tipo.PERCENTUAL, valor=10,
            data_fim=timezone.now() - timedelta(days=1),
        )
        cupom, erro = buscar_cupom_valido("VELHO", Decimal("100"))
        self.assertIsNone(cupom)

    def test_fora_do_periodo_inicial_invalido(self):
        Cupom.objects.create(
            codigo="FUTURO", tipo=Cupom.Tipo.PERCENTUAL, valor=10,
            data_inicio=timezone.now() + timedelta(days=1),
        )
        cupom, _ = buscar_cupom_valido("FUTURO", Decimal("100"))
        self.assertIsNone(cupom)

    def test_uso_maximo_atingido_invalido(self):
        Cupom.objects.create(
            codigo="LIMITE", tipo=Cupom.Tipo.PERCENTUAL, valor=10,
            uso_maximo=1, usos_realizados=1,
        )
        cupom, _ = buscar_cupom_valido("LIMITE", Decimal("100"))
        self.assertIsNone(cupom)

    def test_valor_minimo_valida_subtotal(self):
        Cupom.objects.create(
            codigo="MIN", tipo=Cupom.Tipo.PERCENTUAL, valor=10,
            valor_minimo_pedido=Decimal("100"),
        )
        cupom, _ = buscar_cupom_valido("MIN", Decimal("50"))
        self.assertIsNone(cupom)
        cupom, _ = buscar_cupom_valido("MIN", Decimal("150"))
        self.assertIsNotNone(cupom)

    def test_registrar_uso_incrementa(self):
        cupom = Cupom.objects.create(codigo="USO", tipo=Cupom.Tipo.PERCENTUAL, valor=10)
        registrar_uso(cupom)
        cupom.refresh_from_db()
        self.assertEqual(cupom.usos_realizados, 1)

    def test_registrar_uso_respeita_limite(self):
        cupom = Cupom.objects.create(
            codigo="USO1", tipo=Cupom.Tipo.PERCENTUAL, valor=10,
            uso_maximo=1, usos_realizados=1,
        )
        with self.assertRaises(CupomIndisponivel):
            registrar_uso(cupom)

    def test_codigo_normalizado_para_maiusculas(self):
        cupom = Cupom.objects.create(codigo="  minusculo ", tipo=Cupom.Tipo.PERCENTUAL, valor=5)
        self.assertEqual(cupom.codigo, "MINUSCULO")
