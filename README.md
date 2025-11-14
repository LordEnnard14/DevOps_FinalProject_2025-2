# 📚 Biblioteca DevOps  
**Proyecto Final – DevOps 2025-2**

Este proyecto implementa un **sistema de gestión de biblioteca** con autenticación, CRUD completo de libros y una **pipeline DevOps avanzada**, incluyendo:

- Backend con FastAPI  
- Frontend con Jinja2  
- Base de datos SQLite + Alembic (migraciones)  
- Pruebas unitarias, de API, funcionales y de rendimiento  
- Análisis de calidad de código  
- Cobertura > 80%  
- Generación de artefactos (ZIP + Wheel)  
- Pipeline CI/CD con GitHub Actions  
- Deploy simulado automático  

---

## 🧩 1. Arquitectura del Proyecto

biblioteca-devops/
├── app/
│ ├── main.py # FastAPI + rutas API + vistas Jinja
│ ├── auth.py # Autenticación básica
│ ├── crud.py # Lógica de acceso a datos
│ ├── db.py # SQLAlchemy + Alembic
│ ├── models.py # ORM models
│ └── schemas.py # Pydantic schemas
│
├── templates/ # Frontend Jinja2
│ ├── login.html
│ ├── books_list.html
│ ├── books_edit.html
│ └── books_new.html
│
├── tests/
│ ├── unit/ # Pruebas unitarias
│ ├── api/ # Pruebas API de FastAPI
│ ├── ui/ # Pruebas de vistas Jinja
│ └── functional/ # Selenium (pruebas funcionales)
│
├── jmeter/
│ └── api_books.jmx # Prueba de rendimiento
│
├── postman/
│ └── biblioteca.postman_collection.json
│
├── alembic/ # Migraciones de BD
│ ├── versions/
│ └── env.py
│
├── dist/ # Artefactos .whl
├── library.db # Base de datos SQLite
├── pyproject.toml
├── requirements.txt
└── README.md

yaml
Copy code

---

## 🛠️ 2. Tecnologías Utilizadas

| Categoría | Herramienta |
|----------|-------------|
| Backend | FastAPI |
| Frontend | Jinja2 |
| Base de Datos | SQLite |
| ORM | SQLAlchemy |
| Migraciones | Alembic |
| Calidad | Black, Isort, Flake8, Mypy |
| Pruebas Unitarias | Pytest + Coverage |
| Pruebas API | Postman + Newman |
| Pruebas Funcionales | Selenium |
| Pruebas de Rendimiento | Apache JMeter |
| CI/CD | GitHub Actions |
| Artefactos | Wheel + Git Archive |

---

## 🚀 3. Ejecución local

### 3.1 Activar entorno virtual

```bash
python -m venv .venv
source .venv/bin/activate   # Linux/Mac
.\.venv\Scripts\activate    # Windows
3.2 Instalar dependencias
bash
Copy code
pip install -r requirements.txt
3.3 Ejecutar la app
bash
Copy code
uvicorn app.main:app --reload
La app estará disponible en:

arduino
Copy code
http://127.0.0.1:8000/login
Usuario: admin
Contraseña: admin

🗄️ 4. Migraciones con Alembic
Inicializar Alembic (ya hecho)
bash
Copy code
alembic init alembic
Crear migración
bash
Copy code
alembic revision -m "create books table" --autogenerate
Aplicar migración
bash
Copy code
alembic upgrade head
🧪 5. Pruebas Unitarias + Cobertura
Ejecutar:

bash
Copy code
pytest --cov=app --cov-report=term-missing
Se exige al menos 80%.
Este proyecto alcanza 93%.

🧪 6. Pruebas Funcionales (Selenium)
Archivo:

bash
Copy code
tests/functional/test_login_selenium.py
Ejecutar:

bash
Copy code
uvicorn app.main:app --reload
pytest tests/functional
Selenium verifica:

✔ El login
✔ La navegación
✔ Corre en navegador real

También se ejecuta automáticamente en GitHub Actions.

🌐 7. Pruebas API REST (Postman + Newman)
Ejecutar:

bash
Copy code
newman run postman/biblioteca.postman_collection.json
Incluye assertions:

status code

JSON válido

validación de ID

validación de arreglo

⚡ 8. Pruebas de rendimiento (JMeter)
Ejecutar local:

bash
Copy code
jmeter -n -t jmeter/api_books.jmx -l jmeter/results.jtl -e -o jmeter/report
El reporte HTML se genera en:

bash
Copy code
jmeter/report/
📦 9. Artefactos
9.1 Wheel (Python Package)
bash
Copy code
python -m build
Generado en:

Copy code
dist/*.whl
9.2 ZIP versionado
bash
Copy code
git archive --format zip --output biblioteca-devops_1.0.0.zip HEAD
☁️ 10. CI/CD con GitHub Actions (7 JOBS)
La pipeline completa incluye:

Calidad de código

Pruebas unitarias + cobertura

Pruebas de API (Newman)

Pruebas de rendimiento (JMeter)

Construcción de artefactos (wheel + zip)

Pruebas funcionales (Selenium)

Deploy simulado automático

Diagrama:

mathematica
Copy code
Quality → Tests → API Tests → Performance → Artifacts → Selenium → Deploy
Cada etapa sube sus reportes como artefactos.

🚀 11. Simulación de Despliegue
En el job final del pipeline, se realiza:

instalación limpia

ejecución automática de FastAPI

smoke test con curl

Se simula un entorno productivo en el puerto 9000.