# คู่มือ Automated Testing สำหรับ Python + FastAPI (ฉบับขยาย)

> คู่มือฉบับสมบูรณ์ตั้งแต่พื้นฐาน pytest ไปจนถึง CI/CD บน Production
> **เนื้อหาแบ่งเป็น 5 Phase ต่อเนื่องกัน + Class Reference ครบทุก library**

> 💬 **ภาษาชาวบ้าน:** Test = "ตรวจ QC อัตโนมัติ" — เขียน script ตรวจครั้งเดียว ใช้ตลอด ทุกครั้งแก้โค้ด → script ตรวจให้ว่าของเก่าไม่พัง

## 📚 สารบัญ

- [Phase 1: ปรับ Mindset และพื้นฐาน pytest](#phase-1)
- [Phase 2: Testing FastAPI ด้วย TestClient](#phase-2)
- [Phase 3: Database Testing ด้วย SQLAlchemy + Async](#phase-3)
- [Phase 4: Production Ready — Coverage, Load Test, CI/CD](#phase-4)
- [Phase 5: Testing Libraries Class Reference (ครบทุกตัว)](#phase-5)

---

<a id="phase-1"></a>

# Phase 1: Mindset & พื้นฐาน Automated Testing ด้วย pytest

> "เทสที่ดีไม่ใช่เทสที่ยาวที่สุด แต่คือเทสที่อ่านแล้วเข้าใจได้ทันทีว่ากำลังเช็คอะไร"

## 1.1 Mindset ก่อนเริ่มเขียนเทส

### ทำไมต้องเขียน Automated Test?

| เหตุผล                      | ภาษาชาวบ้าน                                                                      |
| --------------------------- | -------------------------------------------------------------------------------- |
| **Regression Safety**       | "ใส่หมวกกันน็อค" — แก้โค้ดเก่าโดยไม่ต้องกลัวพังของเดิม                           |
| **Documentation ที่รันได้** | "ตัวอย่างที่ไม่มีวันล้าสมัย" — code เปลี่ยน test ก็พัง ต้องอัพเดท → docs ตรงเสมอ |
| **Refactor ได้มั่นใจ**      | "safety net ใต้กายกรรม" — ตกก็ไม่เจ็บ                                            |
| **Design ดีขึ้น**           | "code ที่ test ยาก = code ที่ design ไม่ดี" — บังคับให้แยกหน้าที่                |
| **Onboard คนใหม่**          | "อ่าน test เข้าใจว่า code ทำอะไร"                                                |

### หลักการ FIRST

| หลักการ             | คำอธิบาย                    | ภาษาชาวบ้าน                                     |
| ------------------- | --------------------------- | ----------------------------------------------- |
| **F**ast            | เทสรันเร็ว                  | "ช้า = dev ไม่อยากรัน = ไม่ค่อยรัน = บั๊กลาม"   |
| **I**ndependent     | เทสไม่พึ่งพากัน             | "test 1 ตกแล้ว test 2 ก็พังตาม = ไม่รู้ตัวจริง" |
| **R**epeatable      | รันที่ไหนเมื่อไรก็เหมือนกัน | "บนเครื่อง dev ผ่าน บน CI ตก = flaky"           |
| **S**elf-validating | รู้ผล pass/fail เอง         | "ไม่ต้องไปดู log เอง"                           |
| **T**imely          | เขียนพร้อม/ก่อน production  | "เขียนทีหลังแล้ว = อ้างว่าไม่มีเวลา"            |

### Test Pyramid

```
          /\
         /e2e\         5%  — ช้า, mock น้อย, fragile
        /------\
       /  api   \      25% — touch DB จริง, mock external
      /----------\
     /   unit     \    70% — pure logic, mock heavy
    /--------------\
```

> 💬 **Pyramid คือ:** ยิ่ง integration ลึกยิ่งช้า — ให้มี unit เยอะที่สุด แล้วลดหลั่นลงมา

---

## 1.2 AAA Pattern (Arrange, Act, Assert)

```python
def test_calculate_total_price():
    # Arrange — เตรียมข้อมูล/dependencies (จัดของลงโต๊ะ)
    cart = ShoppingCart()
    cart.add_item("apple", price=10, qty=3)
    cart.add_item("banana", price=5, qty=2)

    # Act — เรียกฟังก์ชันที่ต้องการเทส (กดปุ่ม)
    total = cart.calculate_total()

    # Assert — ตรวจสอบผลลัพธ์ (เช็คผล)
    assert total == 40
```

### กฎทอง 3 ข้อ

1. **One Act per test** — มี action หลักแค่อันเดียว
2. **Clear separation** — บรรทัดว่าง/คอมเมนต์แยก 3 ส่วน
3. **Test name อธิบายพฤติกรรม** — `test_<what>_<when>_<then>`
   - ✅ `test_calculate_total_returns_zero_when_cart_is_empty`
   - ❌ `test_total_1`

### ตัวอย่างหลาย scenario

```python
class TestShoppingCart:
    def test_calculate_total_returns_zero_when_empty(self):
        cart = ShoppingCart()
        assert cart.calculate_total() == 0

    def test_add_item_increases_total(self):
        cart = ShoppingCart()
        cart.add_item("apple", price=10, qty=3)
        assert cart.calculate_total() == 30

    def test_apply_discount_reduces_total(self):
        cart = ShoppingCart()
        cart.add_item("apple", price=100, qty=1)
        cart.apply_discount(0.1)
        assert cart.calculate_total() == 90

    def test_apply_discount_raises_when_negative(self):
        cart = ShoppingCart()
        with pytest.raises(ValueError, match="discount must be 0-1"):
            cart.apply_discount(-0.1)
```

---

## 1.3 ติดตั้งและโครงสร้างโปรเจกต์

```bash
uv add --dev pytest pytest-cov pytest-asyncio pytest-mock pytest-xdist \
              factory_boy faker freezegun respx
```

```
my_project/
├── app/
│   ├── __init__.py
│   ├── calculator.py
│   └── services/
├── tests/
│   ├── __init__.py
│   ├── conftest.py           # fixtures ร่วม
│   ├── factories.py          # test data factories
│   ├── unit/
│   ├── integration/
│   └── e2e/
├── pyproject.toml
└── pytest.ini
```

### `pyproject.toml` (แนะนำมากกว่า pytest.ini)

```toml
[tool.pytest.ini_options]
minversion = "7.0"
testpaths = ["tests"]
python_files = ["test_*.py", "*_test.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]
addopts = [
    "-v",
    "--strict-markers",
    "--strict-config",
    "--tb=short",
    "-ra",                          # show short summary of all
]
asyncio_mode = "auto"               # ไม่ต้อง @pytest.mark.asyncio ทุกตัว
markers = [
    "slow: marks tests as slow",
    "integration: integration tests",
    "e2e: end-to-end tests",
]
filterwarnings = [
    "error",                        # treat warnings as errors
    "ignore::DeprecationWarning:pkg_resources",
]
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
    assert add(2, 3) == 5

def test_divide_raises_error_when_dividing_by_zero():
    with pytest.raises(ValueError, match="Cannot divide by zero"):
        divide(10, 0)

def test_divide_normal_case():
    assert divide(10, 2) == 5.0
    assert divide(7, 2) == 3.5
```

### Parametrize — ทดสอบหลาย case ใน 1 test

> 💬 **Parametrize คือ:** "ใส่ค่าหลายชุดเข้า test เดียวกัน" — ลด copy-paste

```python
@pytest.mark.parametrize("number, expected", [
    (2, True),
    (3, False),
    (0, True),
    (-4, True),
    (1, False),
])
def test_is_even(number, expected):
    assert is_even(number) == expected

# Parametrize หลาย parameter พร้อมกัน
@pytest.mark.parametrize("a, b, expected", [
    (1, 2, 3),
    (5, 5, 10),
    (-1, 1, 0),
    (0, 0, 0),
])
def test_add(a, b, expected):
    assert add(a, b) == expected

# Parametrize ด้วย id (อ่าน output ง่ายขึ้น)
@pytest.mark.parametrize("input,expected", [
    ("hello", "HELLO"),
    ("world", "WORLD"),
], ids=["lowercase", "mixed-case"])
def test_upper(input, expected):
    assert input.upper() == expected
```

### Indirect Parametrize (ผ่าน fixture)

```python
@pytest.fixture
def db_user(request):
    return User(name=request.param)

@pytest.mark.parametrize("db_user", ["alice", "bob"], indirect=True)
def test_user_name(db_user):
    assert db_user.name in ["alice", "bob"]
```

---

## 1.5 Fixtures — หัวใจของ pytest

> 💬 **Fixture คือ:** "เครื่องเตรียมของให้ test" — ของที่ test ต้องใช้บ่อยๆ (DB, client, mock) เขียนครั้งเดียว ใช้ซ้ำได้

```python
# tests/conftest.py
import pytest
from app.calculator import ShoppingCart

@pytest.fixture
def empty_cart():
    """Cart ว่างเปล่า"""
    return ShoppingCart()

@pytest.fixture
def cart_with_items():
    cart = ShoppingCart()
    cart.add_item("apple", price=10, qty=3)
    cart.add_item("banana", price=5, qty=2)
    return cart
```

```python
def test_empty_cart_total_is_zero(empty_cart):
    assert empty_cart.calculate_total() == 0

def test_cart_with_items_calculates_correctly(cart_with_items):
    assert cart_with_items.calculate_total() == 40
```

### Fixture Scope

| Scope                | สร้างใหม่เมื่อ | ใช้กับ                | ภาษาชาวบ้าน               |
| -------------------- | -------------- | --------------------- | ------------------------- |
| `function` (default) | ทุก test       | ข้อมูล fresh          | "เปลี่ยนของใหม่ทุกรอบ"    |
| `class`              | แต่ละ class    | state แชร์ใน class    | "ของชุดเดียวกันใน class"  |
| `module`             | แต่ละไฟล์      | DB connection, config | "ของชุดเดียวกันในไฟล์"    |
| `package`            | แต่ละ folder   | shared module setup   | "ของชุดเดียวกันใน folder" |
| `session`            | ทั้ง test run  | resource ราคาแพง      | "ของชุดเดียวตลอด session" |

```python
@pytest.fixture(scope="session")
def expensive_resource():
    """สร้างครั้งเดียวตลอด pytest run"""
    resource = create_expensive_resource()
    yield resource
    resource.close()
```

### Setup/Teardown ด้วย `yield`

```python
@pytest.fixture
def temp_file(tmp_path):
    """Fixture ที่ create + cleanup"""
    file_path = tmp_path / "test.txt"
    file_path.write_text("hello")
    yield file_path                    # ↑ ส่วนนี้ run ก่อน test
    # ↓ ส่วนนี้ run หลัง test (cleanup)
    if file_path.exists():
        file_path.unlink()

@pytest.fixture
def db_connection():
    conn = create_connection()
    try:
        yield conn
    finally:
        conn.close()
```

### Auto-use fixture (ใช้ทุก test โดยไม่ต้อง declare)

```python
@pytest.fixture(autouse=True)
def reset_cache():
    """Run ก่อนทุก test"""
    cache.clear()
    yield
    cache.clear()
```

### Built-in fixtures ที่ใช้บ่อย

| Fixture            | ใช้ทำอะไร                           |
| ------------------ | ----------------------------------- |
| `tmp_path`         | สร้าง temp folder (`pathlib.Path`)  |
| `tmp_path_factory` | สร้าง temp folder shared cross-test |
| `monkeypatch`      | mock env vars / attribute           |
| `capsys`           | จับ stdout/stderr                   |
| `caplog`           | จับ logging output                  |
| `request`          | ข้อมูล test ปัจจุบัน                |
| `pytestconfig`     | access pytest config                |

```python
# tmp_path
def test_write_file(tmp_path):
    p = tmp_path / "data.txt"
    p.write_text("hello")
    assert p.read_text() == "hello"

# monkeypatch
def test_env_var(monkeypatch):
    monkeypatch.setenv("API_KEY", "fake-key")
    monkeypatch.setattr("app.config.DEBUG", True)
    # test code

# capsys
def test_print(capsys):
    print("hello")
    captured = capsys.readouterr()
    assert captured.out == "hello\n"

# caplog
def test_log_emitted(caplog):
    import logging
    with caplog.at_level(logging.WARNING):
        logging.warning("oops")
    assert "oops" in caplog.text
```

### Fixture จาก fixture (Composition)

```python
@pytest.fixture
def db():
    return create_db()

@pytest.fixture
def user(db):                       # ใช้ fixture อื่น
    u = User(name="Alice")
    db.add(u)
    return u

@pytest.fixture
def order(db, user):
    o = Order(user=user, total=100)
    db.add(o)
    return o

def test_order_belongs_to_user(order, user):
    assert order.user == user
```

---

## 1.6 คำสั่ง pytest ที่ใช้บ่อย

```bash
pytest                                          # รันทั้งหมด
pytest tests/unit/test_calculator.py            # ไฟล์เดียว
pytest tests/unit/test_calculator.py::test_add  # เทสเดียว
pytest tests/unit/test_calculator.py::TestClass::test_method  # method ใน class

pytest -k "divide"                              # match keyword
pytest -k "not slow"                            # exclude
pytest -m "not slow"                            # ตาม marker
pytest -m "integration"                         # only integration

pytest -v                                       # verbose
pytest -vv                                      # extra verbose (diff ของ assert)
pytest -s                                       # show print
pytest --tb=short                               # short traceback
pytest --tb=long                                # full traceback
pytest --tb=no                                  # no traceback

pytest -x                                       # หยุดเมื่อ fail ครั้งแรก
pytest --maxfail=3                              # หยุดเมื่อ fail 3 ตัว
pytest --lf                                     # last-failed: รันเฉพาะที่ fail ครั้งล่าสุด
pytest --ff                                     # failed-first: รันที่ fail ก่อน

pytest -n auto                                  # parallel (pytest-xdist)
pytest --randomly-seed=12345                    # fix seed (pytest-randomly)

pytest --collect-only                           # แค่ list test ไม่รัน
pytest --markers                                # list markers ทั้งหมด
pytest --fixtures                               # list fixtures ทั้งหมด
```

### Pytest Markers

```python
import pytest

@pytest.mark.slow
def test_long_running():
    ...

@pytest.mark.integration
def test_db():
    ...

@pytest.mark.skip(reason="Not implemented yet")
def test_future():
    ...

@pytest.mark.skipif(sys.platform == "win32", reason="Linux only")
def test_linux_only():
    ...

@pytest.mark.xfail(reason="known bug #123")
def test_known_bug():
    assert 1 == 2    # ถ้า fail = xfail (expected fail), ถ้า pass = xpass (เตือน)
```

---

<a id="phase-2"></a>

# Phase 2: Testing FastAPI ด้วย TestClient

> "การเทส API ที่ดีคือการจำลอง client จริง"

## 2.1 ทำความรู้จัก TestClient

```bash
uv add fastapi pytest httpx
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

> 💬 **TestClient คือ:** "ลูกค้าจำลอง" — ส่ง HTTP request เข้า FastAPI โดยไม่ต้องเปิด server จริง

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

> 💡 **autouse=True** = ใช้ทุก test โดยไม่ต้องประกาศ → กันเทสปนเปื้อนกัน

---

## 2.3 Test ทุก HTTP Method

### GET

```python
def test_get_item_returns_404_when_not_found(client):
    response = client.get("/items/999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Item not found"}

def test_get_item_returns_correct_data(client):
    client.post("/items/1", json={"name": "Apple", "price": 10.5})
    response = client.get("/items/1")
    assert response.status_code == 200
    assert response.json() == {"name": "Apple", "price": 10.5}
```

### POST

```python
def test_create_item_returns_201(client):
    payload = {"name": "Apple", "price": 10.5}
    response = client.post("/items/1", json=payload)
    assert response.status_code == 201
    assert response.json() == payload

def test_create_item_with_invalid_payload_returns_422(client):
    response = client.post("/items/1", json={"name": "Apple"})    # ขาด price
    assert response.status_code == 422
    errors = response.json()["detail"]
    assert any(e["loc"] == ["body", "price"] for e in errors)

def test_create_duplicate_returns_409(client):
    client.post("/items/1", json={"name": "Apple", "price": 10})
    response = client.post("/items/1", json={"name": "Banana", "price": 5})
    assert response.status_code == 409
```

### PUT / PATCH / DELETE

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

### Headers / Query Params / Cookies

```python
def test_protected_endpoint_with_token(client):
    response = client.get("/protected", headers={"Authorization": "Bearer secret123"})
    assert response.status_code == 200

def test_protected_endpoint_without_token(client):
    response = client.get("/protected")
    assert response.status_code == 401

def test_search_with_query_param(client):
    response = client.get("/items/search", params={"q": "apple", "limit": 10})
    assert response.status_code == 200

def test_with_cookies(client):
    response = client.get("/me", cookies={"session_id": "abc123"})
```

### Upload File

```python
def test_upload_image(client):
    with open("tests/fixtures/sample.jpg", "rb") as f:
        response = client.post(
            "/upload",
            files={"file": ("sample.jpg", f, "image/jpeg")},
        )
    assert response.status_code == 200
    assert response.json()["saved"].endswith("sample.jpg")

# จาก in-memory bytes
def test_upload_in_memory(client):
    import io
    fake = io.BytesIO(b"fake image data")
    response = client.post(
        "/upload",
        files={"file": ("test.jpg", fake, "image/jpeg")},
    )
```

---

## 2.4 Dependency Injection และการ Mock (Superpower)

```python
# app/dependencies.py
class EmailService:
    def __init__(self, api_key: str):
        self.api_key = api_key

    def send(self, user_id: int, message: str):
        # ส่งจริงๆ → ไม่อยากให้ test ส่งจริง!
        ...

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
    app.dependency_overrides.clear()    # ⚠️ สำคัญมาก!

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

def test_admin_only_endpoint_allows_admin(authenticated_client):
    response = authenticated_client.delete("/users/2")
    assert response.status_code == 204
```

> 💬 **ทำไมไม่ mock JWT ตรงๆ?** — เพราะ override dependency คือเทส **behavior** ไม่ใช่ implementation วันหลังเปลี่ยน auth library เทสก็ยังใช้ได้

### Multiple Roles in Fixture

```python
@pytest.fixture
def make_client():
    """Factory fixture — สร้าง client พร้อม role ที่อยากได้"""
    def _make(role: str = "viewer"):
        user = User(id=1, role=role)
        app.dependency_overrides[get_current_user] = lambda: user
        return TestClient(app)
    yield _make
    app.dependency_overrides.clear()

def test_admin_can_delete(make_client):
    admin_client = make_client(role="admin")
    assert admin_client.delete("/users/2").status_code == 204

def test_viewer_cannot_delete(make_client):
    viewer_client = make_client(role="viewer")
    assert viewer_client.delete("/users/2").status_code == 403
```

---

<a id="phase-3"></a>

# Phase 3: Database Testing — SQLAlchemy & Mocking

> "Test กับ DB จริงๆ ไม่ใช่ mock — แต่ต้องเป็น DB ของเรา ไม่ใช่ของ prod"

## 3.1 ตัวเลือก Test Database

| ทางเลือก                   | ข้อดี                    | ข้อเสีย                  | เหมาะกับ               |
| -------------------------- | ------------------------ | ------------------------ | ---------------------- |
| **In-memory SQLite**       | เร็วมาก, ไม่ต้อง setup   | SQL dialect ต่างจาก prod | Unit test, model logic |
| **SQLite file**            | persistent ระหว่างเทส    | ยังต่างจาก prod          | Quick integration      |
| **Test DB แยก (Postgres)** | dialect ตรง prod 100%    | setup ซับซ้อน            | Integration test จริง  |
| **Testcontainers** ⭐      | spin up DB จริงใน Docker | dependency เยอะ          | CI/CD pipeline         |

> 💬 **Tip:** ใช้ **Postgres test DB** ถ้า prod ใช้ Postgres — SQLite จะหลอกตา เช่น `JSONB`, `ARRAY`, partial index, full-text search ใช้ไม่ได้

### Testcontainers — รัน Postgres จริงใน test

```python
# conftest.py
import pytest
from testcontainers.postgres import PostgresContainer

@pytest.fixture(scope="session")
def postgres_url():
    with PostgresContainer("postgres:16-alpine") as pg:
        yield pg.get_connection_url()

@pytest.fixture
def engine(postgres_url):
    from sqlalchemy import create_engine
    e = create_engine(postgres_url)
    Base.metadata.create_all(e)
    yield e
    Base.metadata.drop_all(e)
    e.dispose()
```

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
        await transaction.rollback()   # ✨ เคลียร์ทุกอย่างหลังเทสจบ
```

---

## 3.3 pytest-asyncio สำหรับ async function

```bash
uv add --dev pytest-asyncio aiosqlite
```

```toml
# pyproject.toml
[tool.pytest.ini_options]
asyncio_mode = "auto"    # ไม่ต้องเขียน @pytest.mark.asyncio
```

```python
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

### Rollback Pattern

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
    from httpx import AsyncClient, ASGITransport
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    ) as ac:
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

# Sync function/method
mock_sync = MagicMock()
mock_sync.send.return_value = {"id": 1}
result = mock_sync.send("hello")              # OK

# Async function/method
mock_async = AsyncMock()
mock_async.send.return_value = {"id": 1}
result = await mock_async.send("hello")       # OK (await ได้)

# ตรวจการเรียก
mock_sync.send.assert_called_once_with("hello")
mock_async.send.assert_awaited_once_with("hello")
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
from unittest.mock import patch, AsyncMock, MagicMock
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
    with patch(
        "app.api.checkout.charge_credit_card",      # ← patch ที่ใช้ ไม่ใช่ที่ define
        new=AsyncMock(return_value={"id": "ch_123"}),
    ) as mock_charge:
        response = await client.post("/checkout", json={"amount": 1000, "token": "tok_x"})
        assert response.status_code == 200
        mock_charge.assert_awaited_once_with(1000, "tok_x")
```

> **กฎสำคัญ:** patch path ที่ **ใช้** ไม่ใช่ที่ **define**
> ถ้า `app.api.checkout` import `charge_credit_card` จาก `app.services.payment`
> ให้ patch `"app.api.checkout.charge_credit_card"` ไม่ใช่ `"app.services.payment.charge_credit_card"`

### `pytest-mock` (ดีกว่า unittest.mock เพราะมี fixture)

```python
def test_with_mocker(mocker):
    mock_send = mocker.patch("app.services.email.send_email")
    mock_send.return_value = True

    result = notify_user(1, "hi")

    mock_send.assert_called_once_with("user@example.com", "hi")

# Patch chain ของ class
def test_with_class_mock(mocker):
    mock_client = mocker.patch("app.api.stripe.Client")
    mock_client.return_value.charge.return_value = {"id": "ch_1"}
```

### Mock HTTP ด้วย `respx` (สำหรับ httpx)

```python
import respx

@respx.mock
async def test_external_api():
    route = respx.get("https://api.example.com/users/1").mock(
        return_value=httpx.Response(200, json={"id": 1, "name": "Alice"})
    )

    result = await fetch_user(1)
    assert result["name"] == "Alice"
    assert route.called
    assert route.call_count == 1
```

---

## 3.6 Pattern: Factory สำหรับ Test Data

```bash
uv add --dev factory_boy faker
```

```python
# tests/factories.py
import factory
from factory.alchemy import SQLAlchemyModelFactory
from app.models import User, Order

class UserFactory(SQLAlchemyModelFactory):
    class Meta:
        model = User
        sqlalchemy_session_persistence = "commit"

    name = factory.Faker("name", locale="th_TH")
    email = factory.Faker("email")
    is_active = True

class OrderFactory(SQLAlchemyModelFactory):
    class Meta:
        model = Order
        sqlalchemy_session_persistence = "commit"

    user = factory.SubFactory(UserFactory)
    total = factory.Faker("pyfloat", min_value=10, max_value=1000, right_digits=2)
    status = factory.Iterator(["pending", "paid", "shipped"])

# ใช้
async def test_user_can_have_multiple_orders(db_session):
    UserFactory._meta.sqlalchemy_session = db_session
    user = UserFactory()
    orders = OrderFactory.create_batch(3, user=user)
    await db_session.commit()

    assert len(user.orders) == 3
```

### Faker ใช้ได้ใน parametrize ด้วย

```python
import faker

fake = faker.Faker("th_TH")

@pytest.mark.parametrize("name", [fake.name() for _ in range(5)])
def test_can_save_thai_name(db_session, name):
    user = User(name=name)
    db_session.add(user)
    db_session.commit()
    assert db_session.get(User, user.id).name == name
```

---

## 3.7 Freeze Time ด้วย `freezegun`

> 💬 **freezegun คือ:** "หยุดเวลา" — test เรื่อง expiry, scheduling, timestamp โดยไม่ flaky

```bash
uv add --dev freezegun
```

```python
from freezegun import freeze_time
from datetime import datetime, timedelta

@freeze_time("2026-05-14 12:00:00")
def test_token_expires_in_15_minutes():
    token = create_access_token({"sub": "1"})
    payload = decode_token(token)
    assert payload["exp"] == int(datetime(2026, 5, 14, 12, 15).timestamp())

# Tick time ภายในเทส
def test_session_expires():
    with freeze_time("2026-01-01") as frozen:
        session = create_session()
        frozen.tick(timedelta(hours=2))
        assert session.is_expired()
```

---

## 3.8 Pattern: AsyncContextManager Mock

```python
# จะ patch async context manager ใช้ตัวช่วย
class AsyncContextManagerMock:
    def __init__(self, return_value):
        self.return_value = return_value
    async def __aenter__(self):
        return self.return_value
    async def __aexit__(self, *args):
        pass

@pytest.mark.asyncio
async def test_redis_lock(mocker):
    mock_redis = AsyncMock()
    mock_redis.lock.return_value = AsyncContextManagerMock(None)
    mocker.patch("app.cache.r", mock_redis)

    await process_with_lock("key1")
    mock_redis.lock.assert_called_once_with("lock:key1", timeout=5)
```

---

<a id="phase-4"></a>

# Phase 4: สู่ Production — CI/CD & Best Practices

> "เทสที่รันแค่บนเครื่อง dev = เทสที่ไม่มีอยู่จริง"

## 4.1 Code Coverage ด้วย pytest-cov

```bash
uv add --dev pytest-cov
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

# Multiple reports
pytest --cov=app --cov-report=term --cov-report=html --cov-report=xml
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
    "@abstractmethod",
]
fail_under = 80
show_missing = true
skip_covered = false
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
uv add --dev locust
```

> 💬 **Locust คือ:** "user จำลอง 1000 คนยิงพร้อมกัน" — วัดว่า server รับได้ไหม

### `locustfile.py`

```python
from locust import HttpUser, task, between, events

class WebsiteUser(HttpUser):
    wait_time = between(1, 3)    # delay ระหว่าง request

    def on_start(self):
        """รันก่อน user แต่ละคนเริ่ม — login + เก็บ token"""
        response = self.client.post("/login", json={
            "username": "test",
            "password": "test"
        })
        self.token = response.json()["access_token"]
        self.client.headers.update({"Authorization": f"Bearer {self.token}"})

    @task(3)    # weight = ทำบ่อยกว่า task อื่น 3 เท่า
    def get_items(self):
        self.client.get("/items")

    @task(1)
    def create_item(self):
        self.client.post("/items", json={"name": "Test", "price": 10})

    @task(2)
    def search_items(self):
        self.client.get("/items/search", params={"q": "apple"}, name="/items/search")
        # ↑ ใช้ name= เพื่อรวม endpoint ที่มี query param ต่างกันให้นับเป็น 1 group

@events.test_start.add_listener
def on_test_start(environment, **kwargs):
    print("🚀 Load test starting")

@events.request.add_listener
def on_request(request_type, name, response_time, response_length, exception, **kwargs):
    if exception:
        print(f"❌ {name}: {exception}")
```

### รัน

```bash
# Web UI ที่ http://localhost:8089
locust -f locustfile.py --host=http://localhost:8000

# Headless mode (CI-friendly)
locust -f locustfile.py --host=http://localhost:8000 \
    --users 100 --spawn-rate 10 --run-time 5m --headless \
    --html report.html --csv results
```

### Metrics ที่ต้องดู

| Metric                | ภาษาชาวบ้าน                        | เป้า                          |
| --------------------- | ---------------------------------- | ----------------------------- |
| **Requests/sec**      | "ความถี่ที่ทำได้"                  | สูงกว่า expected traffic 2-3x |
| **p50 latency**       | "เวลาตอบกลาง"                      | < 200ms (web)                 |
| **p95 latency**       | "เวลาตอบ 95% ของลูกค้า"            | < 500ms                       |
| **p99 latency**       | "เวลาตอบ worst case ของลูกค้าจริง" | < 1s                          |
| **Failure rate**      | "% request ที่ตก"                  | ≈ 0%                          |
| **Connection errors** | "เซิร์ฟเวอร์ตก"                    | 0                             |

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

      redis:
        image: redis:7
        ports:
          - 6379:6379
        options: >-
          --health-cmd "redis-cli ping"
          --health-interval 5s

    strategy:
      fail-fast: false
      matrix:
        python-version: ["3.11", "3.12"]

    steps:
      - uses: actions/checkout@v4

      - name: Install uv
        uses: astral-sh/setup-uv@v3
        with:
          version: "latest"
          enable-cache: true

      - name: Set up Python ${{ matrix.python-version }}
        run: uv python install ${{ matrix.python-version }}

      - name: Install dependencies
        run: uv sync --frozen --all-extras

      - name: Lint with ruff
        run: uv run ruff check app tests

      - name: Format check with ruff
        run: uv run ruff format --check app tests

      - name: Type check with mypy
        run: uv run mypy app

      - name: Run tests with coverage
        env:
          DATABASE_URL: postgresql+asyncpg://test:test@localhost:5432/test_db
          REDIS_URL: redis://localhost:6379/0
          SECRET_KEY: test-secret-key-32-characters-long-x
        run: |
          uv run pytest \
            --cov=app --cov-report=xml --cov-report=term-missing \
            --cov-fail-under=80 \
            -n auto

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
- **cache** uv/pip ลดเวลา install
- แยก **lint / type-check / test** เป็น step ต่างกัน → debug ง่าย
- เก็บ **artifact** ไว้ดู report ภายหลัง
- ใช้ `pytest -n auto` เพื่อ parallel

---

## 4.4 โครงสร้าง Folder สำหรับโปรเจกต์ขนาดใหญ่

```
my_project/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── api/v1/users.py
│   ├── core/
│   ├── models/
│   ├── schemas/
│   ├── services/
│   └── repositories/
│
├── tests/
│   ├── __init__.py
│   ├── conftest.py             # global fixtures (client, db_session)
│   ├── factories.py            # factory_boy data factories
│   │
│   ├── unit/                   # ⚡ เร็ว, ไม่ touch DB/network
│   │   ├── conftest.py
│   │   ├── services/test_user_service.py
│   │   └── utils/
│   │
│   ├── integration/            # 🔌 touch DB จริง / Redis
│   │   ├── conftest.py
│   │   ├── repositories/test_user_repo.py
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
├── .github/workflows/
│   ├── tests.yml
│   └── deploy.yml
│
├── pyproject.toml
└── README.md
```

### หลักการแยกชั้น

| Layer           | ความเร็ว     | Mock อะไร             | สัดส่วน |
| --------------- | ------------ | --------------------- | ------- |
| **unit**        | < 0.1s/test  | ทุก dependency ภายนอก | 70%     |
| **integration** | < 1s/test    | external API เท่านั้น | 25%     |
| **e2e**         | หลายวินาที   | ไม่ mock เลย          | 5%      |
| **load**        | นาที-ชั่วโมง | -                     | manual  |

### `conftest.py` หลายระดับ

```
tests/conftest.py            → fixtures ทุกเทส (client, db, fake_redis)
tests/unit/conftest.py       → fixtures unit เท่านั้น (mocks)
tests/integration/conftest.py → fixtures DB จริง
```

---

## 4.5 Best Practices สำหรับ Production

### ✅ Do

- รัน lint + type-check + test ใน pre-commit hook
- แบ่ง marker `@pytest.mark.slow` ให้ skip ใน dev loop (`pytest -m "not slow"`)
- ใช้ `pytest-xdist` รันเทสคู่ขนาน: `pytest -n auto`
- ตั้ง coverage threshold 70-80% (อย่าตั้ง 100% บังคับ)
- เทส **error path** เท่ากับ happy path
- เทส migration ก่อน deploy (`alembic upgrade head` แล้ว `alembic downgrade base`)
- เก็บ test fixtures ใน folder แยก (`tests/fixtures/`)
- ใช้ `pytest --collect-only` ก่อน push เพื่อตรวจว่า test ทุกตัว discoverable

### ❌ Don't

- อย่ายิง API จริง / ส่งอีเมลจริง / ส่ง LINE จริงในเทส
- อย่าใช้ `time.sleep()` ในเทส — ใช้ `freezegun` หรือ inject clock
- อย่าใช้ random seed ที่ไม่ fix — ใช้ `factory.Faker` หรือ fix `random.seed()`
- อย่าทิ้ง state ระหว่างเทส — rollback / cleanup ทุกครั้ง
- อย่า skip flaky test — แก้ให้หาย ไม่งั้นจะเกิด tests ที่ "passed" หลอกๆ
- อย่า assert ละเอียดจน test fragile (เช่น `assert dict == {exact: huge}`) — assert เฉพาะที่ matter
- อย่า test ที่ implementation detail (private method) — test public behavior

---

## 4.6 Tools เสริมที่ควรรู้

| Tool                    | ใช้ทำอะไร                            | ภาษาชาวบ้าน                      |
| ----------------------- | ------------------------------------ | -------------------------------- |
| `pytest-xdist`          | รันเทสคู่ขนาน (`-n auto`)            | "กระจายงานหลาย CPU"              |
| `pytest-mock`           | `mocker` fixture แทน `unittest.mock` | "mock ง่ายขึ้น"                  |
| `pytest-randomly`       | shuffle ลำดับเทส                     | "จับ test ที่ขึ้นกับลำดับ"       |
| `pytest-timeout`        | กัน test ค้าง                        | "หยุดถ้านานเกิน"                 |
| `pytest-sugar`          | UI สวยขึ้น                           | "ปรับ output ให้อ่านง่าย"        |
| `pytest-benchmark`      | เทส performance regression           | "วัดเวลา function"               |
| `pytest-snapshot`       | snapshot testing                     | "เทียบกับ snapshot ที่ save ไว้" |
| `freezegun`             | freeze เวลา                          | "หยุดเวลา"                       |
| `time-machine`          | freezegun แต่เร็วกว่า                | "หยุดเวลา (รุ่นใหม่)"            |
| `responses`             | mock `requests`                      | "API ปลอม sync"                  |
| `respx`                 | mock `httpx`                         | "API ปลอม async"                 |
| `vcrpy`                 | record + replay HTTP                 | "อัด HTTP ไว้ replay"            |
| `factory_boy`           | สร้าง test data                      | "โรงงาน test data"               |
| `polyfactory`           | จาก Pydantic                         | "factory แบบ type-safe"          |
| `hypothesis`            | property-based testing               | "AI สุ่ม input ให้"              |
| `mutmut` / `cosmic-ray` | mutation testing                     | "ตรวจคุณภาพ test"                |
| `schemathesis`          | API fuzz test จาก OpenAPI            | "fuzz API อัตโนมัติ"             |
| `playwright`            | browser E2E                          | "ลูกค้าจำลองในเบราว์เซอร์"       |

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
- [ ] มี smoke test สำหรับ critical path (login, checkout, etc.)
- [ ] Performance test runs nightly บน staging

---

<a id="phase-5"></a>

# Phase 5: Testing Libraries Class Reference (ครบทุกตัว)

> 💬 ส่วนนี้คือ **คู่มืออ้างอิงแบบเปิดดูได้** — ทุก class/method สำคัญพร้อมตัวอย่าง

## 5.1 `pytest` Core

### `pytest.fixture`

> 💬 **คือ:** decorator สร้าง fixture (ตัวเตรียมของ)

```python
@pytest.fixture(
    scope="function",        # function/class/module/package/session
    params=[1, 2, 3],        # generate test ต่อค่า param
    autouse=False,           # apply ทุก test ที่ scope ครอบไหม
    ids=["a", "b", "c"],     # ชื่อแสดงใน output
    name="custom_name",      # alias ของ fixture
)
def my_fixture(request):
    return request.param * 10
```

### `pytest.mark`

| Marker             | ทำอะไร                                | ตัวอย่าง                                 |
| ------------------ | ------------------------------------- | ---------------------------------------- |
| `mark.parametrize` | inject ค่าหลายชุด                     | `@pytest.mark.parametrize("x", [1,2])`   |
| `mark.skip`        | ข้าม test                             | `@pytest.mark.skip(reason="WIP")`        |
| `mark.skipif`      | ข้ามถ้าตรง condition                  | `@pytest.mark.skipif(sys.version < ...)` |
| `mark.xfail`       | คาดว่า fail (known bug)               | `@pytest.mark.xfail`                     |
| `mark.usefixtures` | ใช้ fixture แต่ไม่ inject             | `@pytest.mark.usefixtures("db")`         |
| `mark.asyncio`     | mark async test (ถ้าไม่ใช้ auto mode) | `@pytest.mark.asyncio`                   |
| `mark.timeout`     | timeout (pytest-timeout)              | `@pytest.mark.timeout(5)`                |
| `mark.<custom>`    | custom marker                         | `@pytest.mark.slow`                      |

### `pytest.raises` — assert exception

```python
with pytest.raises(ValueError):
    do_bad_thing()

# Match regex
with pytest.raises(ValueError, match=r"invalid.*format"):
    do_bad_thing()

# Capture exception
with pytest.raises(ValueError) as exc_info:
    do_bad_thing()
assert exc_info.value.args[0] == "specific error"
assert exc_info.type is ValueError
```

### `pytest.warns` — assert warning

```python
with pytest.warns(DeprecationWarning, match="use .* instead"):
    legacy_function()
```

### `pytest.approx` — float comparison

```python
assert 0.1 + 0.2 == pytest.approx(0.3)
assert [0.1, 0.2] == pytest.approx([0.1, 0.2])
assert 1000 == pytest.approx(1001, rel=1e-3)        # 0.1% tolerance
assert 1000 == pytest.approx(1001, abs=10)          # ±10
```

### `pytest.MonkeyPatch` (via fixture)

```python
def test_env(monkeypatch):
    monkeypatch.setenv("KEY", "value")
    monkeypatch.delenv("OTHER", raising=False)
    monkeypatch.setattr("module.attribute", new_value)
    monkeypatch.setitem(some_dict, "key", "value")
    monkeypatch.chdir("/tmp")
    monkeypatch.syspath_prepend("/custom/path")
```

---

## 5.2 `unittest.mock`

### `MagicMock`

> 💬 **คือ:** "Mock อเนกประสงค์" — มี magic method ครบ (`__call__`, `__len__`, etc.)

```python
from unittest.mock import MagicMock

mock = MagicMock()

# Return value
mock.method.return_value = 42
mock.method()              # → 42

# Side effect (exception)
mock.method.side_effect = ValueError("oops")
mock.method()              # → raises ValueError

# Side effect (function)
mock.method.side_effect = lambda x: x * 2
mock.method(5)             # → 10

# Side effect (iterable — return per call)
mock.method.side_effect = [1, 2, 3]
mock.method()              # → 1
mock.method()              # → 2

# Configure on init
mock = MagicMock(return_value=10, name="my_mock")

# Spec — restrict to actual class API
mock = MagicMock(spec=MyService)
mock.real_method()         # OK
mock.fake_method()         # AttributeError!
```

### `AsyncMock`

```python
from unittest.mock import AsyncMock

mock = AsyncMock()
mock.method.return_value = "result"
result = await mock.method()        # → "result"
mock.method.assert_awaited_once()
```

### `patch`

```python
from unittest.mock import patch

# As decorator
@patch("module.path.function")
def test_x(mock_fn):
    mock_fn.return_value = 1
    ...

# As context manager
def test_y():
    with patch("module.path.function") as mock_fn:
        mock_fn.return_value = 1
        ...

# patch.object — patch attribute ของ object
with patch.object(MyClass, "method", return_value=42):
    ...

# patch.dict — patch dict
with patch.dict(os.environ, {"KEY": "value"}):
    ...

# patch multiple
@patch("module.a")
@patch("module.b")
def test_z(mock_b, mock_a):    # ⚠️ stack from bottom up
    ...
```

### Assertion methods

```python
mock.assert_called()                          # called at least once
mock.assert_called_once()                     # called exactly 1
mock.assert_called_with(1, 2, key="value")    # last call args
mock.assert_called_once_with(1, 2)            # exactly 1 + args
mock.assert_any_call(1, 2)                    # any call with these args
mock.assert_not_called()
mock.assert_has_calls([call(1), call(2)])     # in order
mock.assert_has_calls([call(1), call(2)], any_order=True)

# For AsyncMock
mock.assert_awaited()
mock.assert_awaited_once()
mock.assert_awaited_with(...)
mock.assert_awaited_once_with(...)

# Inspect
mock.call_count                # int
mock.call_args                 # call(arg1, arg2, key=value)
mock.call_args_list            # [call(...), call(...)]
mock.method_calls              # all method calls in tree
mock.mock_calls
```

---

## 5.3 `pytest-mock`

> 💬 **คือ:** wrapper รอบ `unittest.mock` ที่ให้ใช้เป็น fixture (`mocker`) — auto cleanup

```python
def test_x(mocker):
    # patch
    mock_fn = mocker.patch("module.function")
    mock_fn.return_value = 1

    # patch.object
    mock_method = mocker.patch.object(MyClass, "method")

    # patch.dict
    mocker.patch.dict("os.environ", {"KEY": "value"})

    # spy — เรียก function จริง + บันทึก call
    spy = mocker.spy(module, "function")
    function(1)
    spy.assert_called_once_with(1)

    # stub
    stub = mocker.stub(name="my_stub")
    callback(stub)
    stub.assert_called()
```

---

## 5.4 `factory_boy`

> 💬 **คือ:** "โรงงาน test data" — สร้าง object ที่มี default ครบ ไม่ต้อง type field ทุกตัวเอง

### `factory.Factory` (base — สำหรับ plain Python objects)

```python
import factory

class UserFactory(factory.Factory):
    class Meta:
        model = User

    name = "default name"
    age = 25

UserFactory()                       # User(name="default name", age=25)
UserFactory(name="Alice")           # override
UserFactory.build()                 # ไม่ save
UserFactory.create()                # save (ถ้า has session)
UserFactory.create_batch(5)         # list of 5
UserFactory.build_batch(3, age=30)
```

### `factory.alchemy.SQLAlchemyModelFactory`

```python
from factory.alchemy import SQLAlchemyModelFactory

class UserFactory(SQLAlchemyModelFactory):
    class Meta:
        model = User
        sqlalchemy_session = db_session
        sqlalchemy_session_persistence = "commit"   # "flush" หรือ "commit"

    name = factory.Faker("name")
```

### Field declarations

| Declaration                                                | ใช้ทำอะไร                |
| ---------------------------------------------------------- | ------------------------ |
| `factory.Sequence(lambda n: f"user{n}")`                   | auto-increment           |
| `factory.Faker("name", locale="th_TH")`                    | fake data                |
| `factory.LazyFunction(datetime.now)`                       | call function ตอน create |
| `factory.LazyAttribute(lambda o: f"{o.name}@example.com")` | depend on other field    |
| `factory.SubFactory(UserFactory)`                          | nested object            |
| `factory.RelatedFactory(OrderFactory, "user")`             | one-to-many              |
| `factory.Iterator(["a", "b", "c"])`                        | cycle through values     |
| `factory.RandomChoice([1, 2, 3])`                          | random pick              |
| `factory.Trait(...)`                                       | named variant            |
| `factory.PostGeneration(...)`                              | hook after create        |

### Traits (named variants)

```python
class UserFactory(SQLAlchemyModelFactory):
    class Meta:
        model = User

    name = factory.Faker("name")
    is_active = True
    role = "viewer"

    class Params:
        admin = factory.Trait(role="admin", is_active=True)
        banned = factory.Trait(is_active=False)

UserFactory(admin=True)              # role="admin"
UserFactory(banned=True)             # is_active=False
```

### PostGeneration

```python
class UserFactory(SQLAlchemyModelFactory):
    name = factory.Faker("name")

    @factory.post_generation
    def groups(obj, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for g in extracted:
                obj.groups.append(g)

UserFactory(groups=[admin_group, editor_group])
```

---

## 5.5 `faker`

> 💬 **คือ:** "เครื่องปั่นข้อมูลปลอมจริงสมจริง" — สร้างชื่อ, email, address, เลข ปลอมตามรูปแบบ

```python
from faker import Faker

fake = Faker()                       # English (default)
fake_th = Faker("th_TH")             # Thai

fake.name()                          # "John Smith"
fake.first_name()
fake.last_name()
fake.email()
fake.phone_number()
fake.address()                       # multi-line

fake_th.name()                       # "สมชาย ใจดี"
fake_th.address()                    # ที่อยู่ไทย

# Date / time
fake.date_of_birth(minimum_age=18, maximum_age=80)
fake.date_between(start_date="-30y", end_date="today")
fake.future_datetime(end_date="+30d")

# Numbers
fake.random_int(min=1, max=100)
fake.pyfloat(min_value=0, max_value=1000, right_digits=2)
fake.pydecimal(left_digits=5, right_digits=2)

# Text
fake.sentence(nb_words=10)
fake.paragraph()
fake.text(max_nb_chars=200)

# Internet
fake.url()
fake.ipv4()
fake.ipv6()
fake.mac_address()
fake.user_agent()
fake.domain_name()

# Misc
fake.uuid4()
fake.color_name()
fake.currency_code()
fake.credit_card_number()
fake.iban()
fake.ssn()

# Localized (Thai)
fake_th.thai_id_card()               # 13-digit ID
fake_th.province()
fake_th.tambon()
```

### Reproducible (seed)

```python
Faker.seed(12345)
fake = Faker()
fake.name()                          # เดิมทุกครั้งเมื่อ seed เดิม
```

---

## 5.6 `freezegun`

```python
from freezegun import freeze_time
from datetime import datetime, timedelta

# As decorator
@freeze_time("2026-05-14 12:00:00")
def test_x():
    assert datetime.now() == datetime(2026, 5, 14, 12, 0)

# As context manager
def test_y():
    with freeze_time("2026-01-01"):
        ...

# Tick
def test_z():
    with freeze_time("2026-01-01", tick=True) as frozen:
        # tick=True → เวลาเดินจริง
        ...
        frozen.tick(timedelta(hours=1))
        ...
        frozen.move_to("2026-06-01")

# Function form
freezer = freeze_time("2026-01-01")
freezer.start()
# ... code
freezer.stop()

# Ignore certain modules (เช่น tqdm)
freeze_time("2026", ignore=["tqdm"])
```

---

## 5.7 `respx` (mock httpx)

```python
import respx
import httpx
from httpx import Response

@respx.mock
async def test_external_api():
    # Mock GET
    route = respx.get("https://api.example.com/users/1").mock(
        return_value=Response(200, json={"id": 1, "name": "Alice"})
    )
    result = await fetch_user(1)
    assert route.called

# As context manager
async def test_y():
    async with respx.mock(base_url="https://api.example.com") as mock:
        mock.get("/users/1").respond(200, json={"id": 1})
        mock.post("/users").respond(201)
        mock.delete("/users/1").respond(204)

# Pattern matching
respx.get(url__regex=r"https://api\.example\.com/users/\d+")
respx.post("/users", json__name="Alice")
respx.get("/users", params={"limit": 10})

# Different responses per call
route = respx.get("/health").mock(side_effect=[
    Response(503),       # first call → 503
    Response(200),       # second → 200
])

# Pass-through (call real API)
respx.get("/local").pass_through()

# Inspect calls
assert route.called
assert route.call_count == 2
assert route.calls.last.request.url.path == "/users/1"
```

---

## 5.8 `hypothesis` — Property-Based Testing

> 💬 **คือ:** "AI generate input ปลอมเพื่อหา edge case" — เขียน property ทั่วไป แล้ว hypothesis สุ่มลอง 100+ case

```python
from hypothesis import given, strategies as st

@given(st.integers())
def test_double_is_even(n):
    assert (n * 2) % 2 == 0

@given(st.lists(st.integers()))
def test_reverse_twice_equals_original(lst):
    assert list(reversed(list(reversed(lst)))) == lst

@given(st.text(min_size=1, max_size=100))
def test_strip_idempotent(s):
    assert s.strip().strip() == s.strip()

# Composite strategies
@given(
    name=st.text(min_size=1, max_size=50),
    age=st.integers(min_value=0, max_value=150),
    email=st.emails(),
)
def test_create_user(name, age, email):
    user = User(name=name, age=age, email=email)
    assert user.name == name
```

### Built-in strategies

| Strategy                                                | ตัวอย่าง         |
| ------------------------------------------------------- | ---------------- |
| `st.integers(min_value=0, max_value=100)`               | int ในช่วง       |
| `st.floats(allow_nan=False, allow_infinity=False)`      | float            |
| `st.text(alphabet="abc", min_size=1)`                   | string           |
| `st.booleans()`                                         | bool             |
| `st.dates()` / `st.datetimes()`                         | dates            |
| `st.lists(st.integers(), min_size=1, max_size=10)`      | lists            |
| `st.dictionaries(keys=st.text(), values=st.integers())` | dicts            |
| `st.tuples(st.integers(), st.text())`                   | tuple            |
| `st.one_of(st.text(), st.integers())`                   | union            |
| `st.emails()`, `st.ip_addresses()`, `st.uuids()`        | semantic         |
| `st.builds(User, name=st.text(), age=st.integers())`    | build from class |

### Settings & decorators

```python
from hypothesis import settings, Verbosity, example

@settings(max_examples=500, deadline=300, verbosity=Verbosity.verbose)
@given(st.integers())
@example(0)                          # always test edge case
@example(-1)
def test_x(n):
    ...
```

---

## 5.9 `httpx.AsyncClient` (สำหรับ test ASGI app)

```python
from httpx import AsyncClient, ASGITransport

@pytest.mark.asyncio
async def test_async_api():
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    ) as ac:
        response = await ac.get("/items")
        assert response.status_code == 200

        # POST with JSON
        response = await ac.post("/items", json={"name": "Apple"})

        # Headers
        response = await ac.get("/me", headers={"Authorization": "Bearer xxx"})

        # Query params
        response = await ac.get("/search", params={"q": "apple", "limit": 10})

        # File upload
        with open("test.jpg", "rb") as f:
            response = await ac.post("/upload", files={"file": f})

        # Form data
        response = await ac.post("/login", data={"username": "a", "password": "b"})
```

---

## 5.10 `fastapi.testclient.TestClient` (sync)

> 💬 **คือ:** based on `httpx.Client` (sync) — เรียก ASGI app ตรงๆ

```python
from fastapi.testclient import TestClient

client = TestClient(app)

# Basic
response = client.get("/")
response = client.post("/items", json={...})
response = client.put("/items/1", json={...})
response = client.patch("/items/1", json={...})
response = client.delete("/items/1")

# Headers / Cookies / Params
response = client.get("/", headers={"X-Token": "secret"})
response = client.get("/", cookies={"session": "abc"})
response = client.get("/search", params={"q": "term"})

# Auth shortcuts
response = client.get("/secure", auth=("user", "pass"))            # Basic auth
response = client.get("/secure", auth=BearerAuth("token"))         # Custom auth

# Response inspection
response.status_code
response.json()
response.text
response.content                   # bytes
response.headers
response.cookies
response.url

# Context manager (for lifespan events)
with TestClient(app) as client:
    # ทำให้ startup events ทำงาน
    response = client.get("/")
# ↑ shutdown events ทำงานตอนออก

# WebSocket
with client.websocket_connect("/ws") as websocket:
    websocket.send_text("hello")
    data = websocket.receive_text()
    websocket.close()
```

---

## 5.11 `testcontainers`

```python
from testcontainers.postgres import PostgresContainer
from testcontainers.redis import RedisContainer
from testcontainers.minio import MinioContainer

@pytest.fixture(scope="session")
def postgres():
    with PostgresContainer("postgres:16-alpine") as pg:
        yield pg

@pytest.fixture(scope="session")
def redis():
    with RedisContainer("redis:7-alpine") as r:
        yield r.get_connection_url()

@pytest.fixture(scope="session")
def minio():
    with MinioContainer() as m:
        yield m

# Generic container
from testcontainers.core.container import DockerContainer

@pytest.fixture
def custom_container():
    container = (
        DockerContainer("my-image:latest")
        .with_exposed_ports(8080)
        .with_env("KEY", "value")
        .with_volume_mapping("/host/path", "/container/path")
    )
    with container as c:
        yield c
```

---

## 5.12 `locust` Classes

### `HttpUser` / `FastHttpUser`

```python
from locust import HttpUser, FastHttpUser, task, between, constant

class BasicUser(HttpUser):
    wait_time = between(1, 5)           # delay 1-5 วินาที
    # wait_time = constant(2)           # fixed 2 sec

    host = "http://localhost:8000"      # default base URL

    def on_start(self):
        """ทำเมื่อ user เริ่ม"""
        pass

    def on_stop(self):
        """ทำเมื่อ user หยุด"""
        pass

    @task
    def index(self):
        self.client.get("/")

    @task(3)                            # weight = 3
    def items(self):
        self.client.get("/items")
```

### `TaskSet` (group tasks)

```python
from locust import TaskSet, task

class BrowsingBehavior(TaskSet):
    @task
    def list_items(self):
        self.client.get("/items")

    @task
    def view_item(self):
        self.client.get("/items/1")

class WebsiteUser(HttpUser):
    tasks = [BrowsingBehavior]
```

### `SequentialTaskSet`

```python
from locust import SequentialTaskSet, task

class CheckoutFlow(SequentialTaskSet):
    @task
    def step1_login(self):
        self.client.post("/login", json={...})

    @task
    def step2_add_to_cart(self):
        self.client.post("/cart", json={...})

    @task
    def step3_checkout(self):
        self.client.post("/checkout")
```

---

## 5.13 SQLAlchemy Testing Helpers

```python
from sqlalchemy.pool import StaticPool
from sqlalchemy import create_engine, event

# SQLite in-memory ต้อง StaticPool + connect_args
engine = create_engine(
    "sqlite:///:memory:",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

# Listener (debugging)
@event.listens_for(engine, "before_cursor_execute")
def log_sql(conn, cursor, statement, params, context, executemany):
    print(f"SQL: {statement}")
    print(f"Params: {params}")

# Inspector
from sqlalchemy import inspect
insp = inspect(engine)
insp.get_table_names()
insp.get_columns("users")
insp.get_foreign_keys("posts")
```

---

## 5.14 Real-World Example — Combined

```python
# tests/integration/api/test_orders.py
import pytest
from datetime import datetime
from freezegun import freeze_time
import respx
from httpx import Response
from tests.factories import UserFactory, ProductFactory, OrderFactory

@pytest.mark.asyncio
@freeze_time("2026-05-14 10:00:00")
async def test_create_order_charges_payment_and_sends_email(
    client,
    db_session,
    mocker,
):
    # Arrange
    user = UserFactory(email="buyer@example.com")
    product = ProductFactory(price=100, stock=10)
    await db_session.commit()

    mock_email = mocker.patch("app.services.email.send_email", new=AsyncMock())

    with respx.mock(base_url="https://api.stripe.com") as stripe:
        stripe.post("/charges").mock(
            return_value=Response(200, json={"id": "ch_123", "status": "succeeded"})
        )

        # Act
        response = await client.post(
            "/orders",
            json={"product_id": product.id, "quantity": 2},
            headers={"Authorization": f"Bearer {make_token(user)}"},
        )

        # Assert — response
        assert response.status_code == 201
        body = response.json()
        assert body["total"] == 200
        assert body["status"] == "paid"
        assert body["created_at"] == "2026-05-14T10:00:00"

        # Assert — DB
        await db_session.refresh(product)
        assert product.stock == 8

        # Assert — Stripe was called
        assert stripe.calls.call_count == 1
        assert stripe.calls.last.request.url.path == "/charges"

        # Assert — email sent
        mock_email.assert_awaited_once_with(
            to="buyer@example.com",
            subject="Order confirmation",
        )
```

---

## 🎯 สรุปทั้งคู่มือ

| Phase | สิ่งที่ได้                                   | Library หลัก                                            |
| ----- | -------------------------------------------- | ------------------------------------------------------- |
| **1** | เขียน unit test ตาม AAA + fixtures           | `pytest`                                                |
| **2** | เทส FastAPI endpoints + override deps        | `pytest`, `httpx`, `TestClient`                         |
| **3** | เทส DB จริง rollback pattern + mock external | `pytest-asyncio`, `aiosqlite`, `respx`, `unittest.mock` |
| **4** | Coverage, Load test, CI/CD                   | `pytest-cov`, `locust`, GitHub Actions                  |
| **5** | Class reference — เปิดดูตอน implement        | ทุก library                                             |

> "Tests are a safety harness for refactoring, a documentation that compiles, and a design tool that exposes bad coupling. Write them with the same care as production code — because they are."

---

## 📖 Resources

| Link                                                                | คำอธิบาย                           |
| ------------------------------------------------------------------- | ---------------------------------- |
| [pytest docs](https://docs.pytest.org)                              | docs ต้นฉบับ ครบ                   |
| [pytest-asyncio docs](https://pytest-asyncio.readthedocs.io)        | async testing                      |
| [factory_boy docs](https://factoryboy.readthedocs.io)               | data factories                     |
| [hypothesis docs](https://hypothesis.readthedocs.io)                | property-based testing             |
| [Locust docs](https://docs.locust.io)                               | load testing                       |
| [respx docs](https://lundberg.github.io/respx/)                     | httpx mocking                      |
| [Real Python — Testing](https://realpython.com/python-testing/)     | tutorial ดีๆ                       |
| Book: _Architecture Patterns with Python_                           | layered + testable architecture    |
| Book: _Test-Driven Development with Python_ (Obey the Testing Goat) | TDD เน้น Django แต่หลักการเดียวกัน |
