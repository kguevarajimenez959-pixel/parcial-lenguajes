# PARCIAL LENGUAJES

## Punto 4

# Proyecto Punto 4 – Comparación de rendimiento: CYK vs LL(1)

Este proyecto implementa dos analizadores sintácticos en Python para el mismo lenguaje, uno con el algoritmo **CYK** (O(n³)) y otro con **LL(1)** (O(n)), y compara su rendimiento mediante mediciones de tiempo.


## Instalación

### 1. Crear carpeta del proyecto

```
mkdir punto4
cd punto4
```

### 2. Crear los archivos del proyecto

#### 2.1 Archivo `cyk.py`

```
nano cyk.py
```

#### 2.2 Archivo `ll1.py`

```
nano ll1.py
```

#### 2.3 Archivo `bench.py`

```
nano bench.py
```

#### 2.4 Archivo `README.md`

```
nano README.md
```

## Uso

### Ejecución del analizador LL(1)

```
python3 ll1.py "id + id + id"
```

### Ejecución del analizador CYK

```
python3 cyk.py "id + id + id"
```

### Casos de prueba válidos

```
python3 ll1.py "id + id + id"
python3 cyk.py "id + id + id"
```

### Casos inválidos

```
python3 ll1.py "id +"
python3 cyk.py "id + + id"
```


## Benchmark

Para ejecutar la comparación de rendimiento entre ambos algoritmos:

```
python3 bench.py | tee resultados.csv
```

Este comando:
- Ejecuta múltiples pruebas con diferentes tamaños de entrada
- Mide los tiempos de ejecución de ambos algoritmos
- Guarda los resultados en `resultados.csv`


## Complejidad esperada

| Algoritmo | Complejidad temporal |
|-----------|---------------------|
| **LL(1)** | O(n)               |
| **CYK**   | O(n³)              |

### Salida esperada del benchmark

```
n_ids;cases;cyk_min;cyk_med;ll1_min;ll1_med
5;40;0.002255;0.002386;0.000079;0.000080
10;40;0.011179;0.011236;0.000152;0.000159
20;40;0.069512;0.070870;0.000288;0.000296
40;40;0.479992;0.484146;0.000513;0.000514
80;40;4.189541;4.273013;0.001182;0.001198
```

**Interpretación de las columnas:**
- `n_ids`: Número de identificadores en la cadena de prueba
- `cases`: Cantidad de casos ejecutados
- `cyk_min`: Tiempo mínimo de ejecución de CYK (segundos)
- `cyk_med`: Tiempo promedio de ejecución de CYK (segundos)
- `ll1_min`: Tiempo mínimo de ejecución de LL(1) (segundos)
- `ll1_med`: Tiempo promedio de ejecución de LL(1) (segundos)


## Observaciones

Como se puede ver en los resultados, el algoritmo **LL(1)** es significativamente más rápido que **CYK**, especialmente a medida que aumenta el tamaño de la entrada. Esto confirma las complejidades teóricas:

- LL(1) escala linealmente con el tamaño de entrada
- CYK muestra crecimiento cúbico, haciendo que el tiempo de procesamiento se dispare con entradas más grandes




















## Punto 5

<img width="507" height="632" alt="imagen" src="https://github.com/user-attachments/assets/8ea4eed6-28e8-47f5-bfcd-c3d71e392d79" />


