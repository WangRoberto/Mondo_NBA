# Mondo NBA

E-commerce demo per merchandise NBA, refactored con architettura monorepo: backend Django + DRF e frontend Vue.js.

## Struttura del progetto

```
mondo_nba_orchestrator/
├── mondo_nba_backend/          # Django 5.1 + Django REST Framework
│   ├── config/                 # Settings, URL routing, WSGI/ASGI
│   ├── gestione/               # App principale
│   │   ├── models.py           # Product, Cart, Comment, UserPayment
│   │   ├── serializers.py      # DRF serializers
│   │   ├── api_views.py        # APIView sottili (delegano ai services)
│   │   ├── api_urls.py         # URL routing API
│   │   ├── services.py         # Business logic (push to DB)
│   │   ├── selectors.py        # Read queries (pull from DB)
│   │   └── views.py            # Template views (legacy)
│   ├── manage.py
│   ├── setupVariables.sh       # Variabili d'ambiente Stripe (non committato)
│   └── stripe                  # Stripe CLI binary
└── mondo_nba_frontend/         # Vue 3 + Vite 5 + Pinia + Vue Router
    ├── src/
    │   ├── api/                # Axios instance + endpoint helpers
    │   ├── stores/             # Pinia stores (products, cart)
    │   ├── views/              # Home, ProductDetail, Cart, Login, Register, About, Products, Purchased, Admin
    │   ├── components/         # ProductCard, Pagination, StarRating
    │   └── router/             # Vue Router con auth guard
    └── vite.config.js
```

## Tecnologie

### Backend
| Package | Versione |
|---|---|
| Python | 3.10 |
| Django | 5.1 |
| Django REST Framework | latest |
| django-cors-headers | latest |
| djangorestframework-authtoken | latest |
| Stripe | 10.9.0 |
| Pillow | 10.4.0 |
| python-dotenv | 1.0.1 |
| requests | 2.32.3 |

### Frontend
| Package | Versione |
|---|---|
| Vue.js | 3 |
| Vite | 5.4 |
| Vue Router | 4 |
| Pinia | latest |
| Axios | latest |
| Bootstrap | 5.3 |

## Avvio

### Backend
```bash
cd mondo_nba_orchestrator/mondo_nba_backend
source setupVariables.sh
pipenv install
pipenv run python manage.py migrate
pipenv run python manage.py runserver
```
Server su **http://127.0.0.1:8000/**

API: `http://127.0.0.1:8000/api/` (products, cart, comments, payments, auth)

### Frontend (sviluppo)
```bash
cd mondo_nba_orchestrator/mondo_nba_frontend
npm install
npm run dev
```
Frontend su **http://127.0.0.1:5173/**

### Produzione
```bash
cd mondo_nba_orchestrator/mondo_nba_frontend && npm run build
cp -r dist/* ../mondo_nba_backend/static/
cp ../mondo_nba_backend/static/index.html ../mondo_nba_backend/templates/index.html
cd ../mondo_nba_backend && pipenv run python manage.py runserver
```
Solo il backend su porta 8000.

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

## Stripe (pagamenti)
Le variabili d'ambiente sono in `setupVariables.sh` (non committato):
- `STRIPE_SECRET_KEY_TEST`
- `STRIPE_PUBLIC_KEY_TEST`
- `STRIPE_WEBHOOK_SECRET_TEST`
- `PRODUCT_PRICE`

Avvia il listener webhook:
```bash
./stripe listen --forward-to http://127.0.0.1:8000/gestione/stripe_webhook --api-key $STRIPE_SECRET_KEY_TEST
```

Carta di test: `4242 4242 4242 4242`

## Credenziali gestore
- Username: `admin`
- Password: `admin`