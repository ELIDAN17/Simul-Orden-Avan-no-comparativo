# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
import numpy as np
import time
import matplotlib.pyplot as plt
# Importamos todas las funciones de tu archivo simuladorOrden2.py
from simuladorOrden2 import (
    counting_sort, radix_sort, bucket_sort, 
    quick_sort, merge_sort, shell_sort, timsort_manual, cargar_datos_csv
)

st.set_page_config(page_title="Simulador de Ordenamiento no comparativo", layout="wide")

st.title("⚖️ Simulador de Algoritmos de Ordenamiento no comparativo")
st.markdown("---")

# --- SIDEBAR: CONFIGURACIÓN ---
st.sidebar.header("📂 Configuración de Datos")
origen = st.sidebar.radio("Fuente de datos:", ["Datos Aleatorios", "Cargar archivo CSV"])

datos_a_ordenar = []

if origen == "Datos Aleatorios":
    n_elementos = st.sidebar.slider("N° de elementos", 15, 100000, 100)
    rango_max = st.sidebar.number_input("Valor máximo (K)", value=500)
    if st.sidebar.button("Generar Nuevos Datos"):
        st.session_state['datos'] = np.random.randint(0, rango_max, n_elementos).tolist()
    
    if 'datos' in st.session_state:
        datos_a_ordenar = st.session_state['datos']
else:
    archivo = st.sidebar.file_uploader("Sube tu CSV", type=["csv"])
    if archivo:
        df_csv = pd.read_csv(archivo)
        st.write("Vista previa del CSV:", df_csv.head())
        columna = st.sidebar.selectbox("Selecciona la columna numérica", df_csv.columns)
        datos_a_ordenar = df_csv[columna].dropna().tolist()
        st.session_state['datos_totales'] = datos_a_ordenar

# --- CUERPO PRINCIPAL ---
if not datos_a_ordenar:
    st.warning("👈 Por favor, genera datos o sube un archivo CSV para comenzar.")
else:
    # Definimos el diccionario con TODOS los algoritmos del backend
    algos_dict = {
        "Counting Sort": counting_sort,
        "Radix Sort": radix_sort,
        "Bucket Sort": bucket_sort,
        "Quick Sort": quick_sort,
        "Merge Sort": merge_sort,
        "Shell Sort": shell_sort,
        "Timsort (Manual)": timsort_manual
    }

    col_visual, col_stats = st.columns([1.5, 1])

    # --- COLUMNA 1: SIMULACIÓN VISUAL ---
    with col_visual:
        st.subheader("🎬 Visualización del Proceso")
        seleccion_visual = st.selectbox("Elige un algoritmo para ver cómo ordena:", list(algos_dict.keys()))
        
        # Área de animación
        placeholder = st.empty()

        if st.button(f"Simular {seleccion_visual}"):
            muestra_anim = datos_a_ordenar[:25] 
            arr_viz = list(muestra_anim)
            n = len(arr_viz)
    
            # Motor de animación (Ejemplo con Shell Sort)
            gap = n // 2
            while gap > 0:
                for i in range(gap, n):
                    temp = arr_viz[i]
                    j = i
                    # Marcamos en NARANJA la comparación inicial
                    idx_comparando = j
                    idx_con_quien = j - gap
            
                    while j >= gap and arr_viz[j - gap] > temp:
                        # Marcamos en ROJO el intercambio real
                        idx_intercambio_1 = j
                        idx_intercambio_2 = j - gap
                
                        arr_viz[j] = arr_viz[j - gap]
                        j -= gap
                
                        # --- RENDERIZADO CON 3 COLORES ---
                        fig, ax = plt.subplots(figsize=(10, 5))
                
                        colores = []
                        for k in range(n):
                            if k == idx_intercambio_1 or k == idx_intercambio_2:
                                colores.append('#e74c3c') # ROJO: Intercambio
                            elif k == idx_comparando or k == idx_con_quien:
                                colores.append('#f39c12') # NARANJA: Comparación
                            else:
                                colores.append('#34495e') # GRIS/AZUL: En reposo
                
                        bars = ax.bar(range(n), arr_viz, color=colores)
                        ax.bar_label(bars, padding=3, fontsize=9) # Valores visibles
                        ax.set_title(f"Visualización: Rojo=Cambio | Naranja=Comparación")
                        placeholder.pyplot(fig)
                        plt.close()
                        time.sleep(0.1)
            
                    arr_viz[j] = temp
                gap //= 2
            st.success("Ordenamiento completado.")

    # --- COLUMNA 2: TABLA DE RENDIMIENTO (RÁPIDEZ) ---
    with col_stats:
        st.subheader("⏱️ Resultados de Rapidez")
        if st.button("🚀 Comparar Todos los Algoritmos"):
            resultados = []
            progreso = st.progress(0)
            
            for i, (nombre, funcion) in enumerate(algos_dict.items()):
                copia_datos = list(datos_a_ordenar)
                
                inicio = time.perf_counter()
                funcion(copia_datos)
                fin = time.perf_counter()
                
                resultados.append({
                    "Algoritmo": nombre,
                    "Tiempo (ms)": round((fin - inicio) * 1000, 6)
                })
                progreso.progress((i + 1) / len(algos_dict))
            
            # Crear DataFrame y mostrar tabla en líneas
            df_resultados = pd.DataFrame(resultados).sort_values(by="Tiempo (ms)")
            st.table(df_resultados)
            
            # Guardar en session_state para el gráfico inferior
            st.session_state['df_resultados'] = df_resultados

# --- GRÁFICO DE COMPARACIÓN FINAL ---
if 'df_resultados' in st.session_state:
    st.markdown("---")
    st.subheader("📈 Gráfico Comparativo de Tiempos")
    df = st.session_state['df_resultados']
    
    fig_final, ax_final = plt.subplots(figsize=(12, 5))
    ax_final.plot(df["Algoritmo"], df["Tiempo (ms)"], marker='o', color='red', linestyle='dashed')
    ax_final.set_ylabel("Milisegundos (ms)")
    ax_final.set_xlabel("Algoritmos")
    ax_final.grid(True, alpha=0.3)
    st.pyplot(fig_final)
    

if 'df_resultados' in st.session_state:
    st.markdown("---")
    st.subheader("📋 Resultados de Eficiencia")
    
    df = st.session_state['df_resultados']
    ganador = df.iloc[0]["Algoritmo"] # El primero de la tabla ordenada
    tiempo_ganador = df.iloc[0]["Tiempo (ms)"]
    
    # Diseño de tarjetas de resumen
    c1, c2, c3 = st.columns(3)
    with c1:
        st.metric("Algoritmo Más Eficiente", ganador)
    with c2:
        st.metric("Tiempo de Ejecución", f"{tiempo_ganador:.4f} ms")
    with c3:
        # Lógica simple de recomendación según tus datos
        if "Counting" in ganador:
            recomendacion = "Ideal para rangos (K) pequeños."
        else:
            recomendacion = "Excelente para datos con patrones mixtos."
        st.write(f"**Análisis:** {recomendacion}")