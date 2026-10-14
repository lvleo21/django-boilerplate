# Django Boilerplate

Este projeto de boilerplate em Django fornece uma estrutura básica para o desenvolvimento de aplicações web. Ele inclui a configuração inicial de banco de dados, autenticação de usuário, administração, etc.

## Criando um novo projeto

Para usar este repositório como base de um projeto novo, rode uma vez no clone:

```bash
make init
```

O script pergunta o nome do projeto, o nome do pacote, a descrição, o autor, o banco de dados (nome, usuário e senha) e gera a `SECRET_KEY`. Depois atualiza `pyproject.toml`, este README e os arquivos de ambiente (`config/settings/.env` e `.env/.env.local`). Esses arquivos não vão para o git.

O script também oferece criar a `.venv` local. Ele procura um Python compatível com o `pyproject.toml` no `PATH`, no pyenv, no asdf e no uv. Se não encontrar, explica qual versão instalar e não altera nada.

## Estrutura do Projeto

-  **apps/**: Diretório contendo os aplicativos Django.
-  **config/**: Diretório de configuração do projeto.
-  **static/**: Arquivos estáticos (CSS, JavaScript, imagens).
-  **templates/**: Templates HTML.
-  **manage.py**: Script de gerenciamento do Django.

## Pré-requisitos

- Python 3.12+
- Django 5.1.1+
- Docker
- Docker Compose

## Bucket Access Policy

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "PrivateAccessForMedia",
            "Effect": "Allow",
            "Action": [
                "s3:DeleteObject",
                "s3:GetObject",
                "s3:ListBucket",
                "s3:PutObject"
            ],
            "Resource": [
                "arn:aws:s3:::<bucket_name>",
                "arn:aws:s3:::<bucket_name>/media/*"
            ]
        },
        {
            "Sid": "PrivateAccessForStatic",
            "Effect": "Allow",
            "Action": [
                "s3:GetObject",
                "s3:PutObject"
            ],
            "Resource": [
                "arn:aws:s3:::<bucket_name>/static/*"
            ]
        }
    ]
}
```

## Licença
Este projeto está licenciado sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.
