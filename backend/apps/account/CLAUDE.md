# account

## Propósito
Usuários do sistema: o model de usuário customizado do projeto e o perfil associado.

## Entidades
- Account: usuário customizado, herda de `AbstractUser` e `BaseModel`.
- Profile: dados complementares do usuário.

## Regras de negócio e jargões
- A regra de negócio ainda não foi documentada aqui; preencher conforme o app evolui.
- `fixtures/e2e_users.json`: superusuário `e2e_admin` (senha `e2e-pass-123`, hash MD5 das settings de teste), usado só pelo e2e.

## Integrações
- Nenhuma identificada até o momento.

## Decisões e exceções aprovadas
- Nenhuma ainda.
