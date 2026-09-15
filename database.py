# database.py

import sqlite3
from config import ROL_ADMIN

DB_NAME = "sistema_facturacion.db"


# ==========================================
# BLOQUE 1: CONEXIÓN Y CONFIGURACIÓN
# ==========================================

def obtener_conexion():
    """
    Abre y devuelve una conexión activa con la base de datos SQLite.
    Configura row_factory para acceder a las columnas por su nombre.
    """
    conexion = sqlite3.connect(DB_NAME)
    conexion.row_factory = sqlite3.Row
    return conexion


# ==========================================
# BLOQUE 2: INICIALIZACIÓN DE LA ESTRUCTURA
# ==========================================

def inicializar_base_datos():
    """
    Crea la estructura completa de tablas si no existen e
    inserta el usuario administrador por defecto.
    """
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    # Tabla de Clientes
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS clientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            telefono TEXT,
            email TEXT,
            direccion TEXT
        )
    """)

    # Tabla de Proveedores
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS proveedores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            telefono TEXT,
            email TEXT,
            direccion TEXT
        )
    """)

    # Tabla de Empleados
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS empleados (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            puesto TEXT,
            salario REAL,
            fecha_ingreso TEXT
        )
    """)

    # Tabla de Productos (Inventario / Stock)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS productos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            codigo TEXT UNIQUE NOT NULL,
            nombre TEXT NOT NULL,
            precio REAL NOT NULL,
            stock INTEGER NOT NULL
        )
    """)

    # Tabla de Usuarios (Seguridad y Control de Acceso por Roles)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario TEXT UNIQUE NOT NULL,
            contrasena TEXT NOT NULL,
            rol TEXT NOT NULL,
            empleado_id INTEGER,
            FOREIGN KEY (empleado_id) REFERENCES empleados (id)
        )
    """)

    # Tabla de Ventas (Encabezado de la factura)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS ventas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cliente_id INTEGER,
            fecha TEXT NOT NULL,
            total REAL NOT NULL,
            FOREIGN KEY (cliente_id) REFERENCES clientes (id)
        )
    """)

    # Tabla de Detalle de Ventas (Líneas de artículos vendidos)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS detalle_ventas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            venta_id INTEGER NOT NULL,
            producto_id INTEGER NOT NULL,
            cantidad INTEGER NOT NULL,
            precio_unitario REAL NOT NULL,
            FOREIGN KEY (venta_id) REFERENCES ventas (id),
            FOREIGN KEY (producto_id) REFERENCES productos (id)
        )
    """)

    # Creación del usuario inicial 'admin' si la base de datos está recién instalada
    cursor.execute("SELECT COUNT(*) AS total FROM usuarios")
    if cursor.fetchone()["total"] == 0:
        cursor.execute(
            """
            INSERT INTO usuarios (usuario, contrasena, rol)
            VALUES (?, ?, ?)
            """,
            ("admin", "admin123", ROL_ADMIN)
        )

    conexion.commit()
    conexion.close()


# ==========================================
# BLOQUE 3: AUTENTICACIÓN Y SEGURIDAD
# ==========================================

def validar_credenciales(usuario, contrasena):
    """
    Verifica si las credenciales coinciden en la tabla de usuarios.
    Devuelve un diccionario con los datos del usuario o None si falla.
    """
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute(
        """
        SELECT id, usuario, rol, empleado_id 
        FROM usuarios 
        WHERE usuario = ? AND contrasena = ?
        """,
        (usuario, contrasena)
    )
    usuario_encontrado = cursor.fetchone()
    conexion.close()

    if usuario_encontrado:
        return {
            "id": usuario_encontrado["id"],
            "usuario": usuario_encontrado["usuario"],
            "rol": usuario_encontrado["rol"],
            "empleado_id": usuario_encontrado["empleado_id"]
        }
    return None


# ==========================================
# BLOQUE 4: OPERACIONES CRUD - CLIENTES
# ==========================================

def obtener_clientes():
    """Devuelve la lista completa de clientes."""
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM clientes")
    clientes = cursor.fetchall()
    conexion.close()
    return clientes


def insertar_cliente(nombre, telefono, email, direccion):
    """Guarda un nuevo cliente en la base de datos."""
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute(
        "INSERT INTO clientes (nombre, telefono, email, direccion) VALUES (?, ?, ?, ?)",
        (nombre, telefono, email, direccion)
    )
    conexion.commit()
    conexion.close()


def actualizar_cliente(id_cliente, nombre, telefono, email, direccion):
    """Modifica los datos de un cliente existente."""
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute(
        "UPDATE clientes SET nombre=?, telefono=?, email=?, direccion=? WHERE id=?",
        (nombre, telefono, email, direccion, id_cliente)
    )
    conexion.commit()
    conexion.close()


def eliminar_cliente(id_cliente):
    """Borra un cliente según su ID."""
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("DELETE FROM clientes WHERE id=?", (id_cliente,))
    conexion.commit()
    conexion.close()


# ==========================================
# BLOQUE 5: OPERACIONES CRUD - EMPLEADOS
# ==========================================

def obtener_empleados():
    """Devuelve la lista completa de empleados."""
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM empleados")
    empleados = cursor.fetchall()
    conexion.close()
    return empleados


def insertar_empleado(nombre, puesto, salario, fecha_ingreso):
    """Guarda un nuevo empleado en la base de datos."""
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute(
        "INSERT INTO empleados (nombre, puesto, salario, fecha_ingreso) VALUES (?, ?, ?, ?)",
        (nombre, puesto, salario, fecha_ingreso)
    )
    conexion.commit()
    conexion.close()


def actualizar_empleado(id_empleado, nombre, puesto, salario, fecha_ingreso):
    """Modifica los datos de un empleado existente."""
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute(
        "UPDATE empleados SET nombre=?, puesto=?, salario=?, fecha_ingreso=? WHERE id=?",
        (nombre, puesto, salario, fecha_ingreso, id_empleado)
    )
    conexion.commit()
    conexion.close()


def eliminar_empleado(id_empleado):
    """Borra un empleado según su ID."""
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("DELETE FROM empleados WHERE id=?", (id_empleado,))
    conexion.commit()
    conexion.close()


# ==========================================
# BLOQUE 6: OPERACIONES CRUD - PROVEEDORES
# ==========================================

def obtener_proveedores():
    """Devuelve la lista completa de proveedores."""
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM proveedores")
    proveedores = cursor.fetchall()
    conexion.close()
    return proveedores


def insertar_proveedor(nombre, telefono, email, direccion):
    """Guarda un nuevo proveedor en la base de datos."""
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute(
        "INSERT INTO proveedores (nombre, telefono, email, direccion) VALUES (?, ?, ?, ?)",
        (nombre, telefono, email, direccion)
    )
    conexion.commit()
    conexion.close()


def actualizar_proveedor(id_proveedor, nombre, telefono, email, direccion):
    """Modifica los datos de un proveedor existente."""
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute(
        "UPDATE proveedores SET nombre=?, telefono=?, email=?, direccion=? WHERE id=?",
        (nombre, telefono, email, direccion, id_proveedor)
    )
    conexion.commit()
    conexion.close()


def eliminar_proveedor(id_proveedor):
    """Borra un proveedor según su ID."""
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("DELETE FROM proveedores WHERE id=?", (id_proveedor,))
    conexion.commit()
    conexion.close()


# ==========================================
# BLOQUE 7: OPERACIONES CRUD - PRODUCTOS (STOCK)
# ==========================================

def obtener_productos():
    """Devuelve la lista completa de productos en stock."""
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM productos")
    productos = cursor.fetchall()
    conexion.close()
    return productos


def insertar_producto(codigo, nombre, precio, stock):
    """Agrega un nuevo producto al inventario."""
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute(
        "INSERT INTO productos (codigo, nombre, precio, stock) VALUES (?, ?, ?, ?)",
        (codigo, nombre, precio, stock)
    )
    conexion.commit()
    conexion.close()


def actualizar_producto(id_producto, codigo, nombre, precio, stock):
    """Actualiza los datos o las cantidades de un producto."""
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute(
        "UPDATE productos SET codigo=?, nombre=?, precio=?, stock=? WHERE id=?",
        (codigo, nombre, precio, stock, id_producto)
    )
    conexion.commit()
    conexion.close()


def eliminar_producto(id_producto):
    """Elimina un producto del inventario."""
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("DELETE FROM productos WHERE id=?", (id_producto,))
    conexion.commit()
    conexion.close()


# ==========================================
# BLOQUE 8: FACTURACIÓN Y VENTAS
# ==========================================

def registrar_venta(cliente_id, fecha, total, lista_productos):
    """
    Registra una factura completa: guarda la venta principal,
    inserta cada detalle de producto y descuenta el stock disponible.
    """
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    # 1. Crear el encabezado de la venta
    cursor.execute(
        "INSERT INTO ventas (cliente_id, fecha, total) VALUES (?, ?, ?)",
        (cliente_id, fecha, total)
    )
    venta_id = cursor.lastrowid

    # 2. Registrar los detalles y actualizar el inventario
    for prod in lista_productos:
        cursor.execute(
            """
            INSERT INTO detalle_ventas (venta_id, producto_id, cantidad, precio_unitario)
            VALUES (?, ?, ?, ?)
            """,
            (venta_id, prod[0], prod[1], prod[2])
        )

        # Descuenta las unidades vendidas del stock actual
        cursor.execute(
            "UPDATE productos SET stock = stock - ? WHERE id = ?",
            (prod[1], prod[0])
        )

    conexion.commit()
    conexion.close()
    return venta_id


def insertar_factura(cliente_id, fecha, total, lista_productos):
    """Sincroniza la llamada de insertar_factura con la función registrar_venta."""
    return registrar_venta(cliente_id, fecha, total, lista_productos)


def obtener_ventas():
    """Devuelve el historial general de ventas registradas."""
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("""
        SELECT v.id, v.fecha, v.total, c.nombre AS cliente
        FROM ventas v
        LEFT JOIN clientes c ON v.cliente_id = c.id
    """)
    ventas = cursor.fetchall()
    conexion.close()
    return ventas


def obtener_facturas():
    """Sincroniza la llamada de obtener_facturas con la función obtener_ventas."""
    return obtener_ventas()