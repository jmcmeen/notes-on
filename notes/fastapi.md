# Introduction to FastAPI

## Table of Contents

- [What is FastAPI](#what-is-fastapi)
- [Installation](#installation)
- [Your First API](#your-first-api)
- [Path Parameters](#path-parameters)
- [Query Parameters](#query-parameters)
- [Request Body with Pydantic Models](#request-body-with-pydantic-models)
- [Response Models](#response-models)
- [CRUD API Example](#crud-api-example)
- [Dependency Injection](#dependency-injection)
- [Authentication](#authentication)
- [Middleware](#middleware)
- [Error Handling](#error-handling)
- [Background Tasks](#background-tasks)
- [File Upload](#file-upload)
- [WebSockets Basics](#websockets-basics)
- [Testing with TestClient](#testing-with-testclient)
- [Practice Exercises](#practice-exercises)
- [Summary](#summary)
- [Next Steps](#next-steps)
- [Additional Resources](#additional-resources)

---

## What is FastAPI

FastAPI is a modern, high-performance web framework for building APIs with Python 3.7+ based on standard Python type hints. It is built on top of Starlette for the web layer and Pydantic for data validation.

Key features include:
- Automatic interactive API documentation (Swagger UI and ReDoc)
- Type-safe request handling via Python type hints
- Asynchronous support out of the box
- Performance comparable to Node.js and Go frameworks
- Automatic data validation and serialization

---

## Installation

```python
# Install FastAPI and an ASGI server (uvicorn is the recommended choice)
# pip install fastapi uvicorn[standard]

# Verify the installation
import fastapi
print(fastapi.__version__)  # prints the installed version
```

---

## Your First API

```python
# main.py - A minimal FastAPI application
from fastapi import FastAPI

# Create the FastAPI application instance
app = FastAPI(
    title="My API",           # appears in the docs
    description="A demo API", # description in docs
    version="0.1.0"           # version shown in docs
)

# Define a root endpoint using a GET request
@app.get("/")
async def read_root():
    # Return a JSON response automatically
    return {"message": "Hello, World!"}

@app.get("/about")
def about():
    return {"app": "My First API", "version": "1.0.0"}

# Run with: uvicorn main:app --reload
# --reload enables auto-reload on code changes (development only)
# Server starts at http://127.0.0.1:8000
# Docs at http://127.0.0.1:8000/docs (Swagger UI)
```

---

## Path Parameters

```python
from fastapi import FastAPI
from enum import Enum

app = FastAPI()

# Path parameter defined in the URL template with curly braces
@app.get("/items/{item_id}")
def read_item(item_id: int):
    # item_id is automatically validated as an integer
    # If a non-integer is passed, FastAPI returns a 422 error
    return {"item_id": item_id}

# Multiple path parameters
@app.get("/users/{user_id}/posts/{post_id}")
def read_user_post(user_id: int, post_id: int):
    # Both parameters are extracted from the URL path
    return {"user_id": user_id, "post_id": post_id}

# Using Enum for constrained path parameters
class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"

@app.get("/models/{model_name}")
def get_model(model_name: ModelName):
    # Only accepts values defined in the ModelName enum
    return {"model_name": model_name}

# Path parameter with file path
@app.get("/files/{file_path:path}")
def read_file(file_path: str):
    # The :path converter captures the full remaining path including slashes
    return {"file_path": file_path}
```

---

## Query Parameters

```python
from fastapi import FastAPI, Query
from typing import Optional, List

app = FastAPI()

# Query parameters are function parameters not in the path
@app.get("/items/")
def read_items(skip: int = 0, limit: int = 10):
    # skip and limit come from the query string: /items/?skip=0&limit=10
    return {"skip": skip, "limit": limit}

# Required vs optional query parameters
@app.get("/search/")
def search(
    q: str,                        # required (no default value)
    page: int = 1,                 # optional with default
    sort: Optional[str] = None     # explicitly optional
):
    return {"query": q, "page": page, "sort": sort}

# Using Query for additional validation
@app.get("/items/validated/")
def read_items_validated(
    q: Optional[str] = Query(
        default=None,
        min_length=3,          # minimum string length
        max_length=50,         # maximum string length
        title="Search query",  # metadata for docs
    ),
    skip: int = Query(default=0, ge=0),      # greater than or equal to 0
    limit: int = Query(default=10, le=100),   # less than or equal to 100
):
    return {"q": q, "skip": skip, "limit": limit}
```

---

## Request Body with Pydantic Models

```python
from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import Optional

app = FastAPI()

# Define a Pydantic model for request body validation
class Item(BaseModel):
    name: str                                    # required field
    description: Optional[str] = None            # optional field
    price: float = Field(..., gt=0)              # required, must be > 0
    tax: Optional[float] = None                  # optional field
    tags: list[str] = []                         # optional with default empty list

# POST endpoint that accepts a request body
@app.post("/items/")
def create_item(item: Item):
    # FastAPI automatically reads JSON, validates against Item, returns 422 on failure
    item_dict = item.model_dump()  # convert to dictionary
    if item.tax:
        price_with_tax = item.price + item.tax
        item_dict.update({"price_with_tax": price_with_tax})
    return item_dict

# Combining path parameters, query parameters, and request body
@app.put("/items/{item_id}")
def update_item(
    item_id: int,               # path parameter
    item: Item,                 # request body (Pydantic model)
    q: Optional[str] = None    # query parameter
):
    result = {"item_id": item_id, **item.model_dump()}
    if q:
        result.update({"q": q})
    return result

# Nested models
class Address(BaseModel):
    street: str
    city: str
    zip_code: str

class User(BaseModel):
    name: str
    email: str
    address: Address           # nested Pydantic model

@app.post("/users/")
def create_user(user: User):
    # Nested validation happens automatically
    return user
```

---

## Response Models

```python
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

app = FastAPI()

# Input model (what the client sends)
class UserCreate(BaseModel):
    name: str
    email: str
    password: str           # included in input

# Output model (what the API returns)
class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    # password is excluded from the response

# Use response_model to control the output shape
@app.post("/users/", response_model=UserResponse)
def create_user(user: UserCreate):
    fake_db_user = {
        "id": 1,
        "name": user.name,
        "email": user.email,
        "password": user.password   # this will NOT appear in the response
    }
    return fake_db_user  # FastAPI filters using UserResponse

class Item(BaseModel):
    name: str
    price: float

# Returning a list of items
@app.get("/items/", response_model=List[Item])
def list_items():
    # FastAPI validates each item in the list against the model
    return [
        {"name": "Foo", "price": 10.0},
        {"name": "Bar", "price": 20.0},
    ]
```

---

## CRUD API Example

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

# In-memory storage for demonstration
db: dict[int, dict] = {}
counter = 0

class ItemCreate(BaseModel):
    name: str
    description: Optional[str] = None
    price: float

class ItemUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None

class ItemResponse(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    price: float

# CREATE
@app.post("/items/", response_model=ItemResponse, status_code=201)
def create_item(item: ItemCreate):
    global counter
    counter += 1
    item_data = {"id": counter, **item.model_dump()}
    db[counter] = item_data
    return item_data

# READ
@app.get("/items/{item_id}", response_model=ItemResponse)
def read_item(item_id: int):
    if item_id not in db:
        raise HTTPException(status_code=404, detail="Item not found")
    return db[item_id]

# UPDATE
@app.put("/items/{item_id}", response_model=ItemResponse)
def update_item(item_id: int, item: ItemUpdate):
    if item_id not in db:
        raise HTTPException(status_code=404, detail="Item not found")
    stored = db[item_id]
    update_data = item.model_dump(exclude_unset=True)  # only include set fields
    stored.update(update_data)
    return stored

# DELETE
@app.delete("/items/{item_id}", status_code=204)
def delete_item(item_id: int):
    if item_id not in db:
        raise HTTPException(status_code=404, detail="Item not found")
    del db[item_id]
    return None
```

---

## Dependency Injection

```python
from fastapi import FastAPI, Depends, Query, HTTPException, Header
from typing import Optional

app = FastAPI()

# A dependency is a callable that FastAPI resolves before the endpoint
def common_parameters(
    q: Optional[str] = None,
    skip: int = 0,
    limit: int = Query(default=100, le=100)
):
    return {"q": q, "skip": skip, "limit": limit}

@app.get("/items/")
def read_items(commons: dict = Depends(common_parameters)):
    # commons is the return value of common_parameters
    return {"params": commons}

# Dependency for verifying an API key
def verify_api_key(x_api_key: str = Header(...)):
    if x_api_key != "my-secret-key":
        raise HTTPException(status_code=403, detail="Invalid API key")
    return x_api_key

# Dependency with sub-dependencies
def get_current_user(api_key: str = Depends(verify_api_key)):
    # This depends on verify_api_key being resolved first
    return {"username": "admin", "api_key": api_key}

@app.get("/protected/")
def protected_route(user: dict = Depends(get_current_user)):
    return {"message": f"Hello, {user['username']}"}

# Class-based dependencies
class Paginator:
    def __init__(self, skip: int = 0, limit: int = 10):
        self.skip = skip
        self.limit = limit

@app.get("/paginated/")
def paginated_items(paginator: Paginator = Depends()):
    # FastAPI calls Paginator(skip=..., limit=...) with query params
    return {"skip": paginator.skip, "limit": paginator.limit}
```

---

## Authentication

```python
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from datetime import datetime, timedelta
import jwt  # requires: pip install PyJWT

app = FastAPI()

# OAuth2 scheme - tells FastAPI where to find the token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

SECRET_KEY = "your-secret-key-keep-it-secret"
ALGORITHM = "HS256"

fake_users_db = {
    "alice": {"username": "alice", "hashed_password": "fakehashed_secret123",
              "email": "alice@example.com"}
}

class Token(BaseModel):
    access_token: str
    token_type: str

class User(BaseModel):
    username: str
    email: str

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")  # "sub" is the subject claim
        if username is None:
            raise credentials_exception
    except jwt.PyJWTError:
        raise credentials_exception
    user = fake_users_db.get(username)
    if user is None:
        raise credentials_exception
    return User(**user)

@app.post("/token", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = fake_users_db.get(form_data.username)
    if not user or user["hashed_password"] != f"fakehashed_{form_data.password}":
        raise HTTPException(status_code=400, detail="Incorrect credentials")
    access_token = create_access_token(data={"sub": form_data.username})
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/users/me", response_model=User)
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user
```

---

## Middleware

```python
import time
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Middleware runs before and after every request
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)  # pass request to the next handler
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response

# CORS middleware for cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],   # allowed origins
    allow_credentials=True,
    allow_methods=["*"],                       # allow all HTTP methods
    allow_headers=["*"],                       # allow all headers
)
```

---

## Error Handling

```python
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

app = FastAPI()

# Basic HTTPException usage
@app.get("/items/{item_id}")
def read_item(item_id: int):
    if item_id == 0:
        raise HTTPException(
            status_code=404,
            detail="Item not found",
            headers={"X-Error": "Item lookup failed"}
        )
    return {"item_id": item_id}

# Custom exception class and handler
class ItemNotFoundException(Exception):
    def __init__(self, item_id: int):
        self.item_id = item_id

@app.exception_handler(ItemNotFoundException)
async def item_not_found_handler(request: Request, exc: ItemNotFoundException):
    return JSONResponse(
        status_code=404,
        content={"error": "item_not_found",
                 "message": f"Item {exc.item_id} does not exist"},
    )

# Override the default validation error handler
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={"error": "validation_error", "detail": exc.errors()},
    )
```

---

## Background Tasks

```python
from fastapi import FastAPI, BackgroundTasks

app = FastAPI()

# A function to run in the background
def write_log(message: str):
    with open("log.txt", "a") as f:
        f.write(f"{message}\n")

def send_notification(email: str, message: str):
    print(f"Sending to {email}: {message}")

@app.post("/items/")
def create_item(item: dict, background_tasks: BackgroundTasks):
    # Add tasks to run after the response is sent
    background_tasks.add_task(write_log, f"Item created: {item}")
    background_tasks.add_task(send_notification, "admin@example.com", "New item!")
    # Response is returned immediately; tasks run in the background
    return {"message": "Item created", "item": item}
```

---

## File Upload

```python
from fastapi import FastAPI, File, UploadFile
from typing import List
import shutil
from pathlib import Path

app = FastAPI()

# Simple file upload using bytes (loads entire file into memory)
@app.post("/files/")
def create_file(file: bytes = File(...)):
    return {"file_size": len(file)}

# UploadFile for large files (spooled to disk if too large)
@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile):
    contents = await file.read()
    return {
        "filename": file.filename,           # original filename
        "content_type": file.content_type,   # MIME type
        "size": len(contents)
    }

# Multiple file uploads
@app.post("/uploadfiles/")
async def create_upload_files(files: List[UploadFile]):
    return {"files": [{"filename": f.filename, "size": len(await f.read())}
                      for f in files]}

# Saving uploaded files to disk
UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

@app.post("/upload-and-save/")
async def upload_and_save(file: UploadFile):
    file_path = UPLOAD_DIR / file.filename
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return {"filename": file.filename, "saved_to": str(file_path)}
```

---

## WebSockets Basics

```python
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from typing import List

app = FastAPI()

# Basic WebSocket endpoint
@app.websocket("/ws")
async def websocket_endpoint(ws: WebSocket):
    await ws.accept()  # accept the WebSocket connection
    try:
        while True:
            data = await ws.receive_text()
            await ws.send_text(f"Echo: {data}")  # echo the message back
    except WebSocketDisconnect:
        print("Client disconnected")

# Connection manager for multiple clients (chat room pattern)
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

manager = ConnectionManager()

@app.websocket("/ws/chat/{client_id}")
async def chat_endpoint(websocket: WebSocket, client_id: int):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.broadcast(f"Client {client_id}: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"Client {client_id} left the chat")
```

---

## Testing with TestClient

```python
from fastapi import FastAPI
from fastapi.testclient import TestClient
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: str
    price: float

@app.get("/")
def read_root():
    return {"message": "Hello"}

@app.post("/items/", status_code=201)
def create_item(item: Item):
    return {"id": 1, **item.model_dump()}

# Create a TestClient instance (no server needed)
client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello"}

def test_create_item():
    response = client.post("/items/", json={"name": "Widget", "price": 9.99})
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Widget"
    assert "id" in data

def test_create_item_invalid():
    response = client.post("/items/", json={"name": "Widget"})  # missing price
    assert response.status_code == 422  # validation error
```

---

## Practice Exercises

1. **Basic API**: Build a TODO list API with endpoints to create, read, update, and delete tasks. Each task should have a title, description, completed status, and due date.

2. **Query Parameters**: Create an endpoint that accepts filtering, sorting, and pagination query parameters for a list of products.

3. **Authentication**: Implement a simple user registration and login system with JWT tokens and a protected profile endpoint.

4. **File Upload Service**: Build an API that accepts image uploads, validates file types (only .jpg, .png), limits file size, and returns metadata about the uploaded file.

5. **WebSocket Chat**: Create a simple chat application where multiple clients can connect via WebSockets and exchange messages in real time.

6. **Full CRUD with Validation**: Build a book library API with models for authors and books, input validation, response models that exclude internal fields, and proper error handling.

---

## Summary

FastAPI is a high-performance Python web framework that leverages type hints for automatic validation, serialization, and documentation. Key takeaways:

- FastAPI uses Python type hints and Pydantic models for request and response validation
- Path parameters, query parameters, and request bodies are automatically parsed and validated
- The dependency injection system allows clean, reusable code for authentication and shared logic
- Built-in support for async/await enables non-blocking I/O operations
- Interactive API documentation is generated automatically at `/docs` and `/redoc`
- TestClient provides synchronous testing without needing a running server
- Background tasks, file uploads, WebSockets, and middleware are supported out of the box

---

## Next Steps

- Explore database integration with SQLAlchemy or Tortoise ORM
- Learn about FastAPI's support for GraphQL
- Study deployment with Docker, Gunicorn, and reverse proxies (Nginx)
- Investigate advanced security patterns (scopes, role-based access)
- Look into structuring large applications with APIRouter
- Explore rate limiting and caching strategies

---

## Additional Resources

- [FastAPI Official Documentation](https://fastapi.tiangolo.com/)
- [FastAPI GitHub Repository](https://github.com/tiangolo/fastapi)
- [Pydantic Documentation](https://docs.pydantic.dev/)
- [Starlette Documentation](https://www.starlette.io/)
- [Uvicorn Documentation](https://www.uvicorn.org/)
- [Real Python FastAPI Tutorial](https://realpython.com/fastapi-python-web-apis/)
