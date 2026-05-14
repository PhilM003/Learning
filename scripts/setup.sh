# สร้าง venv
python -m venv lecture_env
# Activate และติดตั้ง library รวมถึง ipykernel
.\lecture_env\Scripts\Activate.ps1
pip install -r requirement.txt
pip install ipykernel
# ลงทะเบียน Kernel ให้ Jupyter มองเห็น
python -m ipykernel install --user --name lecture_env --display-name "Python (lecture_env)"
Write-Host "Setup Complete! Please restart VS Code and select 'Python (lecture_env)' kernel." -ForegroundColor Green