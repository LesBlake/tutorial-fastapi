from app import schemas


def test_root(client):
    resp = client.get("/")
    assert resp.json().get("message") == "Welcome to my API."
    assert resp.status_code == 200


def test_users_create_user(client):
    resp = client.post(
        "/users/", json={"email": "les.blake@gmail.com", "password": "passyword"}
    )
    new_user_response_schema = schemas.User(**resp.json())

    assert resp.status_code == 201
    assert new_user_response_schema.email == "les.blake@gmail.com"


def atest_user_get_all_users(client):
    resp = client.get("/users/")
    print(resp.json())
