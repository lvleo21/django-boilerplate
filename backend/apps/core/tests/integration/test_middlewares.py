import pytest
from django.urls import reverse


@pytest.fixture
def shared_props(inertia_client):
    return inertia_client.get(reverse("core:welcome")).json()["props"]


def test_inertia_share_shares_the_active_language(shared_props):
    assert shared_props["language"] == "pt-br"


def test_inertia_share_shares_empty_errors(shared_props):
    assert shared_props["errors"] == {}
