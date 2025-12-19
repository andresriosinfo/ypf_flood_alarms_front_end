# Dashboard Streamlit - Sistema de Predicción de Flood de Alarmas

Este repositorio contiene el dashboard Streamlit con documentación para desarrolladores web.

## Estructura del Proyecto

```
version_argentina/
├── app.py                          # Dashboard principal
├── pages/                          # Páginas de documentación
│   ├── 1_Tarjeta_Estado_Principal.py
│   ├── 2_Tarjetas_Métricas.py
│   ├── 3_Gráfico_Tendencias.py
│   ├── 4_Métricas_Modelo.py
│   ├── 5_Matriz_Confusión.py
│   └── README.md
├── requirements_dashboard.txt       # Dependencias del dashboard
├── requirements.txt                # Dependencias generales
└── .streamlit/                     # Configuración de Streamlit
    └── config.toml
```

## Instalación

```bash
pip install -r requirements_dashboard.txt
```

## Ejecución

```bash
streamlit run app.py
```

## Documentación para Desarrolladores Web

Las páginas en `pages/` contienen documentación completa sobre cómo construir cada visualización desde las tablas SQL, incluyendo:

- Consultas SQL de ejemplo
- Estructura de datos necesaria
- Flujo de datos desde SQL hasta front-end
- Consideraciones importantes

Accede a la documentación desde el menú lateral del dashboard.
