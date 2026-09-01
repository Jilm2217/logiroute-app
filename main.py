from inventario import Inventario

def ejecutar_sistema():
    mi_inventario = Inventario()
    
    while True:
        print("\n--- SISTEMA DE GESTIÓN LOGIROUTE ---")
        print("1. Agregar producto")
        print("2. Consultar producto por SKU")
        print("3. Ver todo el inventario")
        print("4. Salir")
        
        opcion = input("Elige una opción (1-4): ")
        
        if opcion == "1":
            sku = input("Ingresa el SKU del producto (ej. PAL-01): ")
            nombre = input("Ingresa el nombre del producto: ")
            precio = input("Ingresa el precio: ")
            stock = input("Ingresa la cantidad en stock: ")
            
            respuesta = mi_inventario.agregar_producto(sku, nombre, precio, stock)
            print(respuesta)
            
        elif opcion == "2":
            sku = input("Ingresa el SKU a buscar: ")
            print(mi_inventario.consultar_producto(sku))
            
        elif opcion == "3":
            print(mi_inventario.listar_productos())
            
        elif opcion == "4":
            print("Saliendo del sistema...")
            break
        else:
            print("Opción inválida. Intenta de nuevo.")

if __name__ == "__main__":
    ejecutar_sistema()