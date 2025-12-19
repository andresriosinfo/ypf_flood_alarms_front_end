# Configuración de Base de Datos

Este proyecto usa `config.yaml` para centralizar toda la configuración de bases de datos. Esto permite cambiar rápidamente de base de datos sin modificar código.

## Ubicación

El archivo de configuración está en: `version_argentina/config.yaml`

## Estructura

```yaml
database:
  server: "10.147.17.241"
  port: 1433
  username: "sa"
  password: "OtmsSecure2024Dev123"
  driver: "{ODBC Driver 17 for SQL Server}"
  schema: "dbo"

flood_system:
  input_database: "otms_main"                 # Base de datos de entrada
  input_table: "ypf_alarms"                  # Tabla de entrada (datos crudos)
  output_database: "otms_analytics"           # Base de datos de salida
  output_table: "ypf_flood_alarms"            # Tabla de salida (predicciones)

anomaly_system:
  input_database: "otms_main"                 # Base de datos de entrada
  input_table: "datos_proceso"                # Tabla de entrada
  output_database: "otms_analytics"           # Base de datos de salida
  output_table: "anomalies_detector"           # Tabla de salida
```

## Bases de Datos y Tablas

### Sistema de Predicción de Flood
- **Base de datos de entrada**: `otms_main` (configurable en `flood_system.input_database`)
- **Tabla de entrada**: `ypf_alarms` → Datos crudos de alarmas activas
- **Base de datos de salida**: `otms_analytics` (configurable en `flood_system.output_database`)
- **Tabla de salida**: `ypf_flood_alarms` → Predicciones de flood con probabilidades y alertas

### Sistema de Detección de Anomalías
- **Base de datos de entrada**: `otms_main` (configurable en `anomaly_system.input_database`)
- **Tabla de entrada**: `datos_proceso` → Datos de proceso en formato largo (datetime, variable_name, value)
- **Base de datos de salida**: `otms_analytics` (configurable en `anomaly_system.output_database`)
- **Tabla de salida**: `anomalies_detector` → Anomalías detectadas con scores y métricas

## Cómo Cambiar de Base de Datos

1. Edita `config.yaml`:
   ```yaml
   database:
     server: "nuevo_servidor"
     port: 1433
     username: "nuevo_usuario"
     password: "nueva_contraseña"
   ```

2. Si necesitas cambiar las bases de datos o tablas:
   ```yaml
   flood_system:
     input_database: "nueva_base_entrada"
     input_table: "nueva_tabla_entrada"
     output_database: "nueva_base_salida"
     output_table: "nueva_tabla_salida"
   ```

3. ¡Listo! Todos los scripts usarán automáticamente la nueva configuración.

## Scripts que Usan la Configuración

### Sistema de Flood
- `predecir_flood_sql.py` - Lee de `flood_system.input_table`, escribe en `flood_system.output_table`
- `insertar_datos_historicos.py` - Escribe en `flood_system.input_table`
- `crear_tablas_sql.py` - Crea las tablas según la configuración

### Sistema de Anomalías
- `detector_anomalias_streamlit/detect_from_sql.py` - Lee de `anomaly_system.input_table`, escribe en `anomaly_system.output_table`
- `detector_anomalias_streamlit/write_training_data_to_sql.py` - Escribe en `anomaly_system.input_table`
- `detector_anomalias_streamlit/worker_procesamiento.py` - Lee y escribe usando la configuración

## Notas

- El archivo `config.yaml` contiene credenciales sensibles. **NO** lo subas a repositorios públicos.
- Todos los scripts cargan la configuración automáticamente al iniciar.
- Si cambias el nombre de las tablas, asegúrate de que existan o ejecuta los scripts de creación de tablas.

