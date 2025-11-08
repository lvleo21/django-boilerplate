# Django Boilerplate

Este projeto de boilerplate em Django fornece uma estrutura básica para o desenvolvimento de aplicações web. Ele inclui a configuração inicial de banco de dados, autenticação de usuário, administração, etc.

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
