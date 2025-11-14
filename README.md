📚 Biblioteca DevOps — Proyecto Final

Sistema completo de gestión de biblioteca desarrollado como parte del Proyecto Final del curso de DevOps.
Incluye backend en FastAPI, frontend con Jinja2, versionado de base de datos, pruebas automatizadas, pipeline CI/CD multi-job, pruebas de rendimiento, artefactos versionados y análisis completo de calidad de código.

🚀 Tecnologías utilizadas

| Capa                   | Herramienta / Tecnología              |
| ---------------------- | ------------------------------------- |
| Backend                | FastAPI                               |
| Base de datos          | SQLite                                |
| ORM                    | SQLAlchemy                            |
| Migraciones            | Alembic                               |
| Frontend               | Jinja2                                |
| Pruebas unitarias      | Pytest                                |
| Cobertura              | pytest-cov                            |
| Calidad de código      | black, isort, flake8, mypy            |
| Pruebas API REST       | Postman + Newman                      |
| Pruebas de rendimiento | JMeter                                |
| CI/CD                  | GitHub Actions (multi-job)            |
| Artefactos             | git archive ZIP + Python wheel (.whl) |

📁 Estructura principal del proyecto

biblioteca-devops/
├── app/
│   ├── main.py
│   ├── auth.py
│   ├── crud.py
│   ├── db.py
│   ├── models.py
│   ├── schemas.py
│   └── __init__.py
├── templates/
│   ├── login.html
│   ├── list_books.html
│   ├── new_book.html
│   ├── edit_book.html
│   └── base.html
├── alembic/
│   ├── versions/
│   └── env.py
├── tests/
│   ├── unit/
│   ├── ui/
│   └── api/
├── postman/
│   └── biblioteca.postman_collection.json
├── jmeter/
│   └── api_books.jmx
├── dist/ (se genera en el pipeline)
├── Makefile
├── README.md
├── pyproject.toml
└── requirements.txt

🧱 Backend – FastAPI

El backend implementa:

CRUD completo para libros

Modelo Book (título, autor, ISBN, categoría, estado, timestamps)

Autenticación sencilla con cookies (login + logout)

Endpoints REST para integrarse con Postman/Newman y JMeter

Sistema MVC simple con templates Jinja

Para levantarlo:
uvicorn app.main:app --reload


🎨 Frontend – Jinja2

Cuenta con:

Página de login

Panel principal (lista de libros)

Crear libro

Editar libro

Eliminar libro

Plantilla base con navegación

Validación simple de formularios

🗄️ Versionado de Base de Datos – Alembic

Se usó Alembic + SQLAlchemy para versionar el esquema del proyecto.

Comandos utilizados:
alembic init alembic
alembic revision -m "create books table" --autogenerate
alembic upgrade head

Archivo de BD:

library.db

Justificación:

SQLite no requiere un servidor externo ni despliegue remoto → migraciones locales y versionamiento vía alembic/versions/*.

🧪 Pruebas Unitarias – Pytest

Se implementaron pruebas para:

CRUD de libros

API REST

Templates Jinja

Autenticación

Validaciones

Base de datos (uso de DB temporal)

Ejecutar pruebas:

pytest
Con cobertura (mínimo 80%):

bash
Copy code
pytest --cov=app --cov-report=html
Cobertura alcanzada: ~93%

🚦 Pruebas API – Postman + Newman
La colección Postman fue automatizada con Newman:

bash
Copy code
newman run postman/biblioteca.postman_collection.json
Incluye:

GET /api/health

POST /api/books

GET /api/books

Validaciones de estado HTTP

Assertions sobre la respuesta JSON

⚡ Pruebas de Rendimiento – JMeter
Archivo del plan de prueba:

bash
Copy code
jmeter/api_books.jmx
Ejecución automática:

bash
Copy code
jmeter -n -t jmeter/api_books.jmx -l jmeter/results.jtl -e -o jmeter/report
Se mide:

throughput

avg response time

errores

gráficos varias métricas

🧹 Calidad de Código
Se incluye pipeline de análisis estático:

black

isort

flake8

mypy

Se ejecuta automáticamente en el primer job del CI/CD.

📦 Versionado de Artefactos
ZIP versionado:
bash
Copy code
git archive --format zip --output biblioteca-devops_1.0.0.zip HEAD
Wheel (.whl)
Generado con:

bash
Copy code
python -m build
Artefactos generados automáticamente en GitHub Actions.

🔄 Pipeline CI/CD (GitHub Actions – Multi Job)
El pipeline tiene 5 jobs secuenciales:

css
Copy code
[ Calidad de Código ]
        ↓
[ Pruebas Unitarias + Cobertura ]
        ↓
[ Pruebas API (Newman) ]
        ↓
[ Pruebas de Rendimiento (JMeter) ]
        ↓
[ Construcción y Versionado de Artefactos ]
Cada push a main ejecuta:

análisis estático

pruebas con cobertura

ejecución API REST

stress test con JMeter

creación de ZIP + wheel

subida de artefactos

Resultados disponibles en GitHub → Actions → Artifacts.

🧪 Pruebas funcionales con Selenium (Frontend)

El proyecto incluye pruebas funcionales automatizadas usando Selenium + WebDriver Manager, las cuales validan el flujo de inicio de sesión desde el navegador.

🔥 Objetivo: verificar que el usuario pueda iniciar sesión y acceder al módulo de libros.

Para ejecutarlas:

uvicorn app.main:app --reload
pytest tests/functional


En GitHub Actions se ejecutan en un job independiente:

selenium-tests

🚀 Simulación de Despliegue Automático

El proyecto incluye un job adicional que representa un despliegue automatizado en un entorno limpio, ejecutando la aplicación en el puerto 9000 y realizando un smoke test con curl.

Job correspondiente:

deploy


Esto demuestra un proceso CI/CD completo con:

Integración continua

Entrega continua

Despliegue automatizado simulado

🟢 Makefile
Atajos útiles:

makefile
Copy code
run:
	uvicorn app.main:app --reload

test:
	pytest

coverage:
	pytest --cov=app

api-tests:
	newman run postman/biblioteca.postman_collection.json

performance:
	jmeter -n -t jmeter/api_books.jmx -l jmeter/results.jtl -e -o jmeter/report

build-wheel:
	python -m build

zip:
	git archive --format zip --output biblioteca-devops.zip HEAD
🧾 Conclusiones
Este proyecto implementa un pipeline DevOps completo:

✔ Backend + Frontend funcional
✔ Versionado del esquema de base de datos
✔ Tests automatizados (unitarios y funcionales)
✔ Cobertura > 80%
✔ Análisis estático de calidad
✔ Validación API REST
✔ Pruebas de rendimiento
✔ Artefactos versionados (ZIP + wheel)
✔ CI/CD robusto con 5 jobs independientes

Autor: Lord Ennard
Proyecto: DevOps (Automatización CI/CD)