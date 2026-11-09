from django.db import models


class Projeto(models.Model):
    STATUS_CHOICES = [
        ("Pendente", "Pendente"),
        ("Em Andamento", "Em Andamento"),
        ("Concluído", "Concluído"),
    ]

    titulo = models.CharField(max_length=255)
    descricao = models.TextField()
    data_criacao = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="Pendente",
    )

    class Meta:
        verbose_name = "Projeto"
        verbose_name_plural = "Projetos"

    def __str__(self):
        return self.titulo


class Tarefa(models.Model):
    STATUS_CHOICES = [
        ("Pendente", "Pendente"),
        ("Em Andamento", "Em Andamento"),
        ("Concluída", "Concluída"),
    ]

    titulo = models.CharField(max_length=255)
    descricao = models.TextField()
    data_criacao = models.DateTimeField(auto_now_add=True)
    prazo_entrega = models.DateField()
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="Pendente",
    )
    projeto = models.ForeignKey(
        Projeto,
        on_delete=models.CASCADE,
        related_name="tarefas",
    )

    class Meta:
        verbose_name = "Tarefa"
        verbose_name_plural = "Tarefas"

    def __str__(self):
        return f"{self.titulo} ({self.projeto.titulo})"
