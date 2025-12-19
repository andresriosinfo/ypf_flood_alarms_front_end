# Documentación para Desarrolladores Web

Este directorio contiene las páginas de documentación que explican cómo construir cada visualización del dashboard desde las tablas SQL.

## Páginas Disponibles

1. **Tarjeta de Estado Principal** - Explica cómo construir la tarjeta de alerta de flood
2. **Tarjetas de Métricas** - Explica cómo construir las tarjetas de probabilidad y alarmas activas
3. **Gráfico de Tendencias** - Explica cómo construir el gráfico de líneas interactivo
4. **Métricas del Modelo** - Explica cómo calcular y mostrar Accuracy, Precision, Recall, F1-Score
5. **Matriz de Confusión** - Explica cómo construir la tabla de matriz de confusión

## Propósito

Cada página incluye:
- **Descripción** de la visualización
- **Datos necesarios** de las tablas SQL
- **Consultas SQL** de ejemplo listas para usar
- **Guías de implementación front-end** (conceptos generales, sin código específico)
- **Especificaciones de diseño** (colores, tamaños, estilos)
- **Ejemplos de estructura HTML/CSS**
- **Flujo de datos** desde SQL hasta la visualización
- **Consideraciones importantes** para la implementación

## Cómo Acceder

1. Ejecuta el Streamlit: `streamlit run app.py`
2. Usa el menú lateral para navegar entre las páginas
3. O accede directamente desde la URL: `/pages/1_Tarjeta_Estado_Principal`

## Notas para Desarrolladores

- Las consultas SQL están listas para usar, solo ajusta los parámetros según necesites
- Las guías de front-end son conceptuales - adapta a tu framework (React, Vue, Angular, etc.)
- Los colores y estilos siguen el diseño del dashboard principal
- Todas las consultas usan la tabla `ypf_flood_alarms` de la base de datos `otms_analytics`

