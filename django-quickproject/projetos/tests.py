from datetime import date, timedelta

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Projeto, Tarefa


class ProjetoETarefaAPITests(APITestCase):
    def criar_projeto(self, **kwargs):
        dados = {
            "titulo": "Projeto de teste",
            "descricao": "Descricao do projeto",
            "status": "Pendente",
        }
        dados.update(kwargs)
        return Projeto.objects.create(**dados)

    def criar_tarefa(self, projeto, **kwargs):
        dados = {
            "titulo": "Tarefa de teste",
            "descricao": "Descricao da tarefa",
            "prazo_entrega": date.today() + timedelta(days=1),
            "status": "Pendente",
            "projeto": projeto,
        }
        dados.update(kwargs)
        return Tarefa.objects.create(**dados)

    def test_cadastro_com_sucesso(self):
        resposta_projeto = self.client.post(
            reverse("projeto-list"),
            {
                "titulo": "Novo projeto",
                "descricao": "Descricao do novo projeto",
                "status": "Pendente",
            },
            format="json",
        )

        self.assertEqual(resposta_projeto.status_code, status.HTTP_201_CREATED)

        resposta_tarefa = self.client.post(
            reverse("tarefa-list"),
            {
                "titulo": "Nova tarefa",
                "descricao": "Descricao da nova tarefa",
                "prazo_entrega": (date.today() + timedelta(days=1)).isoformat(),
                "status": "Pendente",
                "projeto": resposta_projeto.data["id"],
            },
            format="json",
        )

        self.assertEqual(resposta_tarefa.status_code, status.HTTP_201_CREATED)

    def test_consulta_listagem(self):
        projeto = self.criar_projeto()
        self.criar_tarefa(projeto)

        resposta_projetos = self.client.get(reverse("projeto-list"))
        resposta_tarefas = self.client.get(reverse("tarefa-list"))

        self.assertEqual(resposta_projetos.status_code, status.HTTP_200_OK)
        self.assertEqual(len(resposta_projetos.data), 1)
        self.assertEqual(resposta_tarefas.status_code, status.HTTP_200_OK)
        self.assertEqual(len(resposta_tarefas.data), 1)

    def test_atualizacao_e_exclusao(self):
        projeto = self.criar_projeto()
        tarefa = self.criar_tarefa(projeto)

        resposta_atualizacao = self.client.patch(
            reverse("tarefa-detail", args=[tarefa.id]),
            {"titulo": "Tarefa atualizada"},
            format="json",
        )
        self.assertEqual(resposta_atualizacao.status_code, status.HTTP_200_OK)
        self.assertEqual(resposta_atualizacao.data["titulo"], "Tarefa atualizada")

        resposta_exclusao = self.client.delete(
            reverse("tarefa-detail", args=[tarefa.id])
        )
        self.assertEqual(resposta_exclusao.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Tarefa.objects.filter(pk=tarefa.id).exists())

        resposta_atualizacao_projeto = self.client.patch(
            reverse("projeto-detail", args=[projeto.id]),
            {"titulo": "Projeto atualizado"},
            format="json",
        )
        self.assertEqual(
            resposta_atualizacao_projeto.status_code,
            status.HTTP_200_OK,
        )
        self.assertEqual(
            resposta_atualizacao_projeto.data["titulo"],
            "Projeto atualizado",
        )

        resposta_exclusao_projeto = self.client.delete(
            reverse("projeto-detail", args=[projeto.id])
        )
        self.assertEqual(
            resposta_exclusao_projeto.status_code,
            status.HTTP_204_NO_CONTENT,
        )
        self.assertFalse(Projeto.objects.filter(pk=projeto.id).exists())

    def test_regras_de_negocio(self):
        projeto = self.criar_projeto()
        projeto_concluido = self.criar_projeto(
            titulo="Projeto concluido",
            status="Concluído",
        )
        url_tarefas = reverse("tarefa-list")

        resposta_prazo_passado = self.client.post(
            url_tarefas,
            {
                "titulo": "Tarefa com prazo passado",
                "descricao": "Descricao da tarefa",
                "prazo_entrega": (date.today() - timedelta(days=1)).isoformat(),
                "status": "Pendente",
                "projeto": projeto.id,
            },
            format="json",
        )
        self.assertEqual(
            resposta_prazo_passado.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

        resposta_projeto_concluido = self.client.post(
            url_tarefas,
            {
                "titulo": "Tarefa em projeto concluido",
                "descricao": "Descricao da tarefa",
                "prazo_entrega": (date.today() + timedelta(days=1)).isoformat(),
                "status": "Pendente",
                "projeto": projeto_concluido.id,
            },
            format="json",
        )
        self.assertEqual(
            resposta_projeto_concluido.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

        tarefa = self.criar_tarefa(projeto)
        resposta_prazo_passado_atualizacao = self.client.patch(
            reverse("tarefa-detail", args=[tarefa.id]),
            {
                "prazo_entrega": (
                    date.today() - timedelta(days=1)
                ).isoformat()
            },
            format="json",
        )
        self.assertEqual(
            resposta_prazo_passado_atualizacao.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

        resposta_alteracao_projeto = self.client.patch(
            reverse("tarefa-detail", args=[tarefa.id]),
            {"projeto": projeto_concluido.id},
            format="json",
        )
        self.assertEqual(
            resposta_alteracao_projeto.status_code,
            status.HTTP_400_BAD_REQUEST,
        )
