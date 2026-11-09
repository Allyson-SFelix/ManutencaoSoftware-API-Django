from datetime import date

from rest_framework import serializers

from .models import Projeto, Tarefa


class ProjetoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Projeto
        fields = ["id", "titulo", "descricao", "data_criacao", "status"]
        read_only_fields = ["id", "data_criacao"]


class TarefaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tarefa
        fields = [
            "id",
            "titulo",
            "descricao",
            "data_criacao",
            "prazo_entrega",
            "status",
            "projeto",
        ]
        read_only_fields = ["id", "data_criacao"]

    def validate(self, attrs):
        prazo_entrega = attrs.get(
            "prazo_entrega",
            self.instance.prazo_entrega if self.instance else None,
        )
        if prazo_entrega is not None and prazo_entrega < date.today():
            raise serializers.ValidationError(
                {"prazo_entrega": "O prazo de entrega não pode estar no passado."}
            )

        projeto = attrs.get("projeto")
        if projeto is not None and projeto.status == "Concluído":
            raise serializers.ValidationError(
                {"projeto": "Não é possível associar uma tarefa a um projeto concluído."}
            )

        return attrs
