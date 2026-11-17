# Huerta Comunitaria — Servidor (Django + DRF)

API REST para el intercambio de semillas y cosechas entre vecinos.
Dos modelos relacionados: **Agricultor** (1) → **Cultivo** (N).

## Puesta en marcha

```bash
python -m venv venv
# Windows:  venv\Scripts\activate      |  Linux/Mac:  source venv/bin/activate
pip install -r requirements.txt
python manage.py makemigrations --check   # debe decir "No changes detected"
python manage.py migrate
python manage.py cargar_datos             # opcional: datos de ejemplo para el video
python manage.py createsuperuser          # opcional: para /admin/
python manage.py runserver
```

Si `makemigrations --check` avisa de cambios, ejecuta `python manage.py makemigrations` y haz commit del archivo nuevo.

API: `http://127.0.0.1:8000/api/` · Admin: `http://127.0.0.1:8000/admin/`

Pruebas automáticas: `python manage.py test`

## Endpoints

| Método | Ruta | Acción |
|---|---|---|
| GET / POST | `/api/agricultores/` | listar / crear |
| GET / PUT / PATCH / DELETE | `/api/agricultores/{id}/` | detalle / editar / eliminar |
| GET / POST | `/api/cultivos/` | listar / crear (filtros: `?agricultor=<id>`, `?ofrece=semillas\|cosecha`) |
| GET / PUT / PATCH / DELETE | `/api/cultivos/{id}/` | detalle / editar / eliminar |

Reglas de validación: la fecha de siembra no puede ser futura; si un cultivo ofrece semillas o cosecha, la cantidad debe ser mayor que 0.

## CORS
`django-cors-headers` está en `INSTALLED_APPS` y en `MIDDLEWARE` (antes de `CommonMiddleware`).
Orígenes permitidos en `config/settings.py` → `CORS_ALLOWED_ORIGINS` (Vite usa el puerto 5173).

## Ejemplo de JSON
```json
// POST /api/agricultores/
{ "nombre": "Marta Ríos", "parcela": "Parcela 1", "contacto": "300 111 2233" }

// POST /api/cultivos/
{ "nombre": "Tomate chonto", "tipo": "hortaliza", "estado": "listo",
  "fecha_siembra": "2026-09-01", "ofrece": "cosecha", "cantidad": 5, "unidad": "kg", "agricultor": 1 }
```

Valores válidos — `tipo`: hortaliza, fruta, aromatica, legumbre, tuberculo · `estado`: sembrado, creciendo, listo, cosechado · `ofrece`: nada, semillas, cosecha · `unidad`: unidades, kg, atados, sobres.
