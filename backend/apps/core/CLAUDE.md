# core

## Propósito
Base compartilhada do projeto: model abstrato, admin, storages, templates, traduções e comandos de management usados pelos demais apps. Também guarda a página inicial (`/`, componente `Welcome`), o layout Inertia e o middleware de props compartilhadas do Inertia.

## Entidades
- BaseModel: model abstrato base dos demais apps.

## Regras de negócio e jargões
- Não contém regra de negócio de domínio. Só código genérico reutilizado por outros apps.

## Integrações
- Storages de arquivos em `storages.py` (S3 via django-storages).

## Decisões e exceções aprovadas
- Nenhuma ainda.
