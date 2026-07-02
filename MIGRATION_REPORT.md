# MIGRATION_REPORT.md — Metalab Web Django MVP

**Data da auditoria:** 01/07/2026
**Projeto de origem:** `/Users/macbookair/metalab-farma` (não alterado)
**Projeto de destino:** `/Users/macbookair/metalab_django`

---

## 1. O que foi encontrado no projeto atual

### 1.1 Stack de origem

| Camada | Tecnologia |
|---|---|
| Framework | Next.js 16.2.6 (App Router) + React 19.2.4 |
| Linguagem | TypeScript 5 |
| ORM / Banco | Prisma 7.8 + PostgreSQL (Supabase) |
| Autenticação | NextAuth v5 (beta) + bcryptjs |
| Estilo | Tailwind CSS 4 |
| Estado | Zustand + React Context (carrinho) + TanStack Query |
| Pagamento | Mercado Pago (PIX, cartão, boleto) |
| Frete | Melhor Envio (PAC/SEDEX) |
| ERP | Tiny/Olist (Waves 1 e 2A em produção, DESLIGADAS) |
| E-mail | Resend |
| Imagens | Cloudinary |
| Filas/Jobs | Upstash QStash (carrinho abandonado, expiração PIX, sync Tiny) |
| Rate limit | Upstash Redis |
| Observabilidade | Sentry |
| Testes | Vitest (unit) + Playwright (e2e: home, product, cart, checkout, auth, admin, mobile, vip, catalog, scroll) |
| Deploy | Vercel |

### 1.2 Modelos de dados encontrados (schema.prisma)

- **Usuario** — email, nome, senha, papel (CLIENTE/ADMIN/SUPER_ADMIN), ativo, telefone, cpf, pontosResgatados
- **Account / Session / VerificationToken** — tabelas do NextAuth
- **Categoria** — nome, slug, ordem (13 categorias na taxonomia)
- **Produto** — nome, slug, sku (único), ean, marca, subtítulo, descrições (HTML + curta), composição, modo de uso, preço, preço original, estoque, estoque mínimo, dimensões/peso (Melhor Envio), tipo (SIMPLES/KIT), tags, categoria, cores (visual), imagem, SEO (meta título/descrição/palavras-chave), ativo, destaque
- **ImagemProduto** — galeria por produto (url, alt, ordem)
- **AtributoProduto** — chave/valor por produto
- **KitItem** — composição de kits (kit ↔ produto componente, quantidade)
- **Endereco** — cep, logradouro, número, complemento, bairro, cidade, estado, principal (por usuário)
- **Pedido** — número único, status (AGUARDANDO_PAGAMENTO → … → ENTREGUE/CANCELADO/REEMBOLSADO), subtotal/desconto/frete/total, método pagamento (PIX/CARTAO_CREDITO/CARTAO_DEBITO/BOLETO), campos PIX (QR code), pago/pagoEm, rastreio, snapshot do comprador (nome/email/cpf/telefone/endereço), campos de integração Tiny (id, status, sync, NF-e)
- **ItemPedido** — quantidade, preço unitário, subtotal + snapshot (nome, sku, imagem do produto)
- **Cupom** — código único, tipo (PERCENTUAL/VALOR_FIXO/FRETE_GRATIS), valor, uso máximo/atual, validade, ativo
- **Avaliacao** — nota, título, texto, aprovada (moderação), única por usuário+produto
- **Banner** — título, subtítulo, imagem, link, CTA, cores (bg/accent), campanha, ordem, ativo
- **CartSession** — carrinho abandonado (email, itens JSON, total, convertido)
- **AuditLog** — trilha de auditoria de ações administrativas

### 1.3 Páginas públicas encontradas

`/` (home com hero, banners, carrossel, seções de produtos, trust/quality), `/produtos`, `/produtos/[id]`, `/categoria/[slug]`, `/checkout`, `/login`, `/registro`, `/pedidos` (do cliente), `/avaliacoes`, `/vip` (programa fidelidade Silver/Gold/Platinum/Diamond com pontos, cashback e conquistas), `/sobre`, `/qualidade`, `/certificacoes`, `/politica-de-privacidade`, `/termos-de-uso`, `/trocas-e-devolucoes`

### 1.4 Painel administrativo encontrado

`/admin` (dashboard), `/admin/produtos`, `/admin/pedidos` (+ detalhe), `/admin/clientes`, `/admin/cupons`, `/admin/banners`, `/admin/avaliacoes` (moderação), `/admin/analytics`, `/admin/audit`, `/admin/login`, `/admin/criar-admin`

### 1.5 APIs encontradas (~40 rotas)

- Públicas: produtos, categorias, banners, avaliações, cupons disponíveis, CEP, frete, registro
- Autenticadas: pedidos, perfil, resgate de pontos, stats do usuário
- Admin: CRUD completo + export de pedidos + resync Tiny + upload (Cloudinary) + stats/analytics/audit/notifications
- Pagamento: criar (Mercado Pago), status, webhook
- Jobs (QStash): abandoned-cart, email-pedido, pix-expiry, tiny-sync-pedido
- Dev: health, auth-debug, sentry-test

### 1.6 Regras de negócio já implementadas (fonte: services/, lib/)

- **Carrinho** (`services/cartTotals.ts`): subtotal por item, desconto percentual ou fixo (limitado ao subtotal), cupom frete grátis zera frete, total nunca negativo
- **Frete** (`lib/frete.ts`): cotação Melhor Envio com dimensões/peso SEMPRE do banco (nunca do cliente); kits somam dimensões dos componentes (`calcularPacote`)
- **Cupons** (`services/coupons.ts`): validação de ativo, validade, uso máximo
- **Pedidos**: número único, snapshot de produto/comprador/endereço, recálculo server-side de frete e totais
- **Segurança**: adminGuard, rate limiting, auditoria, validação Zod, mascaramento de dados em logs
- **Fidelidade** (`data/loyalty.ts`): níveis Silver (0-299) / Gold (300-1499) / Platinum / Diamond, multiplicador de pontos, % cashback, frete grátis acima de R$ 199

### 1.7 Dados e assets

- 270 produtos mock em `data/products.ts` (ids `local-*`, com nome, preço, estoque, imagem, cor)
- 345 imagens de produto em `public/products/` (PNG) + fundos em `public/backgrounds/`
- 13 categorias com classificação automática por nome (`utils/categorizeProducts.ts`): Articulações, Vitaminas, Fibras, Compostos Naturais, Cálcio, Melatonina, Xaropes, Outros, etc.
- Dados reais residem no PostgreSQL do Supabase (produção)

---

## 2. O que foi migrado (mapeamento Next.js → Django)

| Origem (Next.js) | Destino (Django) |
|---|---|
| schema.prisma → Usuario | `django.contrib.auth.User` (staff = admin) — simplificação deliberada |
| Categoria, Produto, ImagemProduto | app `produtos` (Categoria, Produto, ImagemProduto) |
| Endereco + dados do comprador | app `clientes` (Cliente com endereço embutido — desnormalização deliberada para o MVP) |
| Pedido, ItemPedido | app `pedidos` (Pedido, ItemPedido, HistoricoStatus) |
| Cupom | app `cupons` (Cupom + services de validação/aplicação) |
| Banner | app `banners` (Banner) |
| CartContext/Zustand + cartTotals.ts | carrinho por sessão em `checkout/cart.py` (mesmas regras de cálculo) |
| Checkout (Mercado Pago) | `checkout` com métodos manuais (PIX_MANUAL/CARTAO_MANUAL/BOLETO_MANUAL) |
| /admin (React) | painel customizado em `/admin/` (Django templates + Bootstrap 5) + Django Admin em `/django-admin/` |
| /api/* | app `api` (JSON views: health, produtos, pedidos, clientes, dashboard) |
| Páginas institucionais | app `core` (home, sobre, contato) |
| Relatórios/analytics | app `relatorios` (dashboard com annotations do ORM) |
| Vitest/Playwright | Django TestCase (models, carrinho, cupom, checkout, estoque, permissões) |
| Vercel | Gunicorn + WhiteNoise + Procfile (Render/Railway/VPS) |

## 3. O que foi adaptado

1. **Status de pedido**: enum da origem (AGUARDANDO_PAGAMENTO, PAGAMENTO_APROVADO, …, REEMBOLSADO) adaptado ao enum do PRD (NOVO, CONFIRMADO, EM_SEPARACAO, ENVIADO, ENTREGUE, CANCELADO) + status de pagamento separado (PENDENTE, PAGO, RECUSADO, ESTORNADO, CANCELADO). O snapshot do comprador foi mantido.
2. **Cliente**: na origem, endereço é tabela separada com N por usuário; no MVP o endereço vive no Cliente (1 endereço), conforme PRD. Cliente pode existir sem User.
3. **Cupom**: ganhou `data_inicio` e `valor_minimo_pedido` (exigidos pelo PRD; a origem só tinha validade final).
4. **Produto**: campos de kit (KitItem), atributos chave/valor, EAN, tags e cores foram deixados de fora do MVP (documentados como pendência). Imagens: `imagem_principal` + `imagem_2..4` conforme PRD, e galeria `ImagemProduto` mantida para compatibilidade futura.
5. **Frete**: sem integração real; estrutura `checkout/services.py::calcular_frete()` preparada (frete grátis via cupom, valor fixo configurável por env `FRETE_FIXO`).
6. **Imagens**: origem usa Cloudinary + `/public/products`; destino usa `ImageField` local (media/) com Pillow. As 345 imagens PNG foram copiadas para `media/produtos/`.
7. **Autenticação**: NextAuth (JWT + OAuth) → sessões nativas do Django; senha bcrypt do NextAuth NÃO é portável diretamente (hashers diferentes) — usuários precisarão redefinir senha se os dados reais forem importados.

## 4. O que ficou pendente (fora do MVP, documentado para não perder)

| Funcionalidade da origem | Situação |
|---|---|
| Integração Mercado Pago real (PIX QR code, webhook, status) | Estrutura pronta (método de pagamento + status), integração desligada |
| Melhor Envio (cotação real PAC/SEDEX, dimensões de kit) | Pendente — `calcular_frete()` é o ponto de extensão |
| Tiny ERP (sync pedidos, NF-e, webhooks) | Pendente — campos não portados; ver `project-tiny-erp-integration` |
| Programa VIP / fidelidade (níveis, pontos, cashback, conquistas) | Pendente — página e lógica não portadas no MVP |
| Avaliações de produtos (com moderação) | Pendente (modelo existe na origem; não portado no MVP) |
| Produtos tipo KIT (KitItem, cálculo de pacote) | Pendente — MVP trata kit como produto simples |
| Carrinho abandonado + e-mails (QStash/Resend) | Pendente |
| Upload Cloudinary | Substituído por upload local (media/) |
| AuditLog administrativo | Pendente (Django Admin já tem LogEntry nativo) |
| Rate limiting (Upstash) | Pendente |
| Sentry | Pendente (adicionar `sentry-sdk` depois) |
| Múltiplos endereços por usuário | Pendente (MVP: 1 endereço por cliente) |
| Páginas institucionais extras (qualidade, certificações, termos, privacidade, trocas, avaliações) | Parcial: sobre/contato criadas; demais são conteúdo estático fácil de portar |
| Importação dos dados reais do Supabase | Pendente — comando `seed_demo` popula categorias + produtos de demonstração com as imagens reais |

## 5. Decisões técnicas tomadas

1. **Python 3.12 via `uv`** (sistema só tem 3.9; Django 5.2 LTS exige ≥3.10).
2. **Django 5.2 LTS** — suporte longo, adequado para quem está aprendendo.
3. **User nativo do Django** em vez de custom user — menos complexidade; `is_staff` controla o painel; papel SUPER_ADMIN vira `is_superuser`.
4. **Carrinho na sessão** (dict `{produto_id: quantidade}`) — sem tabela, conforme PRD.
5. **Regras de negócio em `services.py`** por app (cupons, pedidos, checkout, relatorios) — views finas, modelos com validações.
6. **API com JsonResponse puro** — sem DRF, conforme PRD.
7. **SQLite por padrão local; PostgreSQL via `DATABASE_URL`** (dj-database-url) em produção.
8. **python-decouple** para env vars (mais simples que django-environ).
9. **Bootstrap 5 via CDN** + HTMX via CDN (usado no carrinho) — sem build step de frontend.
10. **Preços em `DecimalField(10,2)`** — nunca float.
11. **Estoque com `PositiveIntegerField` + `F()` expressions** na baixa/devolução para evitar race conditions.
12. **Snapshot de pedido** (nome, SKU, preço do produto + dados do comprador) copiado no momento da compra, como na origem.

## 6. Próximos passos recomendados

1. Importar dados reais do Supabase (script de export CSV → `loaddata`/comando de import).
2. Ativar integração Mercado Pago (PIX) no `checkout/services.py`.
3. Cotação real de frete (Melhor Envio) — portar `calcularPacote` de `lib/freteUtils.ts`.
4. Portar avaliações de produto com moderação.
5. Portar programa VIP/fidelidade.
6. Integração Tiny ERP (Wave 3) quando a loja Django estiver estável.
7. Adicionar Sentry (`sentry-sdk[django]`) e backups do banco.
8. Ajustar design para referência Vitafor (solicitado pelo usuário — aplicado na camada de templates ao final).
