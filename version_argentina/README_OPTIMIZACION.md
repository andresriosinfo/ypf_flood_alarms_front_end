# Optimización de Hiperparámetros - Versión Argentina

Guía para optimizar los hiperparámetros del modelo de predicción de floods.

## 📋 Resumen

Este proceso permite mejorar el rendimiento del modelo ajustando los hiperparámetros mediante búsqueda automatizada.

## 🔄 Modelos de Respaldo

**IMPORTANTE**: Antes de optimizar, se crea automáticamente un respaldo:
- `flood_predictor_argentina_base.pkl` - Modelo original (respaldo)
- `flood_predictor_argentina.pkl` - Modelo actual (se actualiza después de optimizar)
- `flood_predictor_argentina_optimizado.pkl` - Modelo optimizado

## 🚀 Opciones de Optimización

### Opción 1: Optimización Rápida (Recomendada)

Optimiza solo XGBoost (el mejor modelo) con búsqueda rápida.

```bash
cd version_argentina
python optimizar_hiperparametros_rapido.py
```

**Características:**
- ⏱️ Tiempo: 5-10 minutos
- 🎯 Enfoque: Solo XGBoost (mejor modelo)
- 📊 Iteraciones: 25 combinaciones
- ✅ Ideal para: Mejoras rápidas

### Opción 2: Optimización Completa

Optimiza todos los modelos (XGBoost, Random Forest, Gradient Boosting) con búsqueda exhaustiva.

```bash
cd version_argentina
python optimizar_hiperparametros.py
```

**Características:**
- ⏱️ Tiempo: 30-60 minutos
- 🎯 Enfoque: Todos los modelos
- 📊 Iteraciones: 50-30 combinaciones por modelo
- ✅ Ideal para: Máxima optimización

## 📊 Qué se Optimiza

### XGBoost
- `n_estimators`: Número de árboles (150-300)
- `max_depth`: Profundidad máxima (5-8)
- `learning_rate`: Tasa de aprendizaje (0.05-0.15)
- `subsample`: Fracción de muestras (0.85-0.95)
- `colsample_bytree`: Fracción de features (0.85-0.95)
- `min_child_weight`: Peso mínimo por hoja (1-3)
- `gamma`: Reducción mínima de pérdida (0-0.1)
- `reg_alpha`: Regularización L1 (0-0.1)
- `reg_lambda`: Regularización L2 (1-1.5)

### Random Forest
- `n_estimators`: Número de árboles (100-300)
- `max_depth`: Profundidad máxima (10-18)
- `min_samples_split`: Mínimo para dividir (2-10)
- `min_samples_leaf`: Mínimo por hoja (1-5)
- `max_features`: Features por split
- `bootstrap`: Muestreo con reemplazo

### Gradient Boosting
- `n_estimators`: Número de árboles (100-300)
- `max_depth`: Profundidad máxima (3-9)
- `learning_rate`: Tasa de aprendizaje (0.01-0.2)
- `subsample`: Fracción de muestras (0.8-1.0)
- `min_samples_split`: Mínimo para dividir (2-10)
- `min_samples_leaf`: Mínimo por hoja (1-4)

## 📈 Métricas de Evaluación

La optimización busca maximizar el **F1-Score** usando validación cruzada temporal (TimeSeriesSplit).

Después de optimizar, se evalúan:
- **F1-Score**: Balance entre precisión y recall
- **Precision**: Exactitud de predicciones positivas
- **Recall**: Capacidad de detectar floods reales
- **AUC-ROC**: Capacidad discriminativa
- **Average Precision**: Rendimiento en Precision-Recall

## 🔍 Comparación con Modelo Base

Después de optimizar, el script muestra una comparación:

```
Métrica              Base            Optimizado      Mejora
------------------------------------------------------------
F1-Score            0.6587          0.6750          +0.0163
Precision           0.6710          0.6820          +0.0110
Recall              0.6468          0.6680          +0.0212
AUC-ROC             0.9435          0.9450          +0.0015
```

## ⚙️ Proceso de Optimización

1. **Carga de datos**: Se cargan los datos procesados
2. **Preparación**: Se recrean las features y el target
3. **Búsqueda**: RandomizedSearchCV prueba combinaciones aleatorias
4. **Validación**: TimeSeriesSplit respeta el orden temporal
5. **Evaluación**: Se evalúa en conjunto de test
6. **Guardado**: Se guarda el modelo optimizado

## 📝 Salida del Script

El script muestra:
- Progreso de la búsqueda
- Mejores parámetros encontrados
- Métricas en validación cruzada
- Métricas en conjunto de test
- Comparación con modelo base
- Archivos generados

## 🔧 Personalización

Si quieres ajustar la búsqueda, edita los archivos:

### Para optimización rápida:
- `optimizar_hiperparametros_rapido.py`
- Modifica `n_iter` para más/menos iteraciones
- Modifica `param_grid` para cambiar rangos

### Para optimización completa:
- `optimizar_hiperparametros.py`
- Modifica `n_iter` por modelo
- Ajusta `param_grid` de cada modelo

## ⚠️ Notas Importantes

1. **Tiempo de ejecución**: La optimización puede tardar varios minutos
2. **Recursos**: Usa todos los cores disponibles (n_jobs=-1)
3. **Respaldo**: El modelo base se guarda automáticamente
4. **Validación temporal**: Se usa TimeSeriesSplit para respetar orden temporal
5. **Balanceo**: Se aplica SMOTE si está disponible

## 🆘 Solución de Problemas

### Error: "No se encuentra el modelo base"
- Asegúrate de que existe `flood_predictor_argentina_base.pkl`
- Si no existe, el script usará valores por defecto

### Error: "Memoria insuficiente"
- Reduce `n_iter` en el script
- Reduce el tamaño del conjunto de entrenamiento

### Optimización muy lenta
- Usa `optimizar_hiperparametros_rapido.py` en lugar del completo
- Reduce `n_iter` y el rango de parámetros

## 📊 Resultados Esperados

Después de optimizar, puedes esperar mejoras de:
- **F1-Score**: +1-5% típicamente
- **Precision**: +1-3% típicamente
- **Recall**: +1-3% típicamente
- **AUC-ROC**: +0.1-0.5% típicamente (ya es muy alto)

## 🔄 Volver al Modelo Base

Si quieres volver al modelo original:

```bash
cd version_argentina
Copy-Item flood_predictor_argentina_base.pkl flood_predictor_argentina.pkl
```

## 📚 Próximos Pasos

Después de optimizar:
1. Ejecuta `evaluar_modelo_entrenado.py` para ver métricas detalladas
2. Ejecuta `generar_graficas_evaluacion.py` para generar gráficas actualizadas
3. Compara resultados con el modelo base

## 💡 Consejos

- **Primera vez**: Usa optimización rápida para ver mejoras
- **Máxima calidad**: Usa optimización completa si tienes tiempo
- **Iterativo**: Puedes ejecutar múltiples veces ajustando rangos
- **Monitoreo**: Revisa las métricas en cada ejecución









