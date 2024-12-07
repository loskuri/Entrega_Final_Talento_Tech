import sqlite3
from colorama import init, Fore, Style

# Inicializar colorama
init(autoreset=True)

def conectar_db():
    """Crea una conexión a la base de datos 'inventario.db'."""
    return sqlite3.connect("inventario.db")

def crear_tabla():
    """Crea la tabla 'productos' si no existe en la base de datos."""
    conexion = conectar_db()
    cursor = conexion.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS productos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            descripcion TEXT,
            cantidad INTEGER NOT NULL,
            precio REAL NOT NULL,
            categoria TEXT
        )
    """)
    conexion.commit()
    conexion.close()

def input_entero(mensaje):
    """Solicita un número entero al usuario, manejando errores."""
    while True:
        valor = input(Fore.YELLOW + mensaje)
        if valor.isdigit():
            return int(valor)
        else:
            print(Fore.RED + "Por favor, ingrese un valor entero válido.")

def input_flotante(mensaje):
    """Solicita un número flotante al usuario, manejando errores."""
    while True:
        valor = input(Fore.YELLOW + mensaje)
        try:
            return float(valor)
        except ValueError:
            print(Fore.RED + "Por favor, ingrese un valor numérico válido (ej: 10.5).")

def registrar_producto():
    """Registra un nuevo producto solicitando datos al usuario."""
    conexion = conectar_db()
    cursor = conexion.cursor()
    print(Fore.CYAN + "\n--- REGISTRAR PRODUCTO ---")
    nombre = input(Fore.YELLOW + "Nombre: ")
    descripcion = input(Fore.YELLOW + "Descripción: ")
    cantidad = input_entero("Cantidad: ")
    precio = input_flotante("Precio: ")
    categoria = input(Fore.YELLOW + "Categoría: ")
    cursor.execute("""
        INSERT INTO productos (nombre, descripcion, cantidad, precio, categoria)
        VALUES (?, ?, ?, ?, ?)
    """, (nombre, descripcion, cantidad, precio, categoria))
    conexion.commit()
    conexion.close()
    print(Fore.GREEN + "Producto registrado con éxito.")

def visualizar_productos():
    """Muestra todos los productos registrados en la base de datos."""
    conexion = conectar_db()
    cursor = conexion.cursor()
    print(Fore.CYAN + "\n--- LISTA DE PRODUCTOS ---")
    cursor.execute("SELECT id, nombre, descripcion, cantidad, precio, categoria FROM productos")
    productos = cursor.fetchall()
    conexion.close()
    
    if not productos:
        print(Fore.RED + "No hay productos registrados. Por favor, registre un producto primero.")
    else:
        # Imprimir cabecera
        print(Fore.YELLOW + "{:<5} | {:<20} | {:<30} | {:<10} | {:<10} | {:<15}".format(
            "ID", "Nombre", "Descripción", "Cantidad", "Precio", "Categoría"))
        print(Fore.YELLOW + "-"*100)
        for p in productos:
            print(Fore.YELLOW + "{:<5} | {:<20} | {:<30} | {:<10} | ${:<9.2f} | {:<15}".format(
                p[0], p[1], p[2], p[3], p[4], p[5]))

def actualizar_producto():
    """Actualiza la cantidad disponible de un producto específico."""
    conexion = conectar_db()
    cursor = conexion.cursor()
    print(Fore.CYAN + "\n--- ACTUALIZAR PRODUCTO ---")
    id_producto = input(Fore.YELLOW + "ID del producto a actualizar: ")
    cursor.execute("SELECT * FROM productos WHERE id = ?", (id_producto,))
    producto = cursor.fetchone()
    if not producto:
        print(Fore.RED + "El producto no existe.")
        conexion.close()
        return
    nueva_cantidad = input_entero("Nueva cantidad: ")
    cursor.execute("UPDATE productos SET cantidad = ? WHERE id = ?", (nueva_cantidad, id_producto))
    conexion.commit()
    conexion.close()
    print(Fore.GREEN + "Cantidad actualizada con éxito.")

def eliminar_producto():
    """Elimina un producto del inventario a partir de su ID."""
    conexion = conectar_db()
    cursor = conexion.cursor()
    print(Fore.CYAN + "\n--- ELIMINAR PRODUCTO ---")
    id_producto = input(Fore.YELLOW + "ID del producto a eliminar: ")
    cursor.execute("DELETE FROM productos WHERE id = ?", (id_producto,))
    if cursor.rowcount > 0:
        print(Fore.GREEN + "Producto eliminado con éxito.")
    else:
        print(Fore.RED + "El producto no existe.")
    conexion.commit()
    conexion.close()

def generar_reporte_bajo_stock():
    """Genera un reporte de productos con cantidad igual o inferior a un límite especificado."""
    conexion = conectar_db()
    cursor = conexion.cursor()
    print(Fore.CYAN + "\n--- REPORTE DE PRODUCTOS CON BAJO STOCK ---")
    limite = input_entero("Ingrese el límite de stock: ")
    cursor.execute("SELECT id, nombre, descripcion, cantidad, precio, categoria FROM productos WHERE cantidad <= ?", (limite,))
    productos = cursor.fetchall()
    conexion.close()
    
    if not productos:
        print(Fore.GREEN + "No hay productos con bajo stock.")
    else:
        print(Fore.RED + "Productos con bajo stock:")
        print(Fore.YELLOW + "{:<5} | {:<20} | {:<30} | {:<10} | {:<10} | {:<15}".format(
            "ID", "Nombre", "Descripción", "Cantidad", "Precio", "Categoría"))
        print(Fore.YELLOW + "-"*100)
        for p in productos:
            print(Fore.RED + "{:<5} | {:<20} | {:<30} | {:<10} | ${:<9.2f} | {:<15}".format(
                p[0], p[1], p[2], p[3], p[4], p[5]))

def buscar_producto():
    """Busca productos por ID, nombre o categoría."""
    conexion = conectar_db()
    cursor = conexion.cursor()
    print(Fore.CYAN + "\n--- BUSCAR PRODUCTO ---")
    print(Fore.YELLOW + "1. Buscar por ID")
    print(Fore.YELLOW + "2. Buscar por Nombre")
    print(Fore.YELLOW + "3. Buscar por Categoría")
    opcion = input(Fore.GREEN + "Seleccione una opción: ")
    
    if opcion == "1":
        id_producto = input(Fore.YELLOW + "ID del producto: ")
        cursor.execute("SELECT id, nombre, descripcion, cantidad, precio, categoria FROM productos WHERE id = ?", (id_producto,))
    elif opcion == "2":
        nombre = input(Fore.YELLOW + "Nombre (o parte del nombre): ")
        cursor.execute("SELECT id, nombre, descripcion, cantidad, precio, categoria FROM productos WHERE nombre LIKE ?", (f"%{nombre}%",))
    elif opcion == "3":
        categoria = input(Fore.YELLOW + "Categoría (o parte de la categoría): ")
        cursor.execute("SELECT id, nombre, descripcion, cantidad, precio, categoria FROM productos WHERE categoria LIKE ?", (f"%{categoria}%",))
    else:
        print(Fore.RED + "Opción no válida.")
        conexion.close()
        return

    productos = cursor.fetchall()
    conexion.close()
    
    if not productos:
        print(Fore.RED + "No se encontraron productos con ese criterio.")
    else:
        print(Fore.YELLOW + "{:<5} | {:<20} | {:<30} | {:<10} | {:<10} | {:<15}".format(
            "ID", "Nombre", "Descripción", "Cantidad", "Precio", "Categoría"))
        print(Fore.YELLOW + "-"*100)
        for p in productos:
            print(Fore.YELLOW + "{:<5} | {:<20} | {:<30} | {:<10} | ${:<9.2f} | {:<15}".format(
                p[0], p[1], p[2], p[3], p[4], p[5]))
1
def mostrar_menu():
    """Muestra el menú principal y devuelve la opción seleccionada."""
    print(Fore.CYAN + "\n--- MENÚ PRINCIPAL ---")
    print(Fore.YELLOW + "1. Registrar producto")
    print(Fore.YELLOW + "2. Visualizar productos")
    print(Fore.YELLOW + "3. Actualizar producto")
    print(Fore.YELLOW + "4. Eliminar producto por ID")
    print(Fore.YELLOW + "5. Generar reporte de bajo stock")
    print(Fore.YELLOW + "6. Buscar producto")
    print(Fore.YELLOW + "7. Salir")
    return input(Fore.GREEN + "Seleccione una opción: ")

def main():
    """Función principal del programa."""
    crear_tabla()
    while True:
        opcion = mostrar_menu()
        if opcion == "1":
            registrar_producto()
        elif opcion == "2":
            visualizar_productos()
        elif opcion == "3":
            actualizar_producto()
        elif opcion == "4":
            eliminar_producto()
        elif opcion == "5":
            generar_reporte_bajo_stock()
        elif opcion == "6":
            buscar_producto()
        elif opcion == "7":
            print(Fore.GREEN + "Gracias por usar el sistema de inventario. ¡Hasta luego!")
            break
        else:
            print(Fore.RED + "Opción no válida. Intente de nuevo.")

if __name__ == "__main__":
    main()
