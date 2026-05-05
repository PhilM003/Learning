# 🐍 Python Backend Zero to Hero
## FastAPI + SQLAlchemy + Pydantic และ Libraries สำคัญที่ต้องรู้

---

## 📚 สารบัญ

1. [ปูพื้นฐาน: Environment & Tools](#1-ปูพื้นฐาน)
2. [Pydantic – หัวใจของการ Validate Data](#2-pydantic)
3. [FastAPI – Modern Web Framework](#3-fastapi)
4. [SQLAlchemy – ORM ที่ทรงพลัง](#4-sqlalchemy)
5. [Alembic – Database Migration](#5-alembic)
6. [Authentication & Security](#6-authentication--security)
7. [Async, HTTP Client & Background Tasks](#7-async-http-client--background-tasks)
8. [Testing ด้วย Pytest](#8-testing)
9. [Project Structure ระดับ Production](#9-project-structure)
10. [Deployment & Best Practices](#10-deployment)

---

## 1. ปูพื้นฐาน

### 🔧 ติดตั้ง Python และ Virtual Environment

```bash
# ตรวจสอบ Python (ควรเป็น 3.11+)
python --version

# สร้าง virtual environment
python -m venv venv
source venv/bin/activate   # macOS/Linux
# venv\Scripts\activate    # Windows
```

### 📦 ใช้ `uv` หรือ `poetry` สำหรับ project จริง (แนะนำ)

```bash
# uv (เร็วที่สุดในปี 2026 — เขียนด้วย Rust)
pip install uv
uv init my-project
uv add fastapi sqlalchemy pydantic

# หรือ poetry
pipx install poetry
poetry new my-project
poetry add fastapi sqlalchemy
```

### 🎯 Libraries หลักที่จะใช้ใน Lecture นี้

| Library | หน้าที่ |
|---------|---------|
| `fastapi` | Web framework |
| `pydantic` | Data validation |
| `sqlalchemy` | ORM |
| `alembic` | Database migration |
| `uvicorn` | ASGI server |
| `httpx` | Async HTTP client |
| `passlib[bcrypt]` | Password hashing |
| `python-jose[cryptography]` | JWT |
| `pytest`, `pytest-asyncio` | Testing |
| `python-dotenv` | Env variables |

```bash
uv add fastapi "uvicorn[standard]" sqlalchemy alembic pydantic pydantic-settings \
       "passlib[bcrypt]" "python-jose[cryptography]" httpx python-multipart
uv add --dev pytest pytest-asyncio pytest-cov
```

---

## 2. Pydantic

> 💡 **Pydantic v2** เป็นพื้นฐานของ FastAPI — เรียนรู้ก่อนเพื่อให้เข้าใจทุกอย่าง

### 2.1 BaseModel เบื้องต้น

```python
from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional

class User(BaseModel):
    id: int
    name: str = Field(min_length=2, max_length=50)
    email: EmailStr
    age: int = Field(ge=0, le=150)
    is_active: bool = True
    created_at: datetime = Field(default_factory=datetime.now)
    bio: Optional[str] = None

# ใช้งาน
user = User(id=1, name="Somchai", email="som@example.com", age=30)
print(user.model_dump())          # → dict
print(user.model_dump_json())     # → JSON string
```

### 2.2 Validators

```python
from pydantic import BaseModel, field_validator, model_validator

class Product(BaseModel):
    name: str
    price: float
    discount_price: float | None = None

    @field_validator("name")
    @classmethod
    def name_must_not_be_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("name ห้ามเป็นค่าว่าง")
        return v.title()

    @model_validator(mode="after")
    def check_discount(self):
        if self.discount_price and self.discount_price >= self.price:
            raise ValueError("ราคาลดต้องน้อยกว่าราคาเต็ม")
        return self
```

### 2.3 Nested Models & Config

```python
class Address(BaseModel):
    city: str
    zipcode: str

class Customer(BaseModel):
    name: str
    addresses: list[Address]

    model_config = {
        "str_strip_whitespace": True,    # ตัด whitespace อัตโนมัติ
        "from_attributes": True,         # อ่านจาก ORM object ได้
        "json_schema_extra": {
            "example": {"name": "Anan", "addresses": [{"city": "BKK", "zipcode": "10100"}]}
        }
    }
```

### 2.4 Settings Management ด้วย `pydantic-settings`

```python
# config.py
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_name: str = "My API"
    database_url: str
    secret_key: str
    debug: bool = False

    model_config = SettingsConfigDict(env_file=".env", case_sensitive=False)

settings = Settings()
```

```bash
# .env
DATABASE_URL=postgresql://user:pass@localhost/db
SECRET_KEY=super-secret-key
DEBUG=true
```

---

## 3. FastAPI

### 3.1 Hello World

```python
# main.py
from fastapi import FastAPI

app = FastAPI(title="My First API", version="1.0.0")

@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI!"}
```

```bash
uvicorn main:app --reload
# เปิด http://localhost:8000/docs   ← Swagger UI อัตโนมัติ!
# เปิด http://localhost:8000/redoc  ← ReDoc
```

### 3.2 Path & Query Parameters

```python
from fastapi import FastAPI, Query, Path

@app.get("/items/{item_id}")
def get_item(
    item_id: int = Path(gt=0, description="ID ของสินค้า"),
    q: str | None = Query(None, max_length=50),
    skip: int = 0,
    limit: int = 10,
):
    return {"item_id": item_id, "q": q, "skip": skip, "limit": limit}
```

### 3.3 Request Body ด้วย Pydantic

```python
from pydantic import BaseModel

class ItemCreate(BaseModel):
    name: str
    price: float
    tags: list[str] = []

@app.post("/items/", status_code=201)
def create_item(item: ItemCreate):
    return {"created": item}
```

### 3.4 Dependency Injection (หัวใจของ FastAPI)

```python
from fastapi import Depends, HTTPException, Header

def get_token_header(x_token: str = Header()):
    if x_token != "secret-token":
        raise HTTPException(status_code=403, detail="Token ไม่ถูกต้อง")
    return x_token

def common_pagination(skip: int = 0, limit: int = 100):
    return {"skip": skip, "limit": limit}

@app.get("/users/")
def list_users(
    pagination: dict = Depends(common_pagination),
    token: str = Depends(get_token_header),
):
    return {"pagination": pagination}
```

### 3.5 APIRouter (แยก Routes ออกเป็นโมดูล)

```python
# routers/users.py
from fastapi import APIRouter

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/")
def list_users():
    return [{"name": "Somchai"}]

@router.get("/{user_id}")
def get_user(user_id: int):
    return {"id": user_id}

# main.py
from routers import users
app.include_router(users.router)
```

### 3.6 Error Handling & Exception Handlers

```python
from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse

class ItemNotFoundError(Exception):
    def __init__(self, item_id: int):
        self.item_id = item_id

@app.exception_handler(ItemNotFoundError)
async def item_not_found_handler(request: Request, exc: ItemNotFoundError):
    return JSONResponse(
        status_code=404,
        content={"message": f"Item {exc.item_id} not found"},
    )
```

### 3.7 Middleware & CORS

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## 4. SQLAlchemy

> SQLAlchemy 2.0+ ใช้ syntax แบบใหม่ที่ type-safe — เราจะเรียน style ใหม่นี้

### 4.1 Engine, Session, Base

```python
# database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

DATABASE_URL = "postgresql://user:pass@localhost/mydb"
# หรือ SQLite: "sqlite:///./app.db"

engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False)

class Base(DeclarativeBase):
    pass
```

### 4.2 Models (Style 2.0)

```python
# models.py
from datetime import datetime
from sqlalchemy import String, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database import Base

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(120), unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String(255))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    posts: Mapped[list["Post"]] = relationship(back_populates="author", cascade="all, delete")

class Post(Base):
    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(200))
    content: Mapped[str]
    author_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    author: Mapped["User"] = relationship(back_populates="posts")
```

### 4.3 CRUD Operations

```python
from sqlalchemy import select
from sqlalchemy.orm import Session

# CREATE
def create_user(db: Session, email: str, password: str) -> User:
    user = User(email=email, hashed_password=password)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

# READ
def get_user(db: Session, user_id: int) -> User | None:
    return db.get(User, user_id)

def list_users(db: Session, skip: int = 0, limit: int = 100) -> list[User]:
    stmt = select(User).offset(skip).limit(limit)
    return db.scalars(stmt).all()

# UPDATE
def update_user_email(db: Session, user_id: int, new_email: str) -> User | None:
    user = db.get(User, user_id)
    if user:
        user.email = new_email
        db.commit()
        db.refresh(user)
    return user

# DELETE
def delete_user(db: Session, user_id: int) -> bool:
    user = db.get(User, user_id)
    if not user:
        return False
    db.delete(user)
    db.commit()
    return True
```

### 4.4 รวมร่าง: SQLAlchemy + FastAPI

```python
# deps.py
from database import SessionLocal
from sqlalchemy.orm import Session

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# routers/users.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from deps import get_db

router = APIRouter(prefix="/users")

@router.get("/{user_id}")
def read_user(user_id: int, db: Session = Depends(get_db)):
    user = db.get(User, user_id)
    if not user:
        raise HTTPException(404, "User not found")
    return user
```

### 4.5 Async SQLAlchemy (สำหรับ Performance สูง)

```python
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

engine = create_async_engine("postgresql+asyncpg://user:pass@localhost/db")
AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False)

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session

@router.get("/{user_id}")
async def read_user(user_id: int, db: AsyncSession = Depends(get_db)):
    user = await db.get(User, user_id)
    return user
```

---

## 5. Alembic

> ใช้สำหรับ **migrate database schema** เมื่อ models เปลี่ยน

### 5.1 ตั้งค่า

```bash
alembic init alembic
```

แก้ `alembic/env.py`:
```python
from database import Base
from models import *      # import models ทั้งหมด
target_metadata = Base.metadata
```

แก้ `alembic.ini`:
```ini
sqlalchemy.url = postgresql://user:pass@localhost/mydb
```

### 5.2 คำสั่งที่ใช้บ่อย

```bash
# สร้าง migration อัตโนมัติจาก model changes
alembic revision --autogenerate -m "create users table"

# Apply migration
alembic upgrade head

# ย้อนกลับ 1 step
alembic downgrade -1

# ดูประวัติ
alembic history
```

---

## 6. Authentication & Security

### 6.1 Password Hashing ด้วย `passlib`

```python
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(plain: str) -> str:
    return pwd_context.hash(plain)

def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)
```

### 6.2 JWT Token ด้วย `python-jose`

```python
from datetime import datetime, timedelta
from jose import jwt, JWTError

SECRET_KEY = "super-secret"
ALGORITHM = "HS256"

def create_access_token(data: dict, expires_in: int = 30) -> str:
    payload = data.copy()
    payload.update({"exp": datetime.utcnow() + timedelta(minutes=expires_in)})
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def decode_token(token: str) -> dict | None:
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        return None
```

### 6.3 OAuth2 + FastAPI

```python
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

@app.post("/login")
def login(form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.scalar(select(User).where(User.email == form.username))
    if not user or not verify_password(form.password, user.hashed_password):
        raise HTTPException(401, "Wrong credentials")
    token = create_access_token({"sub": str(user.id)})
    return {"access_token": token, "token_type": "bearer"}

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    payload = decode_token(token)
    if not payload:
        raise HTTPException(401, "Invalid token")
    return db.get(User, int(payload["sub"]))

@app.get("/me")
def me(user: User = Depends(get_current_user)):
    return user
```

---

## 7. Async, HTTP Client & Background Tasks

### 7.1 `httpx` – Async HTTP Client

```python
import httpx

async def fetch_weather(city: str):
    async with httpx.AsyncClient(timeout=10) as client:
        r = await client.get(f"https://api.weather.com/v1/{city}")
        r.raise_for_status()
        return r.json()

@app.get("/weather/{city}")
async def get_weather(city: str):
    return await fetch_weather(city)
```

### 7.2 BackgroundTasks

```python
from fastapi import BackgroundTasks

def send_email(to: str, subject: str):
    print(f"Sending email to {to}: {subject}")

@app.post("/notify")
def notify(email: str, bg: BackgroundTasks):
    bg.add_task(send_email, email, "Welcome!")
    return {"status": "queued"}
```

### 7.3 หากงานหนัก → ใช้ `Celery` หรือ `arq` หรือ `TaskIQ`

```python
# arq (Redis-based, async)
from arq import create_pool
from arq.connections import RedisSettings

async def heavy_job(ctx, x, y):
    return x + y

class WorkerSettings:
    functions = [heavy_job]
    redis_settings = RedisSettings()
```

---

## 8. Testing

### 8.1 Pytest พื้นฐาน

```python
# tests/test_users.py
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_read_root():
    r = client.get("/")
    assert r.status_code == 200
    assert r.json() == {"message": "Hello, FastAPI!"}

def test_create_user():
    r = client.post("/users/", json={"email": "a@b.com", "password": "1234"})
    assert r.status_code == 201
    assert r.json()["email"] == "a@b.com"
```

### 8.2 Fixtures + Test Database

```python
# conftest.py
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Base
from deps import get_db
from main import app
from fastapi.testclient import TestClient

@pytest.fixture
def db_session():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()

@pytest.fixture
def client(db_session):
    def override_get_db():
        yield db_session
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    app.dependency_overrides.clear()
```

### 8.3 Async Tests

```python
import pytest
import httpx

@pytest.mark.asyncio
async def test_async_endpoint():
    async with httpx.AsyncClient(app=app, base_url="http://test") as ac:
        r = await ac.get("/")
        assert r.status_code == 200
```

---

## 9. Project Structure

```
my-project/
├── alembic/                  # migrations
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI instance
│   ├── config.py            # pydantic-settings
│   ├── database.py          # engine, SessionLocal
│   ├── deps.py              # shared dependencies
│   │
│   ├── models/              # SQLAlchemy models
│   │   ├── user.py
│   │   └── post.py
│   │
│   ├── schemas/             # Pydantic schemas (DTOs)
│   │   ├── user.py
│   │   └── post.py
│   │
│   ├── crud/                # database operations
│   │   ├── user.py
│   │   └── post.py
│   │
│   ├── routers/             # API endpoints
│   │   ├── auth.py
│   │   ├── users.py
│   │   └── posts.py
│   │
│   ├── services/            # business logic
│   │   └── email.py
│   │
│   └── core/                # security, utils
│       ├── security.py
│       └── exceptions.py
│
├── tests/
│   ├── conftest.py
│   ├── test_users.py
│   └── test_posts.py
│
├── .env
├── .gitignore
├── pyproject.toml
└── README.md
```

### 💡 Pattern: แยก **Model** กับ **Schema** ออกจากกัน

```python
# models/user.py  ← SQLAlchemy (ตัวที่คุยกับ DB)
class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str]

# schemas/user.py ← Pydantic (ตัวที่คุยกับ client)
class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserRead(BaseModel):
    id: int
    email: EmailStr
    model_config = {"from_attributes": True}
```

---

## 10. Deployment

### 10.1 Production Server

```bash
# uvicorn สำหรับ dev
uvicorn app.main:app --host 0.0.0.0 --port 8000

# gunicorn + uvicorn workers สำหรับ production
pip install gunicorn
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker
```

### 10.2 Dockerfile

```dockerfile
FROM python:3.12-slim

WORKDIR /app

COPY pyproject.toml uv.lock ./
RUN pip install uv && uv sync --frozen --no-dev

COPY . .

CMD ["uv", "run", "gunicorn", "app.main:app", \
     "-w", "4", "-k", "uvicorn.workers.UvicornWorker", \
     "--bind", "0.0.0.0:8000"]
```

### 10.3 docker-compose.yml

```yaml
services:
  api:
    build: .
    ports: ["8000:8000"]
    env_file: .env
    depends_on: [db]

  db:
    image: postgres:16
    environment:
      POSTGRES_USER: user
      POSTGRES_PASSWORD: pass
      POSTGRES_DB: mydb
    volumes:
      - pgdata:/var/lib/postgresql/data

volumes:
  pgdata:
```

---

## 🌟 Libraries อื่นๆ ที่ Hero ต้องรู้จัก

| Library | ใช้ทำอะไร |
|---------|-----------|
| `loguru` | Logging แบบเขียนง่ายกว่า `logging` |
| `tenacity` | Retry logic แบบสวย |
| `redis` / `aioredis` | Cache, session, pub/sub |
| `celery` / `arq` / `taskiq` | Background job queue |
| `sqlmodel` | SQLAlchemy + Pydantic รวมกัน (โดยผู้สร้าง FastAPI) |
| `strawberry` / `ariadne` | GraphQL |
| `polars` / `pandas` | Data processing |
| `rich` | Pretty terminal output |
| `typer` | สร้าง CLI สวยๆ (น้องของ FastAPI) |
| `ruff` | Linter + formatter (เร็วมาก) |
| `mypy` / `pyright` | Static type checker |
| `pre-commit` | Git hooks อัตโนมัติ |
| `sentry-sdk` | Error tracking |
| `prometheus-fastapi-instrumentator` | Metrics สำหรับ Grafana |

---

## 🎯 เส้นทางสู่ Hero (Roadmap)

1. ✅ **Week 1–2** — Pydantic ให้แม่น, เข้าใจ type hints
2. ✅ **Week 3–4** — FastAPI: routes, dependencies, schemas
3. ✅ **Week 5–6** — SQLAlchemy 2.0 + Alembic + relationships
4. ✅ **Week 7** — Auth (JWT, OAuth2), security best practices
5. ✅ **Week 8** — Testing (pytest), CI/CD
6. ✅ **Week 9** — Async (httpx, async SQLAlchemy), background tasks
7. ✅ **Week 10** — Docker, deployment, monitoring
8. ✅ **Beyond** — สร้างโปรเจคจริง! (e-commerce, blog, SaaS)

---

## 📖 แหล่งเรียนรู้เพิ่มเติม

- 📘 FastAPI Official: https://fastapi.tiangolo.com
- 📗 SQLAlchemy 2.0: https://docs.sqlalchemy.org
- 📙 Pydantic v2: https://docs.pydantic.dev
- 🎥 ARJanCode (YouTube) — Python clean architecture
- 📚 *Architecture Patterns with Python* (Cosmic Python)

---

> 💪 **คาถาประจำใจ:** *Type hints คือเพื่อนสนิท, Pydantic คือผู้คุ้มกัน, FastAPI คือพาหนะ, SQLAlchemy คือคลังแสง*

ขอให้สนุกกับการเขียน Python นะครับ! 🐍🚀
