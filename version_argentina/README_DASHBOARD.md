# Dashboard - Sistema de Predicción de Flood de Alarmas

Aplicación web en Streamlit para visualizar predicciones y estado del sistema de detección de floods de alarmas.

## 🚀 Instalación

### 1. Instalar dependencias

```bash
pip install -r requirements_dashboard.txt
```

O instalar manualmente:
```bash
pip install streamlit pandas numpy plotly
```

### 2. Ejecutar la aplicación

```bash
streamlit run app.py
```

La aplicación se abrirá automáticamente en tu navegador en `http://localhost:8501`

## 📊 Características

### Estilo Visual
- **Paleta corporativa**: Verde (#00843D), Azul (#0066CC), Gris claro (#F5F5F5)
- **Diseño limpio y minimalista** inspirado en reportes industriales
- **Tarjetas KPI** con indicadores de estado (OK/Advertencia/Crítico)
- **Gráficos profesionales** con Plotly

### Funcionalidades

1. **Resumen Ejecutivo**
   - KPIs principales: Floods reales, predichos, falsas alarmas, no detectados
   - Anticipación promedio del modelo
   - Métricas del modelo: Accuracy, Precision, Recall, F1-Score

2. **Gráfico Principal**
   - Serie temporal de alarmas activas
   - Línea de umbral de flood
   - Marcadores para floods reales (círculos rojos)
   - Marcadores para predicciones (triángulos azules)

3. **Distribución de Riesgo**
   - Gráfico donut con categorías: Bajo, Medio, Alto
   - Colores: Verde (bajo), Amarillo (medio), Rojo (alto)

4. **Tabla de Eventos Relevantes**
   - Eventos con probabilidad ≥ 0.6 o floods actuales
   - Ordenados por fecha descendente
   - Columnas: Fecha/Hora, Alarmas, Probabilidad, Predicción, Flood Actual

5. **Panel de Métricas Detalladas**
   - Métricas de clasificación
   - Tasas de error (FPR, FNR)
   - Matriz de confusión
   - Gráfico de barras de métricas

### Sidebar (Configuración)

- **Rango de fechas**: Filtrar el período a visualizar
- **Umbral de probabilidad**: Ajustar el umbral para predicciones (default: 0.6)
- **Nivel de severidad**: Filtrar por Todos / Sólo Crítico / Sólo Advertencia
- **Umbral de flood**: Número mínimo de alarmas para considerar flood (default: 225)

## 📁 Estructura de Datos

La aplicación espera un DataFrame con las siguientes columnas:

- `timestamp` (datetime): Fecha y hora del registro
- `active_alarms` (int): Número de alarmas activas
- `probabilidad_flood` (float 0-1): Probabilidad de flood en próximas 2 horas
- `prediccion_flood` (0/1): Predicción binaria (se recalcula con el umbral)
- `flood_actual` (0/1): Si hay flood actual (se recalcula con el umbral)

### Nota sobre Datos

Actualmente la función `load_data()` lee desde `prueba/salida_predicciones.csv`.

**Para producción**: Reemplazar `load_data()` para obtener datos directamente del modelo entrenado o de una base de datos.

## 🎨 Personalización

### Colores Corporativos

Los colores están definidos en el CSS inline al inicio del archivo:

- **Verde**: `#00843D` (Schneider Electric)
- **Azul**: `#0066CC` (Encabezados)
- **Rojo**: `#DC143C` (Alertas críticas)
- **Amarillo**: `#FFA500` (Advertencias)
- **Gris**: `#F5F5F5` (Fondos)

### Umbrales de Estado

Los colores de estado se calculan automáticamente:

- **Verde (OK)**: Valor ≥ umbral bueno
- **Amarillo (Advertencia)**: Valor entre umbral bueno y warning
- **Rojo (Crítico)**: Valor < umbral warning

## 🔧 Extensión

### Conectar con Modelo Real

En la función `load_data()`, reemplazar:

```python
# Actual (lee CSV)
df = pd.read_csv('prueba/salida_predicciones.csv')

# Producción (ejemplo)
# from flood_predictor_argentina import FloodPredictorArgentina
# predictor = FloodPredictorArgentina()
# df = predictor.make_predictions(timestamp_actual)
```

### Agregar Nuevas Secciones

El código está estructurado en funciones:

- `load_data()`: Carga de datos
- `compute_metrics()`: Cálculo de métricas
- `plot_time_series()`: Gráfico principal
- `plot_donut_risk()`: Gráfico donut
- `calculate_anticipation()`: Cálculo de anticipación

Puedes agregar nuevas funciones y llamarlas en `main()`.

## 📝 Notas

- La aplicación recalcula `prediccion_flood` y `flood_actual` según los umbrales del sidebar
- Las métricas se calculan en tiempo real según los filtros aplicados
- El dashboard es responsive y se adapta al ancho de la pantalla

## 🆘 Solución de Problemas

### Error: "No se encontró el archivo de datos"
- Asegúrate de que existe `prueba/salida_predicciones.csv`
- O modifica `load_data()` para usar tu fuente de datos

### Error: "ModuleNotFoundError: No module named 'streamlit'"
- Instala las dependencias: `pip install -r requirements_dashboard.txt`

### La aplicación no se abre
- Verifica que el puerto 8501 no esté en uso
- Ejecuta: `streamlit run app.py --server.port 8502`









