# ManutencaoSoftware-API-Django

API REST desenvolvida com Django e Django REST Framework para gerenciamento de
projetos e tarefas. Um projeto pode possuir várias tarefas.

## Tecnologias

- Python 3.12
- Django 4.2
- Django REST Framework
- SQLite
- Testes de API com `APITestCase`

## Organização do projeto

```text
.
├── README.md
├── metricas/
└── django-quickproject/
    ├── manage.py
    ├── requirements.txt
    ├── config/       # Configurações e rotas do Django
    └── projetos/     # Models, serializers, views, rotas via router e testes
```

`config` contém a configuração do projeto Django. A aplicação `projetos`
concentra os models `Projeto` e `Tarefa`, a serialização JSON, os endpoints
CRUD e os testes. Essa separação mantém a estrutura convencional do Django sem
duplicar configurações ou espalhar a lógica do domínio.

## Requisitos

- Python 3.12 ou compatível com Django 4.2
- PowerShell no Windows (ou terminal equivalente)

## Instalação e execução local

No PowerShell, na raiz do repositório:

```powershell
cd django-quickproject
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe manage.py migrate
.\.venv\Scripts\python.exe manage.py runserver
```

A API ficará disponível em `http://127.0.0.1:8000/`. O banco SQLite
`db.sqlite3` é criado localmente pelas migrações.

## Endpoints

| Método | Endpoint | Ação |
|---|---|---|
| GET, POST | `/api/projetos/` | Listar e cadastrar projetos |
| GET, PUT, PATCH, DELETE | `/api/projetos/{id}/` | Consultar, atualizar e excluir projeto |
| GET, POST | `/api/tarefas/` | Listar e cadastrar tarefas |
| GET, PUT, PATCH, DELETE | `/api/tarefas/{id}/` | Consultar, atualizar e excluir tarefa |

As respostas e requisições usam JSON. Uma tarefa deve informar o identificador
do projeto associado, além de `titulo`, `descricao` e `prazo_entrega` no formato
`AAAA-MM-DD`. Os statuses aceitos são:

- Projeto: `Pendente`, `Em Andamento`, `Concluído`
- Tarefa: `Pendente`, `Em Andamento`, `Concluída`

Exemplo de cadastro de tarefa (`POST /api/tarefas/`):

```json
{
  "titulo": "Preparar entrega",
  "descricao": "Revisar os itens do projeto",
  "prazo_entrega": "2026-12-01",
  "status": "Pendente",
  "projeto": 1
}
```

O valor de `projeto` deve ser o ID de um projeto existente e não concluído.

## Regras de negócio

- O prazo de entrega da tarefa não pode estar no passado, tanto ao cadastrar
  quanto ao atualizar.
- Uma tarefa não pode ser criada em um projeto concluído nem ter seu projeto
  alterado para um projeto concluído.
- Violações de validação da API retornam `400 Bad Request`.

## Testes

Execute os testes de API a partir de `django-quickproject`:

```powershell
.\.venv\Scripts\python.exe manage.py test projetos
```

Os testes cobrem cadastro e listagem de projetos e tarefas, atualização e
exclusão de ambos os recursos e rejeição das regras de negócio.

## Métricas

Os relatórios de quantidade de linhas de código e cobertura estão em
[`metricas/`](./metricas/). Os comandos para reproduzir cada medição estão nos
respectivos relatórios.

## Observação de implantação

As configurações atuais são apropriadas para desenvolvimento local. Antes de
publicar em produção, configure segredo, `DEBUG`, hosts permitidos e demais
opções de segurança para o ambiente de implantação.
