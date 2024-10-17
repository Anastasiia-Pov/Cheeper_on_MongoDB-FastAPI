from httpx import AsyncClient
from datetime import date


user1 = {
    "_id": "5eb7cf5a86d5755df3a6c593",
    "name": "testuser3",
    "username": "testuser3",
    "email": "testuser3@example.com",
    "hashed_password": "!TestUser1"
}


pytestuser = {
    "_id": "5eb7cf5a36d9755df3a6c594",
    "name": "pytestuser",
    "username": "pytestuser",
    "email": "pytestuser@example.com",
    "hashed_password": "1PyTestUser!"
}


message1 = {
    '_id': "670fbba83aaf5f12186d718d",
    "text": "New message by pytestuser",
    "created_at": "2024-10-14T15:18:29.735625",
    "updated_at": "2024-10-14T15:18:29.735627",
    "username": "pytestuser"
}

message2 = {
    '_id': "5eb7cf5a86d9755df3a6c593",
    "text": "One more message by pytestuser",
    "created_at": "2024-10-20T15:18:29.735625",
    "updated_at": "2024-10-20T15:18:29.735627",
    "username": "pytestuser"
}


# Register users
async def test_regist_user1(client_test: AsyncClient):
    response = await client_test.post("regist/user", json=user1)
    assert response.status_code == 201
    msg = response.json()
    print(msg)
    assert msg["message"] == "New user created successfully."


async def test_regist_user2(client_test: AsyncClient):
    response = await client_test.post("regist/user", json=pytestuser)
    assert response.status_code == 201
    msg = response.json()
    print(msg)
    assert msg["message"] == "New user created successfully."


async def test_add_message1(client_test: AsyncClient):
    response = await client_test.post("messages/new", json=message1)
    assert response.status_code == 201
    msg = response.json()
    assert msg["message"] == "New message created successfully."


async def test_add_message2(client_test: AsyncClient):
    response = await client_test.post("messages/new", json=message2)
    assert response.status_code == 201
    msg = response.json()
    assert msg["message"] == "New message created successfully."


# existing user
async def test_get_messages_by_user(client_test: AsyncClient):
    response = await client_test.get("messages/by_username/pytestuser")
    assert response.status_code == 200
    msg = response.json()
    assert len(msg) == 2


# nonexisting user
async def test_get_messages_by_nonuser(client_test: AsyncClient):
    response = await client_test.get("messages/by_username/user1324")
    assert response.status_code == 404
    msg = response.json()
    print(msg)
    assert msg["message"] == "Messages not found or user does not exists."


# no messages in a given range
async def test_get_messages_in_range_1(client_test: AsyncClient):
    response = await client_test.get("messages/in_range/pytestuser",
                                     params={"from_date": date(2020, 10, 14),
                                             "to_date": date(2020, 10, 14)})
    assert response.status_code == 404
    msg = response.json()
    assert msg['message'] == "User has no messages in a given range."


# messages are in a given range
async def test_get_messages_in_range_2(client_test: AsyncClient):
    response = await client_test.get("messages/in_range/pytestuser",
                                     params={"from_date": date(2020, 10, 14),
                                             "to_date": date(2040, 10, 14)})
    assert response.status_code == 200
    msg = response.json()
    assert len(msg) == 2


# one message is in a given range
async def test_get_messages_in_range_3(client_test: AsyncClient):
    response = await client_test.get("messages/in_range/pytestuser",
                                     params={"from_date": date(2020, 10, 14),
                                             "to_date": date(2024, 10, 15)})
    assert response.status_code == 200
    msg = response.json()
    assert len(msg) == 1


async def test_get_message_by_id(client_test: AsyncClient):
    response = await client_test.get(f"messages/by_id/{message1['_id']}")
    assert response.status_code == 200
    msg = response.json()
    assert msg["_id"] == message1['_id']
    assert msg["username"] == message1["username"]


async def test_patch_message(client_test: AsyncClient):
    response = await client_test.patch(f"messages/update/{message1['_id']}",
                                       params={"upd_text": "Text for message1 by pytestuser updated."})
    assert response.status_code == 201
    msg = response.json()
    assert msg["message"] == "Message updated successfully."


# Testing likes
async def test_like_message(client_test: AsyncClient):
    response = await client_test.patch(f"messages/like/{message1['_id']}",
                                       params={"username": user1["username"]})
    assert response.status_code == 200
    msg = response.json()
    print(msg)
    assert msg["message"] == "Liked"


async def test_like_message_again(client_test: AsyncClient):
    response = await client_test.patch(f"messages/like/{message1['_id']}",
                                       params={"username": user1["username"]})
    assert response.status_code == 409
    msg = response.json()
    print(msg)
    assert msg["message"] == "Message was already liked."


# Delete tests
async def test_delete_message1(client_test: AsyncClient):
    response = await client_test.delete(f"messages/delete/{message1['_id']}")
    assert response.status_code == 200
    msg = response.json()
    assert msg["message"] == "Message deleted successfully."


async def test_delete_message2(client_test: AsyncClient):
    response = await client_test.delete(f"messages/delete/{message2['_id']}")
    assert response.status_code == 200
    msg = response.json()
    assert msg["message"] == "Message deleted successfully."


async def test_delete_user1(client_test: AsyncClient):
    response = await client_test.delete(f"/regist/user/{user1['_id']}")
    assert response.status_code == 200
    msg = response.json()
    assert msg["message"] == "User deleted successfully"


async def test_delete_user2(client_test: AsyncClient):
    response = await client_test.delete(f"/regist/user/{pytestuser['_id']}")
    assert response.status_code == 200
    msg = response.json()
    assert msg["message"] == "User deleted successfully"