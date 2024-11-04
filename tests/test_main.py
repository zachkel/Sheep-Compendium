from fastapi.testclient import TestClient

from main import app

client = TestClient(app)

def test_read_sheep():
    response = client.get('/sheep/1')

    assert response.status_code == 200

    assert response.json() == {
        "id": 1,
        "name": "Spice",
        "breed": "Gotland",
        "sex": "ewe"
    }

def test_add_sheep():
    # Prepare the new sheep data in a dictionary format.
    new_sheep = {
        "id": 7,
        "name": "Rex",
        "breed": "Suffolk",
        "sex": "ram"
    }

    # Send a POST request to the endpoint "/sheep" with the new sheep data.
    #   Arguments should be your endpoint and new sheep data.
    response = client.post("/sheep", json=new_sheep)

    # Assert that the response status code is 201 (Created)
    assert response.status_code == 201

    #  Assert that the response JSON matches the new sheep data
    assert response.json() == new_sheep

    # Verify that the sheep was actually added to the database by retrieving the new sheep by ID.
    #   include an assert statement to see if the new sheep data can be retrieved.
    get_response = client.get(f"/sheep/{new_sheep['id']}")
    assert get_response.status_code == 200
    assert get_response.json() == new_sheep


def test_delete_sheep():
    response = client.delete("/sheep/1")
    assert response.status_code == 204

    get_response = client.get("/sheep/1")
    assert get_response.status_code == 404

def test_update_sheep():
    updated_sheep = {
        "id": 2,
        "name": "Lessie",
        "breed": "Lincoln Longwool",
        "sex": "ram"
    }

    response = client.put("/sheep/2", json=updated_sheep)
    assert response.status_code == 200
    assert response.json() == updated_sheep

    get_response = client.get("/sheep/2")
    assert get_response.status_code == 200
    assert get_response.json() == updated_sheep


def test_read_all_sheep():
    response = client.get("/sheep")
    assert response.status_code == 200

    # Verify that the response is a list
    sheep_data = response.json()
    assert isinstance(sheep_data, list)

    # Verify expected content if no changes have been made
    expected_sheep = [
        {"id": 1, "name": "Spice", "breed": "Gotland", "sex": "ewe"},
        {"id": 2, "name": "Blondie", "breed": "Polypay", "sex": "ram"},
        {"id": 3, "name": "Deedee", "breed": "Jacobs Four Horns", "sex": "ram"},
        {"id": 4, "name": "Rommy", "breed": "Romney", "sex": "ewe"},
        {"id": 5, "name": "Vala", "breed": "Valais Blacknose", "sex": "ewe"},
        {"id": 6, "name": "Esther", "breed": "Border Leicester", "sex": "ewe"},
    ]
    assert sheep_data == expected_sheep
