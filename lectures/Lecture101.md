# 🐍 Python Backend Zero to Hero (ฉบับขยาย)

## FastAPI + SQLAlchemy + Pydantic + Libraries สำคัญ พร้อมคำอธิบายภาษาชาวบ้าน

> 💬 **ภาษาชาวบ้าน:** คู่มือนี้เหมือนคู่มือทำอาหาร — บอกว่า "เครื่องมือชิ้นนี้ทำอะไร เหมือนของในครัวอะไร แล้วใช้ยังไง"

---

## 📚 สารบัญ

1. [ปูพื้นฐาน: Environment & Tools](#1-ปูพื้นฐาน)
2. [Pydantic – หัวใจของการ Validate Data](#2-pydantic)
3. [FastAPI – Modern Web Framework](#3-fastapi)
4. [SQLAlchemy – ORM ที่ทรงพลัง](#4-sqlalchemy)
5. [Alembic – Database Migration](#5-alembic)
6. [Authentication & Security](#6-authentication--security)
7. [Async, HTTP Client & Background Tasks](#7-async-http-client--background-tasks)
8. [Logging, Monitoring & Error Tracking](#8-logging-monitoring--error-tracking)
9. [Caching & Performance (Redis)](#9-caching--performance-redis)
10. [File Handling, Email, PDF](#10-file-handling-email-pdf)
11. [CLI Tools & Date/Time](#11-cli-tools--datetime)
12. [Testing ด้วย Pytest (ภาพรวม)](#12-testing)
13. [Project Structure ระดับ Production](#13-project-structure)
14. [Deployment & Best Practices](#14-deployment)
15. [Library Cheatsheet สำหรับ Hero](#15-library-cheatsheet)

---

## 1. ปูพื้นฐาน

### 🧠 ก่อนเริ่ม — เข้าใจ "ภาษาคนทำงาน" ก่อน

| คำศัพท์        | ภาษาชาวบ้าน                                                             |
| -------------- | ----------------------------------------------------------------------- |
| **Backend**    | "ครัวร้านอาหาร" — ที่ลูกค้ามองไม่เห็น แต่ทำอาหารจริงๆ                   |
| **API**        | "เมนู + พนักงานเสิร์ฟ" — ลูกค้าสั่งผ่านเมนู ครัวทำให้ตามนั้น            |
| **Framework**  | "เตาครัวสำเร็จรูป" — มีเตา/อ่างล้างจาน/ตู้เย็นพร้อมแล้ว ไม่ต้องสร้างเอง |
| **Library**    | "เครื่องครัวเฉพาะทาง" — เครื่องปั่น เครื่องชั่ง ที่หยิบมาใช้ตอนต้องการ  |
| **ORM**        | "ล่ามแปลภาษา" — Python คุยกับฐานข้อมูล (SQL) ผ่านล่ามตัวนี้             |
| **Async**      | "เปิดไฟหุงข้าวไว้ ระหว่างนั้นไปล้างผัก" — ทำหลายอย่างพร้อมกันโดยไม่รอ   |
| **Type hint**  | "ป้ายแปะถังในตู้เย็น" — บอกล่วงหน้าว่าในกล่องนี้คืออะไร                 |
| **Validation** | "ตรวจของก่อนรับเข้าครัว" — เช็คว่าวัตถุดิบครบ ไม่เน่า ก่อนทำอาหาร       |
| **Migration**  | "แผนรีโนเวทร้าน" — เปลี่ยนแบบครัวเก่า → ใหม่ พร้อมวิธีย้อนกลับถ้าผิด    |

### 🔧 ติดตั้ง Python และ Virtual Environment

> 💬 **Virtual environment คืออะไร:** กล่องแยกของแต่ละโปรเจค — ไม่ให้ library โปรเจค A ชนกับโปรเจค B (เหมือนตู้เครื่องครัวแยกของแต่ละร้าน)

```bash
# ตรวจสอบ Python (ควรเป็น 3.11+ ปี 2026 ใช้ 3.12+)
python --version

# วิธีดั้งเดิม (ช้า แต่ใช้ได้ทุกที่)
python -m venv venv
source venv/bin/activate          # macOS/Linux
# venv\Scripts\activate           # Windows
pip install fastapi
```

### 📦 ใช้ `uv` (แนะนำในปี 2026 — เร็วสุด)

> 💬 **uv คือ:** เครื่องมือจัดการ library + venv รวมในตัวเดียว เขียนด้วย Rust → **เร็วกว่า pip 10-100 เท่า** เหมือนเปลี่ยนจากรถเข็นเป็นรถไฟ

```bash
# ติดตั้ง uv ครั้งเดียว
curl -LsSf https://astral.sh/uv/install.sh | sh

# สร้างโปรเจคใหม่
uv init my-project
cd my-project

# เพิ่ม dependencies
uv add fastapi sqlalchemy pydantic
uv add --dev pytest ruff mypy

# รัน script ในกล่อง (ไม่ต้อง activate venv เอง)
uv run python main.py
uv run pytest

# ติดตั้งจาก lock file (production / CI)
uv sync --frozen --no-dev
```

**เปรียบเทียบเครื่องมือ:**

| เครื่องมือ  | ความเร็ว       | ใช้ทำอะไร               | ภาษาชาวบ้าน           |
| ----------- | -------------- | ----------------------- | --------------------- |
| `pip`       | 🐢 ช้า         | ติดตั้ง package พื้นฐาน | ดั้งเดิม ใช้ได้แต่ช้า |
| `pip-tools` | 🐢 ช้า         | + lock file             | ดั้งเดิม + จดสูตร     |
| `poetry`    | 🐇 กลาง        | จัดการ deps + venv      | ครบเครื่องแต่ช้า      |
| **`uv`** ⭐ | 🚀 **เร็วสุด** | ครบทุกอย่าง + Rust      | รถไฟความเร็วสูง       |
| `pdm`       | 🐇 กลาง        | คล้าย poetry            | ทางเลือก              |

### 🎯 Libraries หลักที่จะใช้ใน Lecture นี้

| Library                    | หน้าที่            | ภาษาชาวบ้าน                                    |
| -------------------------- | ------------------ | ---------------------------------------------- |
| `fastapi`                  | Web framework      | "เตาครัวสำเร็จ" สำหรับสร้าง API                |
| `pydantic`                 | Data validation    | "ผู้คุมประตูครัว" ตรวจว่าของที่ส่งมาถูกต้องไหม |
| `sqlalchemy`               | ORM                | "ล่ามแปลภาษา" — Python คุยกับ DB               |
| `alembic`                  | Database migration | "แผนรีโนเวท" สำหรับ DB schema                  |
| `uvicorn` / `granian`      | ASGI server        | "เครื่องจ่ายไฟ" ให้ FastAPI ทำงาน              |
| `httpx`                    | Async HTTP client  | "คนวิ่งไปซื้อของ" ที่ไปได้หลายร้านพร้อมกัน     |
| `argon2-cffi` / `passlib`  | Password hashing   | "เครื่องปั่นรหัส" ให้พังกลับไม่ได้             |
| `python-jose`              | JWT                | "บัตรผ่านเข้างาน" มี expiry                    |
| `pytest`, `pytest-asyncio` | Testing            | "ผู้ตรวจการ QC" ก่อนส่งของออก                  |
| `pydantic-settings`        | Env config         | "ตู้เซฟใส่กุญแจ" ของ secret/config             |
| `loguru`                   | Logging            | "สมุดจดเหตุการณ์"                              |
| `tenacity`                 | Retry logic        | "ลองใหม่อัตโนมัติ" เมื่อพลาด                   |
| `redis`                    | Cache              | "ตู้เย็นเร็ว" เก็บของที่ใช้บ่อย                |

```bash
uv add fastapi "uvicorn[standard]" sqlalchemy alembic pydantic pydantic-settings \
       "passlib[bcrypt]" argon2-cffi "python-jose[cryptography]" \
       httpx python-multipart loguru tenacity
uv add --dev pytest pytest-asyncio pytest-cov ruff mypy
```

---

## 2. Pydantic

> 💬 **Pydantic คืออะไร:** "ผู้คุมประตูข้อมูล" — ก่อนข้อมูลเข้า/ออกระบบ ต้องผ่านการตรวจสอบที่นี่ ถ้าผิด format จะ reject ทันที **ทำให้บั๊กเจอเร็ว ไม่ลามไปที่อื่น**
>
> Pydantic v2 เขียน core ด้วย Rust → **เร็วกว่า v1 ถึง 5-50 เท่า** เป็นพื้นฐานของ FastAPI

### 2.1 BaseModel เบื้องต้น

```python
from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional

class User(BaseModel):
    id: int
    name: str = Field(min_length=2, max_length=50)
    email: EmailStr
    age: int = Field(ge=0, le=150)              # ge = greater equal, le = less equal
    is_active: bool = True
    created_at: datetime = Field(default_factory=datetime.now)
    bio: Optional[str] = None

# ใช้งาน
user = User(id=1, name="Somchai", email="som@example.com", age=30)
print(user.model_dump())          # → dict
print(user.model_dump_json())     # → JSON string

# ถ้าผิด → ValidationError ทันที (โปรแกรมไม่ลามไป crash ที่อื่น)
try:
    bad = User(id="not-a-number", name="A", email="invalid", age=-5)
except Exception as e:
    print(e)
```

> 💬 **Field() คืออะไร:** ตัวกำหนดเงื่อนไขของ field — เหมือนป้ายติดที่ช่องว่า "ใส่อายุ 0-150 เท่านั้น"

### 2.2 Validators (กฎเฉพาะที่ Field ทำไม่ได้)

```python
from pydantic import BaseModel, field_validator, model_validator

class Product(BaseModel):
    name: str
    price: float
    discount_price: float | None = None

    # ตรวจ field เดี่ยว
    @field_validator("name")
    @classmethod
    def name_must_not_be_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("name ห้ามเป็นค่าว่าง")
        return v.title()    # auto-capitalize

    # ตรวจหลาย field พร้อมกัน
    @model_validator(mode="after")
    def check_discount(self):
        if self.discount_price and self.discount_price >= self.price:
            raise ValueError("ราคาลดต้องน้อยกว่าราคาเต็ม")
        return self
```

> 💬 **Validator คือ:** กฎเฉพาะที่ Field() ทำไม่ได้ — เช่น "ราคาลดต้องน้อยกว่าราคาเต็ม" ต้องดูทั้ง 2 field พร้อมกัน

### 2.3 Nested Models & Config

```python
class Address(BaseModel):
    city: str
    zipcode: str = Field(pattern=r"^\d{5}$")    # ต้องเป็นเลข 5 หลัก

class Customer(BaseModel):
    name: str
    addresses: list[Address]                     # list ของ Address

    model_config = {
        "str_strip_whitespace": True,            # ตัด whitespace อัตโนมัติ
        "from_attributes": True,                 # อ่านจาก ORM object ได้ (SQLAlchemy → Pydantic)
        "json_schema_extra": {
            "example": {"name": "Anan", "addresses": [{"city": "BKK", "zipcode": "10100"}]}
        }
    }

# Pydantic จะ validate nested ให้อัตโนมัติ
c = Customer(name="A", addresses=[{"city": "BKK", "zipcode": "10100"}])
# ↑ addresses[0] กลายเป็น Address object ทันที (ไม่ใช่ dict)
```

### 2.4 Computed Fields (field คำนวณจาก field อื่น)

```python
from pydantic import BaseModel, computed_field

class Order(BaseModel):
    quantity: int
    unit_price: float

    @computed_field
    @property
    def total(self) -> float:
        return self.quantity * self.unit_price

o = Order(quantity=3, unit_price=10.5)
print(o.total)                  # 31.5
print(o.model_dump())           # {"quantity": 3, "unit_price": 10.5, "total": 31.5}
```

> 💬 **Computed field คือ:** field ที่คำนวณจาก field อื่น — เหมือน "ยอดรวม" ใน Excel ที่เป็นสูตร ไม่ต้องพิมพ์เอง

### 2.5 Custom Types & Serializers

```python
from pydantic import BaseModel, field_serializer
from decimal import Decimal
from datetime import datetime

class Invoice(BaseModel):
    number: str
    amount: Decimal
    issued_at: datetime

    # ปรับ format ตอน serialize → JSON
    @field_serializer("amount")
    def ser_amount(self, v: Decimal) -> str:
        return f"{v:,.2f}"      # → "1,234.56"

    @field_serializer("issued_at")
    def ser_date(self, v: datetime) -> str:
        return v.strftime("%d/%m/%Y")
```

### 2.6 Settings Management ด้วย `pydantic-settings`

> 💬 **Settings คือ:** ค่า config ของระบบ (DB URL, secret key) — อ่านจาก environment variable หรือ `.env` file → **ไม่ hardcode ใส่ในโค้ด**

```python
# config.py
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, PostgresDsn

class Settings(BaseSettings):
    # ค่าจาก env vars (case-insensitive)
    app_name: str = "My API"
    database_url: PostgresDsn        # auto-validate ว่าเป็น postgres URL จริง
    secret_key: str = Field(min_length=32)
    debug: bool = False
    redis_url: str = "redis://localhost:6379/0"
    smtp_host: str | None = None
    smtp_port: int = 587

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",      # ignore env var ที่ไม่ได้ define
    )

# ใช้แบบ singleton ทั่วทั้ง app
settings = Settings()
```

```bash
# .env
DATABASE_URL=postgresql://user:pass@localhost/db
SECRET_KEY=super-secret-key-at-least-32-characters-long
DEBUG=true
REDIS_URL=redis://redis:6379/0
```

### 2.7 Discriminated Union (Polymorphism)

> 💬 **คือ:** ของหลายแบบในกล่องเดียวกัน — เช่น order มีได้ทั้ง pickup และ delivery แต่ field ต่างกัน

```python
from typing import Literal, Union
from pydantic import BaseModel, Field

class PickupOrder(BaseModel):
    type: Literal["pickup"]
    branch: str

class DeliveryOrder(BaseModel):
    type: Literal["delivery"]
    address: str
    phone: str

class OrderRequest(BaseModel):
    order: Union[PickupOrder, DeliveryOrder] = Field(discriminator="type")

# Pydantic เห็น type="pickup" → สร้าง PickupOrder อัตโนมัติ
o = OrderRequest(order={"type": "pickup", "branch": "BKK-01"})
```

### 2.8 Pitfalls ที่เจอบ่อย

| Pitfall                                             | คำอธิบาย                               | วิธีแก้                                            |
| --------------------------------------------------- | -------------------------------------- | -------------------------------------------------- |
| `BaseModel` ไม่ support keyword-only ในที่เก่าจริงๆ | v2 ต่างจาก v1 มาก                      | อย่าใช้ tutorial เก่ากว่า 2023                     |
| ลืม `model_config = {"from_attributes": True}`      | SQLAlchemy → Pydantic ไม่ทำงาน         | เพิ่ม config นี้ใน response model                  |
| Validate ตอน assign ทีหลังไม่ทำงาน                  | default ของ v2 = validate only on init | ใส่ `model_config = {"validate_assignment": True}` |
| `Optional[str] = None` vs `str \| None = None`      | เหมือนกัน — `\|` ใหม่กว่า              | ใช้ `str \| None` (Python 3.10+)                   |

---

## 3. FastAPI

> 💬 **FastAPI คือ:** เครื่องมือสร้าง API (เมนูครัว) — เร็ว, มี Swagger UI อัตโนมัติ, type-safe ครบ → **เขียน Python ธรรมดาแล้วได้ API พร้อม docs**

### 3.1 Hello World

```python
# main.py
from fastapi import FastAPI

app = FastAPI(
    title="My First API",
    version="1.0.0",
    description="ตัวอย่าง API สาธิต",
)

@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI!"}
```

```bash
uvicorn main:app --reload
# เปิด http://localhost:8000/docs   ← Swagger UI อัตโนมัติ!
# เปิด http://localhost:8000/redoc  ← ReDoc (อ่านง่ายกว่า)
# เปิด http://localhost:8000/openapi.json ← spec ดิบ
```

> 💬 **--reload:** auto restart เมื่อแก้โค้ด — ใช้แค่ตอน dev, ห้ามใช้ production

### 3.2 Path & Query Parameters

```python
from fastapi import FastAPI, Query, Path

@app.get("/items/{item_id}")
def get_item(
    item_id: int = Path(gt=0, description="ID ของสินค้า"),
    q: str | None = Query(None, max_length=50, description="คำค้นหา"),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    tags: list[str] = Query([]),     # /items/1?tags=a&tags=b
):
    return {"item_id": item_id, "q": q, "skip": skip, "limit": limit, "tags": tags}
```

| Parameter type | ภาษาชาวบ้าน          | ตัวอย่าง URL                        |
| -------------- | -------------------- | ----------------------------------- |
| Path           | "อยู่ในที่อยู่"      | `/items/{item_id}` → `/items/42`    |
| Query          | "ติดท้าย URL หลัง ?" | `?q=apple&limit=10`                 |
| Header         | "ส่งใน header"       | `Authorization: Bearer xxx`         |
| Body           | "ส่งใน request body" | JSON body                           |
| Form           | "ส่งจาก HTML form"   | `application/x-www-form-urlencoded` |
| File           | "อัพโหลดไฟล์"        | `multipart/form-data`               |

### 3.3 Request Body ด้วย Pydantic

```python
from pydantic import BaseModel

class ItemCreate(BaseModel):
    name: str
    price: float
    tags: list[str] = []
    description: str | None = None

class ItemResponse(BaseModel):
    id: int
    name: str
    price: float
    tags: list[str]

@app.post("/items/", response_model=ItemResponse, status_code=201)
def create_item(item: ItemCreate):
    new_id = 1   # สมมติ
    return {**item.model_dump(), "id": new_id}
```

> 💬 **response_model คือ:** กรองข้อมูลก่อนส่งกลับ client — เช่น ใน DB มี `hashed_password` แต่ response_model ไม่มี → ไม่หลุดออกไป

### 3.4 Dependency Injection (หัวใจของ FastAPI)

> 💬 **Dependency injection คือ:** "บอก FastAPI ว่า endpoint นี้ต้องการอะไรประกอบ" แล้ว FastAPI จัดให้ — เหมือนสั่งอาหาร แล้วพ่อครัวเตรียมเครื่องเคียงให้อัตโนมัติ

```python
from fastapi import Depends, HTTPException, Header

# Dependency #1 — ตรวจ token
def get_token_header(x_token: str = Header()):
    if x_token != "secret-token":
        raise HTTPException(status_code=403, detail="Token ไม่ถูกต้อง")
    return x_token

# Dependency #2 — pagination ที่ใช้ซ้ำในหลาย endpoint
def common_pagination(skip: int = 0, limit: int = 100):
    return {"skip": skip, "limit": limit}

@app.get("/users/")
def list_users(
    pagination: dict = Depends(common_pagination),
    token: str = Depends(get_token_header),
):
    return {"pagination": pagination}
```

#### Sub-dependencies (dependency เรียก dependency ได้)

```python
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),       # ← เรียก get_db() ภายใน
):
    return db.get(User, decode_token(token)["sub"])

def require_admin(user: User = Depends(get_current_user)):
    if user.role != "admin":
        raise HTTPException(403, "Admin only")
    return user

# Endpoint ใช้แค่ require_admin → FastAPI ลาก dependency chain ทั้งหมดให้
@app.delete("/users/{user_id}")
def delete_user(user_id: int, admin: User = Depends(require_admin)):
    return {"deleted": user_id, "by": admin.email}
```

### 3.5 APIRouter (แยก Routes เป็นโมดูล)

```python
# routers/users.py
from fastapi import APIRouter, Depends

router = APIRouter(
    prefix="/users",
    tags=["users"],                          # ใช้จัดกลุ่มใน Swagger
    dependencies=[Depends(verify_token)],    # apply ทุก endpoint ใน router นี้
    responses={404: {"description": "Not found"}},
)

@router.get("/")
def list_users():
    return [{"name": "Somchai"}]

@router.get("/{user_id}")
def get_user(user_id: int):
    return {"id": user_id}

# main.py
from routers import users, items, auth
app.include_router(users.router)
app.include_router(items.router, prefix="/api/v1")
app.include_router(auth.router)
```

### 3.6 Error Handling & Exception Handlers

```python
from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse

# Custom exception (ใช้ใน service layer แทน HTTPException → reusable)
class ItemNotFoundError(Exception):
    def __init__(self, item_id: int):
        self.item_id = item_id

@app.exception_handler(ItemNotFoundError)
async def item_not_found_handler(request: Request, exc: ItemNotFoundError):
    return JSONResponse(
        status_code=404,
        content={
            "code": "ITEM_NOT_FOUND",
            "message": f"Item {exc.item_id} not found",
            "path": str(request.url),
        },
    )

# Validation error → ให้ดูสวยขึ้น
from fastapi.exceptions import RequestValidationError
@app.exception_handler(RequestValidationError)
async def validation_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={"code": "VALIDATION_ERROR", "errors": exc.errors()},
    )
```

### 3.7 Middleware & CORS

> 💬 **Middleware คือ:** "ทางผ่านของ request" — ทุก request จะวิ่งผ่านนี่ก่อน/หลัง endpoint เช่น เช็ค auth, logging, CORS, gzip

```python
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
import time

# CORS — อนุญาตให้ frontend ที่ origin ต่างกันเรียก API ได้
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://app.example.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Gzip — บีบอัด response ให้เล็กลง
app.add_middleware(GZipMiddleware, minimum_size=1000)

# Custom middleware — บันทึก response time
class TimingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start = time.perf_counter()
        response = await call_next(request)
        elapsed = (time.perf_counter() - start) * 1000
        response.headers["X-Process-Time-MS"] = f"{elapsed:.2f}"
        return response

app.add_middleware(TimingMiddleware)
```

### 3.8 Lifespan Events (Startup / Shutdown)

> 💬 **คือ:** โค้ดที่รัน "ตอน app เริ่ม" และ "ตอน app ปิด" — เช่น เปิด DB pool, เชื่อม Redis, ปิด connection

```python
from contextlib import asynccontextmanager
from fastapi import FastAPI

@asynccontextmanager
async def lifespan(app: FastAPI):
    # === STARTUP ===
    print("🚀 Starting up...")
    app.state.redis = await create_redis_pool()
    app.state.http = httpx.AsyncClient()
    yield
    # === SHUTDOWN ===
    print("👋 Shutting down...")
    await app.state.redis.close()
    await app.state.http.aclose()

app = FastAPI(lifespan=lifespan)

@app.get("/")
async def root(request: Request):
    redis = request.app.state.redis
    return {"counter": await redis.incr("hits")}
```

### 3.9 File Upload & Streaming Response

```python
from fastapi import File, UploadFile, HTTPException
from fastapi.responses import StreamingResponse
from pathlib import Path

@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    if file.size and file.size > 10 * 1024 * 1024:    # 10 MB limit
        raise HTTPException(413, "ไฟล์ใหญ่เกิน 10MB")

    if not file.content_type.startswith("image/"):
        raise HTTPException(415, "รับเฉพาะรูปภาพ")

    dest = Path("uploads") / file.filename
    dest.parent.mkdir(exist_ok=True)
    with dest.open("wb") as f:
        while chunk := await file.read(1024 * 1024):   # อ่านทีละ 1MB
            f.write(chunk)
    return {"saved": str(dest), "size": dest.stat().st_size}

@app.get("/download/{filename}")
def download(filename: str):
    path = Path("uploads") / filename
    if not path.exists():
        raise HTTPException(404)

    def file_iterator():
        with path.open("rb") as f:
            yield from f
    return StreamingResponse(file_iterator(), media_type="application/octet-stream",
                             headers={"Content-Disposition": f"attachment; filename={filename}"})
```

> 💬 **StreamingResponse คือ:** ส่งไฟล์ทีละชิ้น — ไฟล์ใหญ่ 5GB ไม่ต้องโหลดเข้า memory ทั้งก้อน

### 3.10 WebSocket (Real-time)

```python
from fastapi import WebSocket, WebSocketDisconnect

class ConnectionManager:
    def __init__(self):
        self.active: list[WebSocket] = []

    async def connect(self, ws: WebSocket):
        await ws.accept()
        self.active.append(ws)

    def disconnect(self, ws: WebSocket):
        self.active.remove(ws)

    async def broadcast(self, message: str):
        for ws in self.active:
            await ws.send_text(message)

manager = ConnectionManager()

@app.websocket("/ws/{username}")
async def chat(websocket: WebSocket, username: str):
    await manager.connect(websocket)
    await manager.broadcast(f"👋 {username} joined")
    try:
        while True:
            msg = await websocket.receive_text()
            await manager.broadcast(f"{username}: {msg}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"😢 {username} left")
```

> 💬 **WebSocket คือ:** "สายโทรศัพท์เปิดค้างไว้" — server กับ client ส่งข้อความถึงกันได้ตลอด (ต่างจาก HTTP ที่ต้องถามใหม่ทุกครั้ง)

### 3.11 Background Tasks (งานทำหลัง response แล้ว)

```python
from fastapi import BackgroundTasks

def write_log(message: str):
    with open("log.txt", "a") as f:
        f.write(f"{message}\n")

@app.post("/orders")
async def create_order(order: OrderCreate, bg: BackgroundTasks):
    order_id = save_order(order)
    bg.add_task(write_log, f"Order {order_id} created")
    bg.add_task(send_confirmation_email, order.email)
    return {"id": order_id}    # ↑ response ส่งกลับทันที, งานพื้นหลังรันต่อ
```

---

## 4. SQLAlchemy

> 💬 **SQLAlchemy คือ:** "ล่ามแปลภาษา" ระหว่าง Python ↔ SQL — แทนที่จะเขียน SQL ดิบ ๆ ใช้ Python object แทน
>
> SQLAlchemy 2.0+ ใช้ syntax ใหม่ที่ **type-safe** — IDE auto-complete ได้, mypy เช็คได้

### 4.1 Engine, Session, Base

```python
# database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

DATABASE_URL = "postgresql+psycopg://user:pass@localhost/mydb"
# psycopg3 = ใหม่กว่า psycopg2, async-native

engine = create_engine(
    DATABASE_URL,
    echo=True,                 # log SQL ทุก query (debug only)
    pool_size=10,              # connection pool size
    max_overflow=20,           # extra conns if pool full
    pool_pre_ping=True,        # ping ก่อนใช้ → กัน stale conn
)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

class Base(DeclarativeBase):
    pass
```

| ศัพท์           | ภาษาชาวบ้าน                                            |
| --------------- | ------------------------------------------------------ |
| **Engine**      | "ตู้สวิตช์ไฟ" — จุดเชื่อมเข้า DB                       |
| **Connection**  | "สายไฟ" — 1 ช่องคุยกับ DB                              |
| **Pool**        | "ปลั๊กพ่วง" — มีหลายสายไว้ใช้ ไม่ต้องเสียบใหม่ทุกครั้ง |
| **Session**     | "พนักงาน 1 คน" — รับ-ส่งของกับ DB ใน 1 transaction     |
| **Transaction** | "1 รอบ" — ทำทุกอย่างหรือไม่ทำเลย (atomic)              |

### 4.2 Models (Style 2.0 — Type-safe)

```python
# models.py
from datetime import datetime
from sqlalchemy import String, ForeignKey, DateTime, Integer, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database import Base

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(120), unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String(255))
    full_name: Mapped[str | None] = mapped_column(String(100))
    is_active: Mapped[bool] = mapped_column(default=True)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        server_default=func.now(),
        onupdate=func.now(),     # อัพเดทอัตโนมัติทุกครั้งที่ row เปลี่ยน
    )

    # relationship
    posts: Mapped[list["Post"]] = relationship(
        back_populates="author",
        cascade="all, delete-orphan",     # ลบ user → ลบ posts ตาม
        lazy="selectin",                  # eager load (กัน N+1)
    )

    def __repr__(self) -> str:
        return f"<User {self.id}: {self.email}>"

class Post(Base):
    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(200))
    content: Mapped[str]
    author_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())

    author: Mapped["User"] = relationship(back_populates="posts")
```

> 💬 **Mapped[...] คือ:** ป้ายบอก type — IDE และ mypy รู้ว่า `user.id` คือ `int`, `user.posts` คือ `list[Post]`

#### Cascade options (ลบ parent → ลูกตามไหม)

| Cascade           | ความหมาย                | เมื่อใช้            |
| ----------------- | ----------------------- | ------------------- |
| `"all"`           | apply ทุก cascade       | default ทั่วไป      |
| `"delete-orphan"` | ลบลูกที่หลุดจากแม่      | parent-child strict |
| `"save-update"`   | save แม่ → save ลูกด้วย | most common         |
| `"merge"`         | merge แม่ → merge ลูก   | session sync        |

### 4.3 CRUD Operations

```python
from sqlalchemy import select, update, delete
from sqlalchemy.orm import Session

# CREATE
def create_user(db: Session, email: str, password: str) -> User:
    user = User(email=email, hashed_password=password)
    db.add(user)
    db.commit()
    db.refresh(user)         # อ่านค่า id, created_at ที่ DB ใส่กลับมา
    return user

# READ — by primary key (fast path)
def get_user(db: Session, user_id: int) -> User | None:
    return db.get(User, user_id)

# READ — with filter
def get_user_by_email(db: Session, email: str) -> User | None:
    stmt = select(User).where(User.email == email)
    return db.scalar(stmt)

# READ — list with pagination
def list_users(db: Session, skip: int = 0, limit: int = 100) -> list[User]:
    stmt = select(User).order_by(User.created_at.desc()).offset(skip).limit(limit)
    return list(db.scalars(stmt).all())

# UPDATE — load + modify + commit
def update_user_email(db: Session, user_id: int, new_email: str) -> User | None:
    user = db.get(User, user_id)
    if user:
        user.email = new_email
        db.commit()
        db.refresh(user)
    return user

# UPDATE — bulk (เร็วกว่าเมื่อแก้หลาย row)
def deactivate_old_users(db: Session, days: int):
    cutoff = datetime.now() - timedelta(days=days)
    stmt = update(User).where(User.created_at < cutoff).values(is_active=False)
    result = db.execute(stmt)
    db.commit()
    return result.rowcount

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
        # commit ที่นี่ก็ได้ ถ้าอยากให้ auto-commit
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()

# routers/users.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from deps import get_db
from models import User
from schemas import UserCreate, UserRead

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/{user_id}", response_model=UserRead)
def read_user(user_id: int, db: Session = Depends(get_db)):
    user = db.get(User, user_id)
    if not user:
        raise HTTPException(404, "User not found")
    return user

@router.post("/", response_model=UserRead, status_code=201)
def create_user(data: UserCreate, db: Session = Depends(get_db)):
    if db.scalar(select(User).where(User.email == data.email)):
        raise HTTPException(409, "Email taken")
    user = User(email=data.email, hashed_password=hash_password(data.password))
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
```

### 4.5 Joins & Eager Loading (กันปัญหา N+1)

> 💬 **N+1 problem คือ:** ดึง 10 users แล้ววน loop ดึง posts ของแต่ละคน → 1 query หา users + 10 query หา posts = **11 queries** แทนที่จะใช้ 1 query เท่านั้น

```python
from sqlalchemy.orm import selectinload, joinedload

# ❌ BAD — N+1 problem
users = db.scalars(select(User)).all()
for u in users:
    print(u.posts)         # ← query เพิ่ม 1 รอบต่อ user!

# ✅ GOOD — eager load ด้วย selectinload (2 query รวม)
stmt = select(User).options(selectinload(User.posts))
users = db.scalars(stmt).all()
for u in users:
    print(u.posts)         # ← ไม่ query เพิ่ม

# ✅ GOOD — joinedload (1 query รวม, LEFT JOIN)
stmt = select(User).options(joinedload(User.posts))

# JOIN แบบ explicit
stmt = (
    select(User, Post)
    .join(Post, Post.author_id == User.id)
    .where(Post.title.like("%FastAPI%"))
)
for user, post in db.execute(stmt):
    print(user.email, post.title)
```

| Loading strategy          | กี่ query | เหมาะกับ                           |
| ------------------------- | --------- | ---------------------------------- |
| `selectinload` ⭐         | 2         | one-to-many ทั่วไป                 |
| `joinedload`              | 1         | one-to-one, many-to-one            |
| `subqueryload`            | 2         | legacy (เก่ากว่า selectinload)     |
| `lazy="select"` (default) | N+1       | dev เริ่มต้น (ใช้แค่ตอน prototype) |

### 4.6 Aggregations & Group By

```python
from sqlalchemy import func, desc

# COUNT
stmt = select(func.count()).select_from(User)
total = db.scalar(stmt)

# GROUP BY
stmt = (
    select(User.id, User.email, func.count(Post.id).label("post_count"))
    .outerjoin(Post)
    .group_by(User.id)
    .order_by(desc("post_count"))
    .limit(10)
)
for row in db.execute(stmt):
    print(row.email, row.post_count)

# SUM, AVG, MIN, MAX
stmt = select(
    func.sum(Order.total).label("revenue"),
    func.avg(Order.total).label("avg_order"),
    func.count().label("orders"),
).where(Order.created_at >= start_date)
result = db.execute(stmt).one()
```

### 4.7 Hybrid Properties (ใช้ได้ทั้ง Python และ SQL)

```python
from sqlalchemy.ext.hybrid import hybrid_property

class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str]
    last_name: Mapped[str]

    @hybrid_property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"

    @full_name.expression
    @classmethod
    def full_name(cls):
        return func.concat(cls.first_name, " ", cls.last_name)

# ใช้ใน Python
user.full_name                    # "Somchai Jaidee"

# ใช้ใน query → กลายเป็น SQL CONCAT
stmt = select(User).where(User.full_name.like("Som%"))
```

### 4.8 Async SQLAlchemy (สำหรับ High Performance)

> 💬 **Async คือ:** "ทำหลายงานซ้อนได้" — รอ DB ตอบขณะอื่นทำงานอื่น เหมาะกับ web app ที่มี traffic สูง

```python
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

# ใช้ asyncpg driver
engine = create_async_engine("postgresql+asyncpg://user:pass@localhost/db")
AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False)

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session

@router.get("/{user_id}", response_model=UserRead)
async def read_user(user_id: int, db: AsyncSession = Depends(get_db)):
    user = await db.get(User, user_id)
    if not user:
        raise HTTPException(404)
    return user

@router.get("/", response_model=list[UserRead])
async def list_users(db: AsyncSession = Depends(get_db)):
    stmt = select(User).options(selectinload(User.posts))
    result = await db.scalars(stmt)
    return list(result.all())
```

### 4.9 Raw SQL (เมื่อ ORM ทำไม่ได้)

```python
from sqlalchemy import text

# Read-only query
stmt = text("SELECT id, email FROM users WHERE created_at > :since")
rows = db.execute(stmt, {"since": "2026-01-01"}).all()

# Stored procedure / complex CTE
stmt = text("""
    WITH active_users AS (
        SELECT id FROM users WHERE is_active = TRUE
    )
    SELECT u.email, COUNT(p.id) AS posts
    FROM active_users u
    LEFT JOIN posts p ON p.author_id = u.id
    GROUP BY u.id, u.email
""")
result = db.execute(stmt).mappings().all()
```

> ⚠️ **ห้ามใช้ f-string ใส่ค่าใน SQL** → SQL injection!
> ✅ ใช้ `:param_name` กับ dict parameter เสมอ

---

## 5. Alembic

> 💬 **Alembic คือ:** "สมุดบันทึก + แผนการรีโนเวท DB" — เปลี่ยน schema ทีไรเขียน migration script เก็บไว้ ทุกที่ deploy ใช้ script ชุดเดียวกัน

### 5.1 ตั้งค่า

```bash
alembic init alembic
```

แก้ `alembic/env.py`:

```python
from database import Base
from models import *      # import models ทั้งหมด — ให้ alembic เห็น
target_metadata = Base.metadata

# Read URL จาก env
import os
config.set_main_option("sqlalchemy.url", os.environ["DATABASE_URL"])
```

### 5.2 คำสั่งที่ใช้บ่อย

```bash
# สร้าง migration อัตโนมัติจาก model changes
alembic revision --autogenerate -m "create users table"

# สร้าง migration เปล่า (เพื่อเขียน data migration เอง)
alembic revision -m "backfill user.full_name"

# Apply migration ขึ้นล่าสุด
alembic upgrade head

# Apply ไปจุดใดจุดหนึ่ง
alembic upgrade ae1027a6acf

# Apply เพิ่ม 1 step
alembic upgrade +1

# ย้อนกลับ 1 step
alembic downgrade -1

# ดูประวัติ
alembic history
alembic current

# Generate SQL ออกมาดู (ไม่รัน)
alembic upgrade head --sql
```

### 5.3 Migration ตัวอย่าง

```python
# alembic/versions/abc123_add_user_table.py
"""add user table

Revision ID: abc123
Revises:
Create Date: 2026-05-14
"""
from alembic import op
import sqlalchemy as sa

revision = "abc123"
down_revision = None

def upgrade():
    op.create_table(
        "users",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("email", sa.String(120), unique=True, nullable=False),
        sa.Column("created_at", sa.DateTime, server_default=sa.func.now()),
    )
    op.create_index("ix_users_email", "users", ["email"])

def downgrade():
    op.drop_index("ix_users_email", "users")
    op.drop_table("users")
```

### 5.4 Data Migration (ย้ายข้อมูล ไม่ใช่ schema)

```python
def upgrade():
    # 1. Add column
    op.add_column("users", sa.Column("full_name", sa.String(200)))

    # 2. Backfill data
    conn = op.get_bind()
    conn.execute(sa.text("""
        UPDATE users
        SET full_name = email
        WHERE full_name IS NULL
    """))

    # 3. Make column NOT NULL
    op.alter_column("users", "full_name", nullable=False)
```

### 5.5 Pitfalls

| Pitfall                     | คำอธิบาย                                          |
| --------------------------- | ------------------------------------------------- |
| Autogen ตรวจไม่ครบ          | constraint, check, enum, partial index → เขียนเอง |
| ลืม import models ใน env.py | autogen ไม่เห็น = ไม่ generate                    |
| Drop column บน prod ทันที   | ✅ พักไว้ใน revision หลัง deploy code ใหม่แล้ว    |
| Conflict เมื่อ merge branch | ใช้ `alembic merge heads -m "merge"`              |

---

## 6. Authentication & Security

### 6.1 Password Hashing

> 💬 **Hash คือ:** "เครื่องปั่นที่ปั่นกลับไม่ได้" — รหัส "1234" → "$argon2id$v=19$..." ใครเห็นใน DB ก็ใช้ไม่ได้

#### ตัวเลือก: argon2 (แนะนำ 2026) > bcrypt > scrypt

```python
# วิธีที่ 1 — argon2-cffi (OWASP recommended 2024+)
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

ph = PasswordHasher()

def hash_password(plain: str) -> str:
    return ph.hash(plain)

def verify_password(plain: str, hashed: str) -> bool:
    try:
        ph.verify(hashed, plain)
        return True
    except VerifyMismatchError:
        return False
```

```python
# วิธีที่ 2 — passlib (รองรับหลาย algorithm)
from passlib.context import CryptContext

pwd_context = CryptContext(
    schemes=["argon2", "bcrypt"],   # argon2 = preferred, bcrypt = fallback for old hashes
    deprecated="auto",
)

def hash_password(plain: str) -> str:
    return pwd_context.hash(plain)

def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)

# Auto re-hash ถ้า scheme deprecated
def verify_and_update(plain: str, hashed: str) -> tuple[bool, str | None]:
    ok, new_hash = pwd_context.verify_and_update(plain, hashed)
    return ok, new_hash    # new_hash != None → ควร save แทนของเก่า
```

### 6.2 JWT Token

> 💬 **JWT คือ:** "บัตรผ่านที่ปลอมไม่ได้" — server เซ็นชื่อบนบัตร client ถือไว้ ทุกครั้งที่ขอเข้าระบบ server ตรวจลายเซ็นเอง ไม่ต้องเก็บ session

```python
from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError
from pydantic import BaseModel

SECRET_KEY = "super-secret-256-bit-key-from-env"
ALGORITHM = "HS256"
ACCESS_EXPIRE_MIN = 15            # access token สั้นๆ
REFRESH_EXPIRE_DAYS = 30          # refresh token นานหน่อย

class TokenData(BaseModel):
    sub: str        # user id (subject)
    exp: int        # expiry timestamp
    type: str       # "access" หรือ "refresh"

def create_access_token(user_id: int) -> str:
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_EXPIRE_MIN)
    payload = {"sub": str(user_id), "exp": expire, "type": "access"}
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def create_refresh_token(user_id: int) -> str:
    expire = datetime.now(timezone.utc) + timedelta(days=REFRESH_EXPIRE_DAYS)
    payload = {"sub": str(user_id), "exp": expire, "type": "refresh"}
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def decode_token(token: str, expected_type: str = "access") -> dict | None:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        if payload.get("type") != expected_type:
            return None
        return payload
    except JWTError:
        return None
```

### 6.3 OAuth2 + FastAPI

```python
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

@app.post("/login")
def login(
    form: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    user = db.scalar(select(User).where(User.email == form.username))
    if not user or not verify_password(form.password, user.hashed_password):
        raise HTTPException(401, "Wrong credentials")

    return {
        "access_token": create_access_token(user.id),
        "refresh_token": create_refresh_token(user.id),
        "token_type": "bearer",
    }

@app.post("/refresh")
def refresh(refresh_token: str, db: Session = Depends(get_db)):
    payload = decode_token(refresh_token, expected_type="refresh")
    if not payload:
        raise HTTPException(401, "Invalid refresh token")
    user_id = int(payload["sub"])
    return {"access_token": create_access_token(user_id), "token_type": "bearer"}

def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> User:
    payload = decode_token(token)
    if not payload:
        raise HTTPException(401, "Invalid token", headers={"WWW-Authenticate": "Bearer"})
    user = db.get(User, int(payload["sub"]))
    if not user or not user.is_active:
        raise HTTPException(401, "User inactive")
    return user

@app.get("/me", response_model=UserRead)
def me(user: User = Depends(get_current_user)):
    return user
```

### 6.4 Role-Based Access Control (RBAC)

```python
from enum import StrEnum
from functools import wraps

class Role(StrEnum):
    ADMIN = "admin"
    EDITOR = "editor"
    VIEWER = "viewer"

def require_roles(*allowed: Role):
    def dep(user: User = Depends(get_current_user)) -> User:
        if user.role not in allowed:
            raise HTTPException(403, f"Need role: {[r.value for r in allowed]}")
        return user
    return dep

@app.delete("/posts/{post_id}")
def delete_post(
    post_id: int,
    user: User = Depends(require_roles(Role.ADMIN, Role.EDITOR)),
):
    ...
```

### 6.5 Field-Level Encryption (PDPA-sensitive)

```python
from cryptography.fernet import Fernet

# ตั้งครั้งเดียว เก็บ key ใน env
KEY = Fernet(settings.encryption_key.encode())

def encrypt(plain: str) -> str:
    return KEY.encrypt(plain.encode()).decode()

def decrypt(cipher: str) -> str:
    return KEY.decrypt(cipher.encode()).decode()

class Citizen(Base):
    __tablename__ = "citizens"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    encrypted_id_card: Mapped[str]    # เก็บ Fernet-encrypted

# ใช้
citizen.encrypted_id_card = encrypt("1100123456789")
print(decrypt(citizen.encrypted_id_card))
```

### 6.6 Rate Limiting

```python
# ใช้ slowapi
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

@app.post("/login")
@limiter.limit("5/minute")    # 5 attempts/IP/นาที — กัน brute force
def login(...): ...
```

---

## 7. Async, HTTP Client & Background Tasks

### 7.1 `httpx` – Async HTTP Client (แทน `requests`)

> 💬 **httpx คือ:** "คนวิ่งไปซื้อของ" — เหมือน `requests` แต่ทำหลายงานพร้อมกันได้ (async)

```python
import httpx

# Sync (เหมือน requests)
def fetch_sync():
    r = httpx.get("https://api.example.com/users")
    r.raise_for_status()
    return r.json()

# Async — ใช้ใน FastAPI
async def fetch_async():
    async with httpx.AsyncClient(timeout=10) as client:
        r = await client.get("https://api.example.com/users")
        r.raise_for_status()
        return r.json()

# ส่งหลาย request พร้อมกัน (concurrent)
import asyncio

async def fetch_many(urls: list[str]):
    async with httpx.AsyncClient() as client:
        results = await asyncio.gather(*[client.get(u) for u in urls])
        return [r.json() for r in results]

# Reuse client (สำคัญ — connection pool)
client = httpx.AsyncClient(
    base_url="https://api.example.com",
    headers={"Authorization": "Bearer xxx"},
    timeout=httpx.Timeout(connect=5, read=10),
    limits=httpx.Limits(max_connections=100, max_keepalive_connections=20),
)
# ปิดตอน shutdown:  await client.aclose()
```

### 7.2 Retry ด้วย `tenacity`

> 💬 **Retry คือ:** "ลองใหม่ถ้าพลาด" — network อาจ flap หรือ remote API ช้า → retry 3 ครั้งก่อน fail

```python
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

@retry(
    stop=stop_after_attempt(3),                    # ลองสูงสุด 3 ครั้ง
    wait=wait_exponential(multiplier=1, min=2, max=10),    # รอ 2, 4, 8 วินาที
    retry=retry_if_exception_type(httpx.HTTPError),
    reraise=True,
)
async def fetch_with_retry(url: str):
    async with httpx.AsyncClient() as client:
        r = await client.get(url, timeout=5)
        r.raise_for_status()
        return r.json()
```

### 7.3 Concurrent Tasks ด้วย `asyncio`

```python
import asyncio

# ทำพร้อมกัน — รอทั้งหมดเสร็จ
async def main():
    results = await asyncio.gather(
        fetch_user(1),
        fetch_posts(1),
        fetch_comments(1),
    )
    user, posts, comments = results

# จำกัด concurrency
async def fetch_all_limited(urls: list[str], max_concurrent: int = 10):
    semaphore = asyncio.Semaphore(max_concurrent)
    async def fetch_one(url):
        async with semaphore:
            return await fetch_with_retry(url)
    return await asyncio.gather(*[fetch_one(u) for u in urls])

# Timeout overall
async def main():
    try:
        result = await asyncio.wait_for(fetch_slow(), timeout=5)
    except asyncio.TimeoutError:
        print("เกิน 5 วิ ยังไม่เสร็จ")
```

| Pattern               | ภาษาชาวบ้าน                        | ตัวอย่าง          |
| --------------------- | ---------------------------------- | ----------------- |
| `asyncio.gather`      | "ส่ง 3 คนไปคนละทาง รอกลับพร้อมกัน" | fetch จากหลาย API |
| `asyncio.create_task` | "ส่งคนไปทำ ไม่ต้องรอ"              | fire-and-forget   |
| `asyncio.wait_for`    | "ตั้งนาฬิกาจับเวลา"                | timeout           |
| `Semaphore(N)`        | "บัตรคิว N ใบ"                     | limit concurrency |

### 7.4 BackgroundTasks (ในตัว FastAPI)

```python
from fastapi import BackgroundTasks

def send_email(to: str, subject: str):
    print(f"Sending email to {to}: {subject}")

@app.post("/notify")
def notify(email: str, bg: BackgroundTasks):
    bg.add_task(send_email, email, "Welcome!")
    return {"status": "queued"}
```

> ⚠️ BackgroundTasks รันใน process เดียวกับ web → ถ้า server restart งานหาย, เหมาะกับงานสั้นๆ เท่านั้น

### 7.5 งานหนัก → Celery / arq / TaskIQ

```python
# arq (Redis-based, async — แนะนำสำหรับ FastAPI)
from arq import create_pool
from arq.connections import RedisSettings

async def heavy_job(ctx, x, y):
    await asyncio.sleep(10)
    return x + y

class WorkerSettings:
    functions = [heavy_job]
    redis_settings = RedisSettings(host="redis", port=6379)
    max_jobs = 10

# ส่งงาน
async def enqueue():
    redis = await create_pool(RedisSettings())
    job = await redis.enqueue_job("heavy_job", 1, 2)
    print(job.job_id)
```

| Library           | สไตล์                 | ภาษาชาวบ้าน                           |
| ----------------- | --------------------- | ------------------------------------- |
| `BackgroundTasks` | in-process            | "ทำหลัง response ส่งเสร็จ"            |
| `arq`             | Redis + async         | "ส่งใบงานเข้าตู้ Redis worker หยิบทำ" |
| `Celery`          | Redis/RabbitMQ + sync | "มาตรฐาน Python แต่ sync, ใหญ่กว่า"   |
| `TaskIQ`          | คล้าย arq + Pydantic  | "ใหม่กว่า, สวยกว่า"                   |
| `APScheduler`     | cron-like             | "ตั้งเวลารัน เช่น 00:00 ทุกวัน"       |

### 7.6 Scheduled Jobs ด้วย APScheduler

```python
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

scheduler = AsyncIOScheduler()

async def annual_evaluation():
    print("รวมคะแนน vendor ประจำปี")

# ทุก 31 ธ.ค. เที่ยงคืน
scheduler.add_job(annual_evaluation, CronTrigger(month=12, day=31, hour=0, minute=0))

# ทุก 5 นาที
scheduler.add_job(check_pending_pos, "interval", minutes=5)

# Start ใน lifespan
@asynccontextmanager
async def lifespan(app):
    scheduler.start()
    yield
    scheduler.shutdown()
```

---

## 8. Logging, Monitoring & Error Tracking

### 8.1 `loguru` – Logging ที่ใช้ง่าย

> 💬 **Loguru คือ:** "สมุดจดเหตุการณ์อัตโนมัติ" — เขียน 1 บรรทัด ได้ทั้งสี + format + rotate file + JSON ส่งไปไหนก็ได้ (ดีกว่า `logging` ของ stdlib)

```python
from loguru import logger
import sys

# ตั้งครั้งเดียวที่ startup
logger.remove()    # ลบ default handler

# Console — มีสี
logger.add(sys.stderr, format="<green>{time}</green> <level>{level}</level> {message}",
           level="INFO", colorize=True)

# File — rotate ทุก 100MB, เก็บ 30 วัน
logger.add("logs/app_{time}.log", rotation="100 MB", retention="30 days",
           compression="gz", level="DEBUG")

# JSON ส่งไป log aggregator (Loki/Datadog)
logger.add("logs/app.json", serialize=True, level="INFO")

# ใช้
logger.debug("debug info")
logger.info("user {user_id} logged in", user_id=123)
logger.warning("disk usage {pct}%", pct=87)
logger.error("payment failed")
logger.exception("uncaught")     # auto-include traceback

# Context bind
log = logger.bind(request_id="abc-123")
log.info("processing")    # → message รวม request_id ทุกครั้ง

# Decorator
@logger.catch                    # auto log uncaught exception
def risky(x):
    return 1 / x
```

### 8.2 Structured Logging กับ Request ID

```python
from contextvars import ContextVar
import uuid

request_id_var: ContextVar[str] = ContextVar("request_id", default="")

class RequestIdMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        req_id = request.headers.get("X-Request-ID") or str(uuid.uuid4())
        token = request_id_var.set(req_id)
        try:
            with logger.contextualize(request_id=req_id):
                response = await call_next(request)
            response.headers["X-Request-ID"] = req_id
            return response
        finally:
            request_id_var.reset(token)
```

### 8.3 Error Tracking ด้วย Sentry

```python
import sentry_sdk
from sentry_sdk.integrations.fastapi import FastApiIntegration
from sentry_sdk.integrations.sqlalchemy import SqlalchemyIntegration

sentry_sdk.init(
    dsn="https://xxx@sentry.io/yyy",
    environment=settings.environment,    # prod / staging
    traces_sample_rate=0.1,              # 10% performance trace
    profiles_sample_rate=0.1,
    integrations=[FastApiIntegration(), SqlalchemyIntegration()],
    send_default_pii=False,              # PDPA-safe
)

# ส่ง error เอง
sentry_sdk.capture_exception(e)
sentry_sdk.capture_message("Suspicious activity", level="warning")
```

### 8.4 Metrics ด้วย Prometheus

```python
from prometheus_fastapi_instrumentator import Instrumentator

# ใส่ /metrics endpoint อัตโนมัติ
Instrumentator().instrument(app).expose(app)
# → GET /metrics → Prometheus scrape → Grafana visualize
```

---

## 9. Caching & Performance (Redis)

> 💬 **Cache คือ:** "ตู้เย็นเก็บของที่ใช้บ่อย" — แทนที่จะทำใหม่ทุกครั้ง เก็บไว้ในตู้ ดึงมาใช้ซ้ำเร็วกว่า
>
> **Redis คือ:** in-memory database — เก็บใน RAM → เร็วกว่า disk-based DB **100-1000 เท่า**

### 9.1 ติดตั้ง

```bash
uv add redis        # มี async client built-in (ตั้งแต่ v4.2)
```

### 9.2 Basic Operations

```python
import redis.asyncio as redis

# Connection pool (reuse, แนะนำ)
r = redis.from_url("redis://localhost:6379/0", decode_responses=True)

async def demo():
    # String
    await r.set("user:1:name", "Somchai", ex=3600)    # expire 1 hour
    name = await r.get("user:1:name")

    # Counter
    hits = await r.incr("page:home:hits")

    # Hash (เหมือน dict)
    await r.hset("user:1", mapping={"name": "Somchai", "age": "30"})
    data = await r.hgetall("user:1")

    # List (queue)
    await r.rpush("queue:emails", "user@example.com")
    job = await r.lpop("queue:emails")

    # Set
    await r.sadd("tags:post:1", "python", "fastapi")
    tags = await r.smembers("tags:post:1")

    # Sorted set (leaderboard)
    await r.zadd("scores", {"alice": 100, "bob": 200})
    top = await r.zrevrange("scores", 0, 9, withscores=True)
```

### 9.3 Cache Pattern (Cache-Aside)

```python
import json
from functools import wraps

def cache(ttl: int = 300):
    def deco(fn):
        @wraps(fn)
        async def wrapper(*args, **kwargs):
            key = f"{fn.__name__}:{args}:{kwargs}"
            cached = await r.get(key)
            if cached:
                return json.loads(cached)
            result = await fn(*args, **kwargs)
            await r.set(key, json.dumps(result), ex=ttl)
            return result
        return wrapper
    return deco

@cache(ttl=600)
async def get_top_vendors():
    # query DB ที่ช้า — cache ไว้ 10 นาที
    return await heavy_db_query()

# Cache invalidation เมื่อ data เปลี่ยน
async def update_vendor(vendor_id: int, data):
    await db_update(vendor_id, data)
    await r.delete(f"vendor:{vendor_id}", "get_top_vendors:():{}")
```

### 9.4 Distributed Lock

```python
from redis.asyncio.lock import Lock

async def safe_decrement(key: str, amount: int):
    async with r.lock(f"lock:{key}", timeout=5):
        current = int(await r.get(key) or 0)
        await r.set(key, current - amount)
```

### 9.5 Pub/Sub (Real-time)

```python
# Publisher
await r.publish("notifications", json.dumps({"to": "user:1", "msg": "Hi"}))

# Subscriber
async def listen():
    pubsub = r.pubsub()
    await pubsub.subscribe("notifications")
    async for message in pubsub.listen():
        if message["type"] == "message":
            data = json.loads(message["data"])
            print("Got:", data)
```

---

## 10. File Handling, Email, PDF

### 10.1 Image Processing ด้วย `Pillow`

> 💬 **Pillow คือ:** "Photoshop เวอร์ชัน Python" — resize, crop, แปลง format, ใส่ลายน้ำ

```python
from PIL import Image, ImageOps

# Resize + รักษา aspect ratio
img = Image.open("input.jpg")
img.thumbnail((800, 800))
img.save("output.jpg", quality=85, optimize=True)

# Crop ตรงกลางเป็น 1:1
img = ImageOps.fit(img, (500, 500), method=Image.LANCZOS)

# แปลง format
img.save("output.webp", format="WEBP", quality=80)

# ใส่ลายน้ำ
from PIL import ImageDraw, ImageFont
img = Image.open("photo.jpg")
draw = ImageDraw.Draw(img)
font = ImageFont.truetype("Sarabun.ttf", 40)
draw.text((20, 20), "© CMT 2026", font=font, fill="white")
img.save("watermarked.jpg")
```

### 10.2 Email ด้วย `fastapi-mail`

```bash
uv add fastapi-mail
```

```python
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig

conf = ConnectionConfig(
    MAIL_USERNAME="noreply@cmt.co.th",
    MAIL_PASSWORD=settings.smtp_password,
    MAIL_FROM="noreply@cmt.co.th",
    MAIL_SERVER="mail.carpetmaker.co.th",
    MAIL_PORT=587,
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    TEMPLATE_FOLDER="templates/emails",
)

fm = FastMail(conf)

async def send_welcome(to: str, name: str):
    message = MessageSchema(
        subject="ยินดีต้อนรับสู่ CMT",
        recipients=[to],
        template_body={"name": name},
        subtype="html",
    )
    await fm.send_message(message, template_name="welcome.html")

# Jinja2 template
# templates/emails/welcome.html
# <p>สวัสดีคุณ {{ name }} ยินดีต้อนรับ!</p>
```

### 10.3 PDF ด้วย `WeasyPrint`

> 💬 **WeasyPrint คือ:** "เครื่อง print HTML เป็น PDF" — เขียน HTML+CSS ปกติ ออกมาเป็น PDF สวย (รองรับ Thai font)

```python
from weasyprint import HTML, CSS
from jinja2 import Environment, FileSystemLoader

env = Environment(loader=FileSystemLoader("templates/forms"))

def render_purchase_order(po_data: dict) -> bytes:
    template = env.get_template("fr_sc_017.html")
    html_content = template.render(**po_data)
    pdf = HTML(string=html_content, base_url=".").write_pdf(
        stylesheets=[CSS(filename="static/css/print.css")]
    )
    return pdf

@app.get("/po/{po_id}/pdf")
def download_po(po_id: int, db: Session = Depends(get_db)):
    po = db.get(PurchaseOrder, po_id)
    pdf_bytes = render_purchase_order(po.__dict__)
    return Response(
        pdf_bytes,
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename=PO_{po_id}.pdf"},
    )
```

### 10.4 Excel ด้วย `openpyxl`

```python
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill

def export_vendors(vendors: list[Vendor]) -> bytes:
    wb = Workbook()
    ws = wb.active
    ws.title = "Vendors"

    # Header
    headers = ["ID", "Name", "Grade", "Status"]
    ws.append(headers)
    for cell in ws[1]:
        cell.font = Font(bold=True, color="FFFFFF")
        cell.fill = PatternFill("solid", fgColor="1e3a8a")

    # Data
    for v in vendors:
        ws.append([v.id, v.name, v.grade, v.status])

    # Auto-width
    for col in ws.columns:
        max_len = max(len(str(c.value or "")) for c in col)
        ws.column_dimensions[col[0].column_letter].width = max_len + 2

    from io import BytesIO
    buf = BytesIO()
    wb.save(buf)
    return buf.getvalue()
```

### 10.5 CSV — built-in

```python
import csv
from io import StringIO

def to_csv(rows: list[dict]) -> str:
    buf = StringIO()
    writer = csv.DictWriter(buf, fieldnames=rows[0].keys())
    writer.writeheader()
    writer.writerows(rows)
    return buf.getvalue()
```

### 10.6 File storage — Local vs S3/MinIO

```python
# Local
from pathlib import Path

def save_local(file: UploadFile) -> Path:
    dest = Path("uploads") / file.filename
    dest.write_bytes(file.file.read())
    return dest

# S3 / MinIO
import boto3

s3 = boto3.client(
    "s3",
    endpoint_url="http://minio:9000",
    aws_access_key_id=settings.s3_key,
    aws_secret_access_key=settings.s3_secret,
)

def upload_to_s3(file: UploadFile, bucket: str, key: str) -> str:
    s3.upload_fileobj(file.file, bucket, key)
    return f"s3://{bucket}/{key}"

def presigned_url(bucket: str, key: str, expires: int = 3600) -> str:
    return s3.generate_presigned_url(
        "get_object",
        Params={"Bucket": bucket, "Key": key},
        ExpiresIn=expires,
    )
```

---

## 11. CLI Tools & Date/Time

### 11.1 `typer` – สร้าง CLI สวยๆ

> 💬 **Typer คือ:** "FastAPI เวอร์ชัน CLI" — เขียน function ธรรมดา ได้ CLI พร้อม help, validation, type hints

```python
# manage.py
import typer
from rich import print
from rich.table import Table

app = typer.Typer(help="CMT Procurement CLI")

@app.command()
def seed(env: str = "dev"):
    """Seed initial data ลง DB"""
    print(f"[green]Seeding[/green] environment: {env}")

@app.command()
def export_vendors(
    output: typer.FileBinaryWrite,
    grade: str | None = typer.Option(None, help="Filter by grade A/B/C/D"),
    limit: int = typer.Argument(100),
):
    """Export vendors เป็น Excel"""
    vendors = fetch_vendors(grade=grade, limit=limit)
    output.write(export_to_excel(vendors))

@app.command()
def list_users():
    """แสดง users ทั้งหมด"""
    table = Table("ID", "Email", "Role")
    for u in fetch_users():
        table.add_row(str(u.id), u.email, u.role)
    print(table)

if __name__ == "__main__":
    app()
```

```bash
python manage.py seed --env prod
python manage.py export-vendors out.xlsx --grade A 50
python manage.py --help              # auto-generated help
```

### 11.2 `rich` – Pretty Terminal Output

```python
from rich.console import Console
from rich.progress import track
from rich.table import Table
from rich import print as rprint

console = Console()

# สวยๆ
rprint("[bold magenta]Hello[/bold magenta] :rocket:")

# Progress bar
for item in track(range(100), description="Processing..."):
    process(item)

# Table
table = Table(title="Vendors")
table.add_column("ID", style="cyan")
table.add_column("Name", style="green")
table.add_row("V001", "Acme")
console.print(table)

# JSON pretty print
from rich import print_json
print_json(data={"hello": "world"})
```

### 11.3 Date/Time ด้วย `zoneinfo` (built-in, Python 3.9+)

```python
from datetime import datetime, timezone, timedelta
from zoneinfo import ZoneInfo

# UTC (เก็บใน DB เสมอ — best practice)
now_utc = datetime.now(timezone.utc)

# แปลงเป็น Bangkok
bkk = now_utc.astimezone(ZoneInfo("Asia/Bangkok"))
print(bkk.strftime("%d/%m/%Y %H:%M น."))

# พ.ศ.
def to_buddhist_year(dt: datetime) -> str:
    return f"{dt.day:02d}/{dt.month:02d}/{dt.year + 543}"
```

### 11.4 `arrow` / `pendulum` — Date/Time ที่ฉลาดกว่า stdlib

```python
import arrow

a = arrow.now("Asia/Bangkok")
a.format("DD/MM/YYYY HH:mm")           # "14/05/2026 13:45"
a.humanize(locale="th")                 # "เมื่อสักครู่"
a.shift(days=7).date()                  # +7 วัน
a.span("month")                         # tuple (start, end ของเดือน)

# Pendulum — ทำ duration / period ง่ายกว่า
import pendulum
start = pendulum.datetime(2026, 1, 1)
end = pendulum.datetime(2026, 12, 31)
period = end - start
print(period.in_days())                 # 364
print(period.in_words(locale="th"))     # "12 เดือน"
```

---

## 12. Testing

> 📖 **เนื้อหา testing แบบเต็มอยู่ใน Lecture102.md** — ส่วนนี้คือ overview

### 12.1 Pytest พื้นฐาน

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

### 12.2 Fixtures + Test Database

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

### 12.3 Async Tests

```python
import pytest

@pytest.mark.asyncio
async def test_async_endpoint():
    from httpx import AsyncClient, ASGITransport
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        r = await ac.get("/")
        assert r.status_code == 200
```

---

## 13. Project Structure

```
my-project/
├── alembic/                  # migrations
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI instance + middleware + routers
│   ├── config.py            # pydantic-settings
│   ├── database.py          # engine, SessionLocal
│   ├── deps.py              # shared dependencies (get_db, get_current_user)
│   │
│   ├── models/              # SQLAlchemy models (Layer: Persistence)
│   │   ├── __init__.py
│   │   ├── user.py
│   │   └── post.py
│   │
│   ├── schemas/             # Pydantic schemas / DTOs (Layer: API contract)
│   │   ├── user.py
│   │   └── post.py
│   │
│   ├── crud/                # Database operations (Layer: Data Access)
│   │   ├── user.py
│   │   └── post.py
│   │
│   ├── services/            # Business logic (Layer: Domain)
│   │   ├── email.py
│   │   └── scoring.py
│   │
│   ├── routers/             # FastAPI endpoints (Layer: Presentation)
│   │   ├── auth.py
│   │   ├── users.py
│   │   └── posts.py
│   │
│   └── core/                # Cross-cutting: security, exceptions, utils
│       ├── security.py
│       ├── exceptions.py
│       └── logging.py
│
├── tests/
│   ├── conftest.py
│   ├── unit/
│   ├── integration/
│   └── e2e/
│
├── scripts/                 # CLI tools (typer)
│   └── seed.py
│
├── .env
├── .gitignore
├── pyproject.toml
└── README.md
```

### 💡 Pattern: แยก **Model** กับ **Schema** ออกจากกัน

```python
# models/user.py — SQLAlchemy (คุยกับ DB)
class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str]
    hashed_password: Mapped[str]    # ← internal เท่านั้น

# schemas/user.py — Pydantic (คุยกับ client)
class UserCreate(BaseModel):
    email: EmailStr
    password: str                    # ← input plain — hash ก่อน save

class UserRead(BaseModel):
    id: int
    email: EmailStr                  # ← ไม่มี hashed_password!
    model_config = {"from_attributes": True}

class UserUpdate(BaseModel):
    email: EmailStr | None = None
    full_name: str | None = None
```

> 💬 **ทำไมแยก:** Model = DB schema (กว้าง), Schema = ข้อตกลงกับ client (แคบเฉพาะที่ปลอดภัย) — กัน password หลุด, รองรับ versioning

### Clean Architecture (Layered)

```
Router (HTTP)
   ↓
Service (Business logic — pure Python, ไม่รู้จัก FastAPI/DB)
   ↓
CRUD/Repository (DB access — SQLAlchemy)
   ↓
Model (DB schema)
```

---

## 14. Deployment

### 14.1 Production Server

```bash
# Dev only
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Production — gunicorn + uvicorn workers
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000

# Production — Granian (Rust-powered, เร็วกว่า)
granian --interface asgi --host 0.0.0.0 --port 8000 --workers 4 app.main:app
```

| Server                       | ภาษาชาวบ้าน             | ใช้เมื่อ                |
| ---------------------------- | ----------------------- | ----------------------- |
| `uvicorn --reload`           | dev server              | dev เท่านั้น            |
| `gunicorn + uvicorn workers` | classic production      | คุ้นเคย stable          |
| `granian` ⭐                 | Rust-powered ASGI       | production ใหม่ เร็วสุด |
| `hypercorn`                  | HTTP/2 + HTTP/3 support | ต้องการ HTTP/2          |

### 14.2 Dockerfile (Multi-stage + uv)

```dockerfile
# Stage 1: deps
FROM python:3.12-slim AS builder
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv
WORKDIR /app
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev --no-install-project

# Stage 2: runtime
FROM python:3.12-slim
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpango-1.0-0 libpangoft2-1.0-0 fonts-thai-tlwg \
    && rm -rf /var/lib/apt/lists/*

# non-root user
RUN useradd -m -u 1000 app
COPY --from=builder /app/.venv /app/.venv
ENV PATH="/app/.venv/bin:$PATH"

WORKDIR /app
COPY --chown=app:app . .
USER app

EXPOSE 8000
HEALTHCHECK --interval=30s --timeout=5s CMD curl -f http://localhost:8000/health || exit 1
CMD ["granian", "--interface", "asgi", "--host", "0.0.0.0", "--port", "8000", "app.main:app"]
```

### 14.3 docker-compose.yml

```yaml
services:
  api:
    build: .
    ports: ["8000:8000"]
    env_file: .env
    depends_on:
      db: { condition: service_healthy }
      redis: { condition: service_started }
    restart: unless-stopped

  db:
    image: postgres:16-alpine
    environment:
      POSTGRES_USER: user
      POSTGRES_PASSWORD: pass
      POSTGRES_DB: mydb
    volumes:
      - pgdata:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD", "pg_isready", "-U", "user"]
      interval: 10s
    restart: unless-stopped

  redis:
    image: redis:7-alpine
    command: redis-server --maxmemory 256mb --maxmemory-policy allkeys-lru
    volumes:
      - redis_data:/data
    restart: unless-stopped

  caddy:
    image: caddy:2-alpine
    ports: ["80:80", "443:443"]
    volumes:
      - ./Caddyfile:/etc/caddy/Caddyfile:ro
      - caddy_data:/data
    depends_on: [api]
    restart: unless-stopped

volumes:
  pgdata:
  redis_data:
  caddy_data:
```

### 14.4 Caddyfile (Auto-HTTPS)

```caddy
api.example.com {
    reverse_proxy api:8000
    encode gzip zstd
    header {
        Strict-Transport-Security "max-age=31536000"
        X-Content-Type-Options "nosniff"
        X-Frame-Options "DENY"
        Referrer-Policy "strict-origin-when-cross-origin"
    }
    log {
        output file /var/log/access.log
    }
}
```

### 14.5 Pre-commit Hooks

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.8.0
    hooks:
      - id: ruff
        args: [--fix]
      - id: ruff-format

  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.13.0
    hooks:
      - id: mypy
        additional_dependencies: [pydantic, sqlalchemy]

  - repo: https://github.com/Yelp/detect-secrets
    rev: v1.5.0
    hooks:
      - id: detect-secrets
```

```bash
uv add --dev pre-commit
pre-commit install            # set git hook
pre-commit run --all-files    # run manually
```

### 14.6 Health Check & Readiness

```python
@app.get("/health")
async def health():
    return {"status": "ok"}

@app.get("/ready")
async def ready(db: Session = Depends(get_db)):
    # ทดสอบ DB connection จริง
    db.execute(text("SELECT 1"))
    # ทดสอบ Redis
    await r.ping()
    return {"status": "ready"}
```

---

## 15. Library Cheatsheet

### 🎨 Core Stack

| Library             | ใช้ทำอะไร       | ภาษาชาวบ้าน        |
| ------------------- | --------------- | ------------------ |
| `fastapi`           | Web framework   | "เตาครัวสำเร็จรูป" |
| `pydantic`          | Data validation | "ผู้คุมประตู"      |
| `sqlalchemy`        | ORM             | "ล่ามแปลภาษา DB"   |
| `alembic`           | DB migration    | "แผนรีโนเวท DB"    |
| `uvicorn`/`granian` | ASGI server     | "เครื่องจ่ายไฟ"    |
| `pydantic-settings` | Config from env | "ตู้เซฟใส่กุญแจ"   |

### 🔒 Security

| Library                     | ใช้ทำอะไร                          |
| --------------------------- | ---------------------------------- |
| `argon2-cffi`               | Password hash (modern, OWASP 2024) |
| `passlib[bcrypt,argon2]`    | Multi-scheme password hashing      |
| `python-jose[cryptography]` | JWT (encode/decode)                |
| `cryptography`              | Field encryption (Fernet, RSA)     |
| `pyotp`                     | TOTP 2FA                           |
| `slowapi`                   | Rate limiting                      |
| `secure`                    | Security headers                   |

### 🌐 HTTP & Async

| Library    | ใช้ทำอะไร                        |
| ---------- | -------------------------------- |
| `httpx`    | Async HTTP client (แทน requests) |
| `aiohttp`  | Async HTTP (older, lower-level)  |
| `tenacity` | Retry / backoff logic            |
| `anyio`    | Async backend-agnostic           |
| `aiocache` | Async cache decorator            |

### 📊 Data Processing

| Library       | ใช้ทำอะไร                         |
| ------------- | --------------------------------- |
| `polars` ⭐   | DataFrame (เร็วกว่า pandas 5-10x) |
| `pandas`      | DataFrame (classic)               |
| `duckdb`      | In-process SQL OLAP               |
| `pyarrow`     | Parquet, columnar memory          |
| `openpyxl`    | Excel read/write                  |
| `python-docx` | Word read/write                   |

### 📄 Documents

| Library          | ใช้ทำอะไร                 |
| ---------------- | ------------------------- |
| `weasyprint`     | HTML → PDF (Thai font OK) |
| `reportlab`      | PDF construct directly    |
| `pypdf`          | PDF read/manipulate       |
| `pdfplumber`     | Extract text from PDF     |
| `jinja2`         | Template engine           |
| `markdown-it-py` | Markdown → HTML           |

### 🖼️ Media

| Library          | ใช้ทำอะไร          |
| ---------------- | ------------------ |
| `Pillow`         | Image processing   |
| `imagehash`      | Perceptual hashing |
| `qrcode`         | Generate QR        |
| `python-barcode` | Barcode            |

### 🧰 Background Jobs

| Library              | ใช้ทำอะไร                            |
| -------------------- | ------------------------------------ |
| `arq` ⭐             | Redis-based async (FastAPI-friendly) |
| `taskiq`             | Modern, Pydantic-style               |
| `celery`             | Classic, mature                      |
| `dramatiq`           | Simpler than Celery                  |
| `apscheduler`        | Cron-style scheduled jobs            |
| `redis-queue` (`rq`) | Simple Redis queue                   |

### 📦 Caching

| Library         | ใช้ทำอะไร                       |
| --------------- | ------------------------------- |
| `redis`         | Redis client (4.2+ มี async)    |
| `aiocache`      | Async cache backend abstraction |
| `cachetools`    | In-memory LRU/TTL               |
| `dogpile.cache` | Multi-region cache              |

### 🔍 Observability

| Library                             | ใช้ทำอะไร            |
| ----------------------------------- | -------------------- |
| `loguru`                            | Logging ที่เขียนง่าย |
| `structlog`                         | Structured logging   |
| `sentry-sdk`                        | Error tracking       |
| `prometheus-fastapi-instrumentator` | Metrics              |
| `opentelemetry-api`                 | Distributed tracing  |

### 🛠️ Dev Tools

| Library            | ใช้ทำอะไร                        |
| ------------------ | -------------------------------- |
| `ruff` ⭐          | Linter + formatter (Rust, ครบจบ) |
| `mypy` / `pyright` | Static type check                |
| `pre-commit`       | Git hooks                        |
| `pytest` + extras  | Testing (ดู Lecture 102)         |
| `ipdb` / `pudb`    | Debugger ดีกว่า pdb              |
| `rich`             | Terminal pretty output           |
| `typer`            | CLI builder                      |

### 📊 GraphQL (ถ้าต้อง)

| Library         | ใช้ทำอะไร                  |
| --------------- | -------------------------- |
| `strawberry` ⭐ | GraphQL ด้วย type hints    |
| `ariadne`       | Schema-first GraphQL       |
| `graphene`      | Classic GraphQL (เก่ากว่า) |

### 🔌 External Integrations

| Library                       | ใช้ทำอะไร        |
| ----------------------------- | ---------------- |
| `boto3`                       | AWS SDK          |
| `google-cloud-*`              | Google Cloud SDK |
| `slack-sdk`                   | Slack            |
| `line-bot-sdk`                | LINE Messaging   |
| `gspread`                     | Google Sheets    |
| `gmail-api` (via google-auth) | Gmail            |

---

## 🎯 เส้นทางสู่ Hero (Roadmap)

| สัปดาห์    | เน้น                           | Library หลัก                               |
| ---------- | ------------------------------ | ------------------------------------------ |
| **1-2**    | Pydantic + Type hints          | `pydantic`                                 |
| **3-4**    | FastAPI: routes, deps, schemas | `fastapi`, `uvicorn`                       |
| **5-6**    | SQLAlchemy 2.0 + Alembic       | `sqlalchemy`, `alembic`                    |
| **7**      | Auth (JWT, OAuth2)             | `python-jose`, `passlib`, `argon2-cffi`    |
| **8**      | Testing                        | `pytest`, `pytest-asyncio` (→ Lecture 102) |
| **9**      | Async, HTTP client, BG tasks   | `httpx`, `tenacity`, `arq`                 |
| **10**     | Logging, monitoring            | `loguru`, `sentry-sdk`, `prometheus`       |
| **11**     | Caching + Redis                | `redis`, `aiocache`                        |
| **12**     | Docker + deploy                | `docker`, `caddy`, `granian`               |
| **Beyond** | สร้างโปรเจคจริง!               | ทั้งหมด                                    |

---

## 📖 แหล่งเรียนรู้เพิ่มเติม

| ลิงก์                                                  | ภาษาชาวบ้าน                    |
| ------------------------------------------------------ | ------------------------------ |
| 📘 [FastAPI Docs](https://fastapi.tiangolo.com)        | คู่มือต้นฉบับ — อ่านง่ายที่สุด |
| 📗 [SQLAlchemy 2.0](https://docs.sqlalchemy.org)       | ละเอียดมาก ใช้ search          |
| 📙 [Pydantic v2 Docs](https://docs.pydantic.dev)       | ตัวอย่างเยอะ                   |
| 📕 [Real Python](https://realpython.com)               | tutorial มืออาชีพ              |
| 🎥 ArjanCode (YouTube)                                 | Clean architecture in Python   |
| 📚 _Architecture Patterns with Python_ (Cosmic Python) | หนังสือต้องอ่าน                |
| 📚 _Fluent Python_ (Luciano Ramalho)                   | เข้าใจ Python ลึกๆ             |

---

> 💪 **คาถาประจำใจ:**
> _Type hints คือเพื่อนสนิท_
> _Pydantic คือผู้คุ้มกัน_
> _FastAPI คือพาหนะ_
> _SQLAlchemy คือคลังแสง_
> _uv คือรถไฟความเร็วสูง_
> _ruff คือไม้กวาดอัจฉริยะ_

ขอให้สนุกกับการเขียน Python นะครับ! 🐍🚀
