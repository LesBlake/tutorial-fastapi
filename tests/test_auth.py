import pytest
from app import schemas
from app.util import utils


def test_login_user(client, test_user):
    resp = client.post(
        "/login/",
        data={"username": test_user["email"], "password": test_user["password"]},
    )
    assert resp.status_code == 200
    assert schemas.Token(**resp.json())

    token_data = utils.verify_access_token(
        schemas.Token(**resp.json()).access_token, test_user["cred_err"]
    )

    assert token_data.id == str(test_user["id"])
    assert token_data.email == test_user["email"]


@pytest.mark.parametrize(
    "email, passwd, status_code",
    [
        ("egon@gmail.com", "WRONG", 403),
        ("WRONG@gmail.com", "ghostyboys123", 403),
        ("Wrong@gmail.com", "wrongpassy", 403),
        (None, "ghostyboys123", 422),
        ("egon@gmail.com", None, 422),
        (None, None, 422),
    ],
)
def test_login_user_invalid_password(client, email, passwd, status_code):
    resp = client.post(
        "/login/",
        data={
            "username": email,
            "password": passwd,
        },
    )
    assert resp.status_code == status_code
    if resp.status_code == 403:
        assert resp.json().get("detail") == "Invalid Credentials"
