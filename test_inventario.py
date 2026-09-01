import os
import pytest
from inventario import Inventario

@pytest.fixture
def inventario_temporal():
    """Fixture para crear un archivo de prueba temporal y evitar sobreescribir el inventario real."""
    archivo_prueba = "test_inventario.json"
    inv = Inventario(archivo_persistencia=archivo_prueba)
    yield inv
    # Limpieza después de las pruebas
    if os.path.exists(archivo_prueba):
        os.remove(archivo_prueba)

def test_agregar_producto(inventario_temporal):
    resultado = inventario_temporal.agregar_producto("TEST-01", "Paleta de Prueba", 10.0, 20)
    assert "Éxito" in resultado
    assert "TEST-01" in inventario_temporal.productos
    assert inventario_temporal.productos["TEST-01"]["nombre"] == "Paleta de Prueba"

def test_agregar_producto_duplicado(inventario_temporal):
    inventario_temporal.agregar_producto("TEST-01", "Paleta 1", 10.0, 20)
    resultado = inventario_temporal.agregar_producto("TEST-01", "Paleta Duplicada", 15.0, 10)
    assert "Error" in resultado

def test_consultar_producto(inventario_temporal):
    inventario_temporal.agregar_producto("TEST-02", "Paleta de Limón", 12.0, 15)
    consulta = inventario_temporal.consultar_producto("TEST-02")
    assert "TEST-02" in consulta
    assert "Paleta de Limón" in consulta

def test_eliminar_producto(inventario_temporal):
    inventario_temporal.agregar_producto("TEST-03", "Paleta de Mango", 14.0, 30)
    resultado = inventario_temporal.eliminar_producto("TEST-03")
    assert "Éxito" in resultado
    assert "TEST-03" not in inventario_temporal.productos