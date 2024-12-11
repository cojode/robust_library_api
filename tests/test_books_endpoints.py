import pytest
from httpx import AsyncClient
from fastapi import FastAPI, status

@pytest.mark.anyio
async def test_add_book(client: AsyncClient, fastapi_app: FastAPI) -> None:
    """
    Tests adding a new book.
    """
    url = fastapi_app.url_path_for("create_book")
    payload = {
        "title": "The Great Gatsby",
        "description": "A novel by F. Scott Fitzgerald",
        "author_id": 1,
        "remaining_amount": 5
    }
    response = await client.post(url, json=payload)
    assert response.status_code == status.HTTP_201_CREATED
    response_data = response.json()["data"]
    assert response_data["title"] == payload["title"]
    assert response_data["description"] == payload["description"]
    assert response_data["author_id"] == payload["author_id"]
    assert response_data["remaining_amount"] == payload["remaining_amount"]

@pytest.mark.anyio
async def test_get_books(client: AsyncClient, fastapi_app: FastAPI) -> None:
    """
    Tests retrieving the list of books.
    """
    url = fastapi_app.url_path_for("list_books")
    response = await client.get(url)
    assert response.status_code == status.HTTP_200_OK
    response_data = response.json()["data"]
    assert isinstance(response_data, list)

@pytest.mark.anyio
async def test_get_book_by_id(client: AsyncClient, fastapi_app: FastAPI) -> None:
    """
    Tests retrieving a book by its ID.
    """
    book_id = 1
    url = fastapi_app.url_path_for("get_book_info", id=book_id)
    response = await client.get(url)
    assert response.status_code == status.HTTP_200_OK
    response_data = response.json()["data"]
    assert response_data["id"] == book_id

@pytest.mark.anyio
async def test_update_book(client: AsyncClient, fastapi_app: FastAPI) -> None:
    """
    Tests updating book information.
    """
    book_id = 1
    url = fastapi_app.url_path_for("update_book", id=book_id)
    payload = {
        "title": "The Great Gatsby - Updated",
        "description": "Updated description",
        "remaining_amount": 10
    }
    response = await client.put(url, json=payload)
    assert response.status_code == status.HTTP_200_OK
    response_data = response.json()["data"]
    assert response_data == 1
    
    url = fastapi_app.url_path_for("get_book_info", id=book_id)
    response = await client.get(url)
    
    assert response.status_code == status.HTTP_200_OK
    response_data = response.json()["data"]
    for key in payload.keys():
        assert response_data[key] == payload[key]

@pytest.mark.anyio
async def test_partial_update_book(client: AsyncClient, fastapi_app: FastAPI) -> None:
    """
    Tests updating book information.
    """
    book_id = 1
    url = fastapi_app.url_path_for("update_book", id=book_id)
    payload = {
        "title": "The Great Gatsby - Updated again",
    }
    response = await client.put(url, json=payload)
    assert response.status_code == status.HTTP_200_OK
    response_data = response.json()["data"]
    assert response_data == 1
    
    url = fastapi_app.url_path_for("get_book_info", id=book_id)
    response = await client.get(url)
    
    assert response.status_code == status.HTTP_200_OK
    response_data = response.json()["data"]
    for key in payload.keys():
        assert response_data[key] == payload[key]
    

@pytest.mark.anyio
async def test_delete_book(client: AsyncClient, fastapi_app: FastAPI) -> None:
    """
    Tests deleting a book by its ID.
    """
    book_id = 1
    url = fastapi_app.url_path_for("delete_book", id=book_id)
    response = await client.delete(url)
    assert response.status_code == status.HTTP_204_NO_CONTENT
    get_url = fastapi_app.url_path_for("get_book_info", id=book_id)
    get_response = await client.get(get_url)
    assert get_response.status_code == status.HTTP_404_NOT_FOUND

@pytest.mark.anyio
async def test_create_book_invalid_data(client: AsyncClient, fastapi_app: FastAPI) -> None:
    """
    Tests creating a book with invalid or missing data.
    """
    url = fastapi_app.url_path_for("create_book")

    response = await client.post(url, json={})
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    payload = {"title": 123, "description": [], "author_id": "invalid", "remaining_amount": "not-a-number"}
    response = await client.post(url, json=payload)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

@pytest.mark.anyio
async def test_get_books_empty_list(client: AsyncClient, fastapi_app: FastAPI) -> None:
    """
    Tests retrieving a list of books when none exist.
    """
    url = fastapi_app.url_path_for("list_books")
    response = await client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["data"] == []

@pytest.mark.anyio
async def test_get_non_existent_book(client: AsyncClient, fastapi_app: FastAPI) -> None:
    """
    Tests retrieving a non-existent book by ID.
    """
    url = fastapi_app.url_path_for("get_book_info", id=99999)  
    response = await client.get(url)
    assert response.status_code == status.HTTP_404_NOT_FOUND

@pytest.mark.anyio
async def test_update_non_existent_book(client: AsyncClient, fastapi_app: FastAPI) -> None:
    """
    Tests updating a non-existent book.
    """
    url = fastapi_app.url_path_for("update_book", id=99999)  
    payload = {"title": "Non-existent", "description": "Book", "author_id": 1, "remaining_amount": 10}
    response = await client.put(url, json=payload)
    assert response.status_code == status.HTTP_404_NOT_FOUND

@pytest.mark.anyio
async def test_delete_non_existent_book(client: AsyncClient, fastapi_app: FastAPI) -> None:
    """
    Tests deleting a non-existent book.
    """
    url = fastapi_app.url_path_for("delete_book", id=99999)  
    response = await client.delete(url)
    assert response.status_code == status.HTTP_404_NOT_FOUND

@pytest.mark.anyio
async def test_create_book_boundary_remaining_amount(client: AsyncClient, fastapi_app: FastAPI) -> None:
    """
    Tests creating books with boundary remaining_amount values.
    """
    url = fastapi_app.url_path_for("create_book")

    payload_negative = {"title": "Negative", "description": "Amount", "author_id": 1, "remaining_amount": -1}
    response_negative = await client.post(url, json=payload_negative)
    assert response_negative.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    payload_large = {"title": "Large", "description": "Amount", "author_id": 1, "remaining_amount": 10**9}
    response_large = await client.post(url, json=payload_large)
    assert response_large.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY