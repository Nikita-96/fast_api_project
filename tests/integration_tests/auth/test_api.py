import pytest


@pytest.mark.parametrize("email, password, status_code", [
    ("kot1@pes.com", "1234", 200),
    ("kot1@pes.com", "1234", 401),
    ("kot2@pes.com", "1234", 200),
    ("kot3@pes.com", "1234", 200),
    ("kot3@pes", "1234", 409),
    ("kot3", "1234", 409,)
])
async def test_auth_flow(email: str, password: str, status_code: int, ac):

    response_log = await ac.post(
        "/auth/register",
        json={
            "email": email,
            "password": password
        }
    )
    assert response_log.status_code == status_code
    if status_code != 200:
        return

    response_log = await ac.post(
        "/auth/login",
        json={
            "email": email,
            "password": password
        }
    )
    assert response_log.status_code == status_code
    assert ac.cookies["access_token"]
    assert "access_token" in response_log.json()

    response_me = await ac.get("/auth/me")
    assert response_me.status_code == status_code
    user = response_me.json()
    assert user["email"] == email
    assert "id" in user
    assert "password" not in user
    assert "hashed_password" not in user

    response_logout = await ac.post("/auth/logout")
    assert response_logout.status_code == status_code
    assert "access_token" not in ac.cookies

