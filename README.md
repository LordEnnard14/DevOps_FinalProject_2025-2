📚 Biblioteca DevOps
Proyecto Final – DevOps 2025-2

Este proyecto implementa un sistema completo de gestión de biblioteca utilizando una arquitectura moderna y un pipeline CI/CD profesional basado en GitHub Actions.

Incluye:

🔹 Backend en FastAPI

🔹 Frontend con Jinja2

🔹 Base de datos SQLite + migraciones con Alembic

🔹 Pruebas unitarias, API, funcionales (Selenium) y de rendimiento (JMeter)

🔹 Análisis de calidad de código

🔹 Cobertura ≥ 80% (alcanzado 93%)

🔹 Generación de artefactos (Wheel + ZIP Git Archive)

🔹 Pipeline CI/CD con 7 jobs encadenados

🔹 Simulación de despliegue continuo

🧩 1. Arquitectura del Proyecto
biblioteca-devops/
├── app/
│   ├── main.py           # FastAPI + rutas API + vistas Jinja
│   ├── auth.py           # Autenticación
│   ├── crud.py           # Lógica CRUD
│   ├── db.py             # Conexión SQLAlchemy + SessionLocal
│   ├── models.py         # Modelos ORM
│   └── schemas.py        # Pydantic Schemas
│
├── templates/            # Frontend Jinja2
│   ├── login.html
│   ├── books_list.html
│   ├── books_edit.html
│   └── books_new.html
│
├── tests/
│   ├── unit/             # Pruebas unitarias
│   ├── api/              # Pruebas API de FastAPI
│   ├── ui/               # Pruebas de vistas HTML
│   └── functional/       # Pruebas funcionales (Selenium)
│
├── postman/
│   └── biblioteca.postman_collection.json
│
├── jmeter/
│   └── api_books.jmx
│
├── alembic/
│   ├── env.py
│   └── versions/
│
├── dist/                 # Artefactos .whl generados
├── library.db            # Base de datos SQLite
├── requirements.txt
├── pyproject.toml
└── README.md

🛠️ 2. Tecnologías Utilizadas
Categoría	Herramienta
Backend	FastAPI
Frontend	Jinja2
Base de datos	SQLite
ORM	SQLAlchemy
Migraciones	Alembic
Calidad de código	Black, Isort, Flake8, Mypy
Pruebas unitarias	Pytest + Coverage
Pruebas API REST	Postman + Newman
Pruebas funcionales	Selenium
Pruebas de rendimiento	Apache JMeter
CI/CD	GitHub Actions
Artefactos	Wheel + Git Archive (ZIP)
🚀 3. Ejecución Local
3.1 Crear entorno virtual
python -m venv .venv
source .venv/bin/activate       # Linux/Mac
.\.venv\Scripts\activate        # Windows

3.2 Instalar dependencias
pip install -r requirements.txt

3.3 Correr la aplicación
uvicorn app.main:app --reload


La aplicación estará disponible en:

👉 http://127.0.0.1:8000/login

Usuario: admin
Contraseña: admin

🗄️ 4. Migraciones con Alembic
Inicializar Alembic
alembic init alembic

Crear migración
alembic revision -m "create books table" --autogenerate

Aplicar migración
alembic upgrade head

🧪 5. Pruebas Unitarias + Cobertura

Ejecutar:

pytest --cov=app --cov-report=term-missing


✔ Se exige mínimo 80%
✔ Proyecto alcanzó 93%

🧪 6. Pruebas Funcionales (Selenium)

Selenium se ejecuta contra el servidor FastAPI real.

Archivo:
tests/functional/test_login_selenium.py

Ejecutar local:
uvicorn app.main:app --reload
pytest tests/functional


Selenium verifica:

✔ Login
✔ Navegación
✔ Integración del frontend Jinja
✔ Flujo end-to-end

Se ejecuta también automáticamente en GitHub Actions.

🌐 7. Pruebas API REST (Postman + Newman)

Ejecutar:

newman run postman/biblioteca.postman_collection.json


La colección incluye assertions:

Código HTTP

JSON válido

Presencia de campos

Conteo y tipo de arreglo

⚡ 8. Pruebas de rendimiento (JMeter)

Ejecutar:

jmeter -n -t jmeter/api_books.jmx -l jmeter/results.jtl -e -o jmeter/report


Reportes HTML generados en:

jmeter/report/

📦 9. Artefactos del Proyecto
9.1 Paquete Wheel (Python Package)
python -m build


Se genera:

dist/*.whl

9.2 ZIP versionado (Git Archive)
git archive --format zip --output biblioteca-devops_1.0.0.zip HEAD


Incluye todo el código del repositorio en un solo artefacto descargable.

☁️ 10. Pipeline CI/CD (7 Jobs)

El pipeline está dividido según la rúbrica:

🟦 Fase 1 – Integración Continua (CI)
1️⃣ Calidad de Código

Black

Isort

Flake8

Mypy

2️⃣ Pruebas Unitarias + Cobertura

Pytest con cobertura mínima del 80%.

3️⃣ Pruebas de API REST (Newman)

Ejecuta colección de Postman.

🟧 Fase 2 – Entrega Continua (CD)
4️⃣ Pruebas de Rendimiento – JMeter

Simula múltiples usuarios.

5️⃣ Construcción de Artefactos

Wheel

ZIP versionado

6️⃣ Pruebas Funcionales – Selenium

Valida el funcionamiento extremo a extremo.

🟩 Fase 3 – Despliegue Continuo
7️⃣ Simulación de Deploy

Arranca FastAPI en puerto 9000

Ejecuta smoke test con curl

🧩 Diagrama CI/CD
Calidad → Tests → API → Rendimiento → Artefactos → Selenium → Deploy


Cada job sube sus reportes como artefactos descargables.

🚀 11. Simulación de Despliegue

El pipeline crea un entorno limpio, instala dependencias y ejecuta:

uvicorn app.main:app --host 0.0.0.0 --port 9000
curl -I http://127.0.0.1:9000/api/health


✔ Verificación automática
✔ Similar a entorno productivo
✔ Última etapa del ciclo CI/CD

🎯 Estado Actual del Proyecto
Módulo	Estado
Backend FastAPI	✔ Completo
Frontend Jinja2	✔ Completo
Migraciones Alembic	✔ Aplicadas
Pruebas unitarias	✔ 93% cobertura
Pruebas API	✔ Newman
Pruebas funcionales	✔ Selenium operativo
Pruebas de carga	✔ JMeter
CI/CD	✔ 7 Jobs
Artefactos	✔ Wheel + ZIP
🏁 Conclusión

Este proyecto implementa un pipeline CI/CD profesional, integrando:

Calidad

Testing

Seguridad

Artefactos

Validación E2E

Simulación de despliegue

Cumple y supera ampliamente los requisitos del curso DevOps.