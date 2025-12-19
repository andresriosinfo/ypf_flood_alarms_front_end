"""
Documentación: Tarjetas de Métricas
Explica cómo construir las tarjetas de métricas (Probabilidad, Alarmas Activas) desde las tablas SQL
"""

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

st.set_page_config(
    page_title="Tarjetas Métricas - Documentación",
    page_icon="",
    layout="wide"
)

st.title("Tarjetas de Métricas")
st.markdown("---")

# Mostrar el elemento visual tal como aparece en app.py
st.markdown("### Ejemplo Visual")
st.markdown("Así aparecen las tarjetas de métricas en el dashboard:")

# Crear datos de ejemplo
dates = pd.date_range(start='2025-01-01', periods=100, freq='30min')
df_ejemplo = pd.DataFrame({
    'timestamp': dates,
    'active_alarms': np.random.randint(100, 300, 100),
    'probabilidad_flood': np.random.uniform(0, 1, 100),
})
df_ejemplo['timestamp'] = pd.to_datetime(df_ejemplo['timestamp'])

# Obtener último estado
estado_ejemplo = df_ejemplo.iloc[-1].copy()

# Mostrar tarjetas
col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div style='background-color: #FFFFFF; padding: 1.5rem; border-radius: 12px; border: 2px solid #E5E5E5; text-align: center;'>
        <div style='color: #333333; font-size: 0.9rem; margin-bottom: 0.5rem;'>PROBABILIDAD DE FLOOD</div>
        <div style='color: #2E9A42; font-size: 3rem; font-weight: 700;'>{:.1f}%</div>
        <div style='color: #666666; font-size: 0.8rem; margin-top: 0.5rem;'>Próximas 2 horas</div>
    </div>
    """.format(estado_ejemplo['probabilidad_flood'] * 100), unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div style='background-color: #FFFFFF; padding: 1.5rem; border-radius: 12px; border: 2px solid #E5E5E5; text-align: center;'>
        <div style='color: #333333; font-size: 0.9rem; margin-bottom: 0.5rem;'>ALARMAS ACTIVAS</div>
        <div style='color: #2E9A42; font-size: 3rem; font-weight: 700;'>{}</div>
        <div style='color: #666666; font-size: 0.8rem; margin-top: 0.5rem;'>En este momento</div>
    </div>
    """.format(int(estado_ejemplo['active_alarms'])), unsafe_allow_html=True)

st.markdown("---")

st.markdown("""
## Descripción de la Visualización

Las **Tarjetas de Métricas** muestran información numérica clave en formato de tarjetas compactas. 
En el dashboard principal hay dos tarjetas principales:

1. **Probabilidad de Flood** - Muestra el porcentaje de probabilidad
2. **Alarmas Activas** - Muestra el número actual de alarmas activas

### Características Visuales:
- Tarjetas compactas con información numérica
- Número grande y destacado
- Etiqueta descriptiva
- Valor secundario o contexto adicional
""")

st.markdown("---")

st.markdown("## Datos Necesarios")

st.markdown("""
### Tabla: `ypf_flood_alarms`

**Columnas relevantes:**
- `probabilidad_flood` (FLOAT) - Probabilidad entre 0.0 y 1.0 (convertir a porcentaje)
- `active_actual` (INT) - Número de alarmas activas en el momento de la predicción
- `timestamp` (DATETIME) - Fecha y hora de la predicción
- `fecha_prediccion` (DATETIME) - Para obtener el registro más reciente
""")

st.markdown("---")

st.markdown("## Consultas SQL")

st.markdown("### Consulta para Obtener Métricas Actuales")

st.code("""
-- Obtener las métricas más recientes
SELECT TOP 1
    probabilidad_flood,
    active_actual,
    timestamp,
    fecha_prediccion
FROM dbo.ypf_flood_alarms
ORDER BY fecha_prediccion DESC
""", language="sql")

st.markdown("### Consulta para Estadísticas Adicionales (Opcional)")

st.code("""
-- Obtener promedio de probabilidad en últimas 24 horas
SELECT 
    AVG(probabilidad_flood) as prob_promedio_24h,
    MAX(active_actual) as max_alarmas_24h,
    MIN(active_actual) as min_alarmas_24h
FROM dbo.ypf_flood_alarms
WHERE fecha_prediccion >= DATEADD(HOUR, -24, GETDATE())
""", language="sql")

st.markdown("---")

st.markdown("## Flujo de Datos")

st.markdown("""
```
┌─────────────┐
│  SQL Server │
│ ypf_flood_  │
│   alarms    │
└──────┬──────┘
       │
       │ SELECT probabilidad_flood, active_actual
       │ ORDER BY fecha_prediccion DESC
       ▼
┌─────────────┐
│   Backend   │
│   (API)     │
└──────┬──────┘
       │
       │ JSON: {probabilidad_flood: 0.75, active_actual: 245}
       ▼
┌─────────────┐
│  Frontend   │
│  Component  │
└─────────────┘
       │
       │ Formateo y Renderizado
       ▼
┌─────────────┐
│   Tarjetas  │
│   Métricas  │
└─────────────┘
""")

st.markdown("---")

st.markdown("## Consideraciones Importantes")

st.markdown("""
1. **Formateo de Números**: Usar funciones de formateo de tu framework para consistencia
2. **Colores Dinámicos**: Implementar lógica para cambiar color según el valor de probabilidad
3. **Responsive**: Asegurar que las tarjetas se adapten bien a diferentes tamaños de pantalla
4. **Accesibilidad**: Usar etiquetas semánticas y asegurar contraste adecuado
5. **Animaciones**: Considerar animaciones sutiles al actualizar valores (contador animado)
""")
