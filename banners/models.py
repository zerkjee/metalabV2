from django.db import models


class Banner(models.Model):
    titulo = models.CharField("título", max_length=200, blank=True)
    subtitulo = models.CharField("subtítulo", max_length=300, blank=True)
    imagem = models.ImageField(upload_to="banners/")
    link = models.URLField(blank=True)
    texto_botao = models.CharField("texto do botão", max_length=60, blank=True)
    ativo = models.BooleanField(default=True)
    ordem = models.PositiveIntegerField(default=0)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["ordem", "-criado_em"]

    def __str__(self):
        return self.titulo or f"Banner #{self.pk}"
