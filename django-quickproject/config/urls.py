from django.contrib import admin
git add .from django.urls import include, path
from rest_framework.routers import DefaultRouter

from projetos.views import ProjetoViewSet, TarefaViewSet

router = DefaultRouter()
router.register("projetos", ProjetoViewSet)
router.register("tarefas", TarefaViewSet)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include(router.urls)),
]
