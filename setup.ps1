# เช็คว่ามี Python ติดตั้งอยู่ไหม
if (!(Get-Command python -ErrorAction SilentlyContinue)) {
    Write-Host "❌ Python is not installed!" -ForegroundColor Red
    Write-Host "Opening Python download page..."
    Start-Process "https://www.python.org/downloads/"
    exit
}

# ถ้ามี Python ให้รันสคริปต์ init_project.py ต่อ
python scripts/init_project.py