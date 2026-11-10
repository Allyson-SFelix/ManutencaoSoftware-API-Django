# Métrica: cobertura de testes

- **Data da medição:** 10/11/2026
- **Resultado:** 94% (62 de 66 instruções)
- **Testes executados:** 4, todos aprovados.
- **Escopo de cobertura:** `projetos/models.py`,
  `projetos/serializers.py` e `projetos/views.py`.
- **Exclusões:** o próprio código de testes, configurações do Django e
  migrações.
- **Ferramenta:** Coverage.py 7.17.2, incluída em
  `django-quickproject/requirements.txt`.

Para reproduzir a medição a partir de `django-quickproject`:

```powershell
.\.venv\Scripts\python.exe -m coverage erase
.\.venv\Scripts\python.exe -m coverage run --source=projetos.models,projetos.serializers,projetos.views manage.py test projetos
.\.venv\Scripts\python.exe -m coverage report -m
```

As quatro instruções não cobertas na medição correspondem a caminhos auxiliares
dos models, incluindo representações em texto e erros de validação do model.
As validações expostas pela API são exercitadas pelos testes de regras de
negócio.
