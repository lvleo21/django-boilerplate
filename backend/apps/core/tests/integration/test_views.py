import django
import pytest
from django.urls import reverse


@pytest.fixture
def welcome_page(inertia_client):
    return inertia_client.get(reverse("core:welcome")).json()


def test_welcome_renders_the_welcome_component(welcome_page):
    assert welcome_page["component"] == "Welcome"


def test_welcome_shows_the_project_name(welcome_page, settings):
    assert welcome_page["props"]["project_name"] == settings.PROJECT_NAME


def test_welcome_shows_the_django_version(welcome_page):
    assert welcome_page["props"]["django_version"] == django.get_version()


def test_welcome_links_to_the_admin(welcome_page):
    assert welcome_page["props"]["admin_url"] == reverse("admin:index")


def test_welcome_without_inertia_header_renders_the_html_layout(client):
    response = client.get(reverse("core:welcome"))

    assert b'data-page="app"' in response.content
