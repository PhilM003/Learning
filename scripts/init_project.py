import os
import sys
import subprocess
import platform


def run_command(cmd):
    try:
        subprocess.run(cmd, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Error occurred: {e}")


# ตรวจสอบตำแหน่งที่รันสคริปต์ เพื่อให้ชี้ไปที่ Root ของโปรเจกต์เสมอ
base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
os.chdir(base_dir)

venv_name = "lecture_env"
is_windows = platform.system() == "Windows"

if is_windows:
    python_path = os.path.join(venv_name, "Scripts", "python.exe")
    pip_path = os.path.join(venv_name, "Scripts", "pip.exe")
else:
    python_path = os.path.join(venv_name, "bin", "python")
    pip_path = os.path.join(venv_name, "bin", "pip")

# 1. สร้าง venv
if not os.path.exists(venv_name):
    print(f"📦 Creating virtual environment in {base_dir}...")
    run_command(f"{sys.executable} -m venv {venv_name}")

# 2. ติดตั้ง Dependencies
if os.path.exists("requirement.txt"):
    print("📥 Installing requirements...")
    run_command(f"{pip_path} install -r requirement.txt")
    run_command(f"{pip_path} install ipykernel")

# 3. ลงทะเบียน Kernel สำหรับ Jupyter
print("⚙️ Registering Jupyter Kernel...")
run_command(
    f'{python_path} -m ipykernel install --user --name {venv_name} --display-name "Python ({venv_name})"'
)

print("\n✅ Setup Complete! Please restart VS Code to apply changes.")
