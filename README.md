# Mondo NBA

E-commerce demo per merchandise NBA, refactored con architettura monorepo: backend Django + DRF e frontend Vue.js.

E-commerce demo for NBA merchandise, refactored with monorepo architecture: Django + DRF backend and Vue.js frontend.

## Struttura del progetto / Project structure

```
mondo_nba_orchestrator/
├── mondo_nba_backend/          # Django 5.1 + Django REST Framework
│   ├── config/                 # Settings, URL routing, WSGI/ASGI
│   │   ├── settings/           # base.py, local.py, production.py, test.py
│   │   ├── api_router.py       # API URL routing
│   │   ├── urls.py             # URL routing
│   │   ├── wsgi.py / asgi.py   # Server entry points
│   │   └── views.py            # Template views (legacy)
│   ├── gestione/               # Main app
│   │   ├── models.py           # Product, Cart, Comment, UserPayment
│   │   ├── serializers.py      # DRF serializers
│   │   ├── api_views.py        # Thin APIViews (delegate to services)
│   │   ├── services.py         # Business logic (push to DB)
│   │   ├── selectors.py        # Read queries (pull from DB)
│   │   └── views.py            # Template views (legacy)
│   ├── users/                  # Custom user model (AbstractUser)
│   ├── manage.py               # APPS_DIR added to sys.path
│   ├── .env                    # Environment variables (not committed)
│   └── stripe                  # Stripe CLI binary
└── mondo_nba_frontend/         # Vue 3 + Vite 5 + Pinia + Vue Router
    ├── src/
    │   ├── api/                # Axios instance + endpoint helpers
    │   ├── stores/             # Pinia stores (products, cart)
    │   ├── views/              # Home, ProductDetail, Cart, Login, Register, About, Products, Purchased, Admin
    │   ├── components/         # ProductCard, Pagination, StarRating
    │   └── router/             # Vue Router with auth guard
    └── vite.config.js
```

## Tecnologie / Technologies

### Backend
| Package | Version |
|---|---|
| Python | 3.10 |
| Django | 5.1 |
| Django REST Framework | latest |
| django-cors-headers | latest |
| djangorestframework-authtoken | latest |
| django-environ | latest |
| Stripe | 10.9.0 |
| Pillow | 10.4.0 |
| python-dotenv | 1.0.1 |
| requests | 2.32.3 |

### Frontend
| Package | Version |
|---|---|
| Vue.js | 3 |
| Vite | 5.4 |
| Vue Router | 4 |
| Pinia | latest |
| Axios | latest |
| Bootstrap | 5.3 |

## Avvio / Getting started

### Backend
```bash
cd mondo_nba_orchestrator/mondo_nba_backend
pipenv install
# Crea il file .env con le variabili d'ambiente (vedi sezione Stripe)
pipenv run python manage.py migrate
pipenv run python manage.py runserver
```
Server su **http://127.0.0.1:8000/** — Server at **http://127.0.0.1:8000/**

API: `http://127.0.0.1:8000/api/` (products, cart, comments, payments, auth)

Il frontend Vue viene servito come SPA dal backend Django sulla stessa porta.

The Vue frontend is served as an SPA by the Django backend on the same port.

### Produzione / Production
```bash
cd mondo_nba_orchestrator/mondo_nba_frontend && npm install && npm run build
cp -r dist/* ../mondo_nba_backend/static/
cp ../mondo_nba_backend/static/index.html ../mondo_nba_backend/templates/index.html
cd ../mondo_nba_backend && pipenv run python manage.py runserver
```
Solo il backend su porta 8000. / Only the backend on port 8000.

## Test
```bash
cd mondo_nba_orchestrator/mondo_nba_backend && pipenv run python manage.py test
```

## Lint & Type Check
```bash
cd mondo_nba_orchestrator/mondo_nba_backend
pipenv run ruff check .
pipenv run mypy --explicit-package-bases .
```

## Stripe (pagamenti / payments)
Le variabili d'ambiente sono in `.env` (non committato):
Environment variables are in `.env` (not committed):
- `STRIPE_SECRET_KEY_TEST`
- `STRIPE_PUBLIC_KEY_TEST`
- `STRIPE_WEBHOOK_SECRET_TEST`
- `PRODUCT_PRICE`
- `DJANGO_SECRET_KEY`
- `DJANGO_DEBUG`
- `DJANGO_ALLOWED_HOSTS`
- `DJANGO_READ_DOT_ENV_FILE`

Esempio `.env`:
Example `.env`:
```
DJANGO_SECRET_KEY=your-secret-key
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1
DJANGO_READ_DOT_ENV_FILE=True
STRIPE_SECRET_KEY_TEST=sk_test_...
STRIPE_PUBLIC_KEY_TEST=pk_test_...
STRIPE_WEBHOOK_SECRET_TEST=whsec_...
PRODUCT_PRICE=price_...
```

Avvia il listener webhook:
Start the webhook listener:
```bash
./stripe listen --forward-to http://127.0.0.1:8000/gestione/stripe_webhook --api-key $STRIPE_SECRET_KEY_TEST
```

Carta di test: `4242 4242 4242 4242` / Test card: `4242 4242 4242 4242`

## Settings
I settings sono divisi in `config/settings/`:
Settings are split in `config/settings/`:
- `base.py` — impostazioni comuni (common settings)
- `local.py` — sviluppo (development)
- `production.py` — produzione (production)
- `test.py` — test

Default: `config.settings.local` (impostato in `manage.py`).

## Credenziali gestore / Manager credentials
- Username: `admin`
- Password: `admin`