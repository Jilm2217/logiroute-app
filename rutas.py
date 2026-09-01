import json
import os

class GestorRutas:
    def __init__(self, archivo_persistencia="rutas.json"):
        self.archivo_persistencia = archivo_persistencia
        self.destinos = self.cargar_datos()

    def cargar_datos(self):
        """Carga los destinos guardados desde un archivo JSON."""
        if os.path.exists(self.archivo_persistencia):
            try:
                with open(self.archivo_persistencia, "r", encoding="utf-8") as archivo:
                    return json.load(archivo)
            except Exception:
                return []
        return []

    def guardar_datos(self):
        """Guarda la lista de destinos en disco."""
        try:
            with open(self.archivo_persistencia, "w", encoding="utf-8") as archivo:
                json.dump(self.destinos, archivo, indent=4, ensure_ascii=False)
        except Exception as e:
            print(f"Error al guardar rutas: {e}")

    def agregar_destino(self, cliente, direccion, distancia_km):
        """Agrega un punto de entrega con su respectiva distancia desde el almacén."""
        nuevo_punto = {
            "cliente": cliente,
            "direccion": direccion,
            "distancia_km": float(distancia_km)
        }
        self.destinos.append(nuevo_punto)
        self.guardar_datos()
        return f"Destino para '{cliente}' agregado exitosamente."

    def calcular_ruta_optima(self):
        """
        Aplica un principio básico de ordenamiento por cercanía (algoritmo greedy simple) 
        para simular la optimización de entregas de menor a mayor distancia.
        """
        if not self.destinos:
            return []
        
        # Ordenamos los destinos de menor a mayor distancia (Simulando optimización de ruta)
        ruta_optima = sorted(self.destinos, key=lambda x: x["distancia_km"])
        return ruta_optima