#!/usr/bin/env python3
"""Configura um novo projeto criado a partir deste boilerplate.

Pergunta o nome do projeto, o slug do pacote, a descrição, o autor, o banco e
a senha, gera a SECRET_KEY e atualiza pyproject.toml, README.md e os arquivos
de ambiente. Use apenas em um clone novo, uma vez: rodar de novo sobrescreve
os valores anteriores.

Uso: python scripts/init_project.py
"""

import getpass
import re
import secrets
import sys
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parent.parent
ENV_EXAMPLE = ROOT / "config" / "settings" / ".env-example"
PYPROJECT = ROOT / "pyproject.toml"
README = ROOT / "README.md"
# O Django lê config/settings/.env (local, fora do Docker) e o compose lê
# .env/.env.local. Os dois recebem os mesmos valores, mudando só o host.
ENV_TARGETS = {
    ROOT / "config" / "settings" / ".env": "127.0.0.1",
    ROOT / ".env" / ".env.local": "db",
}
DOCKER_COMPOSE = ROOT / "docker-compose.yml"
TEMPLATE_DESCRIPTION = re.compile(r"^Este projeto de boilerplate.*$", re.M)
SLUG_RE = re.compile(r"^[a-z][a-z0-9-]*$")
DB_NAME_RE = re.compile(r"^[a-zA-Z_][a-zA-Z0-9_]*$")
CONTAINER_PREFIX_RE = re.compile(r"^[a-z][a-z0-9_]*$")


def ask(prompt, default=None, validate=None, hint=None):
    suffix = f" [{default}]" if default else ""
    if hint:
        print(f"  {hint}")
    while True:
        answer = input(f"{prompt}{suffix}: ").strip() or (default or "")
        if not answer:
            print("  Valor obrigatório.")
            continue
        if validate and not validate(answer):
            print("  Valor inválido.")
            continue
        return answer


def confirm(prompt, default=False):
    options = "[S/n]" if default else "[s/N]"
    answer = input(f"{prompt} {options}: ").strip().lower()
    if not answer:
        return default
    return answer in ("s", "sim", "y", "yes")


def escape(value):
    return value.replace("\\", "\\\\").replace('"', '\\"')


def build_database_url(user, password, host, port, name):
    return (
        f"postgres://{quote(user, safe='')}:{quote(password, safe='')}"
        f"@{host}:{port}/{quote(name, safe='')}"
    )


def set_env(text, key, value):
    line = f'{key}="{escape(value)}"'
    pattern = re.compile(rf"^{key}=.*$", re.M)
    if pattern.search(text):
        return pattern.sub(lambda _: line, text, count=1)
    return text.rstrip("\n") + f"\n{line}\n"


def render_env(template, values, host):
    text = template
    text = set_env(text, "PROJECT_NAME", values["project_name"])
    text = set_env(text, "SECRET_KEY", values["secret_key"])
    text = set_env(
        text,
        "DATABASE_URL",
        build_database_url(
            values["db_user"],
            values["db_password"],
            host,
            "5432",
            values["db_name"],
        ),
    )
    return text


def update_pyproject(values):
    text = PYPROJECT.read_text(encoding="utf-8")
    text = re.sub(
        r'^name = ".*"$',
        f'name = "{escape(values["slug"])}"',
        text,
        count=1,
        flags=re.M,
    )
    text = re.sub(
        r'^description = ".*"$',
        f'description = "{escape(values["description"])}"',
        text,
        count=1,
        flags=re.M,
    )
    text = re.sub(
        r"^authors = \[.*\]$",
        f'authors = ["{escape(values["author"])}"]',
        text,
        count=1,
        flags=re.M,
    )
    PYPROJECT.write_text(text, encoding="utf-8")


def update_readme(values):
    text = README.read_text(encoding="utf-8")
    text = re.sub(r"^# .*$", f"# {values['project_name']}", text, count=1, flags=re.M)
    text = TEMPLATE_DESCRIPTION.sub(lambda _: values["description"], text, count=1)
    README.write_text(text, encoding="utf-8")


def update_docker_compose(values):
    prefix = values["container_prefix"]
    text = DOCKER_COMPOSE.read_text(encoding="utf-8")
    # container_name: django_web, django_web_db, django_web_celery_worker...
    text = re.sub(
        r"^(\s*container_name: )django_web(\S*)$",
        lambda m: f"{m.group(1)}{prefix}{m.group(2)}",
        text,
        flags=re.M,
    )
    # image: django_web (serviço web) e django_celery_worker, django_celery_beat...
    text = re.sub(
        r"^(\s*image: )django_web$",
        lambda m: f"{m.group(1)}{prefix}",
        text,
        flags=re.M,
    )
    text = re.sub(
        r"^(\s*image: )django_celery_(\w+)$",
        lambda m: f"{m.group(1)}{prefix}_celery_{m.group(2)}",
        text,
        flags=re.M,
    )
    DOCKER_COMPOSE.write_text(text, encoding="utf-8")


def update_env_example(values):
    text = ENV_EXAMPLE.read_text(encoding="utf-8")
    text = set_env(text, "PROJECT_NAME", values["project_name"])
    text = set_env(
        text,
        "DATABASE_URL",
        f"postgres://{values['db_user']}:<password>@db:5432/{values['db_name']}",
    )
    ENV_EXAMPLE.write_text(text, encoding="utf-8")


def write_env_files(values):
    template = ENV_EXAMPLE.read_text(encoding="utf-8")
    for path, host in ENV_TARGETS.items():
        if path.exists() and not confirm(f"{path.relative_to(ROOT)} já existe. Sobrescrever?"):
            print(f"  Mantido: {path.relative_to(ROOT)}")
            continue
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(render_env(template, values, host), encoding="utf-8")
        print(f"  Gravado: {path.relative_to(ROOT)}")


def collect():
    print("Configuração do novo projeto\n")
    default_name = ROOT.name.replace("-", " ").replace("_", " ").title()
    project_name = ask("Nome do projeto (aparece no admin, Swagger e README)", default_name)
    default_slug = re.sub(r"[^a-z0-9-]+", "-", project_name.lower()).strip("-")
    slug = ask(
        "Nome do pacote (pyproject.toml)",
        default_slug,
        validate=lambda v: bool(SLUG_RE.match(v)),
        hint="Minúsculas, números e hífens, começando por letra.",
    )
    description = ask("Descrição do projeto", "Projeto criado a partir do django-boilerplate")
    author_name = ask("Autor")
    author_email = ask("E-mail do autor")
    db_default = slug.replace("-", "_")
    db_name = ask(
        "Nome do banco de dados",
        db_default,
        validate=lambda v: bool(DB_NAME_RE.match(v)),
        hint="Letras, números e underscore, começando por letra ou underscore.",
    )
    db_user = ask("Usuário do banco", "postgres")
    db_password = getpass.getpass("Senha do banco (oculta): ")
    if not db_password:
        sys.exit("A senha do banco é obrigatória.")
    container_prefix = ask(
        "Prefixo dos containers Docker",
        db_default,
        validate=lambda v: bool(CONTAINER_PREFIX_RE.match(v)),
        hint="Minúsculas, números e underscore, começando por letra. Ex.: minha_loja_web.",
    )
    return {
        "project_name": project_name,
        "slug": slug,
        "description": description,
        "author": f"{author_name} <{author_email}>",
        "db_name": db_name,
        "db_user": db_user,
        "db_password": db_password,
        "container_prefix": container_prefix,
        "secret_key": secrets.token_urlsafe(50),
    }


def main():
    if not all(p.exists() for p in (ENV_EXAMPLE, PYPROJECT, README, DOCKER_COMPOSE)):
        sys.exit("Execute a partir de um clone do boilerplate (arquivos base não encontrados).")

    values = collect()

    print("\nResumo:")
    print(f"  Nome do projeto: {values['project_name']}")
    print(f"  Pacote (pyproject): {values['slug']}")
    print(f"  Descrição: {values['description']}")
    print(f"  Autor: {values['author']}")
    print(f"  Banco: {values['db_name']} (usuário {values['db_user']})")
    print(f"  Prefixo dos containers: {values['container_prefix']}")
    print("  SECRET_KEY: gerada automaticamente")

    if not confirm("\nAplicar essas configurações?", default=True):
        sys.exit("Nada foi alterado.")

    print()
    update_pyproject(values)
    print("  Atualizado: pyproject.toml")
    update_readme(values)
    print("  Atualizado: README.md")
    update_env_example(values)
    print("  Atualizado: config/settings/.env-example")
    update_docker_compose(values)
    print("  Atualizado: docker-compose.yml")
    write_env_files(values)
    print("\nPronto. Próximos passos: revisar o diff e rodar 'make build env=local'.")


if __name__ == "__main__":
    main()
