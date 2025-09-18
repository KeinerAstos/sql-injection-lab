import sqlite3
import os

def init_database():
    """Inicializa la base de datos con tablas y datos de prueba"""
    
    # Crear o conectar a la base de datos
    conn = sqlite3.connect('vulnerable_app.db')
    cursor = conn.cursor()
    
    # Crear tabla de usuarios
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            password TEXT NOT NULL,
            email TEXT NOT NULL,
            role TEXT NOT NULL
        )
    ''')
    
    # Crear tabla de productos
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            price REAL NOT NULL,
            description TEXT
        )
    ''')
    
    # Limpiar datos existentes (para reiniciar)
    cursor.execute('DELETE FROM users')
    cursor.execute('DELETE FROM products')
    
    # Insertar usuarios de prueba
    users_data = [
        ('admin', 'admin123', 'admin@company.com', 'administrator'),
        ('user1', 'password', 'user1@company.com', 'user'),
        ('guest', 'guest123', 'guest@company.com', 'guest'),
        ('manager', 'manager456', 'manager@company.com', 'manager'),
        ('developer', 'dev789', 'dev@company.com', 'developer')
    ]
    
    cursor.executemany('''
        INSERT INTO users (username, password, email, role) 
        VALUES (?, ?, ?, ?)
    ''', users_data)
    
    # Insertar productos de prueba
    products_data = [
        ('Laptop Dell XPS', 1299.99, 'Laptop empresarial de alta gama'),
        ('Mouse Logitech MX', 79.99, 'Mouse ergonómico inalámbrico'),
        ('Teclado Mecánico Corsair', 149.99, 'Teclado gaming con switches mecánicos'),
        ('Monitor Samsung 27"', 329.99, 'Monitor 4K para profesionales'),
        ('Webcam Logitech C920', 89.99, 'Cámara web Full HD'),
        ('Auriculares Sony', 199.99, 'Auriculares con cancelación de ruido')
    ]
    
    cursor.executemany('''
        INSERT INTO products (name, price, description) 
        VALUES (?, ?, ?)
    ''', products_data)
    
    # Confirmar cambios y cerrar conexión
    conn.commit()
    conn.close()
    
    print("✅ Base de datos inicializada correctamente")
    print("👥 Usuarios creados: admin, user1, guest, manager, developer")
    print("📦 Productos creados: 6 productos de ejemplo")

def get_connection():
    """Obtiene una conexión a la base de datos"""
    return sqlite3.connect('vulnerable_app.db')

def show_database_info():
    """Muestra información de la base de datos para debug"""
    conn = get_connection()
    cursor = conn.cursor()
    
    print("\n=== INFORMACIÓN DE LA BASE DE DATOS ===")
    
    # Mostrar usuarios
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    print(f"\n👥 USUARIOS ({len(users)} registros):")
    for user in users:
        print(f"  ID: {user[0]}, Usuario: {user[1]}, Password: {user[2]}, Email: {user[3]}, Rol: {user[4]}")
    
    # Mostrar productos
    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()
    print(f"\n📦 PRODUCTOS ({len(products)} registros):")
    for product in products:
        print(f"  ID: {product[0]}, Nombre: {product[1]}, Precio: ${product[2]}")
    
    conn.close()

if __name__ == "__main__":
    # Si ejecutas este archivo directamente, inicializa la BD
    init_database()
    show_database_info()