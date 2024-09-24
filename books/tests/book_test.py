import pytest
from httpx import AsyncClient
from main import app
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId

# Configurar la base de datos de pruebas
@pytest.fixture(scope="module")
async def client():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac

@pytest.fixture(scope="module")
async def db():
    client = AsyncIOMotorClient("mongodb://localhost:27017")
    db = client["test_database"]
    yield db
    await client.drop_database("test_database")
    client.close()  # Cerrar el cliente después de la prueba

@pytest.mark.asyncio
async def test_update_book(client, db):
    # Insertar un libro de prueba
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
    result = await db.books.insert_one(book_data)
    book_id = str(result.inserted_id)

    # Datos para actualizar
    update_data = {
        "author": "Updated Author"
    }

    # Realizar la solicitud PUT para actualizar el libro
    response = await client.put(f"/books/{book_id}", json=update_data)
    assert response.status_code == 200
    assert response.json() == {"status": "success"}

    # Verificar que el autor se haya actualizado en la base de datos
    updated_book = await db.books.find_one({"_id": ObjectId(book_id)})
    assert updated_book["author"] == "Updated Author"
    assert updated_book["title"] == "Test Book"  # Otros campos permanecen iguales

@pytest.mark.asyncio
async def test_update_book_not_found(client, db):
    # ID inexistente
    fake_id = str(ObjectId())
    update_data = {
        "author": "Nonexistent Author"
    }

    response = await client.put(f"/books/{fake_id}", json=update_data)
    assert response.status_code == 404
    assert response.json() == {"detail": "Book not found"}

@pytest.mark.asyncio
async def test_update_book_invalid_objectid(client, db):
    # ID inválido
    invalid_id = "invalid_id"
    update_data = {
        "author": "Author Name"
    }

    response = await client.put(f"/books/{invalid_id}", json=update_data)
    assert response.status_code == 400
    assert response.json() == {"detail": "Invalid ObjectId"}
