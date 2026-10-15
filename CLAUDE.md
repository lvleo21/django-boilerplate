# Arquitetura de apps Django — regras do projeto

**Estas regras são obrigatórias, não sugestões.** Todo código novo ou alterado deve segui-las, sem exceção por conveniência, prazo ou porque o código existente faz diferente.

- Antes de escrever código, identificar em qual camada e arquivo ele entra segundo este documento.
- Antes de entregar, revisar o código contra cada seção relevante e corrigir o que estiver fora do padrão.
- Código existente fora do padrão encontrado durante uma tarefa: apontar, nunca replicar. Corrigir só se fizer parte da tarefa ou se for pedido.
- Dúvida sobre onde algo entra, caso não coberto ou regra que pareça errada para um caso: parar e perguntar (ver Casos não cobertos). Nunca decidir por conta própria.

## Estrutura do repositório

- `backend/`: projeto Django (`manage.py`, `config/`, `apps/`). Os caminhos de backend citados neste documento e nos `CLAUDE.md` dos apps (`core/...`, `<app>/...`) são relativos a `backend/apps/`; `config/...` é relativo a `backend/`.
- `frontend/`: código React/Inertia (alias `@`). Ver Frontend.
- Raiz: ferramentas e configuração compartilhadas (`pyproject.toml`, `poetry.lock`, `package.json`, `yarn.lock`, `vite.config.ts`, `tsconfig.json`, `components.json`, `i18next.config.ts`, `playwright.config.ts`, `e2e/`, `Makefile`, `docker-compose.yml`, `compose/`, `scripts/`, `.agents/`). Comandos rodam a partir da raiz: `python backend/manage.py <comando>`. No Docker, o diretório de trabalho já é `backend/`.

## Settings

- O módulo de settings (`config/settings/`) é escolhido pelo `DJANGO_SETTINGS_MODULE`, vindo do ambiente do processo (`env_file` do compose, plataforma de deploy, shell) ou de `--settings`.
- Os padrões nos pontos de entrada valem só para desenvolvimento: `manage.py` e `config/celery.py` usam `config.settings.local`; `wsgi.py` e `asgi.py`, `config.settings.prod`. Em produção, definir o `DJANGO_SETTINGS_MODULE` sempre de forma explícita.
- O `.env` local (`config/settings/.env`) é lido só no `base.py`, para as demais variáveis; ele não escolhe o módulo de settings.

## Organização de um app

Organizar por domínio (um app por contexto), e dentro de cada app por camada. Começar com arquivo único (`models.py`, `services.py`…) e virar pacote quando crescer (~400–500 linhas). Exceção: `choices.py` existe desde o início em todo app.

| Módulo | Como dividir quando vira pacote | Responsabilidade |
|---|---|---|
| `models/` | Por entidade (model principal + satélites juntos) | Dados e regras sobre a própria instância |
| `admin/` | Por entidade | Configuração do admin |
| `choices.py` | Arquivo único | Todas as `TextChoices`/`IntegerChoices` do app |
| `exceptions.py` | Arquivo único | Exceções de domínio do app |
| `services/` | Por entidade/contexto | Ações que mudam estado |
| `selectors/` | Por entidade/contexto | Consultas |
| `tasks/` | Por propósito (notifications, sync, periodic) | Tasks Celery finas que chamam services |
| `views/` | Por interface (`api/`, `web/`), depois por entidade | Cola de HTTP |
| `forms/` | Arquivos por entidade; um form por caso de uso | Validação de entrada |
| `middlewares/` | Pacote desde o início, um arquivo por middleware | Cola de request/response comum a várias views |
| `tests/` | Pacote desde o início: `unit/` e `integration/`, com `test_<módulo>.py` | Testes do app (ver Testes) |

### Observações

1. `models/`, `admin/` e `tasks/` **devem** reexportar tudo no `__init__.py`, senão Django/Celery não registram. Nos demais, importar direto do módulo.
2. `utils/` só em `core`, e só para helpers genuinamente genéricos.
3. Choices sempre em `<app>/choices.py`, nomeadas com o prefixo da entidade (`OrderStatus`, `PaymentMethod`). Choices usadas por vários apps vão em `core/choices.py`. Opcional: alias no model (`Status = OrderStatus`) para manter `Order.Status.PAID`.
4. Choice no código vs tabela: se o código decide com base no valor (`if status == PAID`), é choice. Se o negócio precisa editar a lista sem deploy, é model com FK.
5. Constantes transversais (timeouts, limites) em settings ou `core`.
6. Filtros reutilizáveis viram métodos de QuerySet customizado; selectors compõem esses métodos. Não criar camada de repository: o Manager/QuerySet já cumpre esse papel.
7. Toda task com `name=` explícito, para que mover o arquivo não quebre mensagens na fila nem o Celery Beat.
8. Tasks e views finas: só chamam service/selector.
9. Selectors: argumentos só por keyword (`*`), nome no formato `<entidade>_<ação>` (`order_list`, `order_detail`). Não criar selector para query trivial sem regra.
10. Views de API: ViewSet para CRUD simples; APIView por endpoint, com serializers de entrada e saída aninhados, quando houver regra de negócio.
11. Forms validam entrada; a ação fica no service. Não colocar regra em `form.save()`. Erros do service vão para o form com `form.add_error(None, ...)`.
12. Middlewares transversais (ex.: props compartilhadas do Inertia) ficam em `core/middlewares/`. Como views, são finos: regra de negócio vai para service/selector.

## Regras de negócio: model vs service

O model responde perguntas sobre si mesmo; o service executa ações no mundo.

| | Model | Service |
|---|---|---|
| Contém | Properties derivadas, `clean()`, `constraints`, checagens como `can_be_cancelled` | Ações: criar, cancelar, pagar, sincronizar |
| Depende de | Só dos campos da própria instância | Mais de um model, transação, usuário/permissão |
| Efeito colateral | Nunca | E-mail, task, API externa, auditoria |

Para decidir, perguntar: precisa consultar ou alterar outro model? Dispara algo para fora do banco? Depende de quem executa? Precisa de `transaction.atomic`? Qualquer sim → service.

- Preferir `constraints` no Meta; `clean()` só para o que o banco não expressa.
- Evitar efeito colateral em `save()` e signals. Preferir chamada explícita no service.
- Não deixar o model anêmico: lógica pura sobre o próprio estado fica no model, para não se espalhar por views, templates e serializers.
- FKs entre apps como string (`"customers.Customer"`); `PROTECT` para dados históricos.
- Disparar tasks depois do commit: `transaction.on_commit(lambda: task.delay(obj.id))`.

## Exceptions

O service fala a língua do domínio; a view traduz para HTTP.

- `core/exceptions.py`: `ApplicationError` (message + extra), base para erros de regra de negócio que chegam ao usuário.
- `<app>/exceptions.py`: exceções de domínio herdando de `ApplicationError`. Criar exceção específica só quando quem chama trata de forma diferente (status HTTP diferente, front reage a ela, task decide retry). Senão, `ApplicationError` direto.
- Service levanta exceção de domínio; nunca `Http404` ou exceções do DRF.
- API: exception handler do DRF em `core/api/exception_handler.py` converte `ApplicationError` e a `ValidationError` do Django (vinda do `full_clean`) em 400. Views de API sem try/except.
- Web (templates/HTMX): capturar `ApplicationError` na view e usar `form.add_error`.
- Integrações externas: exceção própria (`ExternalServiceError`), separada das de domínio. É ela que vai no `autoretry_for` das tasks. Erro de domínio não faz retry.
- Evitar `except Exception` genérico e capturar só para logar e seguir em frente.

```python
# core/exceptions.py
class ApplicationError(Exception):
    def __init__(self, message: str, extra: dict | None = None):
        super().__init__(message)
        self.message = message
        self.extra = extra or {}
```

## Helpers privados (prefixo `_`)

Função privada é ok se fizer o trabalho da própria camada; se fizer trabalho de outra, move para lá.

| Camada | Helper privado é ok quando… |
|---|---|
| View | É cola de HTTP (request, redirect, props/contexto) |
| Service | É um passo interno da ação (montar payload, validar pré-condição). Query reaproveitável vai para selector |
| Selector | Compõe ou prepara queryset. Filtro reutilizável vira método de QuerySet |
| Task | Não deveria ter. Lógica pertence a um service |
| Model | Depende só da própria instância, sem efeito colateral |

Na revisão, para cada função `_`: ela consulta o banco, decide regra de negócio ou dispara efeito colateral? Se sim e a camada não é service/selector, está no lugar errado.

Reuso: nunca importar função `_` de outro módulo. Usada em mais de um módulo, vira pública no lugar adequado: `<app>/<camada>/helpers.py` ou `core/utils` (se genuinamente genérica).

## Internacionalização (i18n)

Toda string visível ao usuário passa por tradução, com o texto em pt-BR (idioma padrão, `LANGUAGE_CODE = "pt-br"`). Ainda não traduzimos, mas as strings ficam mapeadas.

### Backend (Django)

- Nível de módulo (choices, `verbose_name`, `help_text`, labels de form, atributos de classe): `gettext_lazy as _`.
- Dentro de funções (services, views, mensagens de exceção de domínio): `gettext as _`.
- Templates Django: `{% translate %}` e `{% blocktranslate %}`.
- Nunca f-string dentro de `_()`. Usar placeholders nomeados: `_("Pedido %(order_id)s cancelado.") % {"order_id": order.id}`.
- Em módulos que importam `_`, não usar `_` como variável descartável (`for _ in ...`, `a, _ = ...`). Usar `__` ou `_unused`.
- Não traduzir: logs e exceções internas (ex.: `ExternalServiceError`).

### Front React (Inertia)

- `react-i18next`, com o texto em pt-BR como chave (`keySeparator` e `nsSeparator` desativados, `resources` vazio). Sem catálogo, `t()` devolve o próprio texto.
- Todo texto visível ao usuário em componentes passa por `t()` (`useTranslation`).
- Interpolação com `{{nome}}`: `t("Olá, {{name}}", { name })`. Nunca template literal dentro de `t()`.
- Plural via count: `t("{{count}} pedido", { count })`.
- Idioma vem do Django como prop compartilhada do Inertia (`LANGUAGE_CODE`).

Catálogos separados: `.po` no backend, JSON no front (extração com i18next-cli).

## Comentários

O código diz o quê e como; o comentário diz por quê. Na dúvida, não comente.

Ordem de preferência:

1. Nome claro (variável, função, property) que dispense o comentário.
2. Documentação estruturada: `help_text` em campos de model, docstring em funções/classes públicas.
3. Comentário solto, só para o porquê que não cabe nos anteriores: decisão não óbvia, restrição externa, contorno de bug, motivo de performance.

Não escrever:

- Comentário que narra o código (`# busca o usuário`, `# retorna a resposta`).
- Comentário de seção dentro de função (`# --- validação ---`). Se a função precisa de seções, deve ser dividida.
- Comentário descrevendo a mudança (`# alterado para usar X`). Isso vai na mensagem de commit.
- Código comentado. O Git guarda o histórico.

Docstrings só em services, selectors e funções/classes públicas cujo contrato não é óbvio (pré-condições, exceções levantadas), no formato Google. TODO/FIXME só com contexto para alguém agir. Comentários e docstrings em pt-BR. Ao alterar código, atualizar ou remover comentários que ficaram incorretos.

## API e paginação

APIs com Django REST Framework. Código compartilhado de API fica em `core/api/`; endpoints de cada app em `<app>/views/api/`.

| Arquivo | Conteúdo |
|---|---|
| `core/api/exception_handler.py` | Tradução de exceções para HTTP (ver Exceptions) |
| `core/paginations.py` | `BasePagination` e o helper `get_paginated_response` |
| `<app>/views/api/<entidade>.py` | Endpoints da entidade |
| `<app>/serializers.py` | Só serializers reutilizados por mais de uma view |
| `<app>/urls.py` | Rotas do app, incluídas sob `/api/v1/` |

### API

- Versionamento por prefixo de URL: `/api/v1/`.
- ViewSet para CRUD simples; APIView por endpoint, com `InputSerializer` e `OutputSerializer` aninhados, quando houver regra de negócio.
- Serializer valida entrada e formata saída; nunca contém regra de negócio nem chama `.save()` com lógica. A ação é do service.
- Sucesso devolve os dados do `OutputSerializer`; erro sai sempre pelo exception handler, no formato `{"message", "extra"}`.

### Paginação

- Toda paginação de API vem de `core/paginations.py`; apps não definem classes próprias.
- Padrão: `BasePagination` (PageNumberPagination), configurada em `DEFAULT_PAGINATION_CLASS = "core.paginations.BasePagination"`. O tamanho padrão vem de `PAGE_SIZE` no settings.
- Query params: `page` e `size`.
- Formato da resposta: `count`, `num_pages`, `current_page`, `previous`, `next`, `results`.
- Todo endpoint de listagem é paginado.
- ViewSets paginam sozinhos. APIViews usam o helper `get_paginated_response`, no mesmo arquivo.

```python
# core/paginations.py
from collections import OrderedDict

from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class BasePagination(PageNumberPagination):
    page_size_query_param = "size"

    def get_paginated_response(self, data):
        num_pages = current_page = 0

        if self.page:
            num_pages = self.page.paginator.num_pages
            current_page = self.page.number

        return Response(
            OrderedDict(
                [
                    ("count", self.page.paginator.count),
                    ("num_pages", num_pages),
                    ("current_page", current_page),
                    ("previous", self.get_previous_link()),
                    ("next", self.get_next_link()),
                    ("results", data),
                ]
            )
        )


def get_paginated_response(
    *, serializer_class, queryset, request, view, pagination_class=BasePagination
):
    paginator = pagination_class()
    page = paginator.paginate_queryset(queryset, request, view=view)
    if page is not None:
        return paginator.get_paginated_response(serializer_class(page, many=True).data)
    return Response(serializer_class(queryset, many=True).data)
```

## Testes

Três níveis, separados por pasta. Todo comportamento novo ou alterado entra com teste no nível mais baixo que o cobre.

| Nível | Backend (pytest + pytest-django) | Frontend (Vitest + Testing Library) |
|---|---|---|
| Unidade | `<app>/tests/unit/`: código isolado, sem banco nem client HTTP (properties, `clean()`, validators, helpers). O pytest-django bloqueia o banco | `*.test.ts(x)` ao lado do código: componentes, hooks e `lib/` |
| Integração | `<app>/tests/integration/`: banco (`@pytest.mark.django_db`), views pelo `client`/`inertia_client`, services e selectors | `frontend/tests/integration/`: páginas Inertia renderizadas com `renderPage(inertiaPage(...))`, HTTP via MSW |
| E2E | `e2e/*.spec.ts`: Playwright no navegador contra o Django real (`testserver`, SQLite em memória, fixtures `e2e_*`) + Vite. Uma suíte só, cobrindo front e back | |

- **Um assert por teste**: um `assert`, `pytest.raises` ou `expect` por teste. Para verificar várias coisas do mesmo cenário, um teste para cada, com o cenário montado em fixture (pytest) ou helper (`renderWelcome()`). No e2e, ações e esperas implícitas do Playwright (`click`, `fill`) não contam como assert.
- Nome do teste descreve o comportamento: `test_<o_que>_<resultado>` no pytest, frase no Vitest/Playwright.
- Mock só nas fronteiras do sistema: APIs externas, S3, e-mail. No frontend, a fronteira é o HTTP para o Django (MSW, `frontend/tests/server.ts`; requisição sem handler falha).
- Ao cobrir comportamento que já existe, provar que o teste falha: quebrar o comportamento, ver vermelho, restaurar.
- Backend: settings `config.settings.test`; o pytest marca cada teste como `unit` ou `integration` pela pasta (`backend/conftest.py`). Fixture `inertia_client`: visita Inertia, a resposta é o JSON da página.
- Frontend: buscar por role/label (nomes acessíveis em pt-BR, como na UI). `frontend/tests/inertia.tsx` tipa as props de cada página em `PagePropsByComponent`; página nova exporta o tipo das props e ganha uma entrada lá.
- E2E: fixtures em `<app>/fixtures/e2e_*.json`, carregadas no `testserver` pelo `playwright.config.ts`. Senhas de fixture com o hasher MD5 de `config.settings.test`. Assert em roles e URLs, não em mensagens traduzidas do Django.
- Comandos: `make test-unit`, `make test-integration`, `make test-e2e` ou `make test` (os três). O e2e precisa do Chromium do Playwright: `yarn playwright install chromium`.

## Lint e formatação

- Python: ruff para lint e formatação, configurado no `pyproject.toml` (linha de 88, regras E, W, F, I, B, UP, SIM, DJ e INT). Migrations ficam de fora.
- `make format` corrige o que dá e formata; `make lint` só verifica. Rodar os dois antes de entregar: código entregue passa no `make lint`.
- Precisa do grupo dev do Poetry: `poetry install --with dev`.

## Frontend (Inertia + React)

Páginas são componentes React renderizados pelo Django via Inertia, empacotados pelo Vite e estilizados com Tailwind CSS v4 e shadcn/ui.

| Arquivo | Conteúdo |
|---|---|
| `frontend/main.tsx` | `createInertiaApp`: resolve as páginas, inicia o i18n e usa os nomes de cookie/header de CSRF do Django |
| `frontend/pages/<Componente>.tsx` | Uma página por componente Inertia (`"Orders/Index"` → `pages/Orders/Index.tsx`) |
| `frontend/components/ui/` | Componentes do shadcn/ui |
| `frontend/components/` | Componentes do app (arquivos em kebab-case) |
| `frontend/lib/` | Helpers (`i18n.ts`, `pages.ts`, `utils.ts`) |
| `frontend/types/inertia.d.ts` | Tipos das props compartilhadas |
| `frontend/app.css` | Tailwind e tema do shadcn (variáveis CSS); único CSS global |
| `core/middlewares/inertia.py` | `inertia_share`: props compartilhadas com toda página (`errors`, `language`) |
| `core/templates/core/layouts/base.html` | Layout Inertia (`INERTIA_LAYOUT`) com as tags do django-vite |

- Views web renderizam páginas com `@inertia("<Componente>")` (a view devolve o dict de props) ou `inertia.render(request, "<Componente>", props={...})`. Não criar API JSON nem roteamento no cliente para páginas.
- Cada página tem `export default` e props tipadas.
- Props compartilhadas: ao mudar `inertia_share`, atualizar `frontend/types/inertia.d.ts` na mesma tarefa.
- URLs internas nunca fixas no TSX: vêm como props montadas com `reverse()`. Inertia `<Link>` para páginas Inertia; `<a>` para o resto (ex.: admin).
- Assets seguem o `DEBUG`: com `DEBUG=True`, vêm do servidor do Vite (`yarn dev`, serviço `vite` do compose); sem, de `frontend/dist/manifest.json` (`yarn build`). `INERTIA_VERSION` é o hash do manifest.
- Tailwind sem `tailwind.config.js`: o tema fica em `frontend/app.css`.
- shadcn/ui no estilo `base-nova` (Base UI, não Radix): elementos customizados usam a prop `render`, não `asChild`. Adicionar componentes com `npx shadcn@latest add <componente>`.
- Dependências do frontend com Yarn 1 (`yarn add`, `yarn add -D` para ferramentas de build e tipos). Nunca npm.

## CLAUDE.md

Este documento é o `CLAUDE.md` global, na raiz do projeto. Todo app tem também o seu `<app>/CLAUDE.md`, com o contexto que só vale para aquele app.

| Arquivo | Contém | Não contém |
|---|---|---|
| `CLAUDE.md` (raiz) | Regras de arquitetura válidas para todo o projeto (este documento) | Detalhes de um app específico |
| `<app>/CLAUDE.md` | Propósito do app, entidades principais, regras de negócio e jargões do domínio, integrações externas, decisões e exceções aprovadas para o app | Cópia das regras globais |

- O `CLAUDE.md` do app complementa o global, nunca o contradiz. Uma exceção às regras globais só entra no app depois de aprovada (ver Casos não cobertos).
- Criar o `<app>/CLAUDE.md` junto com o app, mesmo que comece com poucas linhas.
- Ao mudar algo que o `CLAUDE.md` do app descreve (entidade, regra, integração), atualizá-lo na mesma tarefa.

Modelo:

```markdown
# <app>

## Propósito
O que o app faz, em uma ou duas frases.

## Entidades
- <Entidade>: o que representa.

## Regras de negócio e jargões
- Regras do domínio que não são óbvias pelo código.

## Integrações
- Serviços externos usados e onde ficam.

## Decisões e exceções aprovadas
- Decisão, motivo e data.
```

## Casos não cobertos

Se surgir um tipo de código que estas regras não cobrem (ex.: permissions, middleware, management commands, cache, signals), não inventar uma convenção: perguntar antes onde e como deve ficar. O mesmo vale quando seguir uma regra parecer errado para um caso específico: perguntar em vez de abrir exceção por conta própria.

Depois da decisão, registrar a nova regra: se vale para todo o projeto, neste documento, na seção correspondente; se vale só para um app, no `CLAUDE.md` desse app.
