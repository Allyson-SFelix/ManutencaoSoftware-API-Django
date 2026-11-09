from rest_framework.viewsets import ModelViewSet

from .models import Projeto, Tarefa
from .serializers import ProjetoSerializer, TarefaSerializer


class ProjetoViewSet(ModelViewSet):
    queryset = Projeto.objects.all()
    serializer_class = ProjetoSerializer


class TarefaViewSet(ModelViewSet):
    queryset = Tarefa.objects.select_related("projeto").all()
    serializer_class = TarefaSerializer
