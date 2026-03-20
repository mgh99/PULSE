# PULSE — Fashion Intelligence Dashboard

Dashboard de tendencias de moda en tiempo real. Agrega señales de revistas especializadas, Reddit y Google Trends, las sintetiza con IA (Mistral) y las presenta en una interfaz bilingüe (ES/EN) con actualización automática cada 15 minutos.

---

## Stack

| Capa | Tecnología |
|------|------------|
| Frontend | React 19 + Vite + CSS Modules |
| Backend | FastAPI + APScheduler + SQLite |
| IA | Mistral AI (mistral-small) |
| Fuentes | RSS (11 revistas), Reddit (PRAW), Google Trends |

---

## Estructura del proyecto

```
fashion/
├── frontend/          # React + Vite
│   └── src/
│       ├── components/    # Componentes UI (Hero, SignalGrid, ChartRow…)
│       ├── hooks/         # useDashboard.js — polling + refresh
│       ├── i18n/          # LangContext + traducciones EN/ES
│       └── App.jsx        # Layout principal con 5 tabs y filtros
│
├── backend/           # FastAPI + pipeline de datos
│   ├── main.py            # Servidor + scheduler (cada 15 min)
│   ├── pipeline.py        # Orquestación: collect → LLM → store
│   ├── database.py        # Esquema SQLite
│   ├── collectors/        # rss_collector, reddit_collector, trends_collector
│   ├── engine/            # llm_client, prompt_builder, snapshot_store
│   ├── api/routes.py      # 7 endpoints REST
│   └── .env               # Variables de entorno (no subir a git)
│
└── pulse.db           # Base de datos SQLite (se genera automáticamente)
```

---

## Instalación y arranque

### Requisitos previos
- Python 3.10+
- Node.js 18+
- Clave de API de [Mistral AI](https://console.mistral.ai/)

### 1. Backend

```bash
cd backend

# Crear entorno virtual
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # macOS/Linux

# Instalar dependencias
pip install -r requirements.txt
pip install pytrends          # opcional — Google Trends real

# Configurar variables de entorno
# Editar backend/.env con tus credenciales:
#   MISTRAL_API_KEY=tu_clave_aqui
#   REDDIT_CLIENT_ID=opcional
#   REDDIT_CLIENT_SECRET=opcional
#   REDDIT_USER_AGENT=pulse-dashboard/1.0
#   REFRESH_INTERVAL_MINUTES=15

# Arrancar servidor (http://localhost:8000)
python main.py
```

Al arrancar, el pipeline se ejecuta una vez de inmediato y luego cada 15 minutos de forma automática.

### 2. Frontend

```bash
cd frontend

npm install

# Arrancar servidor de desarrollo (http://localhost:5173)
npm run dev
```

El frontend redirige automáticamente `/api/*` al backend en `:8000` gracias al proxy de Vite.

---

## Variables de entorno (`backend/.env`)

| Variable | Obligatoria | Descripción |
|----------|-------------|-------------|
| `MISTRAL_API_KEY` | Sí | Clave de la API de Mistral |
| `REDDIT_CLIENT_ID` | No | ID de app Reddit (sin esto funciona igualmente) |
| `REDDIT_CLIENT_SECRET` | No | Secret de app Reddit |
| `REDDIT_USER_AGENT` | No | User agent para Reddit (ej: `pulse/1.0`) |
| `REFRESH_INTERVAL_MINUTES` | No | Ciclo de refresco en minutos (por defecto: `15`) |

---

## API Endpoints

| Método | Ruta | Descripción |
|--------|------|-------------|
| GET | `/api/health` | Estado del servidor |
| GET | `/api/dashboard?lang=en\|es` | Último snapshot del dashboard |
| GET | `/api/archive?lang=en\|es&limit=10` | Historial de snapshots |
| GET | `/api/velocity-history?days=7` | Histórico de velocidad de tendencias |
| GET | `/api/velocity-chart?days=7` | Datos para gráfico de velocidad |
| GET | `/api/heatmap?days=28` | Mapa de calor regional |
| POST | `/api/refresh?lang=en\|es` | Forzar refresco manual del pipeline |
| GET | `/docs` | Swagger UI interactivo |

---

## Comandos útiles

```bash
# Frontend
npm run build      # Build de producción
npm run lint       # Validación ESLint
npm run preview    # Preview del build de producción

# Backend — logs en tiempo real
python main.py     # Los logs siguen el formato [módulo] mensaje
```

---

## Notas de funcionamiento

- **Sin credenciales de Reddit:** el colector RSS sigue funcionando. Las señales de Reddit se omiten silenciosamente.
- **Sin pytrends:** los datos de Google Trends se sustituyen por mock data automáticamente.
- **Sin Mistral API:** `llm_client.py` devuelve un dashboard de fallback para que el frontend no rompa.
- **Cambio de idioma:** cada idioma (EN/ES) corre su propio ciclo de pipeline en Mistral. El prompt indica explícitamente el idioma de salida.
