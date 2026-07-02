import pedidos.models
from django.db import migrations, models


def preencher_tokens(apps, schema_editor):
    Pedido = apps.get_model("pedidos", "Pedido")
    for pedido in Pedido.objects.filter(recibo_token__isnull=True):
        token = pedidos.models.gerar_token_recibo()
        while Pedido.objects.filter(recibo_token=token).exists():
            token = pedidos.models.gerar_token_recibo()
        pedido.recibo_token = token
        pedido.save(update_fields=["recibo_token"])


class Migration(migrations.Migration):
    dependencies = [
        ("pedidos", "0002_pedido_idempotency_token"),
    ]

    operations = [
        migrations.AddField(
            model_name="pedido",
            name="recibo_token",
            field=models.CharField(max_length=96, null=True, blank=True),
        ),
        migrations.RunPython(preencher_tokens, migrations.RunPython.noop),
        migrations.AlterField(
            model_name="pedido",
            name="recibo_token",
            field=models.CharField(
                default=pedidos.models.gerar_token_recibo,
                max_length=96,
                unique=True,
            ),
        ),
    ]
