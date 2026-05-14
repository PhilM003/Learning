# 📚 Library Class Reference — เปิดดูทีละ Class

> 💬 **คู่มือนี้คือ:** "พจนานุกรม" ของทุก class สำคัญในทุก library — เปิดดูตอน implement
> ทุก class มี **คำอธิบายภาษาชาวบ้าน + ตัวอย่างใช้งานจริง**

## 📑 สารบัญ

1. [Pydantic v2](#1-pydantic-v2)
2. [FastAPI](#2-fastapi)
3. [Starlette (พื้นฐานของ FastAPI)](#3-starlette)
4. [SQLAlchemy 2.0](#4-sqlalchemy-20)
5. [Alembic](#5-alembic)
6. [httpx](#6-httpx)
7. [Authentication (passlib, jose, argon2)](#7-authentication)
8. [Redis](#8-redis)
9. [Loguru](#9-loguru)
10. [Jinja2](#10-jinja2)
11. [WeasyPrint](#11-weasyprint)
12. [Pillow](#12-pillow)
13. [Openpyxl](#13-openpyxl)
14. [Tenacity](#14-tenacity)
15. [APScheduler](#15-apscheduler)
16. [Typer + Rich](#16-typer--rich)

---

## 1. Pydantic v2

> 💬 **Pydantic คืออะไร:** ผู้คุมประตูข้อมูล — ตรวจ + แปลง + serialize Python object ⇄ JSON อย่างปลอดภัย

### 1.1 `BaseModel` — class แม่ของทุก data model

```python
from pydantic import BaseModel

class User(BaseModel):
    id: int
    name: str
    age: int = 18    # default

# สร้าง
u = User(id=1, name="A", age=30)
u = User.model_validate({"id": 1, "name": "A", "age": 30})
u = User.model_validate_json('{"id": 1, "name": "A", "age": 30}')

# Export
u.model_dump()                       # → dict
u.model_dump(exclude={"age"})        # → dict ไม่มี age
u.model_dump(include={"id"})         # → เฉพาะ id
u.model_dump_json(indent=2)          # → pretty JSON
u.model_dump_json(exclude_none=True) # ตัด field ที่เป็น None

# Copy
u2 = u.model_copy()
u3 = u.model_copy(update={"name": "B"})

# Class methods
User.model_fields              # dict ของ field metadata
User.model_json_schema()       # OpenAPI schema
User.model_validate_strings({"id": "1"})    # cast "1" → 1
```

### 1.2 `Field` — กำหนดเงื่อนไข field

> 💬 **คือ:** "ป้ายข้อกำหนด" ติดที่ field — บอกค่า default, validation, metadata

```python
from pydantic import BaseModel, Field

class Product(BaseModel):
    id: int = Field(..., description="Product ID")    # ... = required
    name: str = Field(min_length=3, max_length=50)
    price: float = Field(gt=0, le=1_000_000)          # > 0, <= 1M
    stock: int = Field(ge=0, default=0)               # >= 0
    sku: str = Field(pattern=r"^[A-Z]{3}-\d{4}$")
    tags: list[str] = Field(default_factory=list)     # ห้าม `default=[]` (shared!)
    created_at: datetime = Field(default_factory=datetime.now)
    secret: str = Field(repr=False)                    # ไม่แสดงใน repr/log
    legacy_name: str = Field(alias="legacyName")       # JSON: "legacyName" ↔ Python: "legacy_name"
```

| arg                                                  | ภาษาชาวบ้าน                     |
| ---------------------------------------------------- | ------------------------------- |
| `...` หรือ `Required`                                | "ต้องใส่"                       |
| `default` / `default_factory`                        | "ค่าตั้งต้น / ตั้งจาก function" |
| `gt`, `ge`, `lt`, `le`                               | "มากกว่า, >=, น้อยกว่า, <="     |
| `min_length`, `max_length`                           | "ยาวอย่างน้อย/ไม่เกิน"          |
| `pattern`                                            | "regex"                         |
| `alias` / `validation_alias` / `serialization_alias` | "ชื่อต่างกันใน JSON"            |
| `description`, `examples`, `title`                   | "metadata สำหรับ OpenAPI"       |
| `exclude`                                            | "ไม่ใส่ใน dump"                 |
| `frozen`                                             | "อ่านอย่างเดียว"                |
| `repr=False`                                         | "ซ่อนเวลา print"                |

### 1.3 `field_validator` / `model_validator`

```python
from pydantic import BaseModel, field_validator, model_validator

class Order(BaseModel):
    name: str
    quantity: int
    price: float

    @field_validator("name")
    @classmethod
    def name_upper(cls, v: str) -> str:
        return v.strip().upper()

    @field_validator("quantity", mode="before")    # before = ก่อน cast type
    @classmethod
    def parse_qty(cls, v):
        if isinstance(v, str):
            return int(v.replace(",", ""))
        return v

    @model_validator(mode="after")
    def total_sanity(self):
        if self.quantity * self.price > 1_000_000:
            raise ValueError("เกินวงเงิน")
        return self
```

Modes:

- `"before"` — รับ raw input
- `"after"` — รับ value หลัง type cast (default)
- `"wrap"` — ครอบ validation ดั้งเดิม (custom logic)
- `"plain"` — แทน built-in validation ทั้งหมด

### 1.4 `computed_field` — field คำนวณ

```python
from pydantic import BaseModel, computed_field

class Box(BaseModel):
    width: float
    height: float
    depth: float

    @computed_field
    @property
    def volume(self) -> float:
        return self.width * self.height * self.depth

Box(width=2, height=3, depth=4).model_dump()
# → {"width": 2, "height": 3, "depth": 4, "volume": 24}
```

### 1.5 Built-in Types

```python
from pydantic import (
    EmailStr,           # email validator (ต้อง pip install pydantic[email])
    HttpUrl,            # URL
    AnyUrl,             # generic URL
    PostgresDsn,        # postgres://...
    RedisDsn,
    IPvAnyAddress,
    UUID4,
    SecretStr,          # ซ่อนค่าใน repr
    SecretBytes,
    Json,               # parse JSON string
    PositiveInt, NegativeInt, NonNegativeInt, NonPositiveInt,
    PositiveFloat, NegativeFloat,
    PaymentCardNumber,
    constr, conint, confloat, condecimal, conlist, conset,
)

class Settings(BaseModel):
    db: PostgresDsn
    redis: RedisDsn
    admin_email: EmailStr
    api_key: SecretStr
    callback: HttpUrl
    user_id: UUID4
    pin: constr(pattern=r"^\d{4}$")
    score: confloat(ge=0, le=100)

s = Settings(api_key="hush", ...)
print(s.api_key)              # → SecretStr('**********')
s.api_key.get_secret_value()  # → 'hush'
```

### 1.6 `model_config` (per-class config)

```python
class Item(BaseModel):
    model_config = {
        "str_strip_whitespace": True,         # auto .strip()
        "str_to_lower": False,
        "from_attributes": True,              # อ่าน ORM object (SQLAlchemy)
        "populate_by_name": True,             # ใช้ alias หรือ field name ก็ได้
        "extra": "ignore",                    # "allow" / "ignore" / "forbid"
        "validate_assignment": True,          # validate ตอน assign field
        "frozen": True,                       # อ่านอย่างเดียว (immutable)
        "use_enum_values": True,              # serialize Enum เป็น value
        "arbitrary_types_allowed": False,
        "json_schema_extra": {"example": {...}},
        "alias_generator": lambda x: x.replace("_", "-"),
    }
```

### 1.7 `RootModel` (root = list หรือ primitive ไม่ใช่ object)

```python
from pydantic import RootModel

class Tags(RootModel[list[str]]):
    pass

t = Tags(["python", "fastapi"])
t.root                  # ['python', 'fastapi']
t.model_dump()          # ['python', 'fastapi']
```

### 1.8 `Discriminator` (polymorphism)

```python
from typing import Literal, Union
from pydantic import BaseModel, Field

class Cat(BaseModel):
    pet_type: Literal["cat"]
    meow_volume: int

class Dog(BaseModel):
    pet_type: Literal["dog"]
    bark_volume: int

class Owner(BaseModel):
    pet: Union[Cat, Dog] = Field(discriminator="pet_type")

Owner(pet={"pet_type": "cat", "meow_volume": 5})
# Pydantic เลือก Cat ให้อัตโนมัติจาก pet_type
```

### 1.9 `TypeAdapter` (validate type ที่ไม่ใช่ BaseModel)

```python
from pydantic import TypeAdapter

adapter = TypeAdapter(list[int])
adapter.validate_python(["1", "2", "3"])      # → [1, 2, 3]
adapter.validate_json("[1, 2, 3]")            # → [1, 2, 3]
adapter.dump_json([1, 2, 3])                  # → '[1,2,3]'
adapter.json_schema()                          # → JSON schema
```

### 1.10 `pydantic_settings.BaseSettings`

```python
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

class Settings(BaseSettings):
    app_name: str = "MyApp"
    database_url: PostgresDsn
    secret_key: str = Field(min_length=32)
    debug: bool = False

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_prefix="MYAPP_",           # อ่าน MYAPP_DATABASE_URL
        env_nested_delimiter="__",     # SMTP__HOST → smtp.host
        case_sensitive=False,
        extra="ignore",
    )

settings = Settings()    # อ่านจาก .env + env vars
```

### 1.11 Errors / Exceptions

```python
from pydantic import ValidationError

try:
    User(id="abc", name="", age=-1)
except ValidationError as e:
    e.errors()         # list of dict — แต่ละ error
    e.error_count()    # int
    e.json()           # JSON string
    str(e)             # pretty multi-line
```

---

## 2. FastAPI

### 2.1 `FastAPI` — app instance

```python
from fastapi import FastAPI

app = FastAPI(
    title="My API",
    version="1.0.0",
    description="...",
    docs_url="/docs",                # หรือ None ปิด
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    swagger_ui_oauth2_redirect_url="/docs/oauth2-redirect",
    debug=False,
    root_path="/api",                # ถ้าหลัง reverse proxy strip prefix
    contact={"name": "Dev", "email": "dev@cmt.co.th"},
    license_info={"name": "MIT"},
    servers=[{"url": "https://api.example.com"}],
    lifespan=lifespan,
    dependencies=[Depends(common_dep)],     # apply ทุก endpoint
    exception_handlers={Exception: handler},
)

# Methods
app.get("/path")(handler)
app.post(...)
app.put(...)
app.delete(...)
app.patch(...)
app.options(...)
app.head(...)
app.api_route("/path", methods=["GET", "POST"])(handler)

app.include_router(router, prefix="/v1", tags=["v1"], dependencies=[...])
app.add_middleware(MiddlewareClass, **kwargs)
app.exception_handler(ExceptionClass)(handler)
app.add_exception_handler(ExceptionClass, handler)
app.middleware("http")(my_middleware)
app.on_event("startup")(handler)     # deprecated → use lifespan
app.openapi()                        # generate spec
```

### 2.2 `APIRouter`

```python
from fastapi import APIRouter

router = APIRouter(
    prefix="/users",
    tags=["users"],
    dependencies=[Depends(verify_token)],
    responses={404: {"description": "Not found"}},
    deprecated=False,
    include_in_schema=True,
    default_response_class=JSONResponse,
)

@router.get("/", response_model=list[UserRead])
def list_users(): ...

# Nested router
parent = APIRouter()
child = APIRouter()
parent.include_router(child, prefix="/items")
```

### 2.3 `Depends`

> 💬 **คือ:** "บอก FastAPI ว่าต้องเตรียมอะไรให้ก่อนเรียก endpoint" — DI container

```python
from fastapi import Depends

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/items")
def list_items(db: Session = Depends(get_db)):
    ...

# Use_cache (default True — cache ภายใน 1 request)
def get_settings():
    return Settings()

@app.get("/")
def root(s1: Settings = Depends(get_settings), s2: Settings = Depends(get_settings)):
    assert s1 is s2     # cached!

# Use_cache=False — เรียกใหม่ทุกครั้ง
Depends(get_settings, use_cache=False)
```

### 2.4 Path Parameter Classes

```python
from fastapi import Path, Query, Header, Cookie, Body, Form, File, UploadFile, Depends

@app.get("/items/{item_id}")
def get(
    item_id: int = Path(..., gt=0, le=1000, description="Item ID"),
    q: str | None = Query(None, max_length=50, regex=r"^[a-z]+$"),
    user_agent: str = Header(...),
    session: str = Cookie(default=None),
):
    ...

@app.post("/items")
def create(
    item: ItemCreate = Body(..., embed=True),
    api_key: str = Header(...),
    file: UploadFile = File(...),
    description: str = Form(...),
):
    ...
```

| Class                   | ใช้กับ              |
| ----------------------- | ------------------- |
| `Path()`                | path param          |
| `Query()`               | query string `?`    |
| `Header()`              | HTTP header         |
| `Cookie()`              | cookie              |
| `Body()`                | request body (JSON) |
| `Form()`                | form data           |
| `File()` / `UploadFile` | file upload         |

### 2.5 `HTTPException`

```python
from fastapi import HTTPException, status

raise HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Item not found",
    headers={"X-Error": "Not found"},
)

# Common status codes
status.HTTP_200_OK
status.HTTP_201_CREATED
status.HTTP_204_NO_CONTENT
status.HTTP_400_BAD_REQUEST
status.HTTP_401_UNAUTHORIZED
status.HTTP_403_FORBIDDEN
status.HTTP_404_NOT_FOUND
status.HTTP_409_CONFLICT
status.HTTP_422_UNPROCESSABLE_ENTITY
status.HTTP_429_TOO_MANY_REQUESTS
status.HTTP_500_INTERNAL_SERVER_ERROR
status.HTTP_503_SERVICE_UNAVAILABLE
```

### 2.6 `UploadFile`

```python
from fastapi import UploadFile, File

@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    file.filename                # str
    file.content_type            # "image/png"
    file.size                    # bytes (อาจเป็น None ถ้า chunked)
    file.file                    # SpooledTemporaryFile

    content = await file.read()           # bytes ทั้งหมด
    chunk = await file.read(1024)         # read N bytes
    await file.seek(0)                     # rewind
    await file.close()
```

### 2.7 `BackgroundTasks`

```python
from fastapi import BackgroundTasks

def write_log(msg: str):
    with open("log.txt", "a") as f:
        f.write(msg)

@app.post("/notify")
def notify(email: str, bg: BackgroundTasks):
    bg.add_task(write_log, f"notified {email}")
    bg.add_task(send_email, email, "subject", "body")
    return {"ok": True}    # ← bg tasks run หลัง response
```

### 2.8 Response Classes

```python
from fastapi.responses import (
    JSONResponse,
    HTMLResponse,
    PlainTextResponse,
    RedirectResponse,
    StreamingResponse,
    FileResponse,
    Response,            # generic
    ORJSONResponse,      # 5-10x faster than JSON (need orjson)
    UJSONResponse,
)

@app.get("/html", response_class=HTMLResponse)
def html():
    return "<h1>Hello</h1>"

@app.get("/json")
def json():
    return JSONResponse(content={"a": 1}, status_code=200, headers={"X-Custom": "1"})

@app.get("/redirect")
def redirect():
    return RedirectResponse("/new", status_code=302)

@app.get("/file")
def file():
    return FileResponse("path/to/file.pdf", media_type="application/pdf",
                        filename="report.pdf")

@app.get("/stream")
def stream():
    def gen():
        for i in range(100):
            yield f"data: {i}\n\n"
    return StreamingResponse(gen(), media_type="text/event-stream")
```

### 2.9 `WebSocket`

```python
from fastapi import WebSocket, WebSocketDisconnect

@app.websocket("/ws")
async def ws_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            # หรือ: receive_bytes(), receive_json()
            await websocket.send_text(f"echo: {data}")
            # หรือ: send_bytes(), send_json()
    except WebSocketDisconnect:
        print("client gone")
```

### 2.10 Security Classes

```python
from fastapi.security import (
    OAuth2PasswordBearer,
    OAuth2PasswordRequestForm,
    OAuth2AuthorizationCodeBearer,
    HTTPBearer,
    HTTPBasic,
    APIKeyHeader,
    APIKeyQuery,
    APIKeyCookie,
)

oauth2 = OAuth2PasswordBearer(tokenUrl="login")
api_key_header = APIKeyHeader(name="X-API-Key")
basic = HTTPBasic()

@app.get("/secure")
def secure(token: str = Depends(oauth2)):
    ...

@app.get("/with-key")
def with_key(key: str = Depends(api_key_header)):
    ...

@app.get("/basic")
def basic_endpoint(creds: HTTPBasicCredentials = Depends(basic)):
    creds.username, creds.password
```

### 2.11 Middleware Classes

```python
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware

app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True,
                   allow_methods=["*"], allow_headers=["*"])
app.add_middleware(GZipMiddleware, minimum_size=1000)
app.add_middleware(TrustedHostMiddleware, allowed_hosts=["example.com", "*.example.com"])
app.add_middleware(HTTPSRedirectMiddleware)
```

### 2.12 `TestClient`

```python
from fastapi.testclient import TestClient

client = TestClient(app, base_url="http://test", headers={"X-Default": "1"})

# All HTTP methods
response = client.get("/path", params={...}, headers={...}, cookies={...})
response = client.post("/path", json={...}, data={...}, files={...})
response = client.put(...)
response = client.patch(...)
response = client.delete(...)

# WebSocket
with client.websocket_connect("/ws") as ws:
    ws.send_text("hi")
    ws.receive_text()

# Lifespan
with TestClient(app) as client:    # ← startup/shutdown run
    ...
```

---

## 3. Starlette

> 💬 **คือ:** ASGI framework ที่ FastAPI build บนนั้น — เข้าใจ Starlette = เข้าใจ FastAPI ลึกขึ้น

### 3.1 `Request`

```python
from starlette.requests import Request

@app.get("/")
async def root(request: Request):
    request.method                  # "GET"
    request.url                     # URL object
    request.url.path                # "/"
    request.url.query               # "?a=1&b=2" (str)
    request.headers                 # dict-like
    request.headers["user-agent"]
    request.client                  # ClientInfo(host="1.2.3.4", port=5678)
    request.client.host
    request.cookies                 # dict
    request.query_params            # MultiDict
    request.path_params             # dict
    request.state                   # custom data per request

    body = await request.body()
    json = await request.json()
    form = await request.form()
    async for chunk in request.stream():
        ...
```

### 3.2 `BackgroundTasks` (Starlette base)

```python
from starlette.background import BackgroundTask, BackgroundTasks

tasks = BackgroundTasks()
tasks.add_task(send_email, "a@b.c")
```

### 3.3 `Mount` (sub-app)

```python
from starlette.applications import Starlette
from starlette.staticfiles import StaticFiles

app.mount("/static", StaticFiles(directory="static"), name="static")
# → GET /static/css/main.css → serve static file
```

---

## 4. SQLAlchemy 2.0

### 4.1 `Engine` / `create_engine`

```python
from sqlalchemy import create_engine

engine = create_engine(
    "postgresql+psycopg://user:pass@host/db",
    echo=False,                              # log SQL
    echo_pool=False,
    pool_size=5,                             # default = 5
    max_overflow=10,                         # extra ที่เปิดได้ชั่วคราว
    pool_timeout=30,                         # รอ conn สูงสุด (sec)
    pool_recycle=3600,                       # recycle conn ทุก N วินาที
    pool_pre_ping=True,                      # ping ก่อนใช้
    connect_args={"connect_timeout": 5},
    isolation_level="READ COMMITTED",
    future=True,                              # default in 2.0
)

# Inspect
engine.url
engine.dialect.name           # 'postgresql'
engine.pool.status()
engine.connect()
engine.dispose()              # close pool
```

### 4.2 `AsyncEngine` / `create_async_engine`

```python
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine

async_engine = create_async_engine(
    "postgresql+asyncpg://user:pass@host/db",
    # หรือ "postgresql+psycopg://..." (psycopg3 also async)
    pool_size=5, max_overflow=10,
)

async with async_engine.connect() as conn:
    result = await conn.execute(text("SELECT 1"))
```

### 4.3 `Session` / `sessionmaker`

```python
from sqlalchemy.orm import Session, sessionmaker

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=True,
    autocommit=False,
    expire_on_commit=True,
)

with SessionLocal() as session:
    session.add(user)
    session.commit()
    session.refresh(user)

# Methods
session.add(obj)
session.add_all([obj1, obj2])
session.delete(obj)
session.merge(obj)                # upsert-style
session.flush()                    # send to DB without commit
session.commit()
session.rollback()
session.close()
session.refresh(obj)               # reload from DB
session.expire(obj)                # mark stale → reload on access
session.expunge(obj)               # remove from session
session.expunge_all()

# Query
session.get(User, 1)               # by PK (fast)
session.scalar(stmt)                # one scalar
session.scalars(stmt).all()         # list of scalars
session.execute(stmt)               # raw Result
session.execute(stmt).all()         # list of rows
session.execute(stmt).one()         # exactly 1
session.execute(stmt).one_or_none()
session.execute(stmt).first()
session.execute(stmt).mappings().all()    # rows as dict
```

### 4.4 `AsyncSession`

```python
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

AsyncSessionLocal = async_sessionmaker(
    bind=async_engine,
    expire_on_commit=False,    # ⚠️ async — ต้องเป็น False
)

async with AsyncSessionLocal() as session:
    session.add(user)
    await session.commit()
    await session.refresh(user)

    result = await session.scalars(select(User))
    users = result.all()
```

### 4.5 `DeclarativeBase` & `Mapped`

```python
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"
    __table_args__ = (
        Index("ix_users_email_active", "email", "is_active"),
        UniqueConstraint("email", name="uq_users_email"),
        {"schema": "auth"},
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(120), unique=True, index=True)
    name: Mapped[str | None] = mapped_column(String(100))
    age: Mapped[int] = mapped_column(default=0)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())

    posts: Mapped[list["Post"]] = relationship(back_populates="author")

    # method ปกติได้
    def is_adult(self) -> bool:
        return self.age >= 18
```

### 4.6 Column Types

```python
from sqlalchemy import (
    Integer, BigInteger, SmallInteger,
    String, Text, Unicode, UnicodeText,
    Boolean,
    Float, Numeric, Decimal,
    Date, DateTime, Time, Interval,
    JSON,            # cross-DB
    LargeBinary, BLOB,
    Enum,
    Uuid,
    ForeignKey,
    CheckConstraint, UniqueConstraint, Index,
)
from sqlalchemy.dialects.postgresql import (
    JSONB,           # PG-specific (faster + indexable)
    ARRAY,
    UUID,
    INET, CIDR,
    HSTORE,
    TSVECTOR,
)

class Item(Base):
    __tablename__ = "items"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    price: Mapped[Decimal] = mapped_column(Numeric(10, 2))
    metadata: Mapped[dict] = mapped_column(JSONB, default=dict)
    tags: Mapped[list[str]] = mapped_column(ARRAY(String), default=list)
    status: Mapped[str] = mapped_column(
        Enum("draft", "active", "archived", name="item_status"),
        default="draft",
    )
```

### 4.7 `relationship`

```python
class User(Base):
    posts: Mapped[list["Post"]] = relationship(
        back_populates="author",
        cascade="all, delete-orphan",
        lazy="selectin",                # selectin/joined/subquery/select(default)/raise
        order_by="Post.created_at.desc()",
        primaryjoin="User.id == Post.author_id",
        foreign_keys="[Post.author_id]",
        passive_deletes=True,
    )

# Many-to-many (with association table)
post_tags = Table(
    "post_tags", Base.metadata,
    Column("post_id", ForeignKey("posts.id"), primary_key=True),
    Column("tag_id", ForeignKey("tags.id"), primary_key=True),
)

class Post(Base):
    tags: Mapped[list["Tag"]] = relationship(secondary=post_tags, back_populates="posts")
```

### 4.8 `select`, `insert`, `update`, `delete`

```python
from sqlalchemy import select, insert, update, delete

# SELECT
stmt = (
    select(User)
    .where(User.age >= 18, User.is_active == True)
    .order_by(User.name.asc(), User.created_at.desc())
    .offset(10).limit(20)
    .options(selectinload(User.posts))
)

# JOIN
stmt = (
    select(User, Post)
    .join(Post, Post.author_id == User.id)
    .where(Post.title.contains("Python"))
)
# หรือ join via relationship
stmt = select(User).join(User.posts).where(Post.title.contains("X"))

# GROUP BY + aggregates
from sqlalchemy import func
stmt = (
    select(User.id, func.count(Post.id).label("n"))
    .outerjoin(Post)
    .group_by(User.id)
    .having(func.count(Post.id) > 5)
)

# CTE
recent = select(Post).where(Post.created_at > "2026-01-01").cte("recent")
stmt = select(recent.c.title)

# INSERT
stmt = insert(User).values(email="a@b.c", name="A").returning(User.id)
result = session.execute(stmt)

# Bulk insert
session.execute(insert(User), [{"email": "a", "name": "A"}, {"email": "b", "name": "B"}])

# UPDATE
stmt = update(User).where(User.id == 1).values(name="New")
session.execute(stmt)

# DELETE
stmt = delete(User).where(User.age < 18)
session.execute(stmt)
```

### 4.9 Operators

```python
User.name == "Alice"          # =
User.name != "Alice"          # !=
User.age > 18                  # >
User.age >= 18                 # >=
User.age.between(18, 65)
User.name.like("A%")           # LIKE
User.name.ilike("a%")          # ILIKE (case-insensitive)
User.name.contains("li")       # LIKE %li%
User.name.startswith("A")
User.name.endswith("e")
User.id.in_([1, 2, 3])         # IN
User.name.is_(None)            # IS NULL
User.name.is_not(None)         # IS NOT NULL
~User.is_active                 # NOT
User.is_active & User.is_admin  # AND
User.is_active | User.is_admin  # OR

# String functions
func.lower(User.name)
func.upper(User.name)
func.length(User.name)
func.concat(User.first, " ", User.last)

# Date functions
func.date_trunc("month", Order.created_at)
func.extract("year", Order.created_at)
```

### 4.10 Loading Strategies

```python
from sqlalchemy.orm import selectinload, joinedload, subqueryload, lazyload, raiseload

# SELECT IN (best for one-to-many)
select(User).options(selectinload(User.posts))

# JOIN (best for one-to-one / many-to-one)
select(User).options(joinedload(User.profile))

# Lazy (default — N+1 risk)
select(User).options(lazyload(User.posts))

# Raise on access (debug N+1)
select(User).options(raiseload(User.posts))

# Nested
select(User).options(selectinload(User.posts).selectinload(Post.comments))
```

### 4.11 `text()` (raw SQL)

```python
from sqlalchemy import text

stmt = text("SELECT id, name FROM users WHERE age > :age")
rows = session.execute(stmt, {"age": 18}).all()

# Bind to a model
stmt = text("SELECT * FROM users").bindparams()
session.scalars(stmt.columns(User.__table__.columns).cte()).all()
```

### 4.12 Events

```python
from sqlalchemy import event

@event.listens_for(User, "before_insert")
def set_defaults(mapper, connection, target):
    target.created_at = datetime.now(timezone.utc)

@event.listens_for(engine, "before_cursor_execute")
def log_sql(conn, cursor, statement, params, context, executemany):
    print(f"SQL: {statement}")
```

---

## 5. Alembic

```bash
alembic init alembic                          # init folder
alembic revision -m "msg"                     # blank revision
alembic revision --autogenerate -m "msg"      # from model diff
alembic upgrade head                          # apply all
alembic upgrade +1                            # apply 1
alembic upgrade <revision_id>
alembic downgrade -1
alembic downgrade base                        # all the way back
alembic current
alembic history
alembic show <rev>
alembic branches
alembic heads
alembic merge -m "msg" head1 head2
alembic stamp head                            # mark as applied without running
alembic check                                  # autogen would generate nothing
```

### Migration file template

```python
"""description

Revision ID: abc123
Revises: prev_rev_id
Create Date: 2026-05-14
"""
from alembic import op
import sqlalchemy as sa

revision = "abc123"
down_revision = "prev_rev_id"

def upgrade():
    # Tables
    op.create_table("users",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("email", sa.String(120), unique=True, nullable=False),
    )
    op.drop_table("old_table")
    op.rename_table("old_name", "new_name")

    # Columns
    op.add_column("users", sa.Column("age", sa.Integer))
    op.drop_column("users", "deprecated")
    op.alter_column("users", "name",
                    type_=sa.String(200), nullable=False,
                    existing_type=sa.String(100))

    # Indexes / constraints
    op.create_index("ix_users_email", "users", ["email"], unique=True)
    op.drop_index("ix_users_old")
    op.create_unique_constraint("uq_users_email", "users", ["email"])
    op.create_foreign_key("fk_posts_user", "posts", "users", ["user_id"], ["id"])
    op.drop_constraint("fk_posts_user", "posts", type_="foreignkey")
    op.create_check_constraint("ck_age_positive", "users", "age >= 0")

    # Data migration
    op.execute("UPDATE users SET name = email WHERE name IS NULL")

    # Bulk insert seed
    op.bulk_insert(
        sa.table("companies", sa.column("code", sa.String), sa.column("name", sa.String)),
        [{"code": "CMT", "name": "Carpet Maker"}, ...],
    )

def downgrade():
    # reverse ของ upgrade
    ...
```

---

## 6. httpx

### 6.1 `Client` (sync)

```python
import httpx

with httpx.Client(
    base_url="https://api.example.com",
    headers={"Authorization": "Bearer xxx"},
    timeout=httpx.Timeout(connect=5, read=10, write=5, pool=2),
    limits=httpx.Limits(max_connections=100, max_keepalive_connections=20),
    follow_redirects=True,
    verify=True,                              # SSL cert check
    proxy="http://proxy.example.com:8080",
    cookies={"session": "..."},
) as client:
    r = client.get("/users", params={"limit": 10})
    r = client.post("/users", json={"name": "A"})
    r = client.put("/users/1", data={"key": "value"})
    r = client.delete("/users/1")
    r = client.patch("/users/1", json={"name": "B"})
    r = client.head("/users")
    r = client.options("/")

    # Upload file
    with open("file.pdf", "rb") as f:
        r = client.post("/upload", files={"file": ("file.pdf", f, "application/pdf")})
```

### 6.2 `AsyncClient`

```python
async with httpx.AsyncClient() as client:
    r = await client.get("https://api.example.com/data")
    r.raise_for_status()
    data = r.json()
```

### 6.3 `Response`

```python
r.status_code           # 200
r.text                  # str
r.content               # bytes
r.json()                # dict
r.headers               # dict-like
r.cookies               # cookies
r.url                   # URL object
r.is_success            # 200-299
r.is_redirect           # 300-399
r.is_client_error       # 400-499
r.is_server_error       # 500-599
r.elapsed               # timedelta
r.history               # list of redirects
r.raise_for_status()    # raise on 4xx/5xx

# Stream
with httpx.stream("GET", "https://example.com/big.zip") as r:
    for chunk in r.iter_bytes(chunk_size=8192):
        ...
```

### 6.4 Auth

```python
httpx.BasicAuth("user", "pass")
httpx.DigestAuth("user", "pass")

# Custom
class BearerAuth(httpx.Auth):
    def __init__(self, token):
        self.token = token
    def auth_flow(self, request):
        request.headers["Authorization"] = f"Bearer {self.token}"
        yield request

client = httpx.Client(auth=BearerAuth("xxx"))
```

### 6.5 Exceptions

```python
httpx.HTTPError                  # base
  httpx.RequestError
    httpx.ConnectError
    httpx.TimeoutException
      httpx.ConnectTimeout
      httpx.ReadTimeout
      httpx.WriteTimeout
      httpx.PoolTimeout
    httpx.NetworkError
  httpx.HTTPStatusError          # raised by raise_for_status()
  httpx.InvalidURL
  httpx.CookieConflict
```

---

## 7. Authentication

### 7.1 `argon2.PasswordHasher`

```python
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError, InvalidHash, HashingError

ph = PasswordHasher(
    time_cost=2,            # iterations
    memory_cost=65536,      # KB
    parallelism=4,
    hash_len=32,
    salt_len=16,
)

hashed = ph.hash("password")          # → "$argon2id$v=19$..."
ph.verify(hashed, "password")          # → True (or raises)
ph.check_needs_rehash(hashed)          # → bool (params changed?)
```

### 7.2 `passlib.context.CryptContext`

```python
from passlib.context import CryptContext

pwd = CryptContext(
    schemes=["argon2", "bcrypt"],
    deprecated="auto",
    argon2__rounds=4,
    bcrypt__rounds=12,
)

hashed = pwd.hash("password")
pwd.verify("password", hashed)
pwd.identify(hashed)                    # → "argon2"
pwd.needs_update(hashed)                # → True ถ้า scheme deprecated
ok, new_hash = pwd.verify_and_update("password", hashed)
```

### 7.3 `jose.jwt`

```python
from jose import jwt, JWTError, ExpiredSignatureError
from datetime import datetime, timedelta, timezone

# Encode
token = jwt.encode(
    {"sub": "user_id", "exp": datetime.now(timezone.utc) + timedelta(minutes=15)},
    "SECRET_KEY",
    algorithm="HS256",     # หรือ RS256, ES256
)

# Decode
try:
    payload = jwt.decode(token, "SECRET_KEY", algorithms=["HS256"],
                         audience="my-app", issuer="my-issuer")
except ExpiredSignatureError:
    print("token expired")
except JWTError as e:
    print("invalid:", e)

# Get unverified header (เช่น แสดง kid ก่อน verify)
jwt.get_unverified_header(token)
jwt.get_unverified_claims(token)
```

### 7.4 OAuth2 / OpenID Connect — `authlib`

```python
from authlib.integrations.starlette_client import OAuth

oauth = OAuth()
oauth.register(
    name="google",
    client_id=GOOGLE_CLIENT_ID,
    client_secret=GOOGLE_CLIENT_SECRET,
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
    client_kwargs={"scope": "openid email profile"},
)

@app.get("/login/google")
async def login(request):
    redirect_uri = request.url_for("auth_callback")
    return await oauth.google.authorize_redirect(request, redirect_uri)

@app.get("/auth/callback")
async def auth_callback(request):
    token = await oauth.google.authorize_access_token(request)
    user = token["userinfo"]
    # save / create user
```

---

## 8. Redis

```python
import redis.asyncio as redis

r = redis.from_url("redis://localhost:6379/0", decode_responses=True)
# หรือ
r = redis.Redis(host="localhost", port=6379, db=0, password=None,
                decode_responses=True, max_connections=20)
```

### 8.1 String commands

```python
await r.set("key", "value", ex=60)        # expire 60s
await r.set("key", "v", nx=True)           # only if not exist
await r.set("key", "v", xx=True)           # only if exist
await r.get("key")
await r.getset("key", "new")               # set + return old
await r.mset({"k1": "v1", "k2": "v2"})
await r.mget("k1", "k2")
await r.setex("key", 60, "value")
await r.incr("counter")
await r.incrby("counter", 5)
await r.decrby("counter", 2)
await r.incrbyfloat("temp", 0.5)
await r.append("log", " more")
await r.strlen("log")
```

### 8.2 Key commands

```python
await r.exists("key")              # 0 / 1
await r.delete("k1", "k2")          # → count deleted
await r.expire("key", 60)
await r.ttl("key")                  # seconds left (-1 = no expire, -2 = no key)
await r.persist("key")              # remove expire
await r.keys("user:*")              # ⚠️ avoid in prod (O(N))
await r.scan_iter("user:*", count=100)    # safer for prod
await r.type("key")                 # "string" / "hash" / ...
await r.rename("old", "new")
```

### 8.3 Hash commands (เหมือน dict)

```python
await r.hset("user:1", "name", "Alice")
await r.hset("user:1", mapping={"name": "Alice", "age": "30"})
await r.hget("user:1", "name")
await r.hgetall("user:1")
await r.hdel("user:1", "age")
await r.hexists("user:1", "name")
await r.hkeys("user:1")
await r.hvals("user:1")
await r.hincrby("user:1", "views", 1)
await r.hlen("user:1")
```

### 8.4 List commands (queue/stack)

```python
await r.rpush("queue", "job1", "job2")    # push right
await r.lpush("queue", "urgent")           # push left
await r.lpop("queue")                       # pop left
await r.rpop("queue")
await r.blpop("queue", timeout=10)         # blocking pop
await r.lrange("queue", 0, -1)              # all
await r.llen("queue")
await r.lindex("queue", 0)
```

### 8.5 Set commands

```python
await r.sadd("tags", "py", "fastapi")
await r.srem("tags", "py")
await r.smembers("tags")
await r.sismember("tags", "py")
await r.scard("tags")                        # count
await r.sinter("tags1", "tags2")             # intersection
await r.sunion("tags1", "tags2")
await r.sdiff("tags1", "tags2")
```

### 8.6 Sorted set (leaderboard)

```python
await r.zadd("scores", {"alice": 100, "bob": 200})
await r.zincrby("scores", 50, "alice")
await r.zrange("scores", 0, 9, withscores=True)
await r.zrevrange("scores", 0, 9)            # top N
await r.zrangebyscore("scores", 50, 150)
await r.zrank("scores", "alice")
await r.zrem("scores", "alice")
await r.zcard("scores")
```

### 8.7 Pub/Sub

```python
# Publisher
await r.publish("channel", "message")

# Subscriber
pubsub = r.pubsub()
await pubsub.subscribe("channel", "channel2")
async for msg in pubsub.listen():
    if msg["type"] == "message":
        print(msg["channel"], msg["data"])
```

### 8.8 Pipeline (batch)

```python
async with r.pipeline(transaction=True) as pipe:
    pipe.set("k1", "v1")
    pipe.incr("counter")
    pipe.expire("k1", 60)
    results = await pipe.execute()
```

### 8.9 Lock

```python
async with r.lock("resource:lock", timeout=10, blocking_timeout=5):
    # critical section
    ...
```

---

## 9. Loguru

```python
from loguru import logger
```

### 9.1 Methods

```python
logger.trace("very detailed")
logger.debug("debug")
logger.info("info")
logger.success("works!")       # custom level
logger.warning("warn")
logger.error("error")
logger.critical("CRITICAL")
logger.exception("with traceback")    # use in except block
```

### 9.2 `logger.add` — handler

```python
import sys

logger.add(sys.stderr,
           format="<green>{time}</green> | <level>{level: <8}</level> | {message}",
           level="INFO",
           colorize=True,
           backtrace=True,           # show full traceback
           diagnose=True,            # extra value info (turn off in prod for security)
           catch=True,               # catch errors in sink
)

# File
logger.add("logs/app_{time:YYYY-MM-DD}.log",
           rotation="10 MB",         # หรือ "00:00", "1 week"
           retention="30 days",      # หรือ count "10 files"
           compression="gz",
           level="DEBUG",
           encoding="utf-8",
           enqueue=True,             # thread-safe + async write
)

# JSON for log aggregator
logger.add("logs/app.json", serialize=True)

# Send to external (Sentry-style)
def push_to_slack(message):
    httpx.post("https://hooks.slack.com/...", json={"text": message})
logger.add(push_to_slack, level="ERROR")
```

### 9.3 Bind & context

```python
log = logger.bind(request_id="abc-123", user_id=42)
log.info("processing")
# → ใน format ใช้ {extra[request_id]}

# Context manager
with logger.contextualize(request_id="abc"):
    do_work()
```

### 9.4 Decorator

```python
@logger.catch                          # log uncaught exceptions
def risky():
    1 / 0

@logger.catch(reraise=True)            # log + re-raise
def risky2():
    1 / 0
```

### 9.5 Filter

```python
logger.add("admin.log", filter=lambda r: r["extra"].get("admin") == True)
logger.bind(admin=True).info("admin event")    # → goes to admin.log
```

---

## 10. Jinja2

### 10.1 `Environment` / `FileSystemLoader`

```python
from jinja2 import Environment, FileSystemLoader, select_autoescape

env = Environment(
    loader=FileSystemLoader("templates"),
    autoescape=select_autoescape(["html", "xml"]),
    trim_blocks=True,
    lstrip_blocks=True,
    enable_async=False,        # True ถ้าใช้กับ FastAPI async
    cache_size=400,
    auto_reload=True,
)

template = env.get_template("base.html")
html = template.render(user=user, items=items)

# Render string ตรงๆ
template = env.from_string("Hello {{ name }}")
template.render(name="World")
```

### 10.2 Template syntax

```jinja
{# Comment #}

{# Variable #}
{{ user.name }}
{{ user.name | upper }}                      {# filter #}
{{ user.name | default("Anonymous") }}
{{ price | round(2) }}
{{ items | length }}
{{ name | escape }}                          {# alias: e #}
{{ items | join(", ") }}
{{ "hello" | replace("l", "L") }}

{# If #}
{% if user.is_admin %}
  Admin
{% elif user.is_active %}
  User
{% else %}
  Guest
{% endif %}

{# For #}
{% for item in items %}
  {{ loop.index }} - {{ item.name }}
  {% if loop.last %}END{% endif %}
{% endfor %}

{# Set #}
{% set total = items | sum(attribute="price") %}

{# Macro #}
{% macro input(name, value="", type="text") %}
  <input name="{{ name }}" value="{{ value }}" type="{{ type }}">
{% endmacro %}

{{ input("email", value=user.email) }}

{# Include #}
{% include "header.html" %}
{% include "footer.html" ignore missing %}

{# Extend / blocks #}
{% extends "base.html" %}
{% block content %}
  <h1>{{ title }}</h1>
{% endblock %}
{% block sidebar %}{{ super() }} extra{% endblock %}

{# Raw #}
{% raw %}
  {{ this stays as-is }}
{% endraw %}
```

### 10.3 Custom filter / global

```python
def format_thai_baht(n):
    return f"฿{n:,.2f}"

env.filters["baht"] = format_thai_baht
env.globals["site_name"] = "CMT"

# In template:  {{ 1234 | baht }} → ฿1,234.00
```

---

## 11. WeasyPrint

```python
from weasyprint import HTML, CSS

# From string
HTML(string="<h1>Hello</h1>").write_pdf("out.pdf")

# From file
HTML(filename="invoice.html").write_pdf("invoice.pdf")

# From URL
HTML(url="https://example.com").write_pdf("page.pdf")

# Custom CSS
HTML(string=html).write_pdf("out.pdf",
                            stylesheets=[CSS(filename="print.css"),
                                         CSS(string="body { font-family: Sarabun; }")])

# Bytes (no file)
pdf_bytes = HTML(string=html).write_pdf()

# Page settings via @page in CSS
css = CSS(string="""
@page {
  size: A4;
  margin: 2cm 1.5cm;
  @top-center { content: "Invoice"; }
  @bottom-right { content: "Page " counter(page) " of " counter(pages); }
}
""")

# Image (PNG) instead of PDF
HTML(string=html).write_png("out.png")
```

---

## 12. Pillow

```python
from PIL import Image, ImageOps, ImageFilter, ImageEnhance, ImageDraw, ImageFont

# Open / save
img = Image.open("input.jpg")
img.save("output.png")
img.save("output.webp", quality=80, optimize=True)

# Info
img.size            # (W, H)
img.width, img.height
img.mode            # "RGB", "RGBA", "L" (grayscale)
img.format          # "JPEG"

# Resize
img.resize((800, 600), Image.LANCZOS)
img.thumbnail((800, 600))                  # in-place, keep aspect
ImageOps.fit(img, (500, 500))              # crop+resize to exact size
ImageOps.contain(img, (800, 800))           # fit inside, keep aspect

# Crop
img.crop((100, 100, 400, 400))              # (left, top, right, bottom)

# Rotate / flip
img.rotate(45, expand=True)
ImageOps.flip(img)                           # vertical
ImageOps.mirror(img)                         # horizontal
img.transpose(Image.ROTATE_90)

# Filter
img.filter(ImageFilter.BLUR)
img.filter(ImageFilter.GaussianBlur(5))
img.filter(ImageFilter.SHARPEN)
img.filter(ImageFilter.EDGE_ENHANCE)

# Enhance
ImageEnhance.Contrast(img).enhance(1.5)
ImageEnhance.Brightness(img).enhance(1.2)
ImageEnhance.Color(img).enhance(0.5)         # 0 = grayscale

# Convert mode
img.convert("L")                              # grayscale
img.convert("RGBA")
img.convert("RGB")                            # for JPEG save

# Composite / watermark
base = Image.open("photo.jpg")
draw = ImageDraw.Draw(base)
font = ImageFont.truetype("Sarabun.ttf", 40)
draw.text((20, 20), "© CMT", font=font, fill=(255, 255, 255, 200))
draw.rectangle([10, 10, 200, 60], outline="red", width=3)
draw.line([(0, 0), (100, 100)], fill="blue")
base.save("watermarked.jpg")

# Paste
overlay = Image.open("logo.png")
base.paste(overlay, (50, 50), overlay)        # 3rd arg = mask
```

---

## 13. Openpyxl

```python
from openpyxl import Workbook, load_workbook
from openpyxl.styles import Font, Fill, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
from openpyxl.chart import LineChart, BarChart, Reference

# Create
wb = Workbook()
ws = wb.active
ws.title = "Vendors"

# Multiple sheets
ws2 = wb.create_sheet("Summary", index=0)
wb["Vendors"]                                 # access by name
wb.sheetnames                                  # list
wb.remove(wb["Sheet1"])

# Cells
ws["A1"] = "Header"
ws.cell(row=1, column=1, value="Header")
ws["A1"].value
ws["A1:C5"]                                   # tuple of rows

# Append row
ws.append(["Name", "Email", "Grade"])
ws.append(["Alice", "a@b.c", "A"])

# Iterate
for row in ws.iter_rows(min_row=2, values_only=True):
    print(row)
for col in ws.iter_cols(min_col=1, max_col=3):
    ...

# Format
cell = ws["A1"]
cell.font = Font(name="Arial", size=12, bold=True, color="FFFFFF")
cell.fill = PatternFill("solid", fgColor="1e3a8a")
cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
cell.border = Border(left=Side(border_style="thin", color="000000"),
                     right=Side(border_style="thin"),
                     top=Side(border_style="thin"),
                     bottom=Side(border_style="thin"))
cell.number_format = "#,##0.00"               # หรือ "0.00%", "dd/mm/yyyy"

# Column width / row height
ws.column_dimensions["A"].width = 20
ws.row_dimensions[1].height = 30

# Merge
ws.merge_cells("A1:C1")
ws.unmerge_cells("A1:C1")

# Freeze
ws.freeze_panes = "A2"

# Formula
ws["D2"] = "=SUM(A2:C2)"
ws["E1"] = "=VLOOKUP(A1, Sheet2!A:B, 2, FALSE)"

# Chart
chart = BarChart()
data = Reference(ws, min_col=2, min_row=1, max_col=3, max_row=10)
chart.add_data(data, titles_from_data=True)
ws.add_chart(chart, "E2")

# Save
wb.save("output.xlsx")

# Read
wb = load_workbook("input.xlsx", data_only=True)    # data_only=True → formula → value
```

---

## 14. Tenacity

```python
from tenacity import (
    retry,
    stop_after_attempt, stop_after_delay, stop_never,
    wait_fixed, wait_random, wait_exponential, wait_chain,
    retry_if_exception_type, retry_if_result, retry_if_not_exception_type,
    before_sleep_log, after_log,
    Retrying,
)

# Decorator
@retry(
    stop=stop_after_attempt(5),
    wait=wait_exponential(multiplier=1, min=2, max=60),
    retry=retry_if_exception_type((httpx.HTTPError, ConnectionError)),
    reraise=True,
    before_sleep=before_sleep_log(logger, logging.WARNING),
)
async def fetch(url):
    ...

# Stop strategies
stop_after_attempt(3)                      # max 3 tries
stop_after_delay(60)                        # max 60 sec total
stop_after_attempt(3) | stop_after_delay(30)   # OR
stop_never                                  # forever

# Wait strategies
wait_fixed(2)                              # 2 sec between
wait_random(min=1, max=5)
wait_exponential(multiplier=1, min=2, max=60)    # 2, 4, 8, 16, ... 60
wait_chain(*[wait_fixed(1)] * 3 + [wait_fixed(5)])  # 1, 1, 1, 5, 5, ...

# Retry conditions
retry_if_exception_type(ValueError)
retry_if_not_exception_type(KeyError)
retry_if_result(lambda r: r is None)
retry_if_exception_message(match=".*timeout.*")

# Manual retry (without decorator)
for attempt in Retrying(stop=stop_after_attempt(3), wait=wait_fixed(2)):
    with attempt:
        result = risky()
```

---

## 15. APScheduler

```python
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.triggers.date import DateTrigger

scheduler = AsyncIOScheduler(timezone="Asia/Bangkok")

# Cron
scheduler.add_job(
    annual_eval,
    CronTrigger(month=12, day=31, hour=0, minute=0),
    id="annual_eval",
    replace_existing=True,
    misfire_grace_time=3600,
)
# CronTrigger args: year, month, day, week, day_of_week, hour, minute, second
# Day of week: "mon", "tue", ..., "sun" หรือ 0-6
scheduler.add_job(daily_report, "cron", hour=8, minute=0)
scheduler.add_job(weekly_clean, "cron", day_of_week="mon", hour=2)

# Interval
scheduler.add_job(poll_status, "interval", minutes=5)
scheduler.add_job(heartbeat, IntervalTrigger(seconds=30))

# One-time
scheduler.add_job(send_reminder, DateTrigger(run_date="2026-12-31 23:30:00"))

# Args
scheduler.add_job(notify, "cron", hour=9, args=["user@example.com"], kwargs={"urgent": True})

# Lifecycle
scheduler.start()
scheduler.shutdown(wait=True)
scheduler.pause()
scheduler.resume()
scheduler.print_jobs()
scheduler.remove_job("annual_eval")
scheduler.modify_job("annual_eval", trigger="cron", hour=1)

# Persistent jobstore (survive restart)
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
scheduler = AsyncIOScheduler(
    jobstores={"default": SQLAlchemyJobStore(url="postgresql://...")},
)
```

---

## 16. Typer + Rich

### 16.1 `typer.Typer`

```python
import typer
from typing import Optional
from typing_extensions import Annotated

app = typer.Typer(
    name="cmt",
    help="CMT Procurement CLI",
    add_completion=True,
    no_args_is_help=True,
    rich_markup_mode="rich",
)

@app.command()
def hello(
    name: Annotated[str, typer.Argument(help="ชื่อคน")],
    formal: Annotated[bool, typer.Option(help="แบบเป็นทางการ")] = False,
    count: Annotated[int, typer.Option(min=1, max=10)] = 1,
):
    """Say hello"""
    greeting = "สวัสดีครับ" if formal else "หวัดดี"
    for _ in range(count):
        typer.echo(f"{greeting} {name}")

@app.command()
def stats(
    env: Annotated[str, typer.Option("--env", "-e")] = "dev",
    json_output: Annotated[bool, typer.Option("--json")] = False,
):
    ...

# Sub-commands (multi-level)
admin = typer.Typer()
app.add_typer(admin, name="admin")

@admin.command("create-user")
def admin_create_user(email: str): ...

# Run: python cli.py admin create-user --email a@b.c

if __name__ == "__main__":
    app()
```

### 16.2 Typer parameter types

```python
# File / Path
def cmd(
    file: Annotated[typer.FileText, typer.Argument()],
    binary: Annotated[typer.FileBinaryRead, typer.Argument()],
    out: Annotated[typer.FileTextWrite, typer.Option()] = "-",
    path: Annotated[Path, typer.Argument(exists=True, dir_okay=False, readable=True)],
): ...

# Datetime
def cmd(when: datetime = typer.Option(default=None, formats=["%Y-%m-%d"])): ...

# Choice (Enum)
class Env(str, Enum):
    dev = "dev"
    staging = "staging"
    prod = "prod"

def cmd(env: Env = Env.dev): ...

# Prompt / confirmation
def cmd(
    password: str = typer.Option(..., prompt=True, hide_input=True, confirmation_prompt=True),
    delete: bool = typer.Option(..., prompt="Sure?", confirm=True),
):
```

### 16.3 Rich

```python
from rich import print
from rich.console import Console
from rich.table import Table
from rich.tree import Tree
from rich.panel import Panel
from rich.progress import track, Progress, SpinnerColumn, BarColumn, TextColumn
from rich.syntax import Syntax
from rich.markdown import Markdown
from rich.prompt import Prompt, Confirm, IntPrompt
from rich.live import Live

console = Console()

# Print with markup
print("[bold red]Error[/bold red] :warning:")
console.print("Hello", style="bold green on white")

# Table
table = Table(title="Vendors", show_lines=True)
table.add_column("ID", style="cyan", justify="right")
table.add_column("Name", style="green")
table.add_column("Grade", style="yellow")
table.add_row("V001", "Acme", "A")
table.add_row("V002", "Beta", "B")
console.print(table)

# Tree
tree = Tree("📁 Project")
src = tree.add("📁 src")
src.add("📄 main.py")
src.add("📄 models.py")
console.print(tree)

# Panel
console.print(Panel("Hello", title="Greeting", border_style="blue"))

# Progress
for i in track(range(100), description="Processing..."):
    process(i)

# Advanced progress
with Progress(
    SpinnerColumn(),
    TextColumn("[bold blue]{task.description}"),
    BarColumn(),
    "[progress.percentage]{task.percentage:>3.0f}%",
) as prog:
    task = prog.add_task("Downloading", total=100)
    for _ in range(100):
        prog.update(task, advance=1)

# Syntax highlighting
syntax = Syntax("print('hello')", "python", theme="monokai", line_numbers=True)
console.print(syntax)

# Markdown
console.print(Markdown("# Title\n- item 1\n- item 2"))

# Prompt
name = Prompt.ask("ชื่อ?", default="Anonymous")
age = IntPrompt.ask("อายุ?", default=20)
ok = Confirm.ask("ดำเนินการต่อ?")
```

---

## 🎯 Library Quick Lookup

| ต้องการ       | Library       | Class หลัก                                         |
| ------------- | ------------- | -------------------------------------------------- |
| Validate data | pydantic      | `BaseModel`, `Field`, `field_validator`            |
| Build web API | fastapi       | `FastAPI`, `APIRouter`, `Depends`, `HTTPException` |
| ORM           | sqlalchemy    | `DeclarativeBase`, `Mapped`, `Session`, `select`   |
| DB migration  | alembic       | CLI: `alembic revision/upgrade`                    |
| HTTP client   | httpx         | `Client`, `AsyncClient`, `Response`                |
| Password hash | argon2-cffi   | `PasswordHasher`                                   |
| JWT           | python-jose   | `jwt.encode`, `jwt.decode`                         |
| OAuth         | authlib       | `OAuth.register`                                   |
| Cache         | redis         | `Redis`, commands above                            |
| Logging       | loguru        | `logger.add`, `logger.bind`                        |
| Template      | jinja2        | `Environment`, `FileSystemLoader`                  |
| PDF           | weasyprint    | `HTML`, `CSS`                                      |
| Image         | Pillow        | `Image`, `ImageOps`, `ImageDraw`                   |
| Excel         | openpyxl      | `Workbook`, `load_workbook`                        |
| Retry         | tenacity      | `@retry`, `stop_after_attempt`, `wait_exponential` |
| Schedule      | apscheduler   | `AsyncIOScheduler`, `CronTrigger`                  |
| CLI           | typer + rich  | `Typer`, `Console`, `Table`                        |
| Test          | pytest        | `@pytest.fixture`, `@pytest.mark.parametrize`      |
| Mock          | unittest.mock | `MagicMock`, `AsyncMock`, `patch`                  |
| Test data     | factory_boy   | `Factory`, `Faker`, `SubFactory`                   |
| Freeze time   | freezegun     | `freeze_time`                                      |
| Mock HTTP     | respx         | `respx.mock`, `respx.get/post`                     |
| Property test | hypothesis    | `@given`, `strategies as st`                       |
| Load test     | locust        | `HttpUser`, `@task`                                |

---

> 💪 **คาถา:** "เปิดทีละ class ดูตัวอย่าง — ทำงานทันที ไม่ต้องค้น docs ภายนอก"
