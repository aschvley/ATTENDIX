# 🧠 Attendix — Sistema de Asistencia con Reconocimiento Facial
**Attendix** es un sistema inteligente que automatiza el registro de asistencia de estudiantes mediante reconocimiento facial, utilizando Python, OpenCV, FaceNet y una base de datos MySQL.

---

## 📁 Estructura del Proyecto

```
ATTENDIX/
├── attendance/
│   ├── __init__.py
│   └── attendance.py
│
├── database/
│   ├── __init__.py
│   └── db.py
│
├── face_recognition/
│   ├── __init__.py
│   ├── detect_face.py
│   ├── embedder.py
│   └── recognizer.py
│
├── .vscode/
│
├── __init__.py
├── .env
├── config.py
├── main.py
├── recognizer_main.py
├── register_user.py
├── ver_asistencias.py
├── PRUEBAS.py
├── introduccion/
├── readme
└── requirements.txt
```

---

## 🛠 Tecnologías Usadas
- 🐍 Python 3.x  
- 👁 OpenCV  
- 🧬 FaceNet  
- 🗃 MySQL  
- 🧩 VSCode + SQLTools

---

## 🧼 Sistema de Limpieza Automática
Este proyecto incluye un script en PowerShell (clean_project.ps1) que permite limpiar de forma automática archivos temporales, carpetas de caché y archivos compilados de Python.

## 🔧 ¿Qué elimina el script?
- Carpetas __pycache__
- Carpetas que contienen cache en su nombre
- Archivos .pyc y .pyo
- Archivos temporales .tmp
- Logs antiguos (.log) (si decides incluirlo también)

## ▶️ Cómo usarlo:
Desde PowerShell, ejecutar: 
```
.\clean_project.ps1
```
> 💡 Asegúrate de tener el archivo guardado con codificación UTF-8 con BOM para evitar errores de visualización si usas emojis en los mensajes del script.

---

## 🚀 Cómo Iniciar:
1. **Clona el repositorio** o copia el proyecto localmente.
2. **Instala las dependencias** necesarias:
pip install -r requirements.txt

3. **Crea un archivo `.env`** en la raíz del proyecto con tus credenciales de base de datos:
DB_HOST=localhost
DB_USER=tu_usuario
DB_PASSWORD=tu_contraseña
DB_NAME=nombre_de_tu_bd

4. **Ejecuta el sistema**:
python recognizer_main.py

---

## 🧪 Estado del Proyecto
> **🔧 En desarrollo** — Actualmente trabajando en la interfaz gráfica (UI) con PyQt5 y QFluentWidgets.

---

## 📌 Autoría
Proyecto desarrollado por Camila Velázquez, UI diseñada por Valeria Velásquez, Victor Pérez, Hardware proporcionado por Maria Castillo ✨  
*(Uso académico — Sistema para automatizar asistencia en aulas escolares con visión artificial)*
