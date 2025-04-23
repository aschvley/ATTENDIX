# 🧠 Attendix — Sistema de Asistencia con Reconocimiento Facial
**Attendix** es un sistema inteligente que automatiza el registro de asistencia de estudiantes mediante reconocimiento facial, utilizando Python, OpenCV, DeepFace y una base de datos MySQL.

---

## 📁 Estructura del Proyecto

```
ATTENDIX/
├── attendance/               # Lógica para manejo de asistencia
│   └── attendance.py
│
├── database/                 # Módulo de conexión y gestión de la base de datos
│   └── db.py
│
├── face_recognition/        # Módulo de reconocimiento facial
│   ├── detect_face.py       # Detección de rostros con OpenCV
│   ├── embedder.py          # Generación de embeddings con FaceNet
│   └── recognizer.py        # Comparación y reconocimiento de rostros
│
├── UI/                      # Interfaz de usuario con PyQt5
│   ├── components/          # Widgets personalizados
│   ├── resources/           # Imágenes, íconos, y assets visuales
│   └── views/               # Vistas principales de la interfaz
│       └── main_window.py   # Ventana principal de la aplicación
│
├── .gitignore               # Archivos ignorados por Git
├── config.py                # Configuraciones globales del sistema
├── main.py                  # Punto de entrada de la aplicación
├── recognizer_main.py       # Script de reconocimiento facial (interfaz CLI)
├── register_user.py         # Registro de nuevos estudiantes
├── ver_asistencias.py       # Visualización de registros de asistencia
├── PRUEBAS.py               # Archivo auxiliar de pruebas
├── requirements.txt         # Lista de dependencias
└── readme.md                # Este archivo

```

---

## 🛠 Tecnologías Usadas
- 🐍 Python 3.11  
- 👁 OpenCV  
- 🧬 DeepFace  
- 🗃 MySQL  
- 🧩 VSCode + SQLTools

---

## 🧼 Sistema de Limpieza Automática
Este proyecto incluye un script en PowerShell (clean_project.ps1) que permite limpiar de forma automática archivos temporales, carpetas de caché y archivos compilados de Python.

### 🔧 ¿Qué elimina el script?
- Carpetas __pycache__
- Carpetas que contienen cache en su nombre
- Archivos .pyc y .pyo
- Archivos temporales .tmp
- Logs antiguos (.log) (si decides incluirlo también)

### ▶️ Cómo usarlo:
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
```
DB_HOST=localhost
DB_USER=tu_usuario
DB_PASSWORD=tu_contraseña
DB_NAME=nombre_de_tu_bd
```

4. **Ejecuta el sistema**:
python recognizer_main.py

---

## 🧪 Estado del Proyecto
> **🔧 En desarrollo** — Actualmente trabajando en la interfaz gráfica (UI) con PyQt5 y QFluentWidgets.

---

## 📌 Autoría
Proyecto desarrollado por Camila Velázquez, UI diseñada por Valeria Velásquez, Victor Pérez, Hardware proporcionado por Maria Castillo ✨  
*(Uso académico — Sistema para automatizar asistencia en aulas escolares con visión artificial)*
