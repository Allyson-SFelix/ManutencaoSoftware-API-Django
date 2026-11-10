# Métrica: quantidade de linhas de código

- **Data da medição:** 10/11/2026
- **Resultado:** 239 linhas
- **Escopo:** arquivos Python de produção em `django-quickproject/manage.py`,
  `django-quickproject/config/` e no nível principal de
  `django-quickproject/projetos/`.
- **Exclusões:** linhas vazias, linhas cujo primeiro caractere não branco é
  `#`, testes e arquivos de migração.
- **Método:** contagem de linhas físicas não vazias e não comentadas. Linhas de
  documentação (docstrings) são incluídas.

Para reproduzir a contagem com Python a partir de `django-quickproject`:

```powershell
@'
from pathlib import Path

paths = [
    Path("manage.py"),
    *sorted(Path("config").glob("*.py")),
    *sorted(Path("projetos").glob("*.py")),
]
paths = [path for path in paths if path.name != "tests.py"]
total = sum(
    1
    for path in paths
    for line in path.read_text(encoding="utf-8").splitlines()
    if line.strip() and not line.lstrip().startswith("#")
)
print(total)
'@ | .\.venv\Scripts\python.exe -
```
