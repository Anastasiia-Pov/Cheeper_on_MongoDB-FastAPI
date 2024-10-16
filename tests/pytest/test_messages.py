from httpx import AsyncClient
from datetime import date


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


async def test_add_message1(client_test: AsyncClient):
    response = await client_test.post("/messages", json=message1)
    assert response.status_code == 201
    msg = response.json()
    assert msg["message"] == "New message created successfully."


async def test_add_message2(client_test: AsyncClient):
    response = await client_test.post("/messages", json=message2)
    assert response.status_code == 201
    msg = response.json()
    assert msg["message"] == "New message created successfully."


# existing user
async def test_get_messages_by_user(client_test: AsyncClient):
    response = await client_test.get("/messages/pytestuser")
    assert response.status_code == 200
    msg = response.json()
    assert len(msg) == 2


# nonexisting user
async def test_get_messages_by_nonuser(client_test: AsyncClient):
    response = await client_test.get("/messages/user1324")
    assert response.status_code == 404
    msg = response.json()
    print(msg)
    assert msg["message"] == "Messages not found or user does not exists."


# no messages in a given range
async def test_get_messages_in_range_1(client_test: AsyncClient):
    response = await client_test.get("/messages_in_range/pytestuser",
                                     params={"from_date": date(2020, 10, 14),
                                             "to_date": date(2020, 10, 14)})
    assert response.status_code == 404
    msg = response.json()
    assert msg['message'] == "User has no messages in a given range."


# messages are in a given range
async def test_get_messages_in_range_2(client_test: AsyncClient):
    response = await client_test.get("/messages_in_range/pytestuser",
                                     params={"from_date": date(2020, 10, 14),
                                             "to_date": date(2040, 10, 14)})
    assert response.status_code == 200
    msg = response.json()
    assert len(msg) == 2


# one message is in a given range
async def test_get_messages_in_range_3(client_test: AsyncClient):
    response = await client_test.get("/messages_in_range/pytestuser",
                                     params={"from_date": date(2020, 10, 14),
                                             "to_date": date(2024, 10, 15)})
    assert response.status_code == 200
    msg = response.json()
    assert len(msg) == 1


async def test_get_message_by_id(client_test: AsyncClient):
    response = await client_test.get(f"/message/{message1['_id']}")
    assert response.status_code == 200
    msg = response.json()
    assert msg["_id"] == message1['_id']
    assert msg["username"] == message1["username"]


async def test_patch_message(client_test: AsyncClient):
    response = await client_test.patch(f"/message/{message1['_id']}",
                                       params={"upd_text": "Text for message1 by pytestuser updated."})
    assert response.status_code == 201
    msg = response.json()
    assert msg["message"] == "Message updated successfully."


async def test_delete_message1(client_test: AsyncClient):
    response = await client_test.delete(f"/message/{message1['_id']}")
    assert response.status_code == 200
    msg = response.json()
    assert msg["message"] == "Message deleted successfully."


async def test_delete_message2(client_test: AsyncClient):
    response = await client_test.delete(f"/message/{message2['_id']}")
    assert response.status_code == 200
    msg = response.json()
    assert msg["message"] == "Message deleted successfully."
