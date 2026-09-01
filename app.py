import streamlit as st
from inventario import Inventario
from rutas import GestorRutas

# Inicializamos nuestros módulos
mi_inventario = Inventario()
gestor_rutas = GestorRutas()

# Configuración de la página web
st.set_page_config(page_title="LogiRoute - Gestor de Inventario y Logística", page_icon="📦", layout="centered")

st.title("📦 LogiRoute: Sistema de Inventario y Logística")
st.write("Plataforma optimizada con estructuras de datos y algoritmos de optimización.")

# Menú lateral ampliado con opciones de eliminación
menu = st.sidebar.selectbox(
    "Menú de Opciones", 
    [
        "Ver Inventario", 
        "Agregar Producto", 
        "Buscar Producto", 
        "Eliminar Producto",
        "Gestionar Entregas y Rutas", 
        "Eliminar Destino"
    ]
)

# --- SECCIÓN 1: VER INVENTARIO ---
if menu == "Ver Inventario":
    st.subheader("📋 Inventario Actual")
    
    if not mi_inventario.productos:
        st.info("El inventario está vacío. Agrega productos desde el menú lateral.")
    else:
        datos_tabla = []
        for sku, info in mi_inventario.productos.items():
            datos_tabla.append({
                "SKU": sku,
                "Nombre": info["nombre"],
                "Precio ($)": info["precio"],
                "Stock": info["stock"]
            })
        
        st.dataframe(datos_tabla, use_container_width=True)

# --- SECCIÓN 2: AGREGAR PRODUCTO ---
elif menu == "Agregar Producto":
    st.subheader("➕ Registrar Nuevo Producto")
    
    with st.form("form_agregar"):
        sku_input = st.text_input("Código SKU (Ej. PAL-001)")
        nombre_input = st.text_input("Nombre del Producto")
        precio_input = st.number_input("Precio Unitario ($)", min_value=0.0, format="%.2f")
        stock_input = st.number_input("Cantidad en Stock", min_value=0, step=1)
        
        boton_enviar = st.form_submit_button("Guardar Producto")
        
        if boton_enviar:
            if sku_input.strip() == "" or nombre_input.strip() == "":
                st.error("Error: El SKU y el Nombre no pueden estar vacíos.")
            else:
                resultado = mi_inventario.agregar_producto(sku_input, nombre_input, precio_input, stock_input)
                
                if "Éxito" in resultado:
                    st.success(resultado)
                else:
                    st.warning(resultado)

# --- SECCIÓN 3: BUSCAR PRODUCTO ---
elif menu == "Buscar Producto":
    st.subheader("🔍 Búsqueda Rápida por SKU")
    
    sku_a_buscar = st.text_input("Ingresa el SKU que deseas consultar:")
    
    if st.button("Buscar"):
        if sku_a_buscar in mi_inventario.productos:
            p = mi_inventario.productos[sku_a_buscar]
            st.success("¡Producto encontrado!")
            
            col1, col2 = st.columns(2)
            col1.metric("Precio", f"${p['precio']:.2f}")
            col2.metric("Stock Disponible", f"{p['stock']} unidades")
            st.write(f"**Nombre:** {p['nombre']}")
        else:
            st.error(f"No se encontró ningún producto registrado con el SKU: {sku_a_buscar}")

# --- SECCIÓN 4: ELIMINAR PRODUCTO ---
elif menu == "Eliminar Producto":
    st.subheader("🗑️ Eliminar Producto del Inventario")
    
    if not mi_inventario.productos:
        st.info("No hay productos registrados para eliminar.")
    else:
        skus_disponibles = list(mi_inventario.productos.keys())
        sku_seleccionado = st.selectbox("Selecciona el SKU del producto a eliminar:", skus_disponibles)
        
        if sku_seleccionado:
            p_info = mi_inventario.productos[sku_seleccionado]
            st.write(f"Vas a eliminar: **{p_info['nombre']}** (SKU: {sku_seleccionado})")
            
            if st.button("Confirmar Eliminación de Producto", type="primary"):
                res = mi_inventario.eliminar_producto(sku_seleccionado)
                st.success(res)
                st.rerun()

# --- SECCIÓN 5: GESTIONAR ENTREGAS Y RUTAS ---
elif menu == "Gestionar Entregas y Rutas":
    st.subheader("🚚 Optimización de Rutas de Reparto")
    
    with st.form("form_ruta"):
        cliente = st.text_input("Nombre del Cliente")
        direccion = st.text_input("Dirección de Entrega")
        distancia = st.number_input("Distancia desde el almacén (km)", min_value=0.1, format="%.2f")
        
        submitted = st.form_submit_button("Registrar Destino")
        
        if submitted:
            if cliente.strip() == "" or direccion.strip() == "":
                st.error("Por favor completa todos los campos.")
            else:
                msg = gestor_rutas.agregar_destino(cliente, direccion, distancia)
                st.success(msg)
                
    st.markdown("---")
    st.subheader("🗺️ Secuencia de Reparto Optimizada")
    
    destinos_optimos = gestor_rutas.calcular_ruta_optima()
    
    if not destinos_optimos:
        st.info("No hay rutas registradas todavía.")
    else:
        st.write("Los siguientes puntos han sido ordenados por cercanía para reducir costos de traslado:")
        for idx, det in enumerate(destinos_optimos, start=1):
            st.markdown(f"**{idx}. Cliente:** {det['cliente']} | **Dirección:** {det['direccion']} | **Distancia:** {det['distancia_km']} km")

# --- SECCIÓN 6: ELIMINAR DESTINO DE RUTA ---
elif menu == "Eliminar Destino":
    st.subheader("🗑️ Eliminar Destino de Reparto")
    
    if not gestor_rutas.destinos:
        st.info("No hay destinos registrados para eliminar.")
    else:
        opciones_destinos = [f"{i}: {d['cliente']} - {d['direccion']} ({d['distancia_km']} km)" for i, d in enumerate(gestor_rutas.destinos)]
        destino_elegido = st.selectbox("Selecciona el destino a eliminar:", opciones_destinos)
        
        if destino_elegido:
            idx_seleccionado = int(destino_elegido.split(":")[0])
            
            if st.button("Confirmar Eliminación de Destino", type="primary"):
                res = gestor_rutas.eliminar_destino(idx_seleccionado)
                st.success(res)
                st.rerun()