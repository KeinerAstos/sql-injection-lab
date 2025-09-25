# Ciberseguridad - Laboratorio No. 1 - SQL Injection

## Instalación

1. Clonar/Descargar el repositorio

2. Crear el entorno virtual
```bash
python -m venv venv
```

3. Activar entorno virtual
```bash
venv\Scripts\activate
```

4. Instalar dependencias
```bash
pip install -r requirements.txt
```

5. Inicializar la base de datos
```bash
python database.py
```

6. Ejecutar la aplicación
```bash
python -m uvicorn vulnerable_app:app --reload --port 8000
```

7. Abrir en el navegador
```bash
http://localhost:8000
```