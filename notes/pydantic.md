# Introduction to Pydantic

## Table of Contents

- [What is Pydantic](#what-is-pydantic)
- [Installation](#installation)
- [Basic Models](#basic-models)
- [Validation](#validation)
- [Field Configuration](#field-configuration)
- [Nested Models](#nested-models)
- [Optional and Union Types](#optional-and-union-types)
- [Custom Types](#custom-types)
- [Serialization](#serialization)
- [Deserialization](#deserialization)
- [Settings Management](#settings-management)
- [Strict Mode](#strict-mode)
- [Generic Models](#generic-models)
- [Integration with FastAPI](#integration-with-fastapi)
- [Practice Exercises](#practice-exercises)
- [Summary](#summary)
- [Next Steps](#next-steps)
- [Additional Resources](#additional-resources)

---

## What is Pydantic

Pydantic is a data validation and settings management library for Python, using Python type annotations to define data schemas. Version 2 (v2) is a complete rewrite with a Rust-based core that provides significantly faster validation.

Key features:
- Data validation using Python type hints
- Automatic type coercion (in lax mode)
- JSON serialization and deserialization
- Settings management with environment variable support
- Integration with FastAPI, SQLAlchemy, and other frameworks

---

## Installation

```python
# Install Pydantic v2
# pip install pydantic
# pip install pydantic[email]      # with email validation
# pip install pydantic-settings    # for BaseSettings

import pydantic
print(pydantic.__version__)  # should be 2.x.x
```

---

## Basic Models

```python
from pydantic import BaseModel, ValidationError
from datetime import datetime
from typing import Optional

# Define a model by inheriting from BaseModel
class User(BaseModel):
    id: int                          # required integer field
    name: str                        # required string field
    email: str                       # required string field
    is_active: bool = True           # optional with default value
    created_at: datetime = None      # optional, defaults to None

# Create an instance with valid data
user = User(id=1, name="Alice", email="alice@example.com", age=30)
print(user.name)          # "Alice"
print(user.is_active)     # True (default value)
print(user.model_dump())  # convert to dictionary
```

```python
from pydantic import BaseModel, ValidationError

class Product(BaseModel):
    name: str
    price: float
    quantity: int

# Pydantic performs type coercion in lax mode (default)
product = Product(name="Widget", price="19.99", quantity="5")
print(product.price)        # 19.99 (string coerced to float)
print(type(product.price))  # <class 'float'>

# Invalid data raises ValidationError
try:
    bad = Product(name="Widget", price="not-a-number", quantity=5)
except ValidationError as e:
    print(e)                # detailed error messages
    print(e.error_count())  # number of validation errors
    print(e.errors())       # list of error dictionaries
```

```python
from pydantic import BaseModel

class Item(BaseModel):
    name: str
    tags: list[str] = []
    metadata: dict[str, str] = {}

# Creating from a dictionary
data = {"name": "Widget", "tags": ["sale", "new"]}
item = Item(**data)                # unpack dictionary
item2 = Item.model_validate(data)  # equivalent using model_validate
print(item.model_dump_json())      # convert to JSON string
print(item.model_fields_set)       # set of fields explicitly provided
```

---

## Validation

```python
from pydantic import BaseModel, field_validator

class User(BaseModel):
    name: str
    age: int
    email: str

    @field_validator("name")
    @classmethod
    def name_must_not_be_empty(cls, v):
        if not v.strip():
            raise ValueError("Name must not be empty")
        return v.strip()  # return the cleaned value

    @field_validator("age")
    @classmethod
    def age_must_be_positive(cls, v):
        if v < 0 or v > 150:
            raise ValueError("Age must be between 0 and 150")
        return v

    @field_validator("email")
    @classmethod
    def email_must_contain_at(cls, v):
        if "@" not in v:
            raise ValueError("Invalid email address")
        return v.lower()  # normalize to lowercase
```

```python
from pydantic import BaseModel, model_validator

class DateRange(BaseModel):
    start_date: str
    end_date: str

    # model_validator has access to all fields at once
    @model_validator(mode="after")
    def check_dates(self):
        if self.start_date >= self.end_date:
            raise ValueError("start_date must be before end_date")
        return self

# 'before' mode runs before field validation on raw input
class FlexibleInput(BaseModel):
    values: list[int]

    @model_validator(mode="before")
    @classmethod
    def coerce_single_to_list(cls, data):
        if isinstance(data, dict) and isinstance(data.get("values"), int):
            data["values"] = [data["values"]]
        return data
```

---

## Field Configuration

```python
from pydantic import BaseModel, Field

class Product(BaseModel):
    name: str = Field(
        ...,                          # ... means required
        min_length=1, max_length=100,
        description="The name of the product",
        examples=["Widget", "Gadget"]
    )
    price: float = Field(..., gt=0, le=10000, description="Price in USD")
    quantity: int = Field(default=0, ge=0)
    sku: str = Field(..., pattern=r"^[A-Z]{3}-\d{4}$")  # regex constraint
```

```python
from pydantic import BaseModel, Field
from typing import Annotated

# Using alias for different field names in input vs code
class APIResponse(BaseModel):
    model_config = {"populate_by_name": True}  # allow both names

    status_code: int = Field(..., alias="statusCode")
    error_message: str = Field(None, alias="errorMessage")

response = APIResponse(statusCode=200)
print(response.model_dump(by_alias=True))  # uses alias names

# Reusable field types with Annotated
PositiveInt = Annotated[int, Field(gt=0)]
NonEmptyStr = Annotated[str, Field(min_length=1)]

class Score(BaseModel):
    student_id: PositiveInt
    name: NonEmptyStr

# Frozen (immutable) models
class Config(BaseModel):
    model_config = {"frozen": True}
    api_key: str
# config.api_key = "new"  # raises ValidationError

# Exclude fields from serialization
class UserInternal(BaseModel):
    name: str
    password: str = Field(..., exclude=True)
```

---

## Nested Models

```python
from pydantic import BaseModel
from typing import Optional

class Address(BaseModel):
    street: str
    city: str
    zip_code: str
    country: str = "US"

class Company(BaseModel):
    name: str
    address: Address  # nested model

class Employee(BaseModel):
    name: str
    company: Company

# Create with nested dictionaries - Pydantic validates recursively
employee = Employee(
    name="Alice",
    company={"name": "Acme", "address": {"street": "123 Main", "city": "Springfield",
                                          "zip_code": "62701"}}
)
print(employee.company.address.city)  # "Springfield"
```

```python
from pydantic import BaseModel

# Lists of nested models
class OrderItem(BaseModel):
    product_name: str
    quantity: int
    unit_price: float

class Order(BaseModel):
    order_id: int
    items: list[OrderItem]

order = Order(order_id=1001, items=[
    {"product_name": "Widget", "quantity": 2, "unit_price": 9.99},
    {"product_name": "Gadget", "quantity": 1, "unit_price": 24.99},
])
```

---

## Optional and Union Types

```python
from pydantic import BaseModel, Field
from typing import Optional, Union, Literal

class UserProfile(BaseModel):
    name: str
    bio: Optional[str] = None         # can be str or None
    score: Union[int, float] = 0      # accepts int or float

# Discriminated unions for clean type selection
class Cat(BaseModel):
    pet_type: Literal["cat"]
    meow_volume: int

class Dog(BaseModel):
    pet_type: Literal["dog"]
    bark_volume: int

class Owner(BaseModel):
    name: str
    pet: Union[Cat, Dog] = Field(discriminator="pet_type")

owner = Owner(name="Alice", pet={"pet_type": "cat", "meow_volume": 5})
print(type(owner.pet))  # <class 'Cat'>
```

---

## Custom Types

```python
from pydantic import BaseModel, BeforeValidator, AfterValidator
from typing import Annotated

# Using Annotated with validators for lightweight custom types
def validate_positive(v: int) -> int:
    if v <= 0:
        raise ValueError("Must be positive")
    return v

def validate_uppercase(v: str) -> str:
    return v.upper()

PositiveInt = Annotated[int, AfterValidator(validate_positive)]
UpperStr = Annotated[str, AfterValidator(validate_uppercase)]

# BeforeValidator runs before Pydantic's type validation
def parse_csv(v):
    if isinstance(v, str):
        return [item.strip() for item in v.split(",")]
    return v

CSVList = Annotated[list[str], BeforeValidator(parse_csv)]

class Config(BaseModel):
    retries: PositiveInt
    mode: UpperStr
    tags: CSVList

config = Config(retries=3, mode="debug", tags="a, b, c")
print(config.mode)   # "DEBUG"
print(config.tags)   # ["a", "b", "c"]
```

---

## Serialization

```python
from pydantic import BaseModel, field_serializer
from datetime import datetime

class Event(BaseModel):
    name: str
    date: datetime
    location: str = None
    attendees: list[str] = []

event = Event(name="Conf", date=datetime(2025, 6, 15), attendees=["Alice"])

# model_dump() converts to a dictionary
data = event.model_dump()
data_no_none = event.model_dump(exclude_none=True)     # exclude None values
data_minimal = event.model_dump(include={"name", "date"})  # include only these
data_unset = event.model_dump(exclude_unset=True)      # exclude unset fields

# model_dump_json() converts directly to a JSON string
json_str = event.model_dump_json(indent=2)

# Custom serialization for specific fields
class Article(BaseModel):
    title: str
    published: datetime

    @field_serializer("published")
    def serialize_date(self, value: datetime, _info) -> str:
        return value.strftime("%Y-%m-%d")
```

---

## Deserialization

```python
from pydantic import BaseModel, TypeAdapter
from datetime import datetime

class User(BaseModel):
    name: str
    email: str
    joined: datetime

# model_validate from dictionary
user = User.model_validate({"name": "Alice", "email": "a@b.com",
                             "joined": "2025-01-15T10:30:00"})

# model_validate_json from JSON string
user2 = User.model_validate_json('{"name": "Bob", "email": "b@b.com", "joined": "2025-06-01"}')

# From ORM objects with from_attributes
class UserSchema(BaseModel):
    model_config = {"from_attributes": True}
    name: str
    email: str

# TypeAdapter for validating non-model types
adapter = TypeAdapter(list[int])
result = adapter.validate_python(["1", "2", "3"])  # [1, 2, 3]
json_result = adapter.validate_json("[4, 5, 6]")   # [4, 5, 6]
```

---

## Settings Management

```python
# pip install pydantic-settings
from pydantic_settings import BaseSettings

class AppSettings(BaseSettings):
    app_name: str = "My Application"
    debug: bool = False
    database_url: str              # required - must be in env
    api_key: str                   # required
    max_connections: int = 10

    model_config = {
        "env_prefix": "APP_",      # look for APP_DATABASE_URL, etc.
        "env_file": ".env",        # load from .env file
        "case_sensitive": False,
    }

# Reads from environment variables automatically:
# APP_DATABASE_URL=postgresql://user:pass@localhost/db
# APP_API_KEY=sk-12345
settings = AppSettings()
```

---

## Strict Mode

```python
from pydantic import BaseModel, ConfigDict, Strict
from typing import Annotated

# Lax mode (default) allows coercion
class LaxModel(BaseModel):
    count: int

lax = LaxModel(count="42")  # works: string coerced to int

# Strict mode rejects type coercion
class StrictModel(BaseModel):
    model_config = ConfigDict(strict=True)
    count: int

# StrictModel(count="42") raises ValidationError

# Per-field strict mode
class MixedModel(BaseModel):
    id: Annotated[int, Strict()]   # strict: must be int
    name: str                       # lax: allows coercion
```

---

## Generic Models

```python
from pydantic import BaseModel
from typing import TypeVar, Generic, List, Optional

T = TypeVar("T")

class PaginatedResponse(BaseModel, Generic[T]):
    items: List[T]
    total: int
    page: int
    has_next: bool

class User(BaseModel):
    name: str
    email: str

# Use the generic model with a specific type
response = PaginatedResponse[User](
    items=[User(name="Alice", email="a@b.com")],
    total=50, page=1, has_next=True
)

# Generic API response wrapper
class APIResponse(BaseModel, Generic[T]):
    success: bool
    data: Optional[T] = None
    error: Optional[str] = None

success = APIResponse[User](success=True, data={"name": "Alice", "email": "a@b.com"})
```

---

## Integration with FastAPI

```python
from fastapi import FastAPI
from pydantic import BaseModel, Field, field_validator
from typing import Optional

app = FastAPI()

class ItemCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    price: float = Field(..., gt=0)
    tags: list[str] = []

    @field_validator("tags")
    @classmethod
    def validate_tags(cls, v):
        return list(set(v))  # remove duplicates

class ItemResponse(BaseModel):
    id: int
    name: str
    price: float
    model_config = {"from_attributes": True}  # support ORM objects

@app.post("/items/", response_model=ItemResponse)
def create_item(item: ItemCreate):
    return {"id": 1, **item.model_dump()}

# Separate models for create vs update (partial updates)
class ItemUpdate(BaseModel):
    name: Optional[str] = None
    price: Optional[float] = None

@app.patch("/items/{item_id}", response_model=ItemResponse)
def update_item(item_id: int, item: ItemUpdate):
    update_data = item.model_dump(exclude_unset=True)  # only set fields
    return {"id": item_id, "name": "Updated", "price": 9.99}
```

---

## Practice Exercises

1. **User Registration Model**: Create a Pydantic model with username (3-20 chars), email, password (min 8 chars with uppercase, lowercase, digit), and age (18-120).

2. **Nested API Response**: Design nested models for an e-commerce API with Order, OrderItem, Product, and Customer.

3. **Settings Manager**: Create a BaseSettings class that reads database credentials and API keys from environment variables.

4. **Generic Response Wrapper**: Create a generic Pydantic model for paginated API responses with metadata.

---

## Summary

Pydantic v2 is a high-performance data validation library that leverages Python type hints. Key takeaways:

- `BaseModel` provides automatic validation, serialization, and type coercion
- `field_validator` and `model_validator` enable custom validation logic
- `Field()` configures constraints, defaults, aliases, and documentation metadata
- Nested models validate recursively with full support for lists and optional types
- `model_dump()` and `model_dump_json()` serialize models with include/exclude options
- `model_validate()` and `model_validate_json()` deserialize data with validation
- `BaseSettings` reads configuration from environment variables and .env files
- Strict mode disables type coercion; generic models enable reusable schemas
- Pydantic integrates seamlessly with FastAPI for request/response validation

---

## Next Steps

- Explore computed fields with `@computed_field`
- Learn about Pydantic's JSON Schema generation
- Study dataclass integration with `pydantic.dataclasses`
- Investigate custom JSON encoders and decoders
- Explore integration with SQLAlchemy and other ORMs

---

## Additional Resources

- [Pydantic Official Documentation](https://docs.pydantic.dev/)
- [Pydantic GitHub Repository](https://github.com/pydantic/pydantic)
- [Pydantic Settings Documentation](https://docs.pydantic.dev/latest/concepts/pydantic_settings/)
- [Migration Guide: v1 to v2](https://docs.pydantic.dev/latest/migration/)
- [FastAPI and Pydantic Integration](https://fastapi.tiangolo.com/tutorial/body/)
