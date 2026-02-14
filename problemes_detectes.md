-------------------------------------------------------------------
# Linting avec Ruff
----------------------------------------------------------------------

ines@DESKTOP-DK2UDN1:/mnt/c/Users/ins expertise/Documents/SIMPLON/projet-accidents_routiers/Accident-Severity-Prediction-Road-Safety-AI-Project-/back$ uv run ruff check .
I001 [*] Import block is un-sorted or un-formatted
  --> app/api/deps.py:15:1
   |
13 |   """
14 |
15 | / from typing import Annotated, Generator
16 | | from fastapi import Depends, HTTPException, Header, Query, status
17 | | from sqlmodel import Session
18 | | from app.database import get_session
   | |____________________________________^
19 |
20 |   # =============================
   |
help: Organize imports

F401 [*] `typing.Generator` imported but unused
  --> app/api/deps.py:15:31
   |
13 | """
14 |
15 | from typing import Annotated, Generator
   |                               ^^^^^^^^^
16 | from fastapi import Depends, HTTPException, Header, Query, status
17 | from sqlmodel import Session
   |
help: Remove unused import: `typing.Generator`

I001 [*] Import block is un-sorted or un-formatted
 --> app/api/v1/api.py:1:1
  |
1 | / from fastapi import APIRouter
2 | | from app.api.v1.endpoints import accidents
  | |__________________________________________^
3 |
4 |   api_router = APIRouter()
  |
help: Organize imports

I001 [*] Import block is un-sorted or un-formatted
  --> app/api/v1/endpoints/accidents.py:1:1
   |
 1 | / from typing import List
 2 | | import logging
 3 | | from fastapi import APIRouter, HTTPException, status
 4 | |
 5 | | from app.api.deps import SessionDep, PaginationDep
 6 | | from app.schemas.accident import AccidentInput
 7 | | from app.models.accident import Accident
 8 | | from app.repositories.accident_repository import AccidentRepository
 9 | | from app.services.accident_service import AccidentService
   | |_________________________________________________________^
10 |
11 |   logger = logging.getLogger(__name__)
   |
help: Organize imports

I001 [*] Import block is un-sorted or un-formatted
 --> app/core/config.py:1:1
  |
1 | / from pydantic_settings import BaseSettings
2 | | from pathlib import Path
  | |________________________^
3 |
4 |   class Settings(BaseSettings):
  |
help: Organize imports

I001 [*] Import block is un-sorted or un-formatted
  --> app/core/logging.py:4:1
   |
 2 |   """Configuration centralisée du logging"""
 3 |
 4 | / import logging
 5 | | import logging.handlers
 6 | | import sys
 7 | | from pathlib import Path
 8 | | from app.core.config import settings
   | |____________________________________^
 9 |
10 |   # Créer le dossier logs si nécessaire
   |
help: Organize imports

I001 [*] Import block is un-sorted or un-formatted
  --> app/core/security.py:21:1
   |
19 |   """
20 |
21 | / from passlib.context import CryptContext
22 | | from datetime import datetime, timedelta
23 | | from typing import Optional
24 | | import secrets
   | |______________^
25 |
26 |   # Context pour le hashing de mots de passe
   |
help: Organize imports

F401 [*] `datetime.datetime` imported but unused
  --> app/core/security.py:22:22
   |
21 | from passlib.context import CryptContext
22 | from datetime import datetime, timedelta
   |                      ^^^^^^^^
23 | from typing import Optional
24 | import secrets
   |
help: Remove unused import: `datetime.datetime`

I001 [*] Import block is un-sorted or un-formatted
  --> app/database.py:16:1
   |
14 |   """
15 |
16 | / from typing import Annotated, Generator
17 | | from contextlib import contextmanager
18 | | from fastapi import Depends
19 | | from sqlmodel import Session, SQLModel, create_engine
20 | | from app.core.config import settings
21 | | import logging
   | |______________^
22 |
23 |   logger = logging.getLogger(__name__)
   |
help: Organize imports

E501 Line too long (119 > 100)
  --> app/database.py:45:102
   |
43 | engine = create_engine(settings.DATABASE_URL, **engine_config)
44 |
45 | logger.info(f"🗄️  Engine DB créé: {settings.DATABASE_URL.split('@')[-1] if '@'  in settings.DATABASE_URL else 'SQLite'}")
   |
                     ^^^^^^^^^^^^^^^^^^^
   |

I001 [*] Import block is un-sorted or un-formatted
  --> app/main.py:1:1
   |
 1 | / from fastapi import FastAPI, Request, status
 2 | | from fastapi.exceptions import RequestValidationError
 3 | | from fastapi.responses import JSONResponse
 4 | |
 5 | | from app.core.config import settings
 6 | | from app.core.logging import setup_logging, logger
 7 | | from app.database import create_db_and_tables
 8 | | from app.api.v1.api import api_router
   | |_____________________________________^
 9 |
10 |   # Configurer le logging
   |
help: Organize imports

I001 [*] Import block is un-sorted or un-formatted
 --> app/models/accident.py:1:1
  |
1 | / from typing import Optional
2 | | from sqlmodel import Field, SQLModel
3 | | from app.models.base import TimestampMixin
  | |__________________________________________^
  |
help: Organize imports

F401 [*] `sqlmodel.SQLModel` imported but unused
 --> app/models/accident.py:2:29
  |
1 | from typing import Optional
2 | from sqlmodel import Field, SQLModel
  |                             ^^^^^^^^
3 | from app.models.base import TimestampMixin
  |
help: Remove unused import: `sqlmodel.SQLModel`

I001 [*] Import block is un-sorted or un-formatted
  --> app/models/base.py:13:1
   |
11 |   """
12 |
13 | / from datetime import datetime
14 | | from typing import Optional
15 | | from sqlmodel import Field, SQLModel
   | |____________________________________^
   |
help: Organize imports

I001 [*] Import block is un-sorted or un-formatted
 --> app/repositories/accident_repository.py:1:1
  |
1 | / from sqlmodel import Session
2 | | from app.models.accident import Accident
3 | | from app.repositories.base import BaseRepository
  | |________________________________________________^
  |
help: Organize imports

I001 [*] Import block is un-sorted or un-formatted
  --> app/repositories/base.py:23:1
   |
21 |   """
22 |
23 | / from typing import Generic, TypeVar, Type, List, Optional
24 | | from sqlmodel import Session, select, SQLModel, col
   | |___________________________________________________^
25 |
26 |   # TypeVar permet de créer des génériques type-safe
   |
help: Organize imports

I001 [*] Import block is un-sorted or un-formatted
 --> app/schemas/accident.py:1:1
  |
1 | from pydantic import BaseModel
  | ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2 |
3 | class AccidentInput(BaseModel):
  |
help: Organize imports

I001 [*] Import block is un-sorted or un-formatted
 --> app/services/accident_service.py:1:1
  |
1 | / from app.models.accident import Accident
2 | | from app.schemas.accident import AccidentInput
3 | | from app.repositories.accident_repository import AccidentRepository
4 | | from app.services.ml_service import ml_service
  | |______________________________________________^
5 |
6 |   class AccidentService:
  |
help: Organize imports

I001 [*] Import block is un-sorted or un-formatted
 --> app/services/ml_service.py:2:1
  |
1 |   # app/services/ml_service.py
2 | / import joblib
3 | | import pandas as pd
4 | | import logging
5 | | from app.core.config import settings
  | |____________________________________^
6 |
7 |   logger = logging.getLogger(__name__)
  |
help: Organize imports

F401 [*] `pytest` imported but unused
  --> tests/unit/test_api.py:11:8
   |
 9 | """
10 |
11 | import pytest
   |        ^^^^^^
12 | from fastapi.testclient import TestClient
   |
help: Remove unused import: `pytest`

F401 [*] `fastapi.testclient.TestClient` imported but unused
  --> tests/unit/test_api.py:12:32
   |
11 | import pytest
12 | from fastapi.testclient import TestClient
   |                                ^^^^^^^^^^
   |
help: Remove unused import: `fastapi.testclient.TestClient`

I001 [*] Import block is un-sorted or un-formatted
  --> tests/unit/test_models.py:15:1
   |
13 |   """
14 |
15 | / import pytest
16 | | from app.models.accident import Accident
   | |________________________________________^
   |
help: Organize imports

I001 [*] Import block is un-sorted or un-formatted
 --> tests/unit/test_repositories.py:3:1
  |
1 |   """Tests unitaires pour les repositories"""
2 |
3 | / import pytest
4 | | from app.models.accident import Accident
5 | | from app.repositories.accident_repository import AccidentRepository
  | |___________________________________________________________________^
  |
help: Organize imports

F401 [*] `pytest` imported but unused
 --> tests/unit/test_repositories.py:3:8
  |
1 | """Tests unitaires pour les repositories"""
2 |
3 | import pytest
  |        ^^^^^^
4 | from app.models.accident import Accident
5 | from app.repositories.accident_repository import AccidentRepository
  |
help: Remove unused import: `pytest`

Found 24 errors.
[*] 23 fixable with the `--fix` option.

-------------------------------------------------------------------
# Type checking avec Mypy
----------------------------------------------------------------------

ines@DESKTOP-DK2UDN1:/mnt/c/Users/ins expertise/Documents/SIMPLON/projet-accidents_routiers/Accident-Severity-Prediction-Road-Safety-AI-Project-/back$ uv run mypy app/
app/core/security.py:21: error: Library stubs not installed for "passlib.context"  [import-untyped]
app/core/security.py:21: note: Hint: "python3 -m pip install types-passlib"
app/core/security.py:21: note: (or run "mypy --install-types" to install all missing stub packages)
app/core/security.py:21: note: See https://mypy.readthedocs.io/en/stable/running_mypy.html#missing-imports
app/services/ml_service.py:2: error: Skipping analyzing "joblib": module is installed, but missing library stubs or py.typed marker  [import-untyped]
app/services/ml_service.py:3: error: Library stubs not installed for "pandas"  [import-untyped]
app/services/ml_service.py:3: note: Hint: "python3 -m pip install pandas-stubs"
app/repositories/base.py:151: error: "type[ModelType]" has no attribute "id"  [attr-defined]
app/database.py:199: error: No overload variant of "exec" of "Session" matches argument type "str"  [call-overload]
app/database.py:199: note: Possible overload variants:
app/database.py:199: note:     def [_TSelectParam: Any] exec(self, statement: Select[_TSelectParam], *, params: Mapping[str, Any] | Sequence[Mapping[str, Any]] | None = ..., execution_options: Mapping[str, Any] = ..., bind_arguments: dict[str, Any] | None = ..., _parent_execute_state: Any | None = ..., _add_event: Any | None = ...) -> TupleResult[_TSelectParam]
app/database.py:199: note:     def [_TSelectParam: Any] exec(self, statement: SelectOfScalar[_TSelectParam], *, params: Mapping[str, Any] | Sequence[Mapping[str, Any]] | None = ..., execution_options: Mapping[str, Any] = ..., bind_arguments: dict[str, Any] | None = ..., _parent_execute_state: Any | None = ..., _add_event: Any | None = ...) -> ScalarResult[_TSelectParam]
app/database.py:199: note:     def exec(self, statement: UpdateBase, *, params: Mapping[str, Any] | Sequence[Mapping[str, Any]] | None = ..., execution_options: Mapping[str, Any] = ..., bind_arguments: dict[str, Any] | None = ..., _parent_execute_state: Any | None = ..., _add_event: Any | None = ...) -> CursorResult[Any]
Found 5 errors in 4 files (checked 25 source files)

-------------------------------------------------------------------
# Tests
----------------------------------------------------------------------

ines@DESKTOP-DK2UDN1:/mnt/c/Users/ins expertise/Documents/SIMPLON/projet-accidents_routiers/Accident-Severity-Prediction-Road-Safety-AI-Project-/back$ uv run pytest
=============================== test session starts ================================
platform linux -- Python 3.14.3, pytest-9.0.2, pluggy-1.6.0
rootdir: /mnt/c/Users/ins expertise/Documents/SIMPLON/projet-accidents_routiers/Accident-Severity-Prediction-Road-Safety-AI-Project-/back
configfile: pyproject.toml
testpaths: tests
plugins: anyio-4.12.1, cov-7.0.0
collected 12 items / 1 error

====================================== ERRORS ======================================
_____________________ ERROR collecting tests/unit/test_api.py ______________________
.venv/lib/python3.14/site-packages/starlette/testclient.py:38: in <module>
    import httpx
E   ModuleNotFoundError: No module named 'httpx'

During handling of the above exception, another exception occurred:
tests/unit/test_api.py:12: in <module>
    from fastapi.testclient import TestClient
.venv/lib/python3.14/site-packages/fastapi/testclient.py:1: in <module>
    from starlette.testclient import TestClient as TestClient  # noqa
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.venv/lib/python3.14/site-packages/starlette/testclient.py:40: in <module>
    raise RuntimeError(
E   RuntimeError: The starlette.testclient module requires the httpx package to be installed.
E   You can install this with:
E       $ pip install httpx
============================= short test summary info ==============================
ERROR tests/unit/test_api.py - RuntimeError: The starlette.testclient module requires the httpx package to be ...
!!!!!!!!!!!!!!!!!!!!!! Interrupted: 1 error during collection !!!!!!!!!!!!!!!!!!!!!!
================================ 1 error in 21.15s =================================

-------------------------------------------------------------------
# Optionnel - Sécurité avec Bandit
----------------------------------------------------------------------

ines@DESKTOP-DK2UDN1:/mnt/c/Users/ins expertise/Documents/SIMPLON/projet-accidents_routiers/Accident-Severity-Prediction-Road-Safety-AI-Project-/back$ uv run bandit -r app/
[main]  INFO    profile include tests: None
[main]  INFO    profile exclude tests: None
[main]  INFO    cli include tests: None
[main]  INFO    cli exclude tests: None
[main]  INFO    running on Python 3.14.3
Run started:2026-02-13 09:58:35.058962+00:00

Test results:
        No issues identified.

Code scanned:
        Total lines of code: 796
        Total lines skipped (#nosec): 0

Run metrics:
        Total issues (by severity):
                Undefined: 0
                Low: 0
                Medium: 0
                High: 0
        Total issues (by confidence):
                Undefined: 0
                Low: 0
                Medium: 0
                High: 0
Files skipped (0):

# 🔍 Problèmes Détectés - Accident Severity Prediction API

**Date :** 2026-02-13
**Analysé par :** Ines Marouani
**Outils :** Ruff, Mypy, Pytest

---

## 📋 Problèmes par Catégorie

### 🎨 Formatage (19 problèmes)

1. **Imports mal ordonnés** - `app/api/deps.py:15`
   - Imports non triés selon la convention PEP8

2. **Imports mal ordonnés** - `app/api/v1/api.py:1`
   - Imports non triés

3. **Imports mal ordonnés** - `app/api/v1/endpoints/accidents.py:1`
   - Imports non triés

4. **Imports mal ordonnés** - `app/core/config.py:1`
   - Imports non triés

5. **Imports mal ordonnés** - `app/core/logging.py:4`
   - Imports non triés

6. **Imports mal ordonnés** - `app/core/security.py:21`
   - Imports non triés

7. **Imports mal ordonnés** - `app/database.py:16`
   - Imports non triés

8. **Imports mal ordonnés** - `app/main.py:1`
   - Imports non triés

9. **Imports mal ordonnés** - `app/models/accident.py:1`
   - Imports non triés

10. **Imports mal ordonnés** - `app/models/base.py:13`
    - Imports non triés

11. **Imports mal ordonnés** - `app/repositories/accident_repository.py:1`
    - Imports non triés

12. **Imports mal ordonnés** - `app/repositories/base.py:23`
    - Imports non triés

13. **Imports mal ordonnés** - `app/schemas/accident.py:1`
    - Imports non triés

14. **Imports mal ordonnés** - `app/services/accident_service.py:1`
    - Imports non triés

15. **Imports mal ordonnés** - `app/services/ml_service.py:2`
    - Imports non triés

16. **Imports mal ordonnés** - `tests/unit/test_models.py:15`
    - Imports non triés

17. **Imports mal ordonnés** - `tests/unit/test_repositories.py:3`
    - Imports non triés

18. **Imports mal ordonnés** - `tests/unit/test_api.py`
    - Imports non triés

19. **Ligne trop longue** - `app/database.py:45`
    - 119 caractères (limite : 100)

---

### 🔒 Sécurité (0 problème détecté)

✅ **Bandit - Aucun problème de sécurité détecté**

- Total lignes analysées : 796
- Secrets en dur : 0
- Vulnérabilités : 0
- Issues High/Medium/Low : 0/0/0

Le code est **sécurisé** selon l'analyse de Bandit.

---

### 📦 Imports (6 problèmes)

20. **Import inutilisé** - `app/api/deps.py:15`
    - `typing.Generator` importé mais jamais utilisé

21. **Import inutilisé** - `app/core/security.py:22`
    - `datetime.datetime` importé mais jamais utilisé

22. **Import inutilisé** - `app/models/accident.py:2`
    - `sqlmodel.SQLModel` importé mais jamais utilisé

23. **Import inutilisé** - `tests/unit/test_api.py:11`
    - `pytest` importé mais jamais utilisé

24. **Import inutilisé** - `tests/unit/test_api.py:12`
    - `TestClient` importé mais jamais utilisé

25. **Import inutilisé** - `tests/unit/test_repositories.py:3`
    - `pytest` importé mais jamais utilisé

---

### 🏷️ Types (5 problèmes)

26. **Stubs manquants** - `app/core/security.py:21`
    - Bibliothèque `passlib.context` sans stubs de typage

27. **Stubs manquants** - `app/services/ml_service.py:2`
    - Bibliothèque `joblib` sans stubs de typage

28. **Stubs manquants** - `app/services/ml_service.py:3`
    - Bibliothèque `pandas` sans stubs de typage

29. **Erreur de typage** - `app/repositories/base.py:151`
    - `type[ModelType]` n'a pas d'attribut `id`

30. **Erreur de typage** - `app/database.py:199`
    - `Session.exec()` ne prend pas de string brute en argument

---

### 📝 Documentation (0 problème mesuré)

Non vérifié automatiquement dans cette analyse.

*(Nécessiterait inspection manuelle ou outil spécialisé comme pydocstyle)*

---

### ♻️ Code mort (0 problème détecté)

Aucune variable inutilisée ou fonction obsolète détectée par Ruff.

---

## 🚨 Problème Bloquant

**31. Dépendance manquante** - `tests/unit/test_api.py`
- **Erreur :** `ModuleNotFoundError: No module named 'httpx'`
- **Impact :** Les tests ne peuvent pas s'exécuter
- **Solution :** `uv add --dev httpx`

---

## ❓ Questions de Réflexion

### 1. Le code fonctionne, mais :

**Est-il maintenable ?**
- ⚠️ **Partiellement** : Les imports désorganisés rendent le code difficile à lire. Les imports inutilisés créent de la confusion sur les dépendances réelles. L'absence de typage complet (stubs manquants) rend le refactoring plus risqué.

**Est-il sécurisé ?**
- ✅ **Oui** : Aucun secret en dur, mot de passe ou clé API détecté. Bandit a analysé 796 lignes de code sans identifier de vulnérabilité.

**Est-il bien documenté ?**
- ❓ **Non vérifié** : Pas d'analyse automatique effectuée sur les docstrings. Inspection manuelle nécessaire.

---

### 2. Comment détecter ces problèmes automatiquement ?

**Quels outils utiliser ?**

| Problème | Outil | Commande |
|----------|-------|----------|
| Formatage & Imports | **Ruff** | `uv run ruff check .` |
| Typage | **Mypy** | `uv run mypy app/` |
| Sécurité | **Bandit** | `uv run bandit -r app/` |
| Tests | **Pytest** | `uv run pytest` |
| Documentation | **pydocstyle** | `uv run pydocstyle app/` |

**À quel moment les exécuter ?**
- **Avant chaque commit** : Pre-commit hooks
- **À chaque push** : Pipeline CI/CD (GitHub Actions)
- **Avant chaque merge** : Vérification automatique sur les Pull Requests

---

### 3. Comment empêcher ces problèmes à l'avenir ?

**Solutions à mettre en place :**

1. **Pre-commit hooks** (Phase 4)
   - Bloque les commits non conformes localement
   - Exécute Ruff, Mypy avant chaque commit

2. **Pipeline CI/CD** (Phase 3)
   - Automatise les vérifications sur GitHub Actions
   - Bloque les merges si les checks échouent

3. **Protection des branches** (Phase 2) ✅
   - Déjà fait : `main` et `develop` protégées
   - Nécessite que les status checks passent

4. **Conventional Commits** (Phase 2) ✅
   - Déjà appliqué : historique lisible

5. **Configuration des outils** (Phase 3)
   - `pyproject.toml` enrichi avec règles strictes
   - Configuration partagée dans le repo

6. **Culture d'équipe**
   - Code reviews systématiques
   - Documentation des standards

---

## 📊 Résumé

- **Total de problèmes :** 31
- **Auto-corrigibles :** 23 (imports mal ordonnés + imports inutilisés)
- **Nécessitent intervention :** 8 (typage, ligne longue, dépendance)
- **Bloquants :** 1 (httpx manquant)

**Prochaine étape :** Mettre en place le pipeline CI/CD pour automatiser ces vérifications.
