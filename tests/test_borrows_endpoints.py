import pytest
from httpx import AsyncClient
from fastapi import FastAPI, status
from datetime import date

@pytest.mark.anyio
async def test_add_borrow(client: AsyncClient, fastapi_app: FastAPI) -> None:
    """
    Tests adding a new book.
    """
    url = fastapi_app.url_path_for("create_book")
    book_payload = {
        "title": "The Great Gatsby",
        "description": "A novel by F. Scott Fitzgerald",
        "author_id": 1,
        "remaining_amount": 5
    }
    response = await client.post(url, json=book_payload)
    assert response.status_code == status.HTTP_201_CREATED
    
    borrow_payload = {
        "book_id": response.json()["data"]["id"],
        "reader_name": "abyss",
    }
    url = fastapi_app.url_path_for("create_borrow")
    response = await client.post(url, json=borrow_payload)
    assert response.status_code == status.HTTP_201_CREATED
    
    response_data = response.json()["data"]
    
    assert response_data["book_id"] == borrow_payload["book_id"]
    assert response_data["reader_name"] == borrow_payload["reader_name"]
    assert response_data["date_of_issue"] == str(date.today())
    assert "date_of_return" not in response_data

@pytest.mark.anyio
async def test_create_borrow_with_invalid_book_id(client: AsyncClient, fastapi_app: FastAPI) -> None:
    """
    Tests attempts in new borrow registration with invalid book id.
    """
    borrow_payload = {
        "book_id": 99999,
        "reader_name": "abyss",
    }
    url = fastapi_app.url_path_for("create_borrow")
    response = await client.post(url, json=borrow_payload)
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.anyio
async def test_get_borrows(client: AsyncClient, fastapi_app: FastAPI) -> None:
    """
    Tests retrieving the list of borrows.
    """
    url = fastapi_app.url_path_for("list_borrows")
    response = await client.get(url)
    assert response.status_code == status.HTTP_200_OK
    response_data = response.json()["data"]
    assert isinstance(response_data, list)

@pytest.mark.anyio
async def test_get_borrow_by_id(client: AsyncClient, fastapi_app: FastAPI) -> None:
    """
    Tests retrieving a borrow by its ID.
    """
    borrow_id = 1
    url = fastapi_app.url_path_for("get_borrow_info", id=borrow_id)
    response = await client.get(url)
    assert response.status_code == status.HTTP_200_OK
    response_data = response.json()["data"]
    assert response_data["id"] == borrow_id

@pytest.mark.anyio
async def test_get_borrow_by_invalid_id(client: AsyncClient, fastapi_app: FastAPI) -> None:
    """
    Tests retrieving a borrow by invalid ID.
    """
    borrow_id = 99999
    url = fastapi_app.url_path_for("get_borrow_info", id=borrow_id)
    response = await client.get(url)
    assert response.status_code == status.HTTP_404_NOT_FOUND

@pytest.mark.anyio
async def test_patch_borrow(client: AsyncClient, fastapi_app: FastAPI) -> None:
    """
    Tests patching borrow information.
    Verifies related borrow entity is updated with value in field "date_of_return"
    Verifies related book item is updated after borrow entity patching.
    Verifies related book item is not updated on repeated borrow entity patching.
    """
    borrow_id = 1
    url = fastapi_app.url_path_for("get_borrow_info", id=borrow_id)
    response = await client.get(url)
    book_id = response.json()["data"]["book_id"]
    url = fastapi_app.url_path_for("get_book_info", id=book_id)
    response = await client.get(url)
    old_book_remaining_amount = response.json()["data"]["remaining_amount"]
    
    url = fastapi_app.url_path_for("return_borrow", id=borrow_id)
    response = await client.patch(url)
    assert response.status_code == status.HTTP_204_NO_CONTENT
    
    url = fastapi_app.url_path_for("get_borrow_info", id=borrow_id)
    response = await client.get(url)
    assert response.status_code == status.HTTP_200_OK
    new_borrow_data = response.json()["data"]
    
    url = fastapi_app.url_path_for("get_book_info", id=book_id)
    response = await client.get(url)
    assert response.status_code == status.HTTP_200_OK
    new_book_remaining_amount = response.json()["data"]["remaining_amount"]
    
    url = fastapi_app.url_path_for("return_borrow", id=borrow_id)
    response = await client.patch(url)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    
    url = fastapi_app.url_path_for("get_book_info", id=book_id)
    response = await client.get(url)
    assert response.status_code == status.HTTP_200_OK
    newest_book_remaining_amount = response.json()["data"]["remaining_amount"]
    
    assert new_borrow_data["date_of_return"] == str(date.today())
    assert old_book_remaining_amount + 1 == new_book_remaining_amount
    assert new_book_remaining_amount == newest_book_remaining_amount

@pytest.mark.anyio
async def test_delete_with_borrow_integrity_violation(client: AsyncClient, fastapi_app: FastAPI) -> None:
    """
    Tests deleting a book with related borrows.
    """
    url = fastapi_app.url_path_for("list_books")
    response = await client.get(url)
    assert response.status_code == status.HTTP_200_OK
    
    book_id = response.json()["data"][0]["id"]
    
    url = fastapi_app.url_path_for("create_borrow")
    payload = {
        "book_id": book_id,
        "reader_name": "abyss",
    }
    response = await client.post(url, json=payload)
    assert response.status_code == status.HTTP_201_CREATED
    
    url = fastapi_app.url_path_for("delete_book", id=book_id)
    response = await client.delete(url)
    assert response.status_code == status.HTTP_400_BAD_REQUEST