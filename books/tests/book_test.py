""" import pytest
from httpx import AsyncClient, ASGITransport
from main import app
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
import pytest_asyncio

from database import MONGODB_URI

# Configurar la base de datos de pruebas
@pytest_asyncio.fixture(scope="function")
async def client():
    async with AsyncClient(transport=ASGITransport(app), base_url='http://localhost') as ac:
        yield ac  # Devolver el cliente para las pruebas

@pytest_asyncio.fixture(scope="function")
async def db():
    client = AsyncIOMotorClient(MONGODB_URI)
    db = client["test_database"]
    yield db  # Devolver la base de datos para las pruebas
    # Limpiar la base de datos después de que terminen las pruebas
    await client.drop_database("test_database")
    client.close()

@pytest.mark.asyncio
async def test_update_book(client: AsyncClient, db):
    # Insertar un libro de prueba en la colección "books"
    book_data = {
        "title": "Test Book",
        "author": "Original Author",
        "image": "test_image.png",
        "summary": "This is a test summary.",
        "isbn": "1234567890",
        "contact": {
            "name": "Author Name",
            "email": "author@example.com"
        }
    }
    # Inserción en la colección "books"
    result = await db["books"].insert_one(book_data)
    book_id = str(result.inserted_id)
    # Datos para actualizar
    update_data = {
        "author": "Updated Author"
    }


    # Realizar la solicitud PUT para actualizar el libro
    response = await client.put(f"/api/books/{book_id}", json=update_data)   
  

    assert response.status_code == 200
    assert response.json() == {"status": "success"}


    # Verificar que el autor se haya actualizado en la base de datos
    updated_book = await db["books"].find_one({"_id": ObjectId(book_id)})
    assert updated_book["author"] == "Updated Author"
    assert updated_book["title"] == "Test Book"

@pytest.mark.asyncio
async def test_update_book_not_found(client: AsyncClient, db):
    # ID inexistente
    fake_id = str(ObjectId())
    update_data = {
        "author": "Nonexistent Author"
    }

    response = await client.put(f"/api/books/{fake_id}", json=update_data)
    assert response.status_code == 404
    assert response.json() == {"detail": "Book not found"}

@pytest.mark.asyncio
async def test_update_book_invalid_objectid(client: AsyncClient, db):
    # ID inválido
    invalid_id = "invalid_id"
    update_data = {
        "author": "Author Name"
    }

    response = await client.put(f"/api/books/{invalid_id}", json=update_data)
    assert response.status_code == 400
    assert response.json() == {"detail": "Invalid ObjectId"}
 """