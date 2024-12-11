import pytest
from fastapi import FastAPI
from httpx import AsyncClient
from starlette import status

@pytest.mark.anyio
async def test_get_authors_empty_list(client: AsyncClient, fastapi_app: FastAPI) -> None:
    """
    Tests retrieving a list of authors when none exist.
    """
    url = fastapi_app.url_path_for("list_authors")
    response = await client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["data"] == []

@pytest.mark.anyio
async def test_create_author(client: AsyncClient, fastapi_app: FastAPI) -> None:
    """
    Tests creating an author.
    """
    url = fastapi_app.url_path_for("create_author")
    payload = {
        "name": "John",
        "surname": "Doe",
        "birth_date": "1980-01-01"
    }
    response = await client.post(url, json=payload)
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["data"]["name"] == payload["name"]
    assert response.json()["data"]["surname"] == payload["surname"]

@pytest.mark.anyio
async def test_get_authors(client: AsyncClient, fastapi_app: FastAPI) -> None:
    """
    Tests retrieving a list of authors.
    """
    url = fastapi_app.url_path_for("list_authors")
    response = await client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json()["data"], list)
    
@pytest.mark.anyio
async def test_get_author_by_id(client: AsyncClient, fastapi_app: FastAPI) -> None:
    """
    Tests retrieving an author by ID.
    """
    create_url = fastapi_app.url_path_for("create_author")
    print(create_url)
    payload = {
        "name": "Jane",
        "surname": "Smith",
        "birth_date": "1990-05-10"
    }
    create_response = await client.post(create_url, json=payload)
    author_id = create_response.json()["data"]["id"]

    get_url = fastapi_app.url_path_for("get_author_info", id=author_id)
    response = await client.get(get_url)
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["data"]["name"] == payload["name"]

@pytest.mark.anyio
async def test_update_author(client: AsyncClient, fastapi_app: FastAPI) -> None:
    """
    Tests updating an author.
    """
    create_url = fastapi_app.url_path_for("create_author")
    payload = {
        "name": "Alice",
        "surname": "Brown",
        "birth_date": "1975-09-15"
    }
    create_response = await client.post(create_url, json=payload)
    author_id = create_response.json()["data"]["id"]

    update_url = fastapi_app.url_path_for("update_author", id=author_id)
    update_payload = {
        "name": "Alice Updated",
        "surname": "Brown",
        "birth_date": "1975-09-15"
    }
    response = await client.put(update_url, json=update_payload)
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["data"] == 1

@pytest.mark.anyio
async def test_partial_update_author(client: AsyncClient, fastapi_app: FastAPI) -> None:
    """
    Tests updating an author.
    """
    create_url = fastapi_app.url_path_for("create_author")
    payload = {
        "name": "Violet",
        "surname": "Lame",
        "birth_date": "1965-10-15"
    }
    create_response = await client.post(create_url, json=payload)
    author_id = create_response.json()["data"]["id"]

    update_url = fastapi_app.url_path_for("update_author", id=author_id)
    update_payload = {
        "birth_date": "1975-10-15"
    }
    response = await client.put(update_url, json=update_payload)
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["data"] == 1
    
    get_url = fastapi_app.url_path_for("get_author_info", id=author_id)
    get_response = await client.get(get_url)
    assert get_response.status_code == status.HTTP_200_OK
    
    

@pytest.mark.anyio
async def test_delete_author(client: AsyncClient, fastapi_app: FastAPI) -> None:
    """
    Tests deleting an author.
    """
    create_url = fastapi_app.url_path_for("create_author")
    payload = {
        "name": "Bob",
        "surname": "Johnson",
        "birth_date": "1985-02-20"
    }
    create_response = await client.post(create_url, json=payload)
    author_id = create_response.json()["data"]["id"]
    
    list_url = fastapi_app.url_path_for("list_authors")
    before_list_response = await client.get(list_url)

    delete_url = fastapi_app.url_path_for("delete_author", id=author_id)
    response = await client.delete(delete_url)
    assert response.status_code == status.HTTP_204_NO_CONTENT
    
    after_list_response = await client.get(list_url)
    assert len(before_list_response.json()["data"]) - len(after_list_response.json()["data"]) == 1

    get_url = fastapi_app.url_path_for("get_author_info", id=author_id)
    get_response = await client.get(get_url)
    assert get_response.status_code == status.HTTP_404_NOT_FOUND

@pytest.mark.anyio
async def test_create_author_invalid_data(client: AsyncClient, fastapi_app: FastAPI) -> None:
    """
    Tests creating an author with invalid or missing data.
    """
    url = fastapi_app.url_path_for("create_author")

    response = await client.post(url, json={})
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    payload = {"name": "Invalid", "surname": "User", "birth_date": "not-a-date"}
    response = await client.post(url, json=payload)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

@pytest.mark.anyio
async def test_get_non_existent_author(client: AsyncClient, fastapi_app: FastAPI) -> None:
    """
    Tests retrieving a non-existent author by ID.
    """
    url = fastapi_app.url_path_for("get_author_info", id=99999)
    response = await client.get(url)
    assert response.status_code == status.HTTP_404_NOT_FOUND

@pytest.mark.anyio
async def test_update_non_existent_author(client: AsyncClient, fastapi_app: FastAPI) -> None:
    """
    Tests updating a non-existent author.
    """
    url = fastapi_app.url_path_for("update_author", id=99999)
    payload = {"name": "Non-existent", "surname": "Author", "birth_date": "1980-01-01"}
    response = await client.put(url, json=payload)
    assert response.status_code == status.HTTP_404_NOT_FOUND

@pytest.mark.anyio
async def test_delete_non_existent_author(client: AsyncClient, fastapi_app: FastAPI) -> None:
    """
    Tests deleting a non-existent author.
    """
    url = fastapi_app.url_path_for("delete_author", id=99999)
    response = await client.delete(url)
    assert response.status_code == status.HTTP_404_NOT_FOUND
