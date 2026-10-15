#!/usr/bin/env python3
"""Configura um novo projeto criado a partir deste boilerplate.

Pergunta o nome do projeto, o slug do pacote, a descrição, o autor, o banco e
a senha, gera a SECRET_KEY e atualiza pyproject.toml, README.md e os arquivos
de ambiente. Opcionalmente cria a .venv com um Python compatível com o
pyproject.toml, procurado no PATH, no pyenv, no asdf e no uv. Ao final, remove
a si mesmo, o alvo `init` do Makefile e a seção do README que explica como
usá-lo. Use apenas em um clone novo, uma vez.

Uso: python scripts/init_project.py
"""

import getpass
import os
import re
import secrets
import shutil
import subprocess
import sys
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parent.parent
ENV_EXAMPLE = ROOT / "backend" / "config" / "settings" / ".env-example"
PYPROJECT = ROOT / "pyproject.toml"
PACKAGE_JSON = ROOT / "package.json"
README = ROOT / "README.md"
# O Django lê backend/config/settings/.env (local, fora do Docker) e o compose lê
# .env/.env.local. Os dois recebem os mesmos valores, mudando só o host.
ENV_TARGETS = {
    ROOT / "backend" / "config" / "settings" / ".env": "127.0.0.1",
    ROOT / ".env" / ".env.local": "db",
}
DOCKER_COMPOSE = ROOT / "docker-compose.yml"
VENV = ROOT / ".venv"
PYTHON_CONSTRAINT_RE = re.compile(r'^python = "\^(\d+)\.(\d+)', re.M)
PYTHON_BINARY_RE = re.compile(r"^python3(\.\d+)?$")
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


def update_package_json(values):
    text = PACKAGE_JSON.read_text(encoding="utf-8")
    text = re.sub(
        r'^  "name": ".*",$',
        f'  "name": "{escape(values["slug"])}",',
        text,
        count=1,
        flags=re.M,
    )
    PACKAGE_JSON.write_text(text, encoding="utf-8")


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
        if path.exists() and not confirm(
            f"{path.relative_to(ROOT)} já existe. Sobrescrever?"
        ):
            print(f"  Mantido: {path.relative_to(ROOT)}")
            continue
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(render_env(template, values, host), encoding="utf-8")
        print(f"  Gravado: {path.relative_to(ROOT)}")


def required_python():
    match = PYTHON_CONSTRAINT_RE.search(PYPROJECT.read_text(encoding="utf-8"))
    if not match:
        sys.exit(
            "Não consegui ler a versão do Python exigida no pyproject.toml "
            '(esperado algo como python = "^3.13").'
        )
    return int(match.group(1)), int(match.group(2))


def python_candidates():
    for directory in os.environ.get("PATH", "").split(os.pathsep):
        try:
            entries = os.listdir(directory)
        except OSError:
            continue
        for entry in entries:
            if PYTHON_BINARY_RE.match(entry):
                yield Path(directory) / entry

    pyenv_root = Path(os.environ.get("PYENV_ROOT", Path.home() / ".pyenv"))
    yield from pyenv_root.glob("versions/*/bin/python3")
    asdf_root = Path(os.environ.get("ASDF_DATA_DIR", Path.home() / ".asdf"))
    yield from asdf_root.glob("installs/python/*/bin/python3")

    uv = shutil.which("uv")
    if uv:
        major, minor = required_python()
        result = subprocess.run(
            [uv, "python", "find", f">={major}.{minor},<{major + 1}"],
            capture_output=True,
            text=True,
            check=False,
        )
        if result.returncode == 0 and result.stdout.strip():
            yield Path(result.stdout.strip())


def probe_python(executable):
    """Executa o interpretador e devolve o caminho real e a versão dele.

    Passar pelo próprio interpretador resolve shims do pyenv e symlinks, o que
    evita listar a mesma instalação duas vezes.

    Returns:
        Tupla (caminho, (major, minor, micro)) ou None se não executar.
    """
    try:
        result = subprocess.run(
            [
                str(executable),
                "-c",
                "import sys; print(sys.executable); print(*sys.version_info[:3])",
            ],
            capture_output=True,
            text=True,
            timeout=10,
            check=True,
        )
        path, version = result.stdout.strip().splitlines()
        return Path(path), tuple(int(part) for part in version.split())
    except (OSError, subprocess.SubprocessError, ValueError):
        return None


def format_version(version):
    return ".".join(str(part) for part in version)


def find_venv_python():
    """Escolhe o Python usado para criar a .venv.

    Entre as versões compatíveis com o pyproject.toml, prefere a menor série
    (a mesma do Dockerfile) e, dentro dela, o patch mais recente.

    Returns:
        Tupla (caminho, versão) do interpretador escolhido. Encerra o script
        com uma mensagem explicativa se nenhuma versão compatível existir.
    """
    major, minor = required_python()
    installed = {}
    for candidate in python_candidates():
        probed = probe_python(candidate)
        if probed:
            installed.setdefault(*probed)

    compatible = [
        (path, version)
        for path, version in installed.items()
        if version[0] == major and version[1] >= minor
    ]
    if compatible:
        return min(compatible, key=lambda item: (item[1][1], -item[1][2]))

    found = sorted({format_version(v) for v in installed.values()})
    found_line = (
        f"Versões encontradas nesta máquina: {', '.join(found)}."
        if found
        else "Nenhuma instalação do Python 3 foi encontrada nesta máquina."
    )
    sys.exit(
        f"\nNão encontrei um Python compatível para criar a .venv.\n\n"
        f"O projeto precisa do Python {major}.{minor} ou mais recente da série "
        f'{major}.x (pyproject.toml: python = "^{major}.{minor}").\n'
        f"{found_line}\n\n"
        f"Para resolver, instale o Python {major}.{minor} de uma destas formas:\n"
        f"  - pyenv: pyenv install {major}.{minor}\n"
        f"  - uv: uv python install {major}.{minor}\n"
        f"  - pelo gerenciador de pacotes do seu sistema operacional\n\n"
        f"Depois rode 'make init' de novo. Se preferir seguir sem a .venv, "
        f"responda 'não' à pergunta sobre o ambiente virtual.\n"
        f"Nada foi alterado."
    )


def create_venv(python, version):
    if VENV.exists() and not confirm(".venv já existe. Recriar?"):
        print("  Mantido: .venv")
        return
    try:
        subprocess.run(
            [str(python), "-m", "venv", "--clear", str(VENV)],
            check=True,
        )
    except (OSError, subprocess.CalledProcessError):
        major_minor = format_version(version[:2])
        print(
            f"  Não foi possível criar a .venv com {python}.\n"
            f"  Em Debian/Ubuntu, instale o pacote python{major_minor}-venv e "
            f"crie manualmente: {python} -m venv .venv"
        )
        return
    print(f"  Criado: .venv (Python {format_version(version)})")


def collect():
    default_name = ROOT.name.replace("-", " ").replace("_", " ").title()
    project_name = ask(
        "Nome do projeto (aparece no admin, Swagger e README)", default_name
    )
    default_slug = re.sub(r"[^a-z0-9-]+", "-", project_name.lower()).strip("-")
    slug = ask(
        "Nome do pacote (pyproject.toml e package.json)",
        default_slug,
        validate=lambda v: bool(SLUG_RE.match(v)),
        hint="Minúsculas, números e hífens, começando por letra.",
    )
    description = ask(
        "Descrição do projeto", "Projeto criado a partir do django-boilerplate"
    )
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


def remove_setup_artifacts():
    # Depois de configurado, o projeto não precisa mais do script, do alvo
    # `make init` nem da seção de instruções do README.
    makefile = ROOT / "Makefile"
    if makefile.exists():
        text = makefile.read_text(encoding="utf-8")
        text = re.sub(r"\ninit:\n\tpython3 scripts/init_project\.py\n?", "\n", text)
        makefile.write_text(text.rstrip("\n") + "\n", encoding="utf-8")
        print("  Removido: alvo init do Makefile")

    text = README.read_text(encoding="utf-8")
    text = re.sub(
        r"## Criando um novo projeto\n.*?(?=^## )",
        "",
        text,
        count=1,
        flags=re.M | re.S,
    )
    README.write_text(text, encoding="utf-8")
    print("  Removido: seção 'Criando um novo projeto' do README")

    scripts_dir = Path(__file__).resolve().parent
    Path(__file__).resolve().unlink()
    print("  Removido: scripts/init_project.py")
    if scripts_dir.exists() and not any(scripts_dir.iterdir()):
        scripts_dir.rmdir()
        print("  Removido: pasta scripts/ (vazia)")


def main():
    if not all(
        p.exists()
        for p in (ENV_EXAMPLE, PYPROJECT, PACKAGE_JSON, README, DOCKER_COMPOSE)
    ):
        sys.exit(
            "Execute a partir de um clone do boilerplate (arquivos base não encontrados)."
        )

    print("Configuração do novo projeto\n")
    venv_python = None
    if confirm("Criar o ambiente virtual .venv nesta máquina?", default=True):
        venv_python = find_venv_python()
        print(
            f"  Python {format_version(venv_python[1])} encontrado em "
            f"{venv_python[0]}\n"
        )

    values = collect()

    print("\nResumo:")
    print(f"  Nome do projeto: {values['project_name']}")
    print(f"  Pacote (pyproject.toml e package.json): {values['slug']}")
    print(f"  Descrição: {values['description']}")
    print(f"  Autor: {values['author']}")
    print(f"  Banco: {values['db_name']} (usuário {values['db_user']})")
    print(f"  Prefixo dos containers: {values['container_prefix']}")
    print("  SECRET_KEY: gerada automaticamente")
    if venv_python:
        print(f"  Ambiente virtual: .venv com Python {format_version(venv_python[1])}")
    else:
        print("  Ambiente virtual: não será criado")

    if not confirm("\nAplicar essas configurações?", default=True):
        sys.exit("Nada foi alterado.")

    print()
    update_pyproject(values)
    print("  Atualizado: pyproject.toml")
    update_package_json(values)
    print("  Atualizado: package.json")
    update_readme(values)
    print("  Atualizado: README.md")
    update_env_example(values)
    print("  Atualizado: backend/config/settings/.env-example")
    update_docker_compose(values)
    print("  Atualizado: docker-compose.yml")
    write_env_files(values)
    if venv_python:
        create_venv(*venv_python)
    print()
    remove_setup_artifacts()
    print("\nPronto. Próximos passos: revisar o diff e rodar 'make build env=local'.")
    if venv_python and VENV.exists():
        print(
            "Para instalar as dependências na .venv: 'poetry install --with dev' "
            "(o Poetry usa a .venv do projeto automaticamente)."
        )


if __name__ == "__main__":
    main()
