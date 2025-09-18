from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse
import sqlite3
from database import init_database, get_connection
import os

# Crear la aplicación FastAPI
app = FastAPI(
    title="🔒 Laboratorio SQL Injection - VULNERABLE", 
    description="Entorno educativo para aprender sobre vulnerabilidades SQL",
    version="1.0.0"
)

# Configurar templates y archivos estáticos
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

# Inicializar base de datos al arrancar
if not os.path.exists('vulnerable_app.db'):
    print("🔧 Inicializando base de datos por primera vez...")
    init_database()

@app.on_event("startup")
async def startup_event():
    print("🚀 Laboratorio SQL Injection iniciado")
    print("🌐 Accede a: http://localhost:8000")
    print("⚠️  ATENCIÓN: Esta aplicación es INTENCIONALMENTE vulnerable")

# ============================================
# PÁGINA PRINCIPAL
# ============================================
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Página principal con menú de ejercicios"""
    return templates.TemplateResponse("index.html", {"request": request})

# ============================================
# EJERCICIO 1: LOGIN BYPASS
# ============================================
@app.get("/login", response_class=HTMLResponse)
async def login_form(request: Request):
    """Formulario de login vulnerable"""
    return templates.TemplateResponse("login.html", {"request": request})

@app.post("/login")
async def login_vulnerable(request: Request, username: str = Form(...), password: str = Form(...)):
    """
    LOGIN VULNERABLE - Permite SQL Injection
    
    Vulnerabilidades:
    - Concatenación directa de strings en SQL
    - Sin validación de entrada
    - Sin escape de caracteres especiales
    """
    conn = get_connection()
    cursor = conn.cursor()
    
    # 🚨 VULNERABLE: Concatenación directa de SQL
    query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
    
    # Mostrar la query en consola para fines educativos
    print(f"🔍 Query ejecutada: {query}")
    
    try:
        cursor.execute(query)
        result = cursor.fetchone()
        
        if result:
            # Login exitoso
            user_data = {
                "id": result[0],
                "username": result[1], 
                "email": result[3],
                "role": result[4]
            }
            return templates.TemplateResponse("login.html", {
                "request": request, 
                "success": True, 
                "user": user_data,
                "query": query,
                "message": "¡Login exitoso! SQL Injection funcionó."
            })
        else:
            # Credenciales incorrectas
            return templates.TemplateResponse("login.html", {
                "request": request, 
                "error": "Credenciales incorrectas",
                "query": query
            })
            
    except sqlite3.Error as e:
        # Error SQL (puede revelar información útil para el atacante)
        return templates.TemplateResponse("login.html", {
            "request": request, 
            "error": f"Error SQL: {str(e)}",
            "query": query,
            "sql_error": True
        })
    finally:
        conn.close()

# ============================================
# EJERCICIO 2: BÚSQUEDA VULNERABLE 
# ============================================
@app.get("/search", response_class=HTMLResponse)
async def search_form(request: Request):
    """Formulario de búsqueda de productos"""
    return templates.TemplateResponse("search.html", {"request": request})

@app.post("/search")
async def search_vulnerable(request: Request, search_term: str = Form(...)):
    """
    BÚSQUEDA VULNERABLE - Permite extraer datos con UNION
    
    Vulnerabilidades:
    - Concatenación directa en LIKE
    - Sin validación de entrada
    - Permite UNION SELECT
    """
    conn = get_connection()
    cursor = conn.cursor()
    
    # 🚨 VULNERABLE: Concatenación directa
    query = f"SELECT id, name, price, description FROM products WHERE name LIKE '%{search_term}%'"
    
    print(f"🔍 Query ejecutada: {query}")
    
    try:
        cursor.execute(query)
        results = cursor.fetchall()
        
        products = []
        for row in results:
            products.append({
                "id": row[0],
                "name": row[1],
                "price": row[2],
                "description": row[3]
            })
            
        return templates.TemplateResponse("search.html", {
            "request": request,
            "products": products,
            "search_term": search_term,
            "query": query,
            "results_count": len(products)
        })
        
    except sqlite3.Error as e:
        # Mostrar error SQL (información útil para el atacante)
        return templates.TemplateResponse("search.html", {
            "request": request,
            "error": f"Error SQL: {str(e)}",
            "query": query,
            "search_term": search_term
        })
    finally:
        conn.close()

# ============================================
# EJERCICIO 3: BLIND SQL INJECTION
# ============================================
@app.get("/user/{user_id}")
async def get_user_vulnerable(request: Request, user_id: str):
    """
    BLIND SQL INJECTION - Solo devuelve verdadero/falso
    
    Vulnerabilidades:
    - Sin validación de entrada
    - Permite condiciones booleanas
    - Información se puede extraer carácter por carácter
    """
    conn = get_connection()
    cursor = conn.cursor()
    
    # 🚨 VULNERABLE: Sin validación ni parámetros
    query = f"SELECT username FROM users WHERE id='{user_id}'"
    
    print(f"🔍 Query ejecutada: {query}")
    
    try:
        cursor.execute(query)
        result = cursor.fetchone()
        
        if result:
            return JSONResponse({
                "status": "success",
                "message": "Usuario encontrado", 
                "username": result[0],
                "query": query
            })
        else:
            return JSONResponse({
                "status": "not_found",
                "message": "Usuario no encontrado",
                "query": query
            })
            
    except sqlite3.Error as e:
        return JSONResponse({
            "status": "error",
            "message": f"Error SQL: {str(e)}",
            "query": query
        })
    finally:
        conn.close()

# ============================================
# EJERCICIO 4: INFORMACIÓN DEL SISTEMA
# ============================================
@app.get("/info")
async def database_info():
    """
    Endpoint que muestra información de la base de datos
    Útil para que los estudiantes vean la estructura
    """
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        # Obtener información de las tablas
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        
        # Obtener información de usuarios (para referencia)
        cursor.execute("SELECT username, role FROM users")
        users = cursor.fetchall()
        
        # Obtener información de productos
        cursor.execute("SELECT name, price FROM products LIMIT 3")
        products = cursor.fetchall()
        
        return JSONResponse({
            "database": "SQLite",
            "tables": [table[0] for table in tables],
            "sample_users": [{"username": u[0], "role": u[1]} for u in users],
            "sample_products": [{"name": p[0], "price": p[1]} for p in products],
            "note": "Esta información ayuda a los estudiantes a entender la estructura"
        })
        
    except sqlite3.Error as e:
        return JSONResponse({"error": str(e)})
    finally:
        conn.close()

# ============================================
# EJERCICIO BONUS: TIME-BASED INJECTION
# ============================================
@app.get("/product/{product_id}")
async def get_product_vulnerable(request: Request, product_id: str):
    """
    TIME-BASED SQL INJECTION
    Permite detectar información basándose en el tiempo de respuesta
    """
    import time
    start_time = time.time()
    
    conn = get_connection()
    cursor = conn.cursor()
    
    # 🚨 VULNERABLE: Permite funciones como SLEEP (en otros DBMS)
    query = f"SELECT * FROM products WHERE id='{product_id}'"
    
    print(f"🔍 Query ejecutada: {query}")
    
    try:
        cursor.execute(query)
        result = cursor.fetchone()
        
        end_time = time.time()
        response_time = round(end_time - start_time, 3)
        
        if result:
            return JSONResponse({
                "status": "found",
                "product": {
                    "id": result[0],
                    "name": result[1],
                    "price": result[2],
                    "description": result[3]
                },
                "query": query,
                "response_time_seconds": response_time
            })
        else:
            return JSONResponse({
                "status": "not_found",
                "message": "Producto no encontrado",
                "query": query,
                "response_time_seconds": response_time
            })
            
    except sqlite3.Error as e:
        end_time = time.time()
        response_time = round(end_time - start_time, 3)
        
        return JSONResponse({
            "status": "error",
            "message": str(e),
            "query": query,
            "response_time_seconds": response_time
        })
    finally:
        conn.close()

# ============================================
# ENDPOINT PARA REINICIAR LA BASE DE DATOS
# ============================================
@app.post("/reset-database")
async def reset_database():
    """Reinicia la base de datos con datos frescos"""
    try:
        init_database()
        return JSONResponse({
            "status": "success",
            "message": "Base de datos reiniciada correctamente"
        })
    except Exception as e:
        return JSONResponse({
            "status": "error", 
            "message": f"Error al reiniciar: {str(e)}"
        })

if __name__ == "__main__":
    import uvicorn
    print("🚀 Iniciando laboratorio SQL Injection...")
    print("⚠️  ADVERTENCIA: Esta aplicación contiene vulnerabilidades intencionales")
    print("🎓 Solo para uso educativo en entornos controlados")
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)