"""Settings dos testes: pytest e o servidor do e2e (playwright.config.ts)."""

from config.settings.base import *

# O hasher padrão (PBKDF2) é lento de propósito e atrasa testes que criam
# usuários.
PASSWORD_HASHERS = ["django.contrib.auth.hashers.MD5PasswordHasher"]
