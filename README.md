# Cheeper_on_MongoDB-FastAPI

### Requirements
Python 3.12 with all the [requirements.txt](https://github.com/Anastasiia-Pov/Cheeper_on_MongoDB-FastAPI/blob/main/requirements.txt) dependencies installed.


### Project structure: Backend

```
Cheeper-project
├─ src/                                     # highest level of the app, contains common models, configs, and constants, etc.
│  ├─ routers/                              # core of each module with all the endpoints of the app
│  │  ├─ friends.py                         # all the endpoints of the app for friends requests
│  │  ├─ messages.py                        # all the endpoints of the app for messages CRUD
│  │  ├─ users.py                           # all the endpoints of the app for users (create, get user by id)
├─ tests/                                   # tests for functions and api
│  ├─ function_tests/                       # tests for functions
│  │  ├─ test_hash.py                       # test hashing passwords
│  │  ├─ test_password.py                   # test password validation
│  │  ├─ test_user.py                       # test username validation
│  ├─ pytest/                               # tests for api requests
│  │  ├─ conftest.py                        # pytest configuration file
│  │  ├─ test_messages.py                   # test endpoints for messages
│  │  ├─ test_user_and_friends_requests.py  # test endpoints for users and friends requests
│  ├─ Cheeper.postman_collection.json       # postman tests for api
│  ├─ config.py                             # env vars
│  ├─ main.py                               # root of the project, which inits the FastAPI app
│  ├─ models.py                             # db models
│  ├─ mongo_db.py                           # db and models initializations
│  ├─ service_for_passwords.py              # module specific business logic (functions for password checking and hashing)
│  ├─ service_for_users.py                  # module specific business logic (functions for username checking)
│  ├─ pytest.ini                            # pytest configuration file
```


### Scheme of the Cheeper app

<img src="https://github.com/Anastasiia-Pov/Cheeper_on_MongoDB-FastAPI/blob/main/assets/Cheeper.png">


### Launch Cheeper app
- install depandencies from requirements.txt;
- run virtual environment by command ```source <<dir where virtual environment located/bin/activate>>```;
- start app being in the ```src``` dir by command ```uvicorn main:app --reload```.
