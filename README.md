# Metalab Web Django MVP

Loja + painel administrativo em **Python/Django**, migrado do projeto Next.js
`metalab-farma` (ver `MIGRATION_REPORT.md` para o mapeamento completo).

## Stack

- Python 3.12 · Django 5.2 LTS
- SQLite local · PostgreSQL em produção (`DATABASE_URL`)
- Django Templates + Bootstrap 5 (CDN) + HTMX
- WhiteNoise (estáticos) · Gunicorn (produção)
- python-decouple + dj-database-url (configuração por ambiente)

## Rodando localmente

```bash
cd metalab_django
python3.12 -m venv venv            # ou: uv venv --python 3.12 venv
source venv/bin/activate
pip install -r requirements.txt

cp .env.example .env               # ajuste se quiser
python manage.py migrate
python manage.py createsuperuser
python manage.py seed_demo             # importa produtos do projeto original
python manage.py reorganizar_catalogo  # categorias corretas, SEO, cores, linha Inovitann, remove MAXMA
python manage.py runserver
```

- Loja: http://127.0.0.1:8000/
- Painel customizado: http://127.0.0.1:8000/admin/ (exige usuário staff)
- Django Admin: http://127.0.0.1:8000/django-admin/
- API health: http://127.0.0.1:8000/api/health/

## Estrutura

| App | Responsabilidade |
|---|---|
| `core` | home, sobre, contato, 404/500, context processors |
| `accounts` | login/logout, minha conta, decorator `staff_required` |
| `produtos` | Categoria, Produto, catálogo público + CRUD admin |
| `clientes` | Cliente (com endereço) + CRUD admin |
| `pedidos` | Pedido, ItemPedido (snapshot), HistoricoStatus + regras de estoque em `services.py` |
| `cupons` | Cupom (percentual/fixo/frete grátis) + validação em `services.py` |
| `banners` | Banners da home + CRUD admin |
| `checkout` | Carrinho por sessão (`cart.py`) + checkout (`services.py`) |
| `relatorios` | Dashboard e relatórios (annotations do ORM) |
| `api` | JSON interno: health, produtos, pedidos, clientes, resumo |

Regra geral: **models** validam dados, **services.py** concentram regra de negócio,
**views** ficam finas, **templates** só exibem.

## Regras de negócio principais

- Confirmar pedido baixa estoque (F() expressions, sem corrida); cancelar devolve.
- Pedido guarda snapshot de nome/SKU/preço do produto e dados do comprador.
- Total = subtotal − desconto + frete, nunca negativo; cancelado não conta faturamento.
- Cupom valida ativo, período, uso máximo e pedido mínimo; `FRETE_GRATIS` zera frete.
- Frete fixo `FRETE_FIXO` (env), grátis acima de `FRETE_GRATIS_ACIMA_DE`.
- Transições de status validadas (ex.: ENTREGUE não pode ser cancelado).

## Testes

```bash
python manage.py test        # testes: models, carrinho, cupom, checkout, estoque, permissões e hardening
```

## Deploy (Render/Railway/VPS)

Variáveis de ambiente obrigatórias em produção:

```
SECRET_KEY=<valor longo e aleatório>
DEBUG=False
ALLOWED_HOSTS=seudominio.com
DATABASE_URL=postgres://usuario:senha@host:5432/banco
CSRF_TRUSTED_ORIGINS=https://seudominio.com
SECURE_HSTS_SECONDS=3600
SECURE_HSTS_INCLUDE_SUBDOMAINS=False
SECURE_HSTS_PRELOAD=False
```

Build/start:

```bash
pip install -r requirements.txt
python manage.py collectstatic --noinput
python manage.py migrate
gunicorn config.wsgi:application     # ou use o Procfile
```

`runtime.txt` fixa o Python (3.12) e o `Procfile` define o processo web.

## Próximos passos sugeridos

Ver seção 6 do `MIGRATION_REPORT.md` (Mercado Pago, Melhor Envio, avaliações,
programa VIP, Tiny ERP, Sentry, importação dos dados reais do Supabase).
