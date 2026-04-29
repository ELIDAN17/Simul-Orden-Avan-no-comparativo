# -*- coding: utf-8 -*-
import pandas as pd

# --- 1. ALGORITMOS NO COMPARATIVOS (SEMANA 4) ---

def counting_sort(arr):
    if not arr: return arr
    max_val, min_val = int(max(arr)), int(min(arr))
    range_elements = max_val - min_val + 1
    count = [0] * range_elements
    output = [0] * len(arr)
    for i in arr:
        count[int(i) - min_val] += 1
    for i in range(1, len(count)):
        count[i] += count[i-1]
    for i in range(len(arr) - 1, -1, -1):
        output[count[int(arr[i]) - min_val] - 1] = arr[i]
        count[int(arr[i]) - min_val] -= 1
    return output

def radix_sort(arr):
    if not arr: return arr
    def counting_for_radix(a, exp):
        n = len(a)
        out, count = [0] * n, [0] * 10
        for i in range(n):
            index = int((a[i] // exp) % 10)
            count[index] += 1
        for i in range(1, 10):
            count[i] += count[i-1]
        for i in range(n - 1, -1, -1):
            index = int((a[i] // exp) % 10)
            out[count[index] - 1] = a[i]
            count[index] -= 1
        return out
    
    max_v = int(max(arr))
    exp, res = 1, list(arr)
    while max_v // exp > 0:
        res = counting_for_radix(res, exp)
        exp *= 10
    return res

def bucket_sort(arr):
    if not arr: return arr
    n, max_v = len(arr), max(arr)
    buckets = [[] for _ in range(n)]
    for x in arr:
        idx = int(n * x / (max_v + 1))
        buckets[idx].append(x)
    for b in buckets:
        b.sort()
    return [item for b in buckets for item in b]

# --- 2. ALGORITMOS COMPARATIVOS (PEDIDOS POR TI) ---

def quick_sort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quick_sort(left) + middle + quick_sort(right)

def merge_sort(arr):
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    
    res, i, j = [], 0, 0
    while i < len(left) and j < len(right):
        if left[i] < right[j]:
            res.append(left[i])
            i += 1
        else:
            res.append(right[j])
            j += 1
    res.extend(left[i:])
    res.extend(right[j:])
    return res

# --- 3. ALGORITMOS ADICIONALES ---

def shell_sort(arr):
    res = list(arr)
    n = len(res)
    gap = n // 2
    while gap > 0:
        for i in range(gap, n):
            temp = res[i]
            j = i
            while j >= gap and res[j - gap] > temp:
                res[j] = res[j - gap]
                j -= gap
            res[j] = temp
        gap //= 2
    return res

def timsort_nativa(arr):
    # Usamos la implementación de Python optimizada
    return sorted(arr)

# --- 4. FUNCIÓN PARA CARGAR CSV ---

def cargar_datos_csv(archivo, columna):
    """
    Carga una columna específica de un archivo CSV y la convierte en lista.
    """
    try:
        df = pd.read_csv(archivo)
        if columna in df.columns:
            return df[columna].dropna().tolist()
        else:
            return None
    except Exception as e:
        print(f"Error al cargar CSV: {e}")
        return None
    
# --- CONFIGURACIÓN DE TIMSORT ---
# MIN_MERGE es el tamaño del bloque (run). 
# Timsort divide el arreglo en estos trozos para procesarlos.
MIN_MERGE = 32

def calc_min_run(n):
    """Calcula el tamaño óptimo de un 'run' para el proceso de mezcla."""
    r = 0
    while n >= MIN_MERGE:
        r |= n & 1
        n >>= 1
    return n + r

# 1. PARTE DE INSERCIÓN (Para ordenar los runs individuales)
def insertion_sort_timsort(arr, left, right):
    for i in range(left + 1, right + 1):
        temp = arr[i]
        j = i - 1
        while j >= left and arr[j] > temp:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = temp

# 2. PARTE DE MEZCLA (Para unir los runs ya ordenados)
def merge_timsort(arr, l, m, r):
    len1, len2 = m - l + 1, r - m
    left, right = [], []
    for i in range(0, len1): left.append(arr[l + i])
    for i in range(0, len2): right.append(arr[m + 1 + i])

    i, j, k = 0, 0, l
    while i < len1 and j < len2:
        if left[i] <= right[j]:
            arr[k] = left[i]
            i += 1
        else:
            arr[k] = right[j]
            j += 1
        k += 1

    while i < len1:
        arr[k] = left[i]
        k += 1
        i += 1
    while j < len2:
        arr[k] = right[j]
        k += 1
        j += 1

# 3. FUNCIÓN PRINCIPAL DE TIMSORT
def timsort_manual(arr_original):
    # Hacemos una copia para no afectar los datos originales del CSV
    arr = list(arr_original)
    n = len(arr)
    min_run = calc_min_run(n)

    # PASO 1: Dividir el arreglo en 'runs' y ordenarlos con Inserción
    # La inserción es rapidísima para arreglos de tamaño pequeño (32-64 elementos)
    for start in range(0, n, min_run):
        end = min(start + min_run - 1, n - 1)
        insertion_sort_timsort(arr, start, end)

    # PASO 2: Mezclar los runs ordenados usando la lógica de Merge Sort
    size = min_run
    while size < n:
        for left in range(0, n, 2 * size):
            mid = min(n - 1, left + size - 1)
            right = min((left + 2 * size - 1), (n - 1))

            if mid < right:
                merge_timsort(arr, left, mid, right)
        size = 2 * size
        
    return arr