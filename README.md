
```
fastapi
├─ .gitignore
├─ alembic.ini
├─ Dockerfile
├─ migration
│  ├─ env.py
│  ├─ README
│  └─ script.py.mako
├─ pytest.ini
├─ README.md
├─ requirements.txt
├─ src
│  ├─ auth
│  │  ├─ models.py
│  │  ├─ router.py
│  │  ├─ schema.py
│  │  └─ utils.py
│  ├─ config.py
│  ├─ countries
│  │  ├─ models.py
│  │  ├─ posts
│  │  │  ├─ models.py
│  │  │  ├─ replies
│  │  │  │  ├─ models.py
│  │  │  │  ├─ router.py
│  │  │  │  ├─ schemas.py
│  │  │  │  └─ utils.py
│  │  │  ├─ router.py
│  │  │  ├─ schemas.py
│  │  │  └─ utils.py
│  │  ├─ router.py
│  │  ├─ schemas.py
│  │  └─ utils.py
│  ├─ database.py
│  ├─ main.py
│  ├─ mappers
│  │  └─ models.py
│  └─ models.py
├─ test.db
└─ tests
   ├─ config.py
   ├─ test_auth.py
   └─ __init__.py

```