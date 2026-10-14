# upload

## Propósito
Upload de arquivos pelo usuário, com armazenamento no S3 e endpoints de API.

## Entidades
- FileUpload: arquivo enviado, com nome e responsável (`owner`).

## Regras de negócio e jargões
- A regra de negócio ainda não foi documentada aqui; preencher conforme o app evolui.

## Integrações
- S3 via boto3 em `services/boto3.py` (endpoint e credenciais das settings `AWS_*`).

## Decisões e exceções aprovadas
- Nenhuma ainda.
