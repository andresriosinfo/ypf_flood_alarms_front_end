# Sistema de Predicción de Flood de Alarmas

Dashboard web para monitoreo y predicción de floods de alarmas con horizonte de 2 horas.

## 🚀 Despliegue

Esta aplicación está desplegada en [Streamlit Cloud](https://streamlit.io/cloud).

## 📋 Características

- **Predicción en tiempo real**: Horizonte de 2 horas
- **Vista operativa**: Diseñada para operarios de planta
- **Interfaz industrial**: Estilo Schneider Electric
- **Métricas en vivo**: Probabilidad, alarmas activas, nivel de riesgo

## 🛠️ Tecnologías

- **Streamlit**: Framework web
- **XGBoost**: Modelo de Machine Learning
- **Plotly**: Visualizaciones interactivas
- **Pandas**: Procesamiento de datos

## 📁 Estructura

```
├── app.py                    # Aplicación principal
├── requirements.txt          # Dependencias
├── .streamlit/
│   └── config.toml          # Configuración de tema
└── README.md                # Este archivo
```

## 🔧 Configuración Local

```bash
# Instalar dependencias
pip install -r requirements.txt

# Ejecutar aplicación
streamlit run app.py
```

## 📝 Notas

- El modelo base se carga desde `flood_predictor_argentina_base.pkl`
- Los datos se cargan desde `prueba/salida_predicciones.csv`
- En producción, conectar con base de datos o API
