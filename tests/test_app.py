import json

import pytest

import pets
from app import app as flask_app


@pytest.fixture
def client(tmp_path):
    flask_app.config.update(TESTING=True, MESSAGES_FILE=tmp_path / "messages.jsonl")
    return flask_app.test_client()


VALID_FORM = {
    "name": "Jane Doe",
    "email": "jane@example.com",
    "subject": "adopt",
    "message": "Is Hazel still available?",
}


@pytest.mark.parametrize("path", ["/", "/adopt", "/about", "/contact", "/adopt/hazel"])
def test_pages_render(client, path):
    response = client.get(path)
    assert response.status_code == 200
    html = response.get_data(as_text=True)
    assert html.lower().count("<html") == 1  # nav is a partial, not a nested document
    assert 'class="site-nav"' in html


def test_every_pet_has_a_detail_page(client):
    for pet in pets.PETS:
        assert client.get(f"/adopt/{pet['slug']}").status_code == 200


def test_unknown_pet_and_page_return_404(client):
    assert client.get("/adopt/not-a-pet").status_code == 404
    assert client.get("/nope").status_code == 404


def test_home_links_resolve(client):
    html = client.get("/").get_data(as_text=True)
    assert "/all-pets" not in html
    for pet in pets.PETS[:3]:
        assert f'href="/adopt/{pet["slug"]}"' in html


def test_pet_slugs_are_unique_and_use_valid_filter_values():
    slugs = [pet["slug"] for pet in pets.PETS]
    assert len(slugs) == len(set(slugs))
    for pet in pets.PETS:
        assert pet["species"] in pets.SPECIES
        assert pet["age_group"] in pets.AGE_GROUPS
        assert pet["size"] in pets.SIZES


def test_pet_photos_are_distinct_unsplash_urls():
    images = [pet["image"] for pet in pets.PETS]
    assert len(images) == len(set(images))
    assert all(url.startswith("https://images.unsplash.com/photo-") for url in images)


def test_search_filters_combine_with_and_within_group_or():
    cats = pets.search_pets(species=["cat"])
    assert cats and all(p["species"] == "cat" for p in cats)

    baby_dogs = pets.search_pets(species=["dog"], age_group=["baby"])
    assert {p["slug"] for p in baby_dogs} == {"hazel", "buster"}

    small_or_large = pets.search_pets(size=["small", "large"])
    assert all(p["size"] in ("small", "large") for p in small_or_large)

    assert pets.search_pets(species=["cat"], size=["large"]) == []
    assert len(pets.search_pets()) == len(pets.PETS)


def test_search_sorting():
    names = [p["name"] for p in pets.search_pets(sort="name")]
    assert names == sorted(names, key=str.lower)

    newest = [p["arrived"] for p in pets.search_pets(sort="newest")]
    assert newest == sorted(newest, reverse=True)
    oldest = [p["arrived"] for p in pets.search_pets(sort="oldest")]
    assert oldest == sorted(oldest)


def test_adopt_page_applies_query_filters(client):
    html = client.get("/adopt?species=cat").get_data(as_text=True)
    assert "Meet Winston" in html
    assert "Meet Hazel" not in html
    assert "Showing 4 of 9 pets" in html


def test_adopt_page_ignores_unknown_filter_values(client):
    html = client.get("/adopt?species=dragon&sort=bogus").get_data(as_text=True)
    assert "Showing 9 of 9 pets" in html


def test_adopt_page_empty_state(client):
    html = client.get("/adopt?species=cat&size=large").get_data(as_text=True)
    assert "No pets match those filters" in html


def test_contact_prefills_message_for_known_pet(client):
    html = client.get("/contact?pet=hazel").get_data(as_text=True)
    assert "know more about Hazel" in html
    assert "know more about" not in client.get("/contact?pet=nobody").get_data(as_text=True)


def test_contact_submission_is_saved(client):
    response = client.post("/submit-contact", data=VALID_FORM)
    assert response.status_code == 302
    assert response.headers["Location"].endswith("/contact?sent=1")

    lines = flask_app.config["MESSAGES_FILE"].read_text(encoding="utf-8").splitlines()
    assert len(lines) == 1
    saved = json.loads(lines[0])
    assert saved["email"] == "jane@example.com"
    assert saved["message"] == "Is Hazel still available?"

    assert "Thank you" in client.get("/contact?sent=1").get_data(as_text=True)


@pytest.mark.parametrize("field, value", [
    ("name", "   "),
    ("email", "not-an-email"),
    ("subject", "spam"),
    ("message", ""),
    ("message", "x" * 2001),
])
def test_contact_rejects_invalid_input(client, field, value):
    response = client.post("/submit-contact", data={**VALID_FORM, field: value})
    assert response.status_code == 400
    assert "field__error" in response.get_data(as_text=True)
    assert not flask_app.config["MESSAGES_FILE"].exists()


def test_contact_escapes_user_input_when_redisplaying(client):
    response = client.post("/submit-contact", data={**VALID_FORM, "email": "<script>x</script>"})
    html = response.get_data(as_text=True)
    assert response.status_code == 400
    assert "<script>x</script>" not in html


def test_submit_contact_rejects_get(client):
    assert client.get("/submit-contact").status_code == 405
