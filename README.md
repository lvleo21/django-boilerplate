<h1 align="center">
Django Boilerplate
</h1>

<p align="center">
Este projeto de boilerplate em Django fornece uma estrutura básica para o desenvolvimento de aplicações web. Ele inclui a configuração inicial de banco de dados, autenticação de usuário, administração, etc.
</p>

## Estrutura do Projeto

- **app/**: Diretório contendo os aplicativos Django.
- **config/**: Diretório de configuração do projeto.
- **static/**: Arquivos estáticos (CSS, JavaScript, imagens).
- **templates/**: Templates HTML.
- **manage.py**: Script de gerenciamento do Django.

## Pré-requisitos

- Python 3.8+
- Django 3.2+
- Virtualenv

## Instalação

1. Clone o repositório:
    ```bash
    git clone https://github.com/seu-usuario/django-boilerplate.git
    cd django-boilerplate
    ```

2. Crie e ative um ambiente virtual:
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3. Instale as dependências:
    ```bash
    pip install -r requirements.txt
    ```

## Configuração

1. Copie o arquivo de exemplo `.env.example` para `.env` e configure as variáveis de ambiente:
    ```bash
    cp .env.example .env
    ```

2. Execute as migrações do banco de dados:
    ```bash
    python manage.py migrate
    ```

## Execução

1. Inicie o servidor de desenvolvimento:
    ```bash
    python manage.py runserver
    ```

2. Acesse a aplicação em `http://127.0.0.1:8000`.

## Testes

1. Execute os testes:
    ```bash
    python manage.py test
    ```

## Contribuição

1. Faça um fork do projeto.
2. Crie uma nova branch: `git checkout -b minha-nova-feature`.
3. Faça suas alterações e commit: `git commit -m 'Adiciona nova feature'`.
4. Envie para o repositório remoto: `git push origin minha-nova-feature`.
5. Abra um Pull Request.

## Licença

Este projeto está licenciado sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.
