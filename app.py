"""
Dashboard - Sistema de Predicción de Flood de Alarmas
Vista operativa para monitoreo en tiempo real
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# Configuración de la página
st.set_page_config(
    page_title="Sistema de Predicción de Flood",
    page_icon="⚠️",
    layout="wide",
    initial_sidebar_state="expanded"  # Cambiado a expanded para mostrar navegación
)

# CSS personalizado con fuente Nunito y estilo Schneider
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Nunito:wght@300;400;600;700&display=swap');
    
    html, body, [class*="css"]  {
        font-family: 'Nunito', -apple-system, BlinkMacSystemFont,
                     "Segoe UI", Helvetica, Arial, sans-serif;
        color: #333333;
    }
    
    h1, h2, h3 {
        font-weight: 600;
        letter-spacing: 0.02em;
        color: #2E9A42;
    }
    
    .stApp {
        background-color: #F5F5F5;
    }
    
    .main .block-container {
        padding-top: 1rem;
        padding-bottom: 1rem;
    }
    </style>
""", unsafe_allow_html=True)


def load_data():
    """
    Carga los datos de predicción.
    
    NOTA: En producción, reemplazar con la salida directa del modelo entrenado.
    """
    try:
        # Intentar cargar desde diferentes ubicaciones posibles
        paths = [
            'prueba/salida_predicciones.csv',
            'salida_predicciones.csv',
            'data/salida_predicciones.csv'
        ]
        
        df = None
        for path in paths:
            try:
                df = pd.read_csv(path)
                break
            except FileNotFoundError:
                continue
        
        if df is None:
            st.warning("No se encontró el archivo de datos. Usando datos de ejemplo.")
            # Crear datos de ejemplo para demostración
            dates = pd.date_range(start='2025-01-01', periods=100, freq='30min')
            df = pd.DataFrame({
                'timestamp': dates,
                'active_alarms': np.random.randint(100, 300, 100),
                'probabilidad_flood': np.random.uniform(0, 1, 100),
                'prediccion_flood': 0,
                'flood_actual': 0
            })
            df['prediccion_flood'] = (df['probabilidad_flood'] >= 0.6).astype(int)
            df['flood_actual'] = (df['active_alarms'] >= 225).astype(int)
        
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df = df.sort_values('timestamp').reset_index(drop=True)
        return df
    except Exception as e:
        st.error(f"Error cargando datos: {e}")
        return None


def get_current_status(df, prob_threshold=0.6, flood_threshold=225):
    """
    Obtiene el estado actual del sistema (último registro).
    """
    if len(df) == 0:
        return None
    
    # Último registro
    ultimo = df.iloc[-1].copy()
    
    # Recalcular predicción y flood actual
    ultimo['prediccion_flood'] = 1 if ultimo['probabilidad_flood'] >= prob_threshold else 0
    ultimo['flood_actual'] = 1 if ultimo['active_alarms'] >= flood_threshold else 0
    
    return ultimo


def plot_simple_trend(df, flood_threshold=225, n_points=48):
    """
    Gráfico simple de tendencia de las últimas N horas.
    """
    # Últimas N horas (n_points intervalos de 30 min)
    df_recent = df.tail(n_points).copy()
    
    fig = go.Figure()
    
    # Línea de alarmas activas
    fig.add_trace(go.Scatter(
        x=df_recent['timestamp'],
        y=df_recent['active_alarms'],
        mode='lines',
        name='Alarmas Activas',
        line=dict(color='#3DCD58', width=3),
        fill='tozeroy',
        fillcolor='rgba(61, 205, 88, 0.1)',
        hovertemplate='%{x}<br>Alarmas: %{y}<extra></extra>'
    ))
    
    # Umbral de flood
    fig.add_hline(
        y=flood_threshold,
        line_dash="dash",
        line_color="#DC143C",
        line_width=2,
        annotation_text=f"Umbral: {flood_threshold}",
        annotation_position="right"
    )
    
    # Probabilidad de flood (eje secundario)
    fig.add_trace(go.Scatter(
        x=df_recent['timestamp'],
        y=df_recent['probabilidad_flood'] * 100,
        mode='lines',
        name='Probabilidad Flood (%)',
        line=dict(color='#2E9A42', width=2, dash='dot'),
        yaxis='y2',
        hovertemplate='%{x}<br>Probabilidad: %{y:.1f}%<extra></extra>'
    ))
    
    fig.update_layout(
        xaxis_title='Tiempo',
        yaxis_title='Alarmas Activas',
        yaxis2=dict(
            title='Probabilidad Flood (%)',
            overlaying='y',
            side='right',
            range=[0, 100]
        ),
        hovermode='x unified',
        template='plotly_white',
        height=400,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        margin=dict(l=50, r=50, t=20, b=50),
        plot_bgcolor='#FFFFFF',
        paper_bgcolor='#FFFFFF'
    )
    
    return fig


def main():
    """Función principal de la aplicación."""
    
    # Cargar datos
    df = load_data()
    if df is None:
        st.stop()
    
    # Sidebar mínimo
    with st.sidebar:
        st.markdown("### Documentación")
        st.markdown("""
        **Para Desarrolladores Web:**
        
        Las páginas de documentación explican cómo construir cada visualización desde las tablas SQL.
        
        Incluyen:
        - Consultas SQL de ejemplo
        - Guías de implementación front-end
        """)
        st.markdown("---")
        st.markdown("### Configuración")
        
        prob_threshold = st.slider(
            "Umbral de probabilidad",
            min_value=0.0,
            max_value=1.0,
            value=0.6,
            step=0.05
        )
        
        flood_threshold = st.number_input(
            "Umbral de alarmas para flood",
            min_value=0,
            value=225,
            step=10
        )
        
        horas_visualizar = st.slider(
            "Horas a visualizar",
            min_value=6,
            max_value=48,
            value=24,
            step=6
        )
    
    # Obtener estado actual
    estado_actual = get_current_status(df, prob_threshold, flood_threshold)
    
    if estado_actual is None:
        st.error("No hay datos disponibles")
        st.stop()
    
    # ==========================================
    # SECCIÓN PRINCIPAL: ESTADO ACTUAL
    # ==========================================
    
    # Título
    st.title("Sistema de Predicción de Flood de Alarmas")
    
    # Nota sobre documentación
    st.info("""
    **Documentación para Desarrolladores**: 
    Usa el menú lateral para acceder a las páginas de documentación que explican cómo construir 
    cada visualización desde las tablas SQL. Incluye consultas SQL y guías de implementación front-end.
    """)
    
    st.markdown("---")
    
    # Tarjeta de estado principal
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        # Predicción principal
        if estado_actual['prediccion_flood'] == 1:
            st.markdown("""
            <div style='background-color: #DC143C; color: white; padding: 2rem; border-radius: 12px; text-align: center;'>
                <h1 style='color: white; margin: 0; font-size: 3rem;'>ALERTA DE FLOOD</h1>
                <p style='font-size: 1.2rem; margin-top: 1rem;'>Se predice flood de alarmas en las próximas 2 horas</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style='background-color: #3DCD58; color: white; padding: 2rem; border-radius: 12px; text-align: center;'>
                <h1 style='color: white; margin: 0; font-size: 3rem;'>ESTADO NORMAL</h1>
                <p style='font-size: 1.2rem; margin-top: 1rem;'>No se predice flood en las próximas 2 horas</p>
            </div>
            """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style='background-color: #FFFFFF; padding: 1.5rem; border-radius: 12px; border: 2px solid #E5E5E5; text-align: center;'>
            <div style='color: #333333; font-size: 0.9rem; margin-bottom: 0.5rem;'>PROBABILIDAD DE FLOOD</div>
            <div style='color: #2E9A42; font-size: 3rem; font-weight: 700;'>{:.1f}%</div>
            <div style='color: #666666; font-size: 0.8rem; margin-top: 0.5rem;'>Próximas 2 horas</div>
        </div>
        """.format(estado_actual['probabilidad_flood'] * 100), unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style='background-color: #FFFFFF; padding: 1.5rem; border-radius: 12px; border: 2px solid #E5E5E5; text-align: center;'>
            <div style='color: #333333; font-size: 0.9rem; margin-bottom: 0.5rem;'>ALARMAS ACTIVAS</div>
            <div style='color: #2E9A42; font-size: 3rem; font-weight: 700;'>{}</div>
            <div style='color: #666666; font-size: 0.8rem; margin-top: 0.5rem;'>En este momento</div>
        </div>
        """.format(int(estado_actual['active_alarms'])), unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Información adicional
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div style='background-color: #FFFFFF; padding: 1rem; border-radius: 8px; border-left: 4px solid #3DCD58;'>
            <div style='color: #666666; font-size: 0.85rem;'>Última actualización</div>
            <div style='color: #333333; font-size: 1.1rem; font-weight: 600; margin-top: 0.5rem;'>
                {estado_actual['timestamp'].strftime('%H:%M:%S')}
            </div>
            <div style='color: #666666; font-size: 0.8rem; margin-top: 0.2rem;'>
                {estado_actual['timestamp'].strftime('%d/%m/%Y')}
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        # Determinar nivel de riesgo
        prob = estado_actual['probabilidad_flood']
        if prob >= 0.7:
            riesgo = "ALTO"
            color_riesgo = "#DC143C"
        elif prob >= 0.4:
            riesgo = "MEDIO"
            color_riesgo = "#FFA500"
        else:
            riesgo = "BAJO"
            color_riesgo = "#3DCD58"
        
        st.markdown(f"""
        <div style='background-color: #FFFFFF; padding: 1rem; border-radius: 8px; border-left: 4px solid {color_riesgo};'>
            <div style='color: #666666; font-size: 0.85rem;'>Nivel de Riesgo</div>
            <div style='color: {color_riesgo}; font-size: 1.1rem; font-weight: 600; margin-top: 0.5rem;'>
                {riesgo}
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        flood_actual = "SÍ" if estado_actual['flood_actual'] == 1 else "NO"
        color_flood = "#DC143C" if estado_actual['flood_actual'] == 1 else "#3DCD58"
        
        st.markdown(f"""
        <div style='background-color: #FFFFFF; padding: 1rem; border-radius: 8px; border-left: 4px solid {color_flood};'>
            <div style='color: #666666; font-size: 0.85rem;'>Flood Actual</div>
            <div style='color: {color_flood}; font-size: 1.1rem; font-weight: 600; margin-top: 0.5rem;'>
                {flood_actual}
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        # Tiempo hasta próximo flood (si se predice)
        if estado_actual['prediccion_flood'] == 1:
            tiempo_texto = "Inminente"
        else:
            # Buscar próxima predicción de flood
            futuras = df[df['timestamp'] > estado_actual['timestamp']]
            futuras_flood = futuras[futuras['probabilidad_flood'] >= prob_threshold]
            if len(futuras_flood) > 0:
                tiempo_dif = futuras_flood.iloc[0]['timestamp'] - estado_actual['timestamp']
                horas = tiempo_dif.total_seconds() / 3600
                tiempo_texto = f"{horas:.1f} horas"
            else:
                tiempo_texto = "No previsto"
        
        st.markdown(f"""
        <div style='background-color: #FFFFFF; padding: 1rem; border-radius: 8px; border-left: 4px solid #2E9A42;'>
            <div style='color: #666666; font-size: 0.85rem;'>Próximo Flood</div>
            <div style='color: #333333; font-size: 1.1rem; font-weight: 600; margin-top: 0.5rem;'>
                {tiempo_texto}
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # ==========================================
    # GRÁFICO DE TENDENCIA
    # ==========================================
    st.markdown("## Tendencias Recientes")
    
    n_points = int(horas_visualizar * 2)  # Convertir horas a intervalos de 30 min
    fig_trend = plot_simple_trend(df, flood_threshold, n_points)
    st.plotly_chart(fig_trend, use_container_width=True)
    
    st.markdown("---")
    
    # ==========================================
    # INFORMACIÓN ADICIONAL (colapsable)
    # ==========================================
    with st.expander("Información Técnica del Modelo"):
        # Calcular métricas básicas
        df['prediccion_flood'] = (df['probabilidad_flood'] >= prob_threshold).astype(int)
        df['flood_actual'] = (df['active_alarms'] >= flood_threshold).astype(int)
        
        tp = ((df['prediccion_flood'] == 1) & (df['flood_actual'] == 1)).sum()
        tn = ((df['prediccion_flood'] == 0) & (df['flood_actual'] == 0)).sum()
        fp = ((df['prediccion_flood'] == 1) & (df['flood_actual'] == 0)).sum()
        fn = ((df['prediccion_flood'] == 0) & (df['flood_actual'] == 1)).sum()
        
        total = len(df)
        accuracy = (tp + tn) / total if total > 0 else 0
        precision = tp / (tp + fp) if (tp + fp) > 0 else 0
        recall = tp / (tp + fn) if (tp + fn) > 0 else 0
        f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### Métricas del Modelo")
            st.metric("Accuracy", f"{accuracy:.2%}")
            st.metric("Precision", f"{precision:.2%}")
            st.metric("Recall", f"{recall:.2%}")
            st.metric("F1-Score", f"{f1:.2%}")
        
        with col2:
            st.markdown("### Matriz de Confusión")
            st.markdown(f"""
            <table style='width: 100%; border-collapse: collapse;'>
                <tr style='background-color: #2E9A42; color: white;'>
                    <th style='padding: 0.5rem;'></th>
                    <th style='padding: 0.5rem;'>Pred No Flood</th>
                    <th style='padding: 0.5rem;'>Pred Flood</th>
                </tr>
                <tr>
                    <td style='background-color: #F5F5F5; font-weight: 600; padding: 0.5rem;'>Real No Flood</td>
                    <td style='padding: 0.5rem; text-align: center;'>{tn:,}</td>
                    <td style='padding: 0.5rem; text-align: center; color: #DC143C;'>{fp:,}</td>
                </tr>
                <tr>
                    <td style='background-color: #F5F5F5; font-weight: 600; padding: 0.5rem;'>Real Flood</td>
                    <td style='padding: 0.5rem; text-align: center; color: #DC143C;'>{fn:,}</td>
                    <td style='padding: 0.5rem; text-align: center; color: #2E9A42; font-weight: 600;'>{tp:,}</td>
                </tr>
            </table>
            """, unsafe_allow_html=True)
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666666; padding: 1rem; font-size: 0.85rem;'>
        Sistema de Predicción de Flood de Alarmas - Horizonte: 2 horas | Modelo Base (XGBoost)
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
