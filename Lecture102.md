# คู่มือ Automated Testing สำหรับ Python + FastAPI

> คู่มือฉบับสมบูรณ์ตั้งแต่พื้นฐาน pytest ไปจนถึง CI/CD บน Production
> เนื้อหาแบ่งเป็น 4 Phase ต่อเนื่องกัน

## 📚 สารบัญ

- [Phase 1: ปรับ Mindset และพื้นฐาน pytest](#phase-1)
- [Phase 2: Testing FastAPI ด้วย TestClient](#phase-2)
- [Phase 3: Database Testing ด้วย SQLAlchemy + Async](#phase-3)
- [Phase 4: Production Ready — Coverage, Load Test, CI/CD](#phase-4)

---

<a id="phase-1"></a>

# Phase 1: ปรับ Mindset และพื้นฐาน Automated Testing ด้วย pytest

> "เทสที่ดีไม่ใช่เทสที่ยาวที่สุด แต่คือเทสที่อ่านแล้วเข้าใจได้ทันทีว่ากำลังเช็คอะไร"

## 1.1 Mindset ก่อนเริ่มเขียนเทส

### ทำไมต้องเขียน Automated Test?
- **Regression Safety** — แก้โค้ดเก่าโดยไม่ต้องกลัวพังของเดิม
- **Documentation ที่รันได้** — เทสคือตัวอย่างการใช้งานที่ "ไม่มีวันล้าสมัย"
- **Refactor ได้อย่างมั่นใจ** — มี safety net รองรับ
- **Design ดีขึ้นโดยอัตโนมัติ** — โค้ดที่เทสยาก = โค้ดที่ design ไม่ดี

### หลักการ FIRST
| หลักการ | คำอธิบาย |
|--------|---------|
| **F**ast | เทสต้องรันเร็ว — ถ้าช้า dev จะไม่อยากรัน |
| **I**ndependent | เทสแต่ละตัวต้องไม่พึ่งพากัน |
| **R**epeatable | รันที่ไหน เมื่อไหร่ ผลลัพธ์เหมือนกัน |
| **S**elf-validating | รู้ผล pass/fail เองโดยไม่ต้องดูด้วยตา |
| **T**imely | เขียนพร้อม / ก่อน production code |

---

## 1.2 AAA Pattern (Arrange, Act, Assert)

```python
def test_calculate_total_price():
    # Arrange — เตรียมข้อมูลและ dependencies
    cart = ShoppingCart()
    cart.add_item("apple", price=10, qty=3)
    cart.add_item("banana", price=5, qty=2)

    # Act — เรียกฟังก์ชันที่ต้องการเทส (ทำสิ่งเดียว)
    total = cart.calculate_total()

    # Assert — ตรวจสอบผลลัพธ์
    assert total == 40
```

### กฎทอง 3 ข้อ
1. **One Act per test** — มี action หลักแค่อันเดียว
2. **Clear separation** — ใช้บรรทัดว่าง / คอมเมนต์แยก 3 ส่วน
3. **Test name อธิบายพฤติกรรม** — `test_<what>_<when>_<then>`
   - ✅ `test_calculate_total_returns_zero_when_cart_is_empty`
   - ❌ `test_total_1`

---

## 1.3 ติดตั้งและโครงสร้างโปรเจกต์

```bash
pip install pytest pytest-cov pytest-asyncio
```

```
my_project/
├── app/
│   ├── __init__.py
│   ├── calculator.py
│   └── services/
├── tests/
│   ├── __init__.py
│   ├── conftest.py           # fixtures ร่วมกัน
│   ├── unit/
│   └── integration/
├── pyproject.toml
└── pytest.ini
```

### `pytest.ini` พื้นฐาน
```ini
[pytest]
testpaths = tests
python_files = test_*.py
addopts =
    -v
    --strict-markers
    --tb=short
markers =
    slow: marks tests as slow
    integration: integration tests
```

---

## 1.4 เขียนเทสฟังก์ชันแบบง่าย

```python
# app/calculator.py
def add(a: int, b: int) -> int:
    return a + b

def divide(a: float, b: float) -> float:
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b
```

```python
# tests/unit/test_calculator.py
import pytest
from app.calculator import add, divide


def test_add_two_positive_numbers():
    result = add(2, 3)
    assert result == 5


def test_divide_raises_error_when_dividing_by_zero():
    with pytest.raises(ValueError, match="Cannot divide by zero"):
        divide(10, 0)
```

### Parametrize — ทดสอบหลาย case ในเทสเดียว
```python
@pytest.mark.parametrize("number, expected", [
    (2, True),
    (3, False),
    (0, True),
    (-4, True),
])
def test_is_even(number, expected):
    assert is_even(number) == expected
```

---

## 1.5 Fixtures — หัวใจของ pytest

```python
# tests/conftest.py
import pytest
from app.calculator import ShoppingCart

@pytest.fixture
def empty_cart():
    return ShoppingCart()

@pytest.fixture
def cart_with_items():
    cart = ShoppingCart()
    cart.add_item("apple", price=10, qty=3)
    return cart
```

```python
def test_empty_cart_total_is_zero(empty_cart):
    assert empty_cart.calculate_total() == 0
```

### Fixture Scope

| Scope | สร้างใหม่เมื่อ | ใช้กับ |
|-------|--------------|-------|
| `function` (default) | ทุกเทส | ข้อมูลที่ต้อง fresh |
| `class` | แต่ละ class | state ที่แชร์กัน |
| `module` | แต่ละไฟล์ | DB connection, config |
| `session` | ทั้ง test run | resource ราคาแพง |

```python
@pytest.fixture(scope="session")
def expensive_resource():
    resource = create_expensive_resource()
    yield resource
    resource.close()
```

### Setup/Teardown ด้วย `yield`
```python
@pytest.fixture
def temp_file(tmp_path):
    file_path = tmp_path / "test.txt"
    file_path.write_text("hello")
    yield file_path
    if file_path.exists():
        file_path.unlink()
```

---

## 1.6 คำสั่ง pytest ที่ใช้บ่อย

```bash
pytest                                          # รันทั้งหมด
pytest tests/unit/test_calculator.py            # ไฟล์เดียว
pytest tests/unit/test_calculator.py::test_add  # เทสเดียว
pytest -k "divide"                              # match keyword
pytest -m "not slow"                            # ตาม marker
pytest -v -s                                    # verbose + แสดง print
pytest -x                                       # หยุดเมื่อ fail
pytest --lf                                     # รันเฉพาะที่ fail ครั้งล่าสุด
```

---

<a id="phase-2"></a>

# Phase 2: Testing FastAPI ด้วย TestClient

> "การเทส API ที่ดีคือการจำลอง client จริง"

## 2.1 ทำความรู้จัก TestClient

```bash
pip install fastapi pytest httpx
```

```python
# app/main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: str
    price: float

items_db: dict[int, Item] = {}

@app.get("/items/{item_id}")
def read_item(item_id: int):
    if item_id not in items_db:
        raise HTTPException(404, "Item not found")
    return items_db[item_id]

@app.post("/items/{item_id}", status_code=201)
def create_item(item_id: int, item: Item):
    if item_id in items_db:
        raise HTTPException(409, "Already exists")
    items_db[item_id] = item
    return item
```

---

## 2.2 Setup TestClient

```python
# tests/conftest.py
import pytest
from fastapi.testclient import TestClient
from app.main import app, items_db

@pytest.fixture
def client():
    return TestClient(app)

@pytest.fixture(autouse=True)
def reset_db():
    items_db.clear()
    yield
    items_db.clear()
```

---

## 2.3 Test ทุก HTTP Method

### GET
```python
def test_get_item_returns_404_when_not_found(client):
    response = client.get("/items/999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Item not found"}
```

### POST
```python
def test_create_item_returns_201(client):
    payload = {"name": "Apple", "price": 10.5}
    response = client.post("/items/1", json=payload)
    assert response.status_code == 201
    assert response.json() == payload


def test_create_item_with_invalid_payload_returns_422(client):
    response = client.post("/items/1", json={"name": "Apple"})  # ขาด price
    assert response.status_code == 422
```

### PUT / DELETE
```python
def test_update_existing_item(client):
    client.post("/items/1", json={"name": "Apple", "price": 10})
    response = client.put("/items/1", json={"name": "Apple", "price": 15})
    assert response.status_code == 200
    assert response.json()["price"] == 15


def test_delete_item_returns_204(client):
    client.post("/items/1", json={"name": "Apple", "price": 10})
    response = client.delete("/items/1")
    assert response.status_code == 204
    assert client.get("/items/1").status_code == 404
```

### Headers / Query Params
```python
def test_protected_endpoint(client):
    response = client.get(
        "/protected",
        headers={"Authorization": "Bearer secret123"}
    )
    assert response.status_code == 200


def test_search_with_query_param(client):
    response = client.get("/items/search", params={"q": "apple", "limit": 10})
```

---

## 2.4 Dependency Injection และการ Mock

นี่คือ **superpower** ของ FastAPI

```python
# app/dependencies.py
def get_email_service() -> EmailService:
    return EmailService(api_key="real-key")


# app/main.py
from fastapi import Depends

@app.post("/users/{user_id}/notify")
def notify_user(
    user_id: int,
    message: str,
    email_service: EmailService = Depends(get_email_service),
):
    email_service.send(user_id, message)
    return {"status": "sent"}
```

### Override Dependency ในเทส
```python
# tests/test_notify.py
import pytest
from unittest.mock import MagicMock
from fastapi.testclient import TestClient
from app.main import app
from app.dependencies import get_email_service


@pytest.fixture
def mock_email_service():
    return MagicMock()


@pytest.fixture
def client(mock_email_service):
    app.dependency_overrides[get_email_service] = lambda: mock_email_service
    yield TestClient(app)
    app.dependency_overrides.clear()  # สำคัญมาก!


def test_notify_user_calls_email_service(client, mock_email_service):
    response = client.post("/users/1/notify", params={"message": "Hello"})
    assert response.status_code == 200
    mock_email_service.send.assert_called_once_with(1, "Hello")
```

### ตัวอย่างจริง — Mock Authentication
```python
@pytest.fixture
def authenticated_client():
    fake_user = User(id=1, name="Alice", role="admin")
    app.dependency_overrides[get_current_user] = lambda: fake_user
    yield TestClient(app)
    app.dependency_overrides.clear()


def test_get_me_returns_current_user(authenticated_client):
    response = authenticated_client.get("/me")
    assert response.json()["name"] == "Alice"
```

> ทำไมไม่ mock JWT ตรงๆ? — เพราะ override dependency คือเทส **behavior** ไม่ใช่ implementation วันหลังเปลี่ยน auth library เทสก็ยังใช้ได้

---

<a id="phase-3"></a>

# Phase 3: Database Testing — SQLAlchemy & Mocking

> "Test กับ DB จริงๆ ไม่ใช่ mock — แต่ต้องเป็น DB ของเรา ไม่ใช่ของ prod"

## 3.1 ตัวเลือก Test Database

| ทางเลือก | ข้อดี | ข้อเสีย | เหมาะกับ |
|---------|------|--------|---------|
| **In-memory SQLite** | เร็วมาก, ไม่ต้อง setup | SQL dialect ต่างจาก prod | Unit test, model logic |
| **SQLite file** | persistent ระหว่างเทส | ยังต่างจาก prod | Quick integration |
| **Test DB แยก (Postgres)** | dialect ตรง prod 100% | setup ซับซ้อน, ช้ากว่า | Integration test จริง |
| **Testcontainers** | spin up DB จริงใน Docker | dependency เยอะ | CI/CD pipeline |

> **Tip:** ใช้ Postgres test DB ถ้า prod ใช้ Postgres — SQLite จะหลอกตา เช่น `JSONB`, `ARRAY`, partial index ใช้ไม่ได้

---

## 3.2 Setup กับ SQLAlchemy + In-memory SQLite

```python
# app/database.py
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "postgresql+asyncpg://user:pass@localhost/mydb"
engine = create_async_engine(DATABASE_URL)
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
Base = declarative_base()

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
```

```python
# tests/conftest.py
import pytest_asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.database import Base, get_db
from app.main import app


TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"


@pytest_asyncio.fixture
async def test_engine():
    engine = create_async_engine(TEST_DATABASE_URL, echo=False)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield engine
    await engine.dispose()


@pytest_asyncio.fixture
async def db_session(test_engine):
    """Session ใหม่สำหรับแต่ละเทส + rollback อัตโนมัติ"""
    async with test_engine.connect() as connection:
        transaction = await connection.begin()
        TestSession = sessionmaker(
            bind=connection, class_=AsyncSession, expire_on_commit=False
        )
        async with TestSession() as session:
            yield session
        await transaction.rollback()  # ✨ เคลียร์ทุกอย่างหลังเทสจบ
```

---

## 3.3 pytest-asyncio สำหรับ async function

```bash
pip install pytest-asyncio aiosqlite
```

```python
# pytest.ini
[pytest]
asyncio_mode = auto   # ไม่ต้องเขียน @pytest.mark.asyncio ทุกตัว
```

หรือใช้ marker แบบ explicit:
```python
import pytest

@pytest.mark.asyncio
async def test_create_user(db_session):
    user = User(name="Alice")
    db_session.add(user)
    await db_session.commit()

    result = await db_session.execute(select(User).where(User.name == "Alice"))
    assert result.scalar_one().name == "Alice"
```

---

## 3.4 Database Cleanup — Transaction Rollback Pattern

หลักการ: ทุกเทสรันใน transaction แล้ว **rollback** ตอนจบ → ไม่ทิ้งขยะใน DB

### ทำไมไม่ใช้ TRUNCATE หลังเทส?
- ช้ากว่ามาก (โดยเฉพาะตารางใหญ่)
- ต้อง disable constraints ชั่วคราว
- ผิดพลาดง่าย ลืม truncate ตารางใดตารางหนึ่ง

### Rollback Pattern (จาก fixture ข้างบน)
```python
async with test_engine.connect() as connection:
    transaction = await connection.begin()
    # ...session ทำงานในนี้...
    await transaction.rollback()
```

### Override `get_db` ใน app
```python
@pytest_asyncio.fixture
async def client(db_session):
    async def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db
    from httpx import AsyncClient
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac
    app.dependency_overrides.clear()


async def test_create_user_via_api(client):
    response = await client.post("/users", json={"name": "Alice"})
    assert response.status_code == 201
```

---

## 3.5 Mock External Services ด้วย `unittest.mock`

### `MagicMock` vs `AsyncMock`
```python
from unittest.mock import MagicMock, AsyncMock, patch

mock_sync = MagicMock()
mock_sync.send.return_value = {"id": 1}

mock_async = AsyncMock()
mock_async.send.return_value = {"id": 1}  # await ได้
```

### Patch โดยตรง
```python
# app/services/payment.py
import httpx

async def charge_credit_card(amount: float, token: str) -> dict:
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "https://api.stripe.com/v1/charges",
            data={"amount": amount, "source": token},
        )
        return response.json()
```

```python
# tests/test_payment.py
from unittest.mock import patch, AsyncMock
import pytest
from app.services.payment import charge_credit_card


@pytest.mark.asyncio
async def test_charge_credit_card_returns_charge_id():
    fake_response = AsyncMock()
    fake_response.json = MagicMock(return_value={"id": "ch_123", "status": "succeeded"})

    with patch("httpx.AsyncClient.post", return_value=fake_response) as mock_post:
        result = await charge_credit_card(1000, "tok_visa")

        assert result["id"] == "ch_123"
        mock_post.assert_called_once()
```

### Patch ที่ใช้ใน FastAPI Test
```python
@pytest.mark.asyncio
async def test_checkout_endpoint_charges_card(client):
    with patch("app.services.payment.charge_credit_card", new=AsyncMock(
        return_value={"id": "ch_123"}
    )) as mock_charge:
        response = await client.post("/checkout", json={"amount": 1000, "token": "tok_x"})

        assert response.status_code == 200
        mock_charge.assert_awaited_once_with(1000, "tok_x")
```

> **กฎสำคัญ:** patch path ที่ **ใช้** ไม่ใช่ที่ **define**
> ถ้า `app.api.checkout` import `charge_credit_card` จาก `app.services.payment`
> ให้ patch `"app.api.checkout.charge_credit_card"` ไม่ใช่ `"app.services.payment.charge_credit_card"`

---

## 3.6 Pattern: Factory สำหรับ Test Data

```python
# tests/factories.py
import factory
from app.models import User, Order

class UserFactory(factory.Factory):
    class Meta:
        model = User
    name = factory.Faker("name")
    email = factory.Faker("email")


class OrderFactory(factory.Factory):
    class Meta:
        model = Order
    user = factory.SubFactory(UserFactory)
    total = factory.Faker("pyfloat", min_value=10, max_value=1000)
```

```python
async def test_user_can_have_multiple_orders(db_session):
    user = UserFactory()
    orders = [OrderFactory(user=user) for _ in range(3)]
    db_session.add_all([user, *orders])
    await db_session.commit()
    # ...
```

---

<a id="phase-4"></a>

# Phase 4: สู่ Production — CI/CD & Best Practices

> "เทสที่รันแค่บนเครื่อง dev = เทสที่ไม่มีอยู่จริง"

## 4.1 Code Coverage ด้วย pytest-cov

```bash
pip install pytest-cov
```

### รัน
```bash
# Coverage แบบรายงานเทอร์มินัล
pytest --cov=app

# แสดงบรรทัดที่ไม่ได้เทส
pytest --cov=app --cov-report=term-missing

# HTML report (เปิด htmlcov/index.html)
pytest --cov=app --cov-report=html

# Fail ถ้า coverage ต่ำกว่า threshold
pytest --cov=app --cov-fail-under=80
```

### Config ใน `pyproject.toml`
```toml
[tool.coverage.run]
source = ["app"]
omit = [
    "*/tests/*",
    "*/migrations/*",
    "app/main.py",
]
branch = true   # เช็ค branch coverage ด้วย ไม่ใช่แค่ line

[tool.coverage.report]
exclude_lines = [
    "pragma: no cover",
    "raise NotImplementedError",
    "if __name__ == .__main__.:",
    "if TYPE_CHECKING:",
]
fail_under = 80
show_missing = true
```

### อ่านรายงาน
```
Name                       Stmts   Miss Branch BrPart  Cover   Missing
------------------------------------------------------------------------
app/services/user.py         42      3      8      1    92%   45-47, 89->92
```

- **Stmts** = บรรทัดโค้ดที่นับได้
- **Miss** = บรรทัดที่ไม่ได้รัน
- **Branch** = จำนวน if/else branches
- **BrPart** = branch ที่รันแค่ขาเดียว
- **Missing** = ระบุ line / branch ที่ขาด

> ⚠️ **Coverage ≠ Quality** — 100% coverage ไม่ได้แปลว่าเทสครบ
> Code ที่รันแล้ว ≠ Code ที่ถูก assert
> ใช้ coverage หา **โซนที่ยังไม่มีเทสเลย** ไม่ใช่เป็น KPI ตามล่า

---

## 4.2 Load Testing เบื้องต้นด้วย Locust

```bash
pip install locust
```

### `locustfile.py`
```python
from locust import HttpUser, task, between

class WebsiteUser(HttpUser):
    wait_time = between(1, 3)  # delay ระหว่าง request

    def on_start(self):
        """รันก่อน user แต่ละคนเริ่ม — ใช้ login เก็บ token"""
        response = self.client.post("/login", json={
            "username": "test",
            "password": "test"
        })
        self.token = response.json()["access_token"]

    @task(3)  # weight = ทำบ่อยกว่า task อื่น 3 เท่า
    def get_items(self):
        self.client.get("/items", headers={"Authorization": f"Bearer {self.token}"})

    @task(1)
    def create_item(self):
        self.client.post(
            "/items",
            json={"name": "Test", "price": 10},
            headers={"Authorization": f"Bearer {self.token}"}
        )
```

### รัน
```bash
# Web UI ที่ http://localhost:8089
locust -f locustfile.py --host=http://localhost:8000

# Headless mode
locust -f locustfile.py --host=http://localhost:8000 \
    --users 100 --spawn-rate 10 --run-time 5m --headless
```

### Metrics ที่ต้องดู
- **Requests/sec** — throughput ของระบบ
- **p50, p95, p99 latency** — โดยเฉพาะ p99 (worst case ของลูกค้าจริง)
- **Failure rate** — ต้องเป็น 0 หรือใกล้เคียง
- **Connection errors** — แปลว่าเซิร์ฟเวอร์ตก

---

## 4.3 GitHub Actions — รัน Test อัตโนมัติ

```yaml
# .github/workflows/tests.yml
name: Tests

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main, develop]

jobs:
  test:
    runs-on: ubuntu-latest

    services:
      postgres:
        image: postgres:16
        env:
          POSTGRES_USER: test
          POSTGRES_PASSWORD: test
          POSTGRES_DB: test_db
        ports:
          - 5432:5432
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5

    strategy:
      matrix:
        python-version: ["3.11", "3.12"]

    steps:
      - uses: actions/checkout@v4

      - name: Set up Python ${{ matrix.python-version }}
        uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}
          cache: pip

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
          pip install -r requirements-dev.txt

      - name: Lint with ruff
        run: ruff check app tests

      - name: Type check with mypy
        run: mypy app

      - name: Run tests with coverage
        env:
          DATABASE_URL: postgresql+asyncpg://test:test@localhost:5432/test_db
        run: |
          pytest --cov=app --cov-report=xml --cov-report=term-missing \
                 --cov-fail-under=80

      - name: Upload coverage to Codecov
        uses: codecov/codecov-action@v4
        with:
          file: ./coverage.xml
          fail_ci_if_error: true

      - name: Upload test results
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: test-results-${{ matrix.python-version }}
          path: |
            .coverage
            coverage.xml
            htmlcov/
```

### Tips สำหรับ CI
- ใช้ **matrix** เทสหลาย Python version
- ใช้ **service container** สำหรับ DB จริง (Postgres/Redis)
- **cache pip** ลดเวลา install
- แยก **lint / type-check / test** เป็น step ต่างกัน → debug ง่าย
- เก็บ **artifact** ไว้ดู report ภายหลัง

---

## 4.4 โครงสร้าง Folder สำหรับโปรเจกต์ขนาดใหญ่

```
my_project/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── api/                    # FastAPI routers
│   │   ├── v1/
│   │   │   ├── users.py
│   │   │   └── items.py
│   ├── core/                   # config, security
│   ├── models/                 # SQLAlchemy models
│   ├── schemas/                # Pydantic schemas
│   ├── services/               # business logic
│   └── repositories/           # DB access layer
│
├── tests/
│   ├── __init__.py
│   ├── conftest.py             # global fixtures (client, db_session)
│   ├── factories.py            # factory_boy data factories
│   │
│   ├── unit/                   # ⚡ เร็ว, ไม่ touch DB/network
│   │   ├── conftest.py
│   │   ├── services/
│   │   │   └── test_user_service.py
│   │   └── utils/
│   │
│   ├── integration/            # 🔌 touch DB จริง / Redis
│   │   ├── conftest.py
│   │   ├── repositories/
│   │   │   └── test_user_repo.py
│   │   └── api/
│   │       ├── test_users_api.py
│   │       └── test_items_api.py
│   │
│   ├── e2e/                    # 🌐 ทั้ง flow จริง
│   │   └── test_signup_flow.py
│   │
│   └── load/                   # locustfiles
│       └── locustfile_api.py
│
├── .github/
│   └── workflows/
│       ├── tests.yml
│       └── deploy.yml
│
├── pyproject.toml
├── pytest.ini
└── requirements-dev.txt
```

### หลักการแยกชั้น
| Layer | ความเร็ว | Mock อะไร | สัดส่วน (Test Pyramid) |
|-------|---------|----------|----------------------|
| **unit** | < 0.1s ต่อเทส | ทุก dependency ภายนอก | 70% |
| **integration** | < 1s ต่อเทส | external API เท่านั้น | 25% |
| **e2e** | หลายวินาที | ไม่ mock เลย | 5% |
| **load** | นาที-ชั่วโมง | - | manual / scheduled |

### `conftest.py` หลายระดับ
- `tests/conftest.py` → fixtures ที่ทุกเทสใช้ (db, client)
- `tests/unit/conftest.py` → fixtures เฉพาะ unit (mocks)
- `tests/integration/conftest.py` → fixtures DB จริง

---

## 4.5 Best Practices สำหรับ Production

### ✅ Do
- รัน lint + type-check + test ใน pre-commit hook
- แบ่ง marker `@pytest.mark.slow` ให้ skip ใน dev loop
- ใช้ `pytest-xdist` รันเทสคู่ขนานบน CI: `pytest -n auto`
- ตั้ง coverage threshold 70-80% (อย่าตั้ง 100% บังคับ)
- เทส **error path** เท่ากับ happy path
- เทส migration ก่อน deploy (เช่น Alembic upgrade/downgrade)

### ❌ Don't
- อย่ายิง API จริง / ส่งอีเมลจริง / ส่ง LINE จริงในเทส
- อย่าใช้ `time.sleep()` ในเทส — ใช้ `freezegun` หรือ inject clock
- อย่าใช้ random seed ที่ไม่ fix — ใช้ `factory.Faker` หรือ fix `random.seed()`
- อย่าทิ้ง state ระหว่างเทส — rollback / cleanup ทุกครั้ง
- อย่า skip flaky test — แก้ให้หาย ไม่งั้นจะเกิด tests ที่ "passed" หลอกๆ

---

## 4.6 Tools เสริมที่ควรรู้

| Tool | ใช้ทำอะไร |
|------|----------|
| `pytest-xdist` | รันเทสคู่ขนาน (`-n auto`) |
| `pytest-mock` | ใช้ `mocker` fixture แทน `unittest.mock.patch` |
| `pytest-randomly` | shuffle ลำดับเทส → จับ test ที่ขึ้นกับ order |
| `freezegun` | freeze เวลาในเทส |
| `responses` / `respx` | mock HTTP requests/httpx |
| `factory_boy` / `pydantic-factories` | สร้าง test data |
| `pytest-benchmark` | เทส performance regression |
| `mutmut` / `cosmic-ray` | mutation testing — ตรวจคุณภาพเทส |

---

## 4.7 Checklist สู่ Production

- [ ] Coverage ≥ 80% สำหรับโค้ด business logic
- [ ] Test pyramid: unit > integration > e2e
- [ ] CI รันเทสบนทุก PR และ block merge ถ้า fail
- [ ] DB migration มีเทส (upgrade + downgrade)
- [ ] Load test เคยรันแล้วและ baseline บันทึกไว้
- [ ] Security test — SQL injection, XSS, auth bypass
- [ ] เทส run จริงบน Python version เดียวกับ prod
- [ ] No secrets ใน test files (ใช้ env var / `.env.test`)
- [ ] Test report เก็บเป็น artifact ใน CI
- [ ] เทสที่ flaky ถูก track และแก้ ไม่ใช่ skip

---

## 🎯 สรุปทั้งคู่มือ

| Phase | สิ่งที่ได้ |
|-------|----------|
| **1** | เขียน unit test ตาม AAA + ใช้ fixtures คล่อง |
| **2** | เทส FastAPI endpoints + override dependencies |
| **3** | เทส DB จริงด้วย rollback pattern + mock external API |
| **4** | Coverage, Load test, GitHub Actions, project structure |

> "Tests are a safety harness for refactoring, a documentation that compiles, and a design tool that exposes bad coupling. Write them with the same care as production code — because they are."
