# Limpiar __pycache__, .pyc, .pyo y carpetas relacionadas al caché

Write-Host "🔍 Buscando carpetas '__pycache__'..."
Get-ChildItem -Path . -Recurse -Directory -Filter "__pycache__" |
    Remove-Item -Recurse -Force -ErrorAction SilentlyContinue

Write-Host "🧹 Eliminando carpetas que contienen 'cache' en su nombre..."
Get-ChildItem -Path . -Recurse -Directory |
    Where-Object { $_.Name -like "*cache*" } |
    Remove-Item -Recurse -Force -ErrorAction SilentlyContinue

Write-Host "🧽 Borrando archivos .pyc y .pyo..."
Get-ChildItem -Path . -Recurse -Include *.pyc, *.pyo -File |
    Remove-Item -Force -ErrorAction SilentlyContinue

Write-Host "🗑️ Borrando archivos temporales (.tmp)..."
Get-ChildItem -Path . -Recurse -Include *.tmp -File |
    Remove-Item -Force -ErrorAction SilentlyContinue

Write-Host "📄 Borrando archivos de log (.log)..."
Get-ChildItem -Path . -Recurse -Include *.log -File |
    Remove-Item -Force -ErrorAction SilentlyContinue

Write-Host "✅ Limpieza completada correctamente."
