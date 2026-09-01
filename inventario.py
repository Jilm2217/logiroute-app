import json
import os

class Inventario:
    def __init__(self, archivo_persistencia="inventario.json"):
        self.archivo_persistencia = archivo_persistencia
        self.productos = self.cargar_datos()

    def cargar_datos(self):
        """Carga los productos desde el archivo JSON si existe; si no, retorna un diccionario vacío."""
        if os.path.exists(self.archivo_persistencia):
            try:
                with open(self.archivo_persistencia, "r", encoding="utf-8") as archivo:
                    return json.load(archivo)
            except Exception:
                return {}
        return {}

    def guardar_datos(self):
        """Guarda el diccionario actual en el archivo JSON."""
        try:
            with open(self.archivo_persistencia, "w", encoding="utf-8") as archivo:
                json.dump(self.productos, archivo, indent=4, ensure_ascii=False)
        except Exception as e:
            print(f"Error al guardar los datos: {e}")

    def agregar_producto(self, sku, nombre, precio, stock):
        """Agrega un nuevo producto al inventario y lo guarda en disco."""
        if sku in self.productos:
            return f"Error: El producto con SKU {sku} ya existe."
        
        self.productos[sku] = {
            "nombre": nombre,
            "precio": float(precio),
            "stock": int(stock)
        }
        self.guardar_datos()
        return f"Éxito: Producto '{nombre}' agregado y guardado correctamente."

    def eliminar_producto(self, sku):
        """Elimina un producto del inventario usando su SKU y actualiza el archivo JSON."""
        if sku in self.productos:
            nombre_eliminado = self.productos[sku]["nombre"]
            del self.productos[sku]
            self.guardar_datos()
            return f"Éxito: Producto '{nombre_eliminado}' (SKU: {sku}) eliminado correctamente."
        return f"Aviso: No se encontró ningún producto con el SKU {sku}."

    def consultar_producto(self, sku):
        """Busca un producto por su SKU utilizando acceso directo por clave O(1)."""
        if sku in self.productos:
            p = self.productos[sku]
            return f"[{sku}] {p['nombre']} - Precio: ${p['precio']} - Stock: {p['stock']} unidades"
        return f"Aviso: No se encontró ningún producto con el SKU {sku}."

    def listar_productos(self):
        """Devuelve una lista con todos los productos registrados."""
        if not self.productos:
            return "El inventario está vacío."
        
        resultado = "--- INVENTARIO ACTUAL (PERSISTENTE) ---\n"
        for sku, datos in self.productos.items():
            resultado += f"SKU: {sku} | {datos['nombre']} | ${datos['precio']} | Stock: {datos['stock']}\n"
        return resultado