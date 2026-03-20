# PULSE Backend — Setup

## Estructura
```
backend/
├── main.py                  # FastAPI app + scheduler
├── pipeline.py              # Orquestación principal
├── database.py              # SQLite init y conexión
├── collectors/
│   ├── rss_collector.py     # Feeds RSS de revistas
│   ├── reddit_collector.py  # Reddit API
│   └── trends_collector.py  # Google Trends via pytrends
├── engine/
│   ├── prompt_builder.py    # Construye el prompt para Mistral
│   ├── llm_client.py        # Wrapper Mistral API
│   └── snapshot_store.py    # Lee/escribe SQLite
└── api/
    └── routes.py            # Endpoints FastAPI
```

## Setup rápido

```bash
# 1. Entrar al directorio
cd backend

# 2. Crear entorno virtual
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. Instalar dependencias
pip install -r requirements.txt
pip install pytrends  # opcional, para Google Trends real

# 4. Configurar variables de entorno
cp .env.example .env
# Editar .env con tu MISTRAL_API_KEY

# 5. Arrancar
python main.py
```

## Endpoints

| Método | Ruta | Descripción |
|--------|------|-------------|
| GET | `/api/health` | Estado del servidor |
| GET | `/api/dashboard` | Dashboard completo (último snapshot) |
| GET | `/api/velocity-history?days=7` | Histórico de velocidad |
| POST | `/api/refresh` | Forzar refresh manual |
| GET | `/docs` | Swagger UI interactivo |

## Notas

- Al arrancar, el pipeline se ejecuta inmediatamente una vez
- Después se refresca cada 15 minutos (configurable en `.env`)
- Si Mistral falla, devuelve un dashboard de fallback (el frontend no rompe)
- Reddit es opcional — funciona sin credentials
- pytrends tiene rate limiting de Google — usa mock data como fallback automático
