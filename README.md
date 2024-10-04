<p align="center">
<img src=".github/readme/bo.png" />
</p>

<h1 align="center">
Django Boilerplate
</h1>

<p align="center">
Este projeto de boilerplate em Django fornece uma estrutura básica para o desenvolvimento de aplicações web. Ele inclui a configuração inicial de banco de dados, autenticação de usuário, administração, etc.
</p>

## 🛠️ Ajustes e melhorias

O projeto ainda está em desenvolvimento e as próximas atualizações serão voltadas nas seguintes tarefas:

- [ ] Dockerização do projeto
- [ ] Integrar projeto com redis
- [ ] Integrar projeto com celery
- [ ] Action do github para rodar os testes

## 🚀 Configurando o boilerplate

### Pré-requisitos

Antes de começar, você precisará ter os seguintes itens instalados em sua máquina:

- **[Python 3.10+](https://www.python.org/downloads/)** - Para rodar o projeto.
- **[Poetry](https://python-poetry.org/docs/#installation)** - Gerenciador de dependências e ambiente virtual (gerenciado via `pyproject.toml`).

### Configuração

#### Passo 1: Crie uma pasta para o projeto

Crie uma pasta em sua máquina com o nome que desejar:

```bash
mkdir projeto
cd projeto
```

#### Passo 2: Clonar o repositório

Clone este repositório nas pasta criada:

```bash
git clone git@github.com:lvleo21/django-boilerplate.git .
```

#### Passo 3: Configurar variáveis de ambiente

Faça uma copia do arquivo `.env-example` que está localizado dentro de `config/settings/.env-example` e renomei para `.env`.

```bash
cp config/settings/.env-example config/settings/.env
```

Agora, basta preencher com as informações necessárias do arquivo.

#### Passo opcional: Configurar venv do poetry

Caso você deseje que a máquina virtual seja criado dentro do seu projeto,
basta rodar o seguinte comando:

```bash
poetry config virtualenvs.in-project true
```

#### Passo 4: Instale as dependências com o poetry

```bash
poetry install
```

ou com as dependências de desenvolvimento:

```bash
 poetry install --with dev
```

#### Passo 5: Ativar o ambiente virtual do Poetry

```bash
poetry shell
```

#### Passo 6: Aplicar as migrações do banco de dados

```bash
python manage.py migrate
```

#### Passo 7: Rodar o servidor de desenvolvimento

```bash
python manage.py runserver
```

## 🏗️ Estrutura do projeto

```
.
├── apps
│   ├── api
│   │   ├── apps.py
│   │   ├── __init__.py
│   │   ├── locale
│   │   ├── migrations/
│   │   ├── __pycache__/
│   │   └── urls.py
│   ├── core
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── forms.py
│   │   ├── __init__.py
│   │   ├── locale
│   │   │   ├── en
│   │   │   │   └── LC_MESSAGES
│   │   │   │       ├── django.mo
│   │   │   │       └── django.po
│   │   │   └── pt_BR
│   │   │       └── LC_MESSAGES
│   │   │           ├── django.mo
│   │   │           └── django.po
│   │   ├── management
│   │   │   └── commands
│   │   │       ├── do_make_messages.py
│   │   │       ├── generate_secret_key.py
│   │   │       └── __pycache__/
│   │   ├── managers.py
│   │   ├── migrations
│   │   │   ├── 0001_initial.py
│   │   │   ├── __init__.py
│   │   │   └── __pycache__/
│   │   ├── models.py
│   │   ├── __pycache__/
│   │   ├── sites.py
│   │   ├── static
│   │   │   └── core
│   │   │       └── assets
│   │   │           └── admin
│   │   │               └── login-bg.jpg
│   │   ├── templates
│   │   │   └── core
│   │   │       └── layouts
│   │   │           └── base.html
│   │   ├── tests.py
│   │   ├── utils.py
│   │   └── views.py
│   ├── __init__.py
│   └── __pycache__/
├── config
│   ├── asgi.py
│   ├── db.sqlite3
│   ├── __init__.py
│   ├── locale
│   │   ├── en
│   │   │   └── LC_MESSAGES
│   │   │       ├── django.mo
│   │   │       └── django.po
│   │   └── pt_BR
│   │       └── LC_MESSAGES
│   │           ├── django.mo
│   │           └── django.po
│   ├── __pycache__/
│   ├── settings
│   │   ├── base.py
│   │   ├── development.py
│   │   ├── __init__.py
│   │   ├── production.py
│   │   ├── __pycache__/
│   │   └── swagger.py
│   ├── urls.py
│   └── wsgi.py
├── LICENSE
├── manage.py
├── poetry.lock
├── pyproject.toml
├── README.md
└── temp.md
```

## Gerenciamento de Dependências

Este projeto utiliza o Poetry para gerenciamento de dependências. Todas as bibliotecas e pacotes necessários estão listados no arquivo `pyproject.toml`.

Para adicionar uma nova dependência:
```bash
poetry add <pacote>
```

Para remover uma dependência:
```bash
poetry remove <pacote>
```

## Comandos Úteis

Rodar testes
```bash
poetry run pytest
```

ou com a shell ativa

```bash
pytest
```

## 📝 Licença

Esse projeto está sob licença. Veja o arquivo [LICENÇA](https://github.com/lvleo21/django-boilerplate/blob/1e41c8ea27a5627096ae21695d5233c74f1f406a/LICENSE) para mais detalhes.


## ©️ Copyright

Imagem de capa foi retirada do site <a taget="_blank" href="https://www.brawlstarsdicas.com.br/">Brawl Stars Dicas</a>.
