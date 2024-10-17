from httpx import AsyncClient
from datetime import datetime


user1 = {
    "_id": "5eb7cf5a86d9755df3a6c593",
    "name": "testuser1",
    "username": "testuser1",
    "email": "testuser1@example.com",
    "hashed_password": "!TestUser1"
}

project_user1 = {
    "name": "testuser1",
    "username": "testuser1",
    "email": "testuser1@example.com",
}

user2 = {
    "_id": "5eb7cf5a86d9755df3a6c594",
    "name": "testuser2",
    "username": "testuser2",
    "email": "testuser2@example.com",
    "hashed_password": "_TestUser2"
}

project_user2 = {
    "name": "testuser2",
    "username": "testuser2",
    "email": "testuser2@example.com",
}


friends_request1 = {
    "_id": "5eb7cf5a86d9755df3a6c595",
    "request_sender": user1["username"],
    "request_getter": user2["username"]
    }

friends_request_for_nonuser = {
    "_id": "5eb7cf5a86d9755df3a6c595",
    "request_sender": user1["username"],
    "request_getter": 'non_existing_user1234'
    }


# Registration check
async def test_regist_user1(client_test: AsyncClient):
    response = await client_test.post("/regist/user", json=user1)
    assert response.status_code == 201
    msg = response.json()
    print(msg)
    assert msg["message"] == "New user created successfully."


async def test_regist_user2(client_test: AsyncClient):
    response = await client_test.post("/regist/user", json=user2)
    assert response.status_code == 201
    msg = response.json()
    print(msg)
    assert msg["message"] == "New user created successfully."


async def test_regist_user1_again(client_test: AsyncClient):
    response = await client_test.post("/regist/user", json=user1)
    assert response.status_code == 409
    msg = response.json()
    print(msg)
    assert msg["message"] == "Username already registered. Please, change username."


async def test_get_user1(client_test: AsyncClient):
    response = await client_test.get(f"/regist/user/{user1['username']}")
    assert response.status_code == 200
    msg = response.json()
    assert msg == project_user1


# Friends Requests check
# POST new friends request
async def test_post_friendsrequest(client_test: AsyncClient):
    response = await client_test.post(f"/friends/requests/{user1['username']}",
                                      json=friends_request1)
    assert response.status_code == 201
    msg = response.json()
    assert msg["message"] == "Friend request was sent successfully."


# POST friends request again, request already exists
async def test_post_friendsrequest_again(client_test: AsyncClient):
    response = await client_test.post(f"/friends/requests/{user1['username']}",
                                      json=friends_request1)
    assert response.status_code == 409
    msg = response.json()
    assert msg["message"] == "Request already exists."


async def test_post_friendsrequest_for_nonuser(client_test: AsyncClient):
    response = await client_test.post(f"/friends/requests/{user1['username']}",
                                      json=friends_request_for_nonuser)
    assert response.status_code == 404
    msg = response.json()
    assert msg["message"] == "User not found."


# GET REQUEST
async def test_get_friendsrequests_user1(client_test: AsyncClient):
    response = await client_test.get(f"/friends/requests/{user1['username']}")
    assert response.status_code == 200
    msg = response.json()
    assert msg == [friends_request1]


async def test_get_friendsrequests_user2(client_test: AsyncClient):
    response = await client_test.get(f"/friends/requests/{user2['username']}")
    assert response.status_code == 200
    msg = response.json()
    assert msg == [friends_request1]


# PATCH REQUEST
async def test_patch_friendsrequests(client_test: AsyncClient):
    response = await client_test.patch("/friends/requests",
                                       json=friends_request1)
    assert response.status_code == 200
    msg = response.json()
    print(msg)
    assert msg["message"] == f"{user1['username']} and {user2['username']} are now friends!"


# POST REQUEST: users are alreadt friends
async def test_post_friendsrequest_for_friends(client_test: AsyncClient):
    response = await client_test.post(f"/friends/requests/{user1['username']}",
                                      json=friends_request1)
    assert response.status_code == 409
    msg = response.json()
    assert msg["message"] == "Users are already friends"


async def test_get_friends_for_user1(client_test: AsyncClient):
    response = await client_test.get(f"/friends/{user1['username']}")
    assert response.status_code == 200
    msg = response.json()
    assert len(msg) == 1


async def test_get_friends_for_user2(client_test: AsyncClient):
    response = await client_test.get(f"/friends/{user1['username']}")
    assert response.status_code == 200
    msg = response.json()
    assert len(msg) == 1


async def test_get_numfriends_for_user1(client_test: AsyncClient):
    response = await client_test.get(f"/friends/numfriends/{user1['username']}")
    assert response.status_code == 200
    msg = response.json()
    assert msg == 'User testuser1 has 1 friends'


# Delete users
async def test_delete_user1(client_test: AsyncClient):
    response = await client_test.delete(f"/regist/user/{user1['_id']}")
    assert response.status_code == 200
    msg = response.json()
    assert msg["message"] == "User deleted successfully"


async def test_delete_user1_again(client_test: AsyncClient):
    response = await client_test.delete(f"/regist/user/{user1['_id']}")
    assert response.status_code == 404
    msg = response.json()
    assert msg["message"] == "No user found."


async def test_delete_user2(client_test: AsyncClient):
    response = await client_test.delete(f"/regist/user/{user2['_id']}")
    assert response.status_code == 200
    msg = response.json()
    assert msg["message"] == "User deleted successfully"
