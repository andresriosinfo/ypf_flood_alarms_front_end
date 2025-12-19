# Generador de Gráficas de Evaluación - Versión Argentina

Este script genera todas las gráficas de evaluación del modelo de predicción de floods adaptado para datos argentinos.

## 📊 Gráficas Generadas

El script `generar_graficas_evaluacion.py` genera las siguientes 5 gráficas:

### 1. **roc_curve.png** - Curva ROC
- Muestra la capacidad discriminativa del modelo
- AUC-ROC indica qué tan bien el modelo distingue entre floods y no-floods
- Valores cercanos a 1.0 indican excelente capacidad

### 2. **precision_recall_curve.png** - Curva Precision-Recall
- Muestra el balance entre precisión y recall
- Útil cuando hay desbalance de clases
- Average Precision (AP) indica el rendimiento general

### 3. **confusion_matrix.png** - Matriz de Confusión
- Muestra los verdaderos/falsos positivos y negativos
- Permite ver exactamente dónde el modelo se equivoca
- Útil para entender el rendimiento del modelo

### 4. **prediction_distribution.png** - Distribución de Probabilidades
- Muestra cómo se distribuyen las probabilidades predichas
- Compara distribuciones entre clases reales (Flood vs No Flood)
- Incluye el umbral de decisión optimizado

### 5. **distribucion_activa.png** - Distribución de Alarmas Activas
- Muestra la distribución de la variable ACTIVE (alarmas activas)
- Incluye histograma, box plot, distribución logarítmica y serie temporal
- Muestra el umbral de flood utilizado

## 🚀 Uso

### Requisitos Previos

1. **Modelo entrenado**: Debe existir el archivo `flood_predictor_argentina.pkl`
   ```bash
   python flood_predictor_argentina.py
   ```

2. **Datos procesados**: Debe existir el archivo `datos_procesados.csv`
   ```bash
   python analizar_datos_optimizado.py
   ```

### Ejecutar el Script

```bash
cd version_argentina
python generar_graficas_evaluacion.py
```

### Salida

El script generará 5 archivos PNG en la carpeta `version_argentina/`:

```
version_argentina/
├── roc_curve.png
├── precision_recall_curve.png
├── confusion_matrix.png
├── prediction_distribution.png
└── distribucion_activa.png
```

## 📈 Interpretación de Resultados

### Curva ROC
- **AUC > 0.9**: Excelente capacidad discriminativa
- **AUC 0.8-0.9**: Buena capacidad discriminativa
- **AUC 0.7-0.8**: Capacidad aceptable
- **AUC < 0.7**: Capacidad limitada

### Curva Precision-Recall
- **AP > 0.8**: Excelente balance precisión-recall
- **AP 0.6-0.8**: Buen balance
- **AP < 0.6**: Necesita mejoras

### Matriz de Confusión
- **Verdaderos Positivos (TP)**: Floods correctamente predichos
- **Falsos Positivos (FP)**: Falsas alarmas
- **Falsos Negativos (FN)**: Floods no detectados
- **Verdaderos Negativos (TN)**: No-floods correctamente predichos

### Distribución de Probabilidades
- Las probabilidades de la clase "Flood" deberían estar más altas que las de "No Flood"
- El umbral optimizado separa bien las dos clases

### Distribución de Alarmas Activas
- Muestra la distribución de los datos de entrada
- El umbral de flood está marcado en rojo
- Ayuda a entender la naturaleza de los datos

## 🔧 Personalización

Si deseas modificar las gráficas, edita el archivo `generar_graficas_evaluacion.py`:

- **Tamaño de figuras**: Modifica `figsize` en cada función `plot_*`
- **Colores**: Modifica los colores en las funciones de plotting
- **Resolución**: Modifica `dpi` en `plt.savefig()`
- **Estilo**: Modifica `plt.style.use()` al inicio del script

## 📝 Notas

- Las gráficas se generan con alta resolución (300 DPI) para uso en presentaciones
- El script usa el mejor modelo (basado en F1-Score) para generar las gráficas
- Todas las gráficas están adaptadas al sistema argentino con sus datos específicos

## 🆘 Solución de Problemas

### Error: "No se pudo cargar el modelo"
- Ejecuta primero: `python flood_predictor_argentina.py`

### Error: "No se encontraron datos"
- Ejecuta primero: `python analizar_datos_optimizado.py`

### Gráficas no se generan
- Verifica que matplotlib y seaborn estén instalados:
  ```bash
  pip install matplotlib seaborn
  ```

## 📚 Referencias

- Sistema original: Ver `evaluar_modelo.py` y `evaluar_modelo_optimizado.py` en la raíz del proyecto
- Documentación del modelo: Ver `README.md` en esta carpeta
- Resultados de evaluación: Ver `resultados_evaluacion.txt`









