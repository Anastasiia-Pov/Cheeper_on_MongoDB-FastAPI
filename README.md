# Cheeper_on_MongoDB-FastAPI

### Requirements
Python 3.12 with all the [requirements.txt](https://github.com/Anastasiia-Pov/Cheeper_on_MongoDB-FastAPI/blob/main/requirements.txt) dependencies installed.


### Project structure: Backend

```
Cheeper-project
├─ src/                 # highest level of the app, contains common models, configs, and constants, etc.
│  ├─ routers/          # core of each module with all the endpoints of the app
│  │  ├─ friends.py     # all the endpoints of the app for friends requests
│  │  ├─ messages.py    # all the endpoints of the app for messages CRUD
│  │  ├─ users.py       # all the endpoints of the app for users (create, get user by id)
│  ├─ config.py         # env vars
│  ├─ main.py           # root of the project, which inits the FastAPI app
│  ├─ models.py         # db models
│  ├─ mongo_db.py       # db and models initializations
│  ├─ service.py        # module specific business logic (functions for password checking and hashing)
```


### Scheme of the Cheeper app

<img src="https://github.com/Anastasiia-Pov/Cheeper_on_MongoDB-FastAPI/blob/main/assets/Cheeper.jpg">