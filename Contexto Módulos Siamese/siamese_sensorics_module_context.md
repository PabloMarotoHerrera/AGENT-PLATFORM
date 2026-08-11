# Siamese — Módulo de Sensórica e Ingesta de Datos

**Documento:** Contexto técnico del módulo de sensórica dentro de Siamese  
**Proyecto:** Siamese — plataforma agéntica de gemelos digitales energéticos  
**Estado:** Documento de arquitectura conceptual previo a implementación  
**Versión:** 0.1  
**Propósito:** definir el papel del módulo de sensórica en Siamese, sus responsabilidades, arquitectura, conectores, almacenamiento, limpieza de datos, uso para calibración, generación de datasets, modelos surrogados, inferencia, visualización, alertas, DSX Air/NetworkSim y flujos agénticos.

---

## 1. Resumen ejecutivo

El módulo de sensórica es la capa que conecta Siamese con el edificio real.

Hasta este punto, Siamese cuenta con:

```text
EnergyPlus
→ solver físico de simulación energética

Backend Python
→ modelo interno, validación, compilación, ejecución, resultados normalizados

Omniverse Kit
→ interfaz visual, semántica USD, RTX, extensiones y workspace de ingeniería

Calibración
→ ajuste del modelo simulado al comportamiento medido del edificio real
```

La sensórica introduce el dato vivo:

```text
sensores / BMS / CSV / MQTT / APIs
→ datos reales del edificio
→ limpieza y almacenamiento
→ comparación con EnergyPlus
→ calibración
→ entrenamiento de surrogates
→ inferencia
→ visualización
→ recomendaciones
```

Sin sensórica, Siamese puede simular.  
Con sensórica, Siamese puede observar.

La frase central del módulo es:

> **Sin sensores, el modelo calcula. Con sensores, el modelo observa.**

---

## 2. Qué es el módulo de sensórica

El módulo de sensórica e ingesta de datos es el sistema encargado de capturar, normalizar, limpiar, almacenar, consultar y conectar los datos reales del edificio con el resto de módulos de Siamese.

No debe entenderse como un simple lector de sensores.

Debe responder preguntas como:

```text
¿Qué sensores existen?
¿Dónde están colocados?
¿Qué variable mide cada sensor?
¿A qué zona térmica pertenece?
¿Qué calidad tienen sus datos?
¿Están funcionando correctamente?
¿Hay huecos, ruido, outliers o drift?
¿Qué datos sirven para calibrar?
¿Qué datos sirven para inferencia?
¿Qué datos se deben visualizar?
¿Qué datos se deben excluir?
```

En el TFG del C.E.P. Divino Maestro ya apareció este problema de forma práctica: se instalaron sensores Govee de temperatura y humedad, pero los datos debían exportarse a CSV, enviarse por correo, limpiarse y graficarse manualmente. Siamese debe convertir ese flujo en una infraestructura integrada, automatizable y conectada al modelo energético.

---

## 3. Por qué este módulo es crítico

EnergyPlus simula un edificio bajo hipótesis.  
La sensórica muestra cómo se comporta realmente el edificio.

La sensórica permite:

```text
calibrar el modelo energético;
comparar realidad vs simulación;
detectar desviaciones;
visualizar el estado actual;
alimentar modelos surrogados;
inferir estados futuros;
detectar fallos de sensores;
evaluar recomendaciones;
cerrar el ciclo operación → medición → aprendizaje.
```

El paso conceptual es:

```text
modelo energético = hipótesis física
modelo energético + sensórica = modelo calibrable
modelo calibrado + sensórica + surrogate = gemelo energético operativo
```

Este módulo es, por tanto, una pieza fundacional para que Siamese no sea solo una herramienta de simulación, sino una plataforma de gemelos energéticos vivos.

---

## 4. Responsabilidades del módulo

El módulo de sensórica debe asumir las siguientes responsabilidades:

```text
1. Registrar sensores y fuentes de datos.
2. Importar datos históricos desde CSV.
3. Recibir datos en tiempo real mediante MQTT u otros conectores.
4. Conectarse a APIs REST de plataformas externas.
5. Preparar conectores futuros para BACnet, Modbus, OPC-UA y BMS.
6. Normalizar timestamps, unidades, nombres, variables y formatos.
7. Limpiar datos reales.
8. Detectar huecos, outliers, drift, datos congelados y sensores offline.
9. Preservar datos raw para auditoría.
10. Almacenar series temporales normalizadas.
11. Mantener estado live/latest por sensor.
12. Vincular sensores con zonas, espacios, sistemas HVAC y variables.
13. Preparar datos para calibración.
14. Preparar features para modelos surrogados.
15. Alimentar inferencia en tiempo real.
16. Visualizar datos en Omniverse Kit.
17. Generar alertas y diagnósticos.
18. Proveer evidencia a flujos agénticos.
```

La regla central:

```text
Los sensores no deben llegar directamente a Omniverse, calibración, datasets o surrogates.
Primero deben pasar por normalización, control de calidad y almacenamiento.
```

---

## 5. Arquitectura general

Arquitectura conceptual:

```text
Fuentes de datos
    ↓
Connectors
    ↓
Raw Ingestion
    ↓
Normalization
    ↓
Data Quality Layer
    ↓
Time-Series Storage
    ↓
Sensor-Zone Binding
    ↓
Feature Builder
    ↓
Calibración / Surrogates / Visualización / Control
```

Arquitectura detallada:

```text
CSV / MQTT / REST / BACnet / Modbus / OPC-UA / BMS
        ↓
Sensor Connector Layer
        ↓
Raw Sensor Event Store
        ↓
Normalizer + Unit Converter
        ↓
Timestamp Alignment + Cleaning
        ↓
Quality Flags + Sensor Health
        ↓
Time-Series Database / Parquet
        ↓
Sensor Registry + Building Binding
        ↓
Live State API + Historical Query API
        ↓
Omniverse / Calibration / Dataset Factory / Surrogate Inference
```

---

## 6. Fuentes de datos

### 6.1 CSV

CSV será la primera fuente que debe soportar Siamese porque muchos proyectos iniciales tendrán datos históricos exportados desde:

```text
sensores baratos;
apps comerciales;
hojas Excel;
dataloggers;
BMS exportado;
auditorías previas;
contadores energéticos;
proyectos académicos;
mantenedoras.
```

En el caso del TFG, el flujo era:

```text
sensores Govee
→ app Govee Home
→ exportación CSV
→ envío por correo
→ limpieza manual
→ gráficas
→ comparación con DesignBuilder
```

Siamese debe convertir esto en:

```text
CSV
→ import wizard
→ normalización
→ sensor registry
→ quality report
→ storage
→ calibración / visualización / surrogate
```

#### Ventajas de CSV

```text
rápido para MVP;
útil para pilotos;
compatible con datos históricos;
no requiere infraestructura live;
permite calibración inicial.
```

#### Limitaciones de CSV

```text
no es tiempo real;
formatos inconsistentes;
timestamps ambiguos;
separador decimal variable;
nombres de columnas heterogéneos;
unidades no normalizadas;
datos enviados de forma manual.
```

#### CSV Import Wizard

Siamese debe incluir un asistente para:

```text
subir archivo;
detectar columnas;
seleccionar timestamp;
seleccionar variable;
seleccionar unidad;
asignar sensor;
asignar zona;
previsualizar datos;
detectar huecos;
detectar outliers;
generar dataset normalizado;
emitir quality report.
```

### 6.2 MQTT

MQTT será el conector natural para sensórica IoT en tiempo real.

Flujo:

```text
sensor / gateway
→ MQTT broker
→ Siamese MQTT Connector
→ ingestion service
→ time-series storage
→ live state
```

Ejemplo de topic:

```text
siamese/building_001/floor_01/aula_3b/temperature
siamese/building_001/floor_01/aula_3b/humidity
siamese/building_001/hvac/ahu_01/supply_temp
```

Ejemplo de payload recomendado:

```json
{
  "sensor_id": "sensor_aula_3b_temp_01",
  "timestamp": "2026-07-23T10:24:00Z",
  "variable": "temperature",
  "value": 22.8,
  "unit": "C",
  "quality": "raw"
}
```

#### Ventajas de MQTT

```text
ligero;
asíncrono;
extendido en IoT;
útil para gateways edge;
permite streaming;
encaja con edificios distribuidos.
```

#### Riesgos de MQTT

```text
mensajes duplicados;
mensajes fuera de orden;
pérdida de conexión;
QoS mal configurado;
topics inconsistentes;
payloads no versionados;
problemas de autenticación.
```

Siamese debe definir un contrato propio de topic/payload para evitar integración caótica.

### 6.3 REST/API

Muchos sistemas modernos exponen datos por APIs REST.

Casos:

```text
plataformas IoT cloud;
sensores comerciales;
servicios meteorológicos;
contadores;
BMS modernos;
sistemas de mantenimiento;
herramientas de facility management.
```

El conector REST debe soportar:

```text
polling;
autenticación;
paginación;
rate limits;
reintentos;
normalización de respuestas;
mapeo de campos;
detección de duplicados.
```

### 6.4 BACnet

BACnet será importante para edificios con automatización y BMS.

Datos típicos:

```text
temperaturas de zona;
setpoints;
estado de equipos;
válvulas;
fan coils;
UTAs;
alarmas;
horarios;
actuadores.
```

En fases iniciales, BACnet debe ser lectura. La escritura hacia BMS debe reservarse para control supervisado, con permisos y validación.

### 6.5 Modbus

Modbus será útil para:

```text
contadores eléctricos;
analizadores de red;
consumos;
potencias;
caudales;
temperaturas;
equipos HVAC;
sistemas industriales sencillos.
```

### 6.6 OPC-UA

OPC-UA será relevante en contextos industriales o entornos OT más estructurados.

Puede aportar:

```text
modelos de información;
datos OT;
integración robusta;
jerarquías de equipos;
monitorización industrial.
```

### 6.7 BMS

El BMS no es un protocolo concreto, sino una fuente operacional.

Siamese debe poder leer:

```text
estado HVAC;
setpoints;
temperaturas;
caudales;
consumos;
horarios;
alarmas;
modos de operación;
intervenciones manuales.
```

Fases recomendadas:

```text
Fase 1: lectura.
Fase 2: recomendaciones.
Fase 3: shadow mode.
Fase 4: control supervisado.
Fase 5: control limitado.
```

---

## 7. Tipos de datos

### 7.1 Datos ambientales interiores

```text
temperatura;
humedad relativa;
CO₂;
COV;
partículas;
iluminancia;
ruido;
presencia;
ocupación.
```

### 7.2 Datos ambientales exteriores

```text
temperatura exterior;
humedad exterior;
radiación solar;
viento;
precipitación;
datos EPW;
datos meteorológicos locales;
forecast.
```

### 7.3 Datos energéticos

```text
electricidad;
gas;
calor;
frío;
ACS;
potencia instantánea;
energía acumulada;
tarifa;
coste;
emisiones.
```

### 7.4 Datos HVAC

```text
temperatura impulsión;
temperatura retorno;
caudal;
estado de bomba;
estado de ventilador;
posición de válvula;
velocidad VFD;
modo de equipo;
setpoint;
estado UTA;
alarma equipo.
```

### 7.5 Datos operativos

```text
horarios reales;
ocupación real;
eventos especiales;
ventanas abiertas;
persianas;
mantenimiento;
cambios manuales;
incidencias;
modo vacaciones.
```

---

## 8. Sensor Registry

Antes de guardar datos, Siamese debe conocer qué sensores existen.

Cada sensor debe tener identidad propia:

```yaml
Sensor:
  sensor_id: sensor_aula_3b_temp_01
  building_id: building_001
  label: Aula 3B Temperature
  variable: temperature
  unit: C
  source_type: mqtt
  source_id: govee_gateway_01
  status: operational
  created_at: timestamp
```

El registro permite:

```text
mapear sensores a zonas;
visualizarlos en Omniverse;
usarlos como targets de calibración;
usarlos como features para surrogates;
detectar sensores faltantes;
gestionar salud del sensor;
controlar permisos;
emitir alertas.
```

Sin Sensor Registry, Siamese tendría solo series temporales sueltas. Con Sensor Registry, los datos se vuelven entidades del gemelo.

---

## 9. Sensor-Zone Binding

El dato es útil cuando está conectado a una entidad del edificio.

Un sensor debe poder vincularse a:

```text
edificio;
planta;
espacio;
zona térmica;
superficie;
sistema HVAC;
equipo;
variable;
rol operativo.
```

Ejemplo:

```yaml
SensorBinding:
  binding_id: bind_001
  sensor_id: sensor_aula_3b_temp_01
  target_entity_type: ThermalZone
  target_entity_id: aula_3b
  measured_variable: zone_air_temperature
  calibration_role: target
  visualization_role: live_overlay
  surrogate_role: feature
```

Un sensor puede cumplir múltiples roles:

```text
visualización;
calibración;
feature surrogate;
validación;
alertas;
detección de anomalías.
```

---

## 10. Ingesta en tiempo real

Flujo live:

```text
MQTT / REST / BMS
→ Ingestion Service
→ validation
→ normalization
→ time-series write
→ live state cache
→ event bus
→ Omniverse/Web update
→ surrogate feature builder
```

La ingesta live debe separar:

```text
ruta histórica:
dato normalizado → time-series storage

ruta operativa:
último dato válido → live state cache/API

ruta ML:
feature builder → surrogate inference
```

Frecuencias distintas:

```text
sensor mide cada 10 segundos;
dashboard actualiza cada 30 segundos;
surrogate infiere cada 5 minutos;
calibración usa datos agregados a 10 minutos.
```

No todo dato recibido debe disparar inferencia o visualización.

---

## 11. Ingesta histórica

Flujo batch:

```text
CSV / archivo histórico
→ import job
→ schema detection
→ validation
→ cleaning
→ normalized time-series
→ quality report
→ calibration-ready dataset
```

El resultado debe incluir un informe:

```text
número de filas;
periodo cubierto;
frecuencia estimada;
huecos;
outliers;
sensores detectados;
zonas asignadas;
unidades;
calidad global;
usabilidad para calibración;
usabilidad para surrogate.
```

---

## 12. Normalización

La normalización debe resolver:

```text
unidades;
zonas horarias;
timestamps;
nombres de sensores;
nombres de variables;
frecuencia temporal;
formatos de fecha;
separadores decimales;
codificación;
duplicados;
schema de payload.
```

Ejemplo:

```text
"22/04/2024 10:30" → 2024-04-22T08:30:00Z
"Temp" → zone_air_temperature
"ºC" → C
"Aula 3B" → zone_id:aula_3b
```

Siamese debe trabajar con un vocabulario interno estable:

```text
zone_air_temperature
zone_air_relative_humidity
co2_concentration
electric_power
gas_energy
hvac_supply_air_temperature
occupancy_count
```

---

## 13. Limpieza de datos

Los datos reales suelen estar incompletos o contaminados.

Siamese debe detectar:

```text
huecos temporales;
duplicados;
outliers;
saltos imposibles;
sensor congelado;
sensor con drift;
sensor offline;
valores fuera de rango;
frecuencia irregular;
desfase horario;
unidades incorrectas;
valores físicamente imposibles.
```

Ejemplo:

```text
Temperatura de aula pasa de 21 ºC a 58 ºC en 1 minuto.
→ dato inválido o sensor defectuoso.
```

Ejemplo:

```text
Sensor mantiene exactamente 22.1 ºC durante 9 horas.
→ posible sensor congelado o sin actualización real.
```

La limpieza no debe destruir el dato raw. Debe añadir flags.

```yaml
SensorReading:
  value: 58.0
  raw_value: 58.0
  quality_flag: outlier
  usable_for_calibration: false
  usable_for_visualization: false
  raw_value_preserved: true
```

---

## 14. Quality Flags

Cada dato debe tener un estado de calidad.

Estados recomendados:

```text
raw;
valid;
interpolated;
estimated;
outlier;
missing;
stale;
drift_suspected;
sensor_offline;
unit_suspected;
manual_override;
rejected.
```

Uso por módulo:

```text
Calibración:
usa valid + interpolated controlado.

Visualización:
puede mostrar estimated, pero debe etiquetarlo.

Surrogate:
puede usar estimated si el confidence score es suficiente.

Control:
no debe actuar sobre datos críticos outlier/stale.
```

Esto evita que datos malos contaminen calibración, entrenamiento o recomendaciones.

---

## 15. Sensor Health

Siamese debe calcular salud de sensor.

Métricas:

```text
último dato recibido;
frecuencia real vs esperada;
completeness;
outlier rate;
stale periods;
drift score;
battery si disponible;
señal si disponible;
latencia;
duplicados;
calibration usability.
```

Ejemplo:

```yaml
SensorHealth:
  sensor_id: sensor_aula_3b_temp_01
  status: degraded
  completeness_7d: 0.82
  outlier_rate_7d: 0.03
  stale_periods_7d: 4
  latest_timestamp: 2026-07-23T10:24:00Z
  usable_for_calibration: false
```

---

## 16. Almacenamiento

Siamese debe separar tipos de almacenamiento.

### 16.1 Raw Store

Guarda datos originales.

Uso:

```text
auditoría;
reprocesamiento;
debug;
trazabilidad.
```

### 16.2 Normalized Time-Series Store

Guarda datos limpios en schema común.

Campos típicos:

```text
timestamp;
sensor_id;
entity_id;
variable;
value;
unit;
quality_flag;
source;
ingestion_id.
```

### 16.3 Aggregated Store

Guarda agregaciones:

```text
5 min;
10 min;
hourly;
daily;
weekly.
```

### 16.4 Latest State

Guarda el último valor válido por sensor/variable.

Uso:

```text
dashboard live;
Omniverse overlay;
feature builder;
alertas.
```

### 16.5 Feature Store

Guarda features preparadas para ML.

Uso:

```text
surrogate training;
surrogate inference;
validation;
drift detection.
```

### 16.6 Dataset Artifacts

Datasets versionados:

```text
Parquet;
Arrow;
HDF5;
CSV solo para exportación;
manifest JSON/YAML.
```

---

## 17. Tecnología de almacenamiento recomendada

### Para MVP

Opciones razonables:

```text
PostgreSQL + tablas temporales;
PostgreSQL + TimescaleDB;
Parquet para datasets offline;
latest-state table para estado actual.
```

### Para escala posterior

```text
TimescaleDB;
InfluxDB;
PostgreSQL particionado;
Parquet/Delta Lake;
object storage;
Redis para latest state/eventos live.
```

Recomendación inicial:

```text
PostgreSQL + TimescaleDB para series temporales.
Parquet + manifest para datasets ML.
Redis o latest-state table para estado live.
```

---

## 18. Feature Builder

El surrogate no consume datos crudos. Consume vectores de features.

Ejemplo de features:

```text
temperatura actual;
temperatura hace 10 min;
temperatura hace 30 min;
humedad actual;
temperatura exterior;
radiación solar;
ocupación estimada;
estado HVAC;
hora del día;
día de semana;
setpoint actual.
```

Contrato conceptual:

```yaml
SurrogateFeatureVector:
  building_id: building_001
  zone_id: aula_3b
  timestamp: 2026-07-23T10:30:00Z
  features:
    zone_temp_t0: 22.8
    zone_temp_t_minus_30: 21.9
    outdoor_temp: 16.1
    relative_humidity: 45
    occupancy_estimate: 0.72
    heating_status: on
    hour_sin: 0.34
    hour_cos: -0.94
```

El Feature Builder debe garantizar:

```text
sin datos futuros;
timestamps alineados;
features consistentes con entrenamiento;
mismas unidades;
mismo orden;
misma normalización;
mismo schema que el dataset.
```

---

## 19. Sensórica para calibración

Para calibración, el módulo debe crear series temporales alineadas con los outputs simulados.

Flujo:

```text
sensor data
→ cleaning
→ resampling
→ alignment
→ target series
→ metrics evaluator
```

Ejemplo:

```text
Sensor mide cada 1 minuto.
EnergyPlus produce output cada 10 minutos.
Calibración usa media de sensor cada 10 minutos.
```

Decisiones necesarias:

```text
qué huecos se interpolan;
qué periodos se excluyen;
qué sensores son targets;
qué sensores solo validan;
qué sensores no son fiables;
qué frecuencia se usa para comparar.
```

---

## 20. Sensórica para Dataset Factory

La sensórica real aporta:

```text
targets reales;
rangos realistas;
validación contra comportamiento real;
condiciones de operación;
drift;
features de ocupación/HVAC;
corrección residual.
```

Los datasets pueden combinar:

```text
simulated-only;
real-only;
simulated + real;
pretrain simulated, fine-tune real;
physics-informed + real residual correction.
```

La calidad del dataset depende de la calidad de los datos de sensores.

---

## 21. Sensórica para Surrogate Models

Los modelos surrogados necesitan datos de entrenamiento, validación e inferencia.

La sensórica permite:

```text
validar modelos entrenados con datos EnergyPlus;
hacer fine-tuning con realidad;
alimentar inferencia live;
detectar drift;
estimar sensores faltantes;
construir features operativas.
```

Sin esta capa, un surrogate sería un modelo entrenado en simulación.  
Con esta capa, puede compararse y ajustarse a la realidad.

---

## 22. Sensórica para inferencia

Flujo live de inferencia:

```text
latest sensor state
+ weather current/forecast
+ occupancy estimate
+ HVAC state
→ feature builder
→ surrogate inference
→ prediction
→ recommendation/shadow mode
```

Ejemplo:

```text
Aula_3B:
actual 22.3 ºC
predicción 30 min 24.1 ºC
riesgo de sobrecalentamiento
recomendación: reducir consigna o anticipar ventilación
```

La inferencia debe saber si cada input es:

```text
medido;
interpolado;
estimado;
stale;
desconocido.
```

---

## 23. Sensor masking y estimación

Siamese puede usar modelos calibrados y surrogates para estimar valores cuando falla un sensor.

Caso:

```text
Sensor Aula_3B offline.
```

Siamese puede usar:

```text
zonas vecinas;
temperatura exterior;
histórico;
horario;
ocupación;
estado HVAC;
surrogate;
inercia térmica aprendida.
```

Resultado:

```yaml
EstimatedReading:
  sensor_id: sensor_aula_3b_temp_01
  timestamp: 2026-07-23T10:30:00Z
  value: 22.7
  unit: C
  quality_flag: estimated
  source: surrogate_estimation
  confidence: 0.78
```

Regla obligatoria:

```text
Un valor estimado nunca debe mostrarse como valor medido.
```

---

## 24. Visualización en Omniverse Kit

Omniverse debe mostrar la sensórica como parte del edificio.

Funciones:

```text
ver sensores en el modelo 3D;
seleccionar sensor;
ver última lectura;
ver histórico;
ver calidad;
ver zona asociada;
ver sensor vs simulación;
ver sensor vs predicción;
ver sensores offline;
ver zonas sin cobertura;
ver heatmap real;
ver heatmap simulado;
ver heatmap predicho.
```

Convención visual posible:

```text
punto cian = sensor operativo;
punto gris = sensor offline;
punto naranja = sensor degradado;
línea fina = sensor → panel de datos;
zona coloreada = valor agregado por zona.
```

La visualización no debe saturar el viewport. Debe permitir capas:

```text
Live sensor layer;
calibration error layer;
surrogate prediction layer;
HVAC status layer;
alert layer.
```

---

## 25. Alertas

El módulo debe generar alertas cuando detecte eventos relevantes.

Tipos:

```text
sensor offline;
sensor stale;
valor fuera de rango;
drift sospechoso;
zona fuera de confort;
sensor contradice modelo;
sensor contradice zonas vecinas;
HVAC no responde;
CO₂ alto;
consumo anómalo;
dato crítico ausente para inferencia.
```

Contrato:

```yaml
SensorAlert:
  alert_id: alert_001
  type: sensor_stale
  sensor_id: sensor_aula_3b_temp_01
  severity: medium
  message: Sensor has not reported data for 45 minutes.
  affected_modules:
    - visualization
    - calibration
    - surrogate_inference
  created_at: timestamp
```

Estas alertas pueden alimentar:

```text
Omniverse UI;
kanban;
roadmaps;
tareas para el usuario;
agentes;
reportes;
mantenimiento asistido.
```

---

## 26. Relación con DSX Air / NetworkSim

La sensórica también depende de la infraestructura digital.

Siamese puede usar DSX Air / NetworkSim para simular:

```text
sensores;
gateways;
MQTT broker;
latencia;
fallos de red;
pérdida de paquetes;
reconexión;
BMS gateway;
servicio de inferencia;
shadow mode;
control supervisado.
```

Uso:

```text
probar qué pasa si falla un gateway;
medir latencia sensor → surrogate;
probar shadow mode con pérdida de datos;
validar robustez antes de conectar edificio real;
crear datasets de fallos de red;
evaluar fallback operativo.
```

DSX Air / NetworkSim no sustituye al edificio ni a EnergyPlus. Simula la capa de comunicación.

---

## 27. Seguridad y privacidad

Los datos de sensores pueden revelar:

```text
ocupación;
horarios;
patrones de uso;
fallos operativos;
estado HVAC;
rutinas del edificio;
consumo energético;
datos sensibles de cliente.
```

Siamese debe implementar:

```text
permisos por organización;
permisos por edificio;
permisos por zona;
separación de clientes;
auditoría de accesos;
anonimización si aplica;
control de exportaciones;
ocultación de datos crudos a agentes sin permiso;
políticas de retención.
```

Regla:

```text
Los agentes no deben tener acceso libre a todos los datos de sensores.
```

---

## 28. Arquitectura interna propuesta

```text
siamese_backend/sensors/
│
├── contracts/
│   ├── sensor.py
│   ├── sensor_binding.py
│   ├── sensor_reading.py
│   ├── sensor_source.py
│   ├── sensor_quality.py
│   └── sensor_alert.py
│
├── connectors/
│   ├── csv_connector.py
│   ├── mqtt_connector.py
│   ├── rest_connector.py
│   ├── bacnet_connector.py
│   ├── modbus_connector.py
│   └── opcua_connector.py
│
├── ingestion/
│   ├── raw_ingestion.py
│   ├── stream_ingestion.py
│   ├── batch_ingestion.py
│   ├── deduplication.py
│   └── event_bus.py
│
├── normalization/
│   ├── units.py
│   ├── timestamp_parser.py
│   ├── variable_mapping.py
│   ├── timezone.py
│   └── schema_mapper.py
│
├── quality/
│   ├── outlier_detection.py
│   ├── gap_detection.py
│   ├── drift_detection.py
│   ├── stale_detection.py
│   ├── sensor_health.py
│   └── quality_flags.py
│
├── storage/
│   ├── raw_store.py
│   ├── timeseries_store.py
│   ├── latest_state.py
│   ├── aggregates.py
│   └── parquet_export.py
│
├── features/
│   ├── calibration_alignment.py
│   ├── surrogate_feature_builder.py
│   ├── resampling.py
│   ├── windowing.py
│   └── normalization_stats.py
│
├── visualization/
│   ├── sensor_overlay.py
│   ├── zone_live_state.py
│   ├── heatmap_binding.py
│   └── status_panel.py
│
└── alerts/
    ├── alert_rules.py
    ├── alert_engine.py
    ├── alert_routing.py
    └── alert_history.py
```

---

## 29. Contratos principales

### Sensor

```yaml
Sensor:
  id: sensor_aula_3b_temp_01
  building_id: building_001
  label: Aula 3B Temperature
  variable: temperature
  unit: C
  source_type: mqtt
  status: operational
```

### SensorBinding

```yaml
SensorBinding:
  id: binding_001
  sensor_id: sensor_aula_3b_temp_01
  target_type: ThermalZone
  target_id: aula_3b
  roles:
    - visualization
    - calibration_target
    - surrogate_feature
```

### SensorReading

```yaml
SensorReading:
  sensor_id: sensor_aula_3b_temp_01
  timestamp: 2026-07-23T10:30:00Z
  variable: temperature
  value: 22.8
  unit: C
  quality_flag: valid
  source_event_id: mqtt_event_abc
```

### SensorQualityReport

```yaml
SensorQualityReport:
  sensor_id: sensor_aula_3b_temp_01
  period:
    start: 2026-07-01
    end: 2026-07-07
  completeness: 0.96
  outlier_rate: 0.01
  stale_periods: 2
  calibration_usable: true
```

### FeatureVector

```yaml
FeatureVector:
  entity_id: aula_3b
  timestamp: 2026-07-23T10:30:00Z
  features:
    zone_temp: 22.8
    outdoor_temp: 16.1
    humidity: 45
    occupancy_estimate: 0.72
    hvac_status: on
  quality:
    measured_ratio: 0.85
    estimated_ratio: 0.15
```

---

## 30. Relación con flujos agénticos

Un **Sensor Agent** puede:

```text
analizar cobertura de sensores;
proponer ubicación de sensores;
detectar sensores defectuosos;
mapear sensores a zonas;
crear tareas de revisión;
preparar datos para calibración;
detectar si un dataset es usable;
explicar por qué una zona no puede calibrarse todavía.
```

No debe poder:

```text
borrar datos reales;
modificar mediciones;
aprobar datos dudosos sin humano;
cambiar bindings críticos sin revisión;
activar control HVAC.
```

Ejemplo:

```text
Sensor Agent detecta que Aula_4A tiene datos incompletos.
↓
Genera alerta.
↓
Crea tarea:
"Revisar sensor Aula_4A o excluirlo de calibración."
↓
Bloquea CalibrationJob multizona hasta decisión.
```

---

## 31. MVP del módulo

### Objetivo MVP

Importar datos reales de CSV, normalizarlos, mapearlos a una zona y usarlos para comparar sensor vs simulación.

### Alcance MVP

```text
CSV import;
registro básico de sensores;
sensor-zone binding;
normalización de timestamp/unidad;
detección simple de huecos/outliers;
almacenamiento básico;
consulta histórica;
último valor;
visualización básica;
export para calibración.
```

### Fuera del MVP

```text
BACnet;
Modbus;
OPC-UA;
MQTT completo;
BMS real;
feature store avanzado;
sensor masking;
DSX Air;
control.
```

### Resultado esperado

```text
Siamese puede tomar un CSV como los del TFG,
crear sensores,
mapearlos a zonas,
limpiar datos,
mostrar curvas,
y alimentar el módulo de calibración.
```

---

## 32. Evolución por fases

### Fase 1 — CSV histórico

```text
import wizard;
schema detection;
sensor registry;
quality report;
calibration export.
```

### Fase 2 — MQTT live

```text
broker;
topics;
stream ingestion;
latest state;
live dashboard.
```

### Fase 3 — Visualización espacial

```text
sensor overlay en Omniverse;
heatmaps reales;
sensor status.
```

### Fase 4 — Quality Engine

```text
outliers;
gaps;
drift;
sensor health;
alertas.
```

### Fase 5 — Feature Builder

```text
features para surrogate;
alineación temporal;
ventanas;
normalización.
```

### Fase 6 — BMS/protocolos

```text
BACnet;
Modbus;
OPC-UA;
REST industrial.
```

### Fase 7 — Sensor Masking

```text
estimación de sensores fallidos;
confidence score;
fallback operativo.
```

### Fase 8 — DSX Air / NetworkSim

```text
simulación de red sensórica;
fallos;
latencia;
shadow mode robusto.
```

---

## 33. Riesgos principales

### Riesgo 1 — Datos sucios

Mitigación:

```text
quality flags;
raw data preservation;
cleaning reproducible.
```

### Riesgo 2 — Mala ubicación de sensores

Mitigación:

```text
sensor mapping review;
coverage report;
zonas sin sensor;
recomendaciones de instalación.
```

### Riesgo 3 — Mezclar datos medidos y estimados

Mitigación:

```text
quality_flag obligatorio;
confidence score;
visualización explícita.
```

### Riesgo 4 — Dependencia de un protocolo

Mitigación:

```text
connector interface común;
CSV + MQTT primero;
BACnet/Modbus después.
```

### Riesgo 5 — Series temporales dentro de USD

Mitigación:

```text
USD solo para bindings/visualización;
datos pesados en time-series DB o Parquet.
```

### Riesgo 6 — Inferencia con features inconsistentes

Mitigación:

```text
Feature Builder versionado;
schema de entrenamiento e inferencia compartido;
validación previa.
```

---

## 34. Valor estratégico

El módulo de sensórica permite que Siamese pase de:

```text
simular un edificio
```

a:

```text
observar un edificio
```

y después a:

```text
predecir y recomendar sobre un edificio vivo
```

Valor para cliente:

```text
saber qué está pasando ahora;
ver qué zonas están fuera de confort;
detectar sensores fallidos;
comparar realidad vs simulación;
calibrar modelos;
predecir comportamiento;
justificar decisiones;
crear tareas operativas.
```

---

## 35. Frases de presentación

Frase principal:

> **La sensórica conecta el gemelo energético con el edificio real.**

Frase técnica:

> **Siamese ingiere datos desde CSV, MQTT, APIs y BMS, los normaliza, limpia, almacena y convierte en señales fiables para calibración, inferencia, visualización y recomendación.**

Frase comercial:

> **Sin sensores, el modelo calcula. Con sensores, el modelo observa.**

---

## 36. Primeros tickets recomendados

### SENSOR-00 — Sensor module context

Crear documentación base del módulo.

### SENSOR-01 — Sensor contracts

Definir `Sensor`, `SensorBinding`, `SensorReading`, `SensorQualityReport`.

### SENSOR-02 — CSV import MVP

Importar CSV histórico con mapping manual de columnas.

### SENSOR-03 — Timestamp and unit normalization

Normalizar timestamps, zonas horarias y unidades.

### SENSOR-04 — Sensor registry

Registrar sensores y vincularlos a edificios/zonas.

### SENSOR-05 — Sensor-zone binding

Crear relación sensor-zona/variable/rol.

### SENSOR-06 — Quality flags MVP

Detectar huecos, duplicados y outliers simples.

### SENSOR-07 — Time-series storage MVP

Guardar lecturas normalizadas y consultar histórico.

### SENSOR-08 — Latest state API

Exponer último valor válido por sensor/zona.

### SENSOR-09 — Calibration alignment export

Preparar datos para comparación sensor vs EnergyPlus.

### SENSOR-10 — Omniverse sensor overlay

Visualizar sensores y último estado en el viewport.

### SENSOR-11 — MQTT spike

Probar ingesta live mediante broker MQTT.

### SENSOR-12 — Feature builder contract

Definir contrato de features para surrogate inference.

---

## 37. Decisión arquitectónica final

La decisión central:

```text
La sensórica no es un añadido visual.
Es la capa que conecta Siamese con el edificio real.
```

Por tanto:

```text
Los datos deben tener identidad.
Los sensores deben estar registrados.
Las lecturas deben normalizarse.
La calidad debe explicitarse.
Las series temporales deben almacenarse fuera de USD.
Omniverse debe visualizar, no ingerir.
La calibración debe usar datos limpios y alineados.
Los surrogates deben consumir features versionadas.
Los agentes deben operar mediante herramientas gobernadas.
```

Esta frontera permitirá que Siamese sea robusto, escalable y apto para operación real.

---

## 38. Relación con documentos previos

Este módulo depende de:

```text
siamese_energyplus_context.md
→ EnergyPlus como solver físico.

siamese_python_backend_context.md
→ backend Python como capa de gobierno, ejecución y normalización.

siamese_omniverse_kit_context.md
→ Omniverse Kit como interfaz visual, semántica USD y extensible.

siamese_calibration_module_context.md
→ calibración como puente entre modelo y realidad.
```

Y se conecta directamente con módulos futuros:

```text
Dataset Factory;
Surrogate Models;
Control y recomendaciones;
DSX Air / NetworkSim;
Agentic Workflow Engine;
Nucleus collaboration;
Siamese Adoption Model.
```
