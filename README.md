<h1 align="center">
Django Boilerplate
</h1>

<p align="center">
Este projeto de boilerplate em Django fornece uma estrutura básica para o desenvolvimento de aplicações web. Ele inclui a configuração inicial de banco de dados, autenticação de usuário, administração, etc.
</p>

## Estrutura do Projeto

- **apps/**: Diretório contendo os aplicativos Django.
- **config/**: Diretório de configuração do projeto.
- **static/**: Arquivos estáticos (CSS, JavaScript, imagens).
- **templates/**: Templates HTML.
- **manage.py**: Script de gerenciamento do Django.

## Pré-requisitos

- Python 3.12+
- Django 5.1.1+
- Docker
- Docker Compose

## Instalação

1. Clone o repositório:
    ```bash
    git clone https://github.com/seu-usuario/django-boilerplate.git
    cd django-boilerplate
    ```

2. Copie o arquivo de exemplo `.env.example` para `.env` e configure as variáveis de ambiente:
    ```bash
    cp .env.example .env
    ```

3. Construa e inicie os containers Docker usando o Makefile:
    ```bash
    make build
    ```

## Execução

1. Acesse a aplicação em `http://127.0.0.1:8000`.

## Comandos Úteis

- Para parar os containers:
    ```bash
    make down
    ```

- Para executar migrações:
    ```bash
    docker-compose exec web poetry run python manage.py migrate
    ```

- Para coletar arquivos estáticos:
    ```bash
    docker-compose exec web poetry run python manage.py collectstatic --noinput
    ```

## Licença

Este projeto está licenciado sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.
