from pathlib import Path

import pytest

LEVEL_BY_FOLDER = {"unit": pytest.mark.unit, "integration": pytest.mark.integration}


def pytest_collection_modifyitems(items):
    """Marca cada teste com o nível da pasta em que está (`tests/<nível>/`)."""
    for item in items:
        for folder in Path(item.path).parts:
            if folder in LEVEL_BY_FOLDER:
                item.add_marker(LEVEL_BY_FOLDER[folder])


@pytest.fixture
def inertia_client(client):
    """Client que faz visitas Inertia: a resposta é o JSON da página."""
    client.defaults["HTTP_X_INERTIA"] = "true"
    return client
