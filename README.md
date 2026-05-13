---
# 📘 Project Learning Python & Jupyter

โปรเจกต์นี้จัดทำขึ้นเพื่อการเรียนรู้การเขียนโปรแกรมด้วย Python และ Jupyter Notebook โดยเน้นโครงสร้างที่เป็นระเบียบและการจัดการสภาพแวดล้อมจำลอง (Virtual Environment) ที่รันได้ทันทีทั้งบน Windows และ Linux
---

## 📁 โครงสร้างโปรเจกต์ (Project Structure)

```text
.
├── .vscode/               # การตั้งค่าสำหรับ VS Code (Automatic Kernel Selection)
├── lectures/              # รวบรวมบทเรียน (.md) และโค้ดตัวอย่าง (.ipynb)
├── scripts/               # สคริปต์สำหรับการ Setup ระบบอัตโนมัติ
├── .gitignore             # ไฟล์ที่ Git จะไม่เก็บ (เช่น lecture_env)
├── requirement.txt        # รายการ Library ที่จำเป็นต้องใช้
├── setup.ps1              # สคริปต์เริ่มงานสำหรับ Windows (PowerShell)
├── setup.sh               # สคริปต์เริ่มงานสำหรับ Linux/macOS
└── README.md              # คู่มือการใช้งาน

```

---

## 🚀 เริ่มต้นใช้งาน (Getting Started)

เมื่อคุณทำการ Clone โปรเจกต์นี้มาแล้ว ให้ทำตามขั้นตอนดังนี้เพื่อให้ระบบพร้อมทำงาน:

### 1. การเตรียมสภาพแวดล้อม (First Time Setup)

เลือกวิธีรันตามระบบปฏิบัติการที่คุณใช้งาน:

- **สำหรับ Windows (PowerShell):**
  คลิกขวาที่ไฟล์ `setup.ps1` แล้วเลือก _Run with PowerShell_ หรือรันคำสั่งใน Terminal:

```powershell
.\setup.ps1

```

- **สำหรับ Linux / macOS:**
  เปิด Terminal แล้วรันคำสั่ง:

````bash
    bash setup.sh
    ```

> **หมายเหตุ:** สคริปต์จะทำการสร้างโฟลเดอร์ `lecture_env` ติดตั้ง Library ทั้งหมด และลงทะเบียน Kernel ให้ Jupyter โดยอัตโนมัติ

### 2. การเปิดใช้งานบน Visual Studio Code

1.  เปิดโปรเจกต์ด้วย VS Code
2.  ไปที่โฟลเดอร์ `lectures/` และเลือกไฟล์ที่ต้องการเรียนรู้ (เช่น `Leture101.ipynb`)
3.  **Kernel Selection:** VS Code จะเลือก Kernel ชื่อ `Python (lecture_env)` ให้โดยอัตโนมัติจากค่าที่เราตั้งไว้ใน `.vscode/settings.json`
4.  เริ่มรันโค้ดได้ทันที!

---

## 🛠️ รายละเอียดสคริปต์จัดการระบบ

ในโปรเจกต์นี้มีสคริปต์สำคัญ 3 ตัวที่ช่วยอำนวยความสะดวก:

1.  **`scripts/init_project.py`**: หัวใจหลักในการสร้าง venv และเช็กความต่างของ OS เพื่อลงทะเบียน Kernel ให้ถูกต้อง
2.  **`setup.ps1`**: สคริปต์ดักเช็กว่าเครื่อง Windows ของคุณมี Python หรือยัง ถ้าไม่มีจะพาไปหน้า Download ทันที
3.  **`setup.sh`**: สคริปต์สำหรับชาว Linux/macOS เพื่อความสะดวกในการรันคำสั่งเดียวจบ

---

## 📝 คำแนะนำเพิ่มเติมสำหรับการพัฒนา

*   **เมื่อต้องการเพิ่ม Library ใหม่:** ให้เพิ่มชื่อใน `requirement.txt` แล้วรันสคริปต์ Setup อีกครั้ง
*   **การจัดการ Git:** โปรเจกต์นี้ถูกตั้งค่า `.gitignore` ไว้แล้ว ไฟล์ขยะและโฟลเดอร์ `lecture_env` จะไม่ถูก Push ขึ้น GitHub เพื่อความสะอาดของ Repo

---

### รายละเอียดการจัดทำ
*   **Developer:** Film (Full-stack Developer)
*   **Environment:** รองรับ Python 3.x, Ubuntu 24.04 และ Windows 11

````
