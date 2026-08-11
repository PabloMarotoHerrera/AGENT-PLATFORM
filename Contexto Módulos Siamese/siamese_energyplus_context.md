# Siamese — EnergyPlus como solver físico

**Documento:** Contexto técnico del módulo EnergyPlus dentro de Siamese  
**Proyecto:** Siamese — plataforma agéntica de gemelos digitales energéticos  
**Estado:** Documento de arquitectura conceptual previo a implementación  
**Versión:** 0.1  
**Propósito:** definir con precisión qué papel cumple EnergyPlus en Siamese, qué responsabilidades tiene, qué responsabilidades no debe asumir, cómo se relaciona con el backend Python, Omniverse Kit, OpenUSD, Nucleus, sensórica, calibración, datasets, modelos surrogados, control y flujos agénticos.

---

## 1. Resumen ejecutivo

EnergyPlus será el **solver físico principal** de Siamese. Su función es calcular el comportamiento energético y térmico del edificio: temperaturas de zona, humedad, cargas térmicas, consumos, interacción con clima, envolvente, horarios, ocupación, ventilación, infiltración y sistemas HVAC.

EnergyPlus **no debe ser el modelo interno de Siamese**. Debe tratarse como un motor externo, equivalente en filosofía a cómo un backend propio puede envolver OpenDSS en una plataforma eléctrica: el producto mantiene un modelo de dominio propio, lo valida, lo compila a un formato de entrada del solver, ejecuta el motor y normaliza los resultados.

La arquitectura correcta es:

```text
Siamese Energy Domain Model
        ↓
Validación propia
        ↓
Compilador Siamese → IDF / epJSON
        ↓
EnergyPlus Solver
        ↓
Resultados crudos
        ↓
Normalización Siamese
        ↓
Visualización / calibración / datasets / surrogates / control / agentes
```

La decisión clave es que **Siamese debe controlar el ciclo completo alrededor de EnergyPlus**, sin convertirse en un simple editor de IDF ni en una interfaz gráfica dependiente de los objetos nativos del solver.

---

## 2. Posición de EnergyPlus dentro de Siamese

Siamese se plantea como una plataforma modular para construir y operar gemelos digitales energéticos vivos. Sus bloques principales incluyen:

- Backend Python propio.
- EnergyPlus como motor de simulación física.
- Omniverse Kit como interfaz visual y runtime de ingeniería.
- OpenUSD como representación geométrica y semántica.
- Nucleus como capa colaborativa sobre USD.
- Sensórica e ingesta de datos reales.
- Calibración multizona.
- Generación de datasets físicos sintéticos.
- Modelos surrogados physics-informed.
- Recomendación, optimización y control supervisado.
- Flujos agénticos derivados de Pepper/Hermes.

Dentro de esa arquitectura, EnergyPlus ocupa una posición concreta:

```text
EnergyPlus = motor físico de simulación
Siamese Backend = capa de dominio, validación, orquestación y normalización
Omniverse Kit = interfaz visual, comandos y workspace de ingeniería
OpenUSD = geometría, semántica, bindings y capas visuales
Surrogates = inferencia rápida para operación
Agentes = orquestación gobernada de workflows
```

EnergyPlus es imprescindible para dar rigor físico a la plataforma, pero no debe dominar el diseño del producto.

---

## 3. Qué es EnergyPlus para Siamese

EnergyPlus es el motor que resuelve físicamente preguntas como:

```text
¿Cómo evoluciona la temperatura de cada zona?
¿Qué demanda térmica tiene el edificio?
¿Qué impacto tiene una determinada envolvente?
¿Cómo se comporta el edificio con un horario de ocupación concreto?
¿Qué consumo genera una estrategia HVAC?
¿Qué efecto tiene la ventilación natural?
¿Qué ocurre si se modifica una consigna?
¿Cómo cambian humedad, confort y cargas internas?
```

Para Siamese, EnergyPlus debe servir en cinco funciones principales:

1. **Simulación base** de edificios modelados o adoptados.
2. **Calibración** contra datos reales.
3. **Evaluación de escenarios** de mejora.
4. **Generación de datasets físicos sintéticos**.
5. **Validación offline de estrategias de control**.

No debe servir como:

```text
modelo interno del producto;
base de datos de edificios;
fuente de verdad visual;
sistema de sensórica;
sistema de control operativo en tiempo real;
framework agéntico;
interfaz de usuario;
registro de proyectos;
registro de clientes;
registro de modelos surrogados;
registro de decisiones.
```

---

## 4. Qué NO debe ser EnergyPlus

Siamese no debe evolucionar hacia esto:

```text
Siamese = editor visual de IDF
```

Tampoco hacia esto:

```text
Omniverse Kit modifica directamente IDF
Agentes escriben directamente objetos EnergyPlus
Cada módulo parsea outputs a su manera
El frontend conoce detalles internos del solver
La calibración modifica archivos sueltos sin trazabilidad
Los datasets se generan con notebooks no gobernados
```

Ese tipo de arquitectura sería rápida al principio, pero frágil a medio plazo. Repetiría el problema vivido en el TFG: una conexión poderosa, pero manual, dispersa y difícil de mantener.

La regla debe ser:

```text
EnergyPlus calcula.
Siamese gobierna el modelo, la ejecución, la evidencia y el ciclo operativo.
```

---

## 5. Analogía con el backend OpenDSS del TFM

La analogía correcta es la siguiente:

```text
ARACNE / TFM eléctrico
Modelo interno propio
→ validación
→ compilador a comandos/texto OpenDSS
→ ejecución OpenDSS
→ resultados normalizados

Siamese
Modelo energético interno propio
→ validación
→ compilador a IDF/epJSON
→ ejecución EnergyPlus
→ resultados normalizados
```

En ambos casos:

- El solver es externo.
- El producto no expone directamente el lenguaje del solver como modelo de dominio.
- La interfaz no debe escribir directamente el archivo de entrada.
- La lógica fuerte vive en backend.
- Los resultados se normalizan antes de llegar al frontend.
- Los errores del solver se traducen a diagnósticos comprensibles.

Esto permite que Siamese pueda ser usado por perfiles novatos y expertos:

```text
Usuario novato → trabaja con zonas, materiales, sensores, escenarios.
Usuario experto → puede inspeccionar IDF/epJSON, outputs, warnings, diagnósticos.
```

---

## 6. Por qué EnergyPlus es una buena base

EnergyPlus es una base sólida porque aporta:

- Simulación de edificio completo.
- Modelado de consumo energético y agua.
- Cálculo de cargas térmicas.
- Modelado de zonas térmicas.
- Horarios y cargas internas.
- Clima mediante archivos EPW.
- Envolvente y transferencia térmica.
- Sistemas HVAC.
- Variables y medidores de salida.
- Integración con herramientas existentes como DesignBuilder, OpenStudio y flujos IDF/epJSON.

Su fortaleza no está en la experiencia de usuario, sino en la capacidad de cálculo. Siamese debe construir la experiencia de usuario, la gobernanza y el ciclo operativo alrededor de ese motor.

EnergyPlus se puede ejecutar como herramienta de consola con archivos de entrada y archivo climático EPW. También dispone de una Python API sobre su C API, organizada en State API, Functional API, Runtime API y Data Transfer API. Esta API permite callbacks de runtime y transferencia de datos mediante variables, medidores y actuadores durante la simulación.

---

## 7. Formatos de entrada: IDF y epJSON

EnergyPlus trabaja principalmente con dos representaciones de entrada relevantes para Siamese.

### 7.1 IDF

IDF es el formato clásico de EnergyPlus. Es texto estructurado según el Input Data Dictionary.

Ventajas:

```text
muy extendido;
compatible con flujos existentes;
exportable desde herramientas externas;
fácil de versionar como texto;
útil para adopción de modelos existentes.
```

Desventajas:

```text
menos cómodo para generación programática compleja;
puede ser verboso;
requiere manejo cuidadoso de nombres y referencias;
no es ideal como modelo interno de Siamese.
```

### 7.2 epJSON

epJSON es una representación JSON basada en esquema. EnergyPlus documenta un schema epJSON generado a partir del IDD. Esto lo hace más atractivo para herramientas programáticas, validación estructurada y APIs.

Ventajas:

```text
más compatible con generación programática;
mejor para validación estructurada;
mejor para serialización/deserialización en backend;
más natural para APIs y modelos intermedios.
```

Desventajas:

```text
puede variar con versiones de EnergyPlus;
no todos los flujos externos lo usan directamente;
requiere control de schema y versionado.
```

### 7.3 Decisión recomendada

Siamese debería soportar ambos:

```text
IDF
→ compatibilidad, adopción de modelos externos, inspección experta.

epJSON
→ generación programática, validación y compilación interna moderna.
```

Pero ninguno de los dos debe ser la fuente de verdad interna. La fuente de verdad debe ser el **Siamese Energy Domain Model**.

---

## 8. Archivo climático EPW

EnergyPlus necesita condiciones climáticas para simular correctamente. En el TFG ya se evidenció la importancia de elegir datos meteorológicos representativos del edificio. Se compararon estaciones próximas, se justificó la distancia y se seleccionó una semana de estudio con condiciones suficientemente representativas.

En Siamese, el clima debe tratarse como entidad versionada:

```text
WeatherProfile
├── weather_file_id
├── source
├── location
├── epw_path
├── period_coverage
├── station_distance
├── data_quality
├── checksum
└── version
```

El archivo EPW no debe ser solo “un fichero que se pasa al solver”. Debe tener trazabilidad porque afecta directamente a simulaciones, calibraciones, datasets y decisiones operativas.

---

## 9. Modos de integración con EnergyPlus

Siamese debería contemplar tres niveles de integración.

### 9.1 Modo batch por archivos

Este debe ser el primer modo de integración.

```text
Siamese genera IDF/epJSON
→ ejecuta EnergyPlus como proceso externo
→ captura outputs
→ clasifica errores/warnings
→ normaliza resultados
```

Ventajas:

```text
robusto;
fácil de testear;
fácil de aislar;
compatible con ejecución paralela;
similar al backend OpenDSS del TFM;
suficiente para simulación, escenarios, calibración y datasets.
```

Desventajas:

```text
requiere gestión de archivos y directorios;
no es ideal para interacción dinámica durante la simulación;
no es el camino más directo para control runtime.
```

Este modo debe resolver el MVP.

### 9.2 Modo Python API

EnergyPlus expone una Python API que permite interacción más avanzada. La Runtime API permite registrar callbacks en puntos específicos de la simulación. La Data Transfer API permite leer variables/medidores y actuar sobre actuadores mediante handles.

Uso potencial en Siamese:

```text
co-simulación;
validación de estrategias de control;
shadow mode simulado;
experimentos con actuadores;
test de controladores;
interacción con callbacks;
validación de modelos surrogados frente a runtime físico.
```

Este modo debe llegar después del batch mode, no antes.

### 9.3 Modo híbrido

A medio plazo, Siamese debería usar:

```text
Batch mode:
- simulaciones estándar;
- calibración;
- generación de datasets;
- análisis de escenarios.

Python API / Runtime mode:
- control experimental;
- callbacks;
- actuadores;
- co-simulación;
- validación de control.
```

---

## 10. Inputs y outputs del módulo EnergyPlus

### 10.1 Entradas principales

EnergyPlus debe recibir desde Siamese:

```text
CompiledEnergyPlusModel
WeatherProfile
SimulationSettings
OutputRequestSet
EngineRunOptions
```

Ejemplo conceptual:

```yaml
simulation_case:
  id: simcase_001
  building_model: building_model_v12
  compiled_model: epjson_v12_2026_07_22
  weather: epw_vitoria_c040_v1
  period:
    start: 2026-01-01
    end: 2026-12-31
  timestep: 6
  outputs:
    - zone_air_temperature
    - zone_air_relative_humidity
    - heating_energy
    - cooling_energy
    - hvac_supply_air_temperature
    - people_occupant_count
```

### 10.2 Salidas principales

EnergyPlus devuelve outputs crudos:

```text
CSV;
SQL;
ESO;
MTR;
ERR;
HTML/tabular outputs;
logs;
warnings;
error messages.
```

Siamese no debe pasar estos outputs crudos directamente a Omniverse ni al usuario final. Debe transformarlos en contratos normalizados:

```text
NormalizedSimulationResults
DiagnosticReport
TimeseriesBundle
ZoneResultSet
MeterResultSet
HVACResultSet
ComfortResultSet
```

---

## 11. Modelo de dominio energético propio

Siamese debe crear su propio modelo energético intermedio. Este modelo debe ser más estable que IDF/epJSON y más cercano al lenguaje del producto.

Entidades mínimas:

```text
Building
Site
WeatherProfile
ThermalZone
Space
Surface
Opening
Construction
MaterialLayer
InternalLoad
Schedule
OccupancyProfile
VentilationProfile
InfiltrationProfile
HVACSystem
ControlSetpoint
SimulationSettings
OutputRequest
SimulationCase
SimulationRun
SimulationResult
```

EnergyPlus tiene conceptos equivalentes o relacionados, pero Siamese no debe copiar su estructura exactamente. Debe traducir desde su dominio hacia EnergyPlus.

Ejemplo:

```text
Siamese ThermalZone
    ↓
EnergyPlus Zone + Space + ZoneList + outputs + schedules asociados
```

Otro ejemplo:

```text
Siamese SensorBinding
    ↓
no compila necesariamente a EnergyPlus;
se usa para comparar resultados simulados con datos reales durante calibración.
```

---

## 12. Contratos principales

### 12.1 EnergyModel

Representa el modelo energético interno de Siamese antes de compilar a EnergyPlus.

```yaml
EnergyModel:
  model_id: energy_model_v1
  building_id: building_001
  geometry_source: usd_stage
  zones: []
  constructions: []
  schedules: []
  hvac_systems: []
  metadata:
    author: user_or_agent
    created_at: timestamp
    version: 1
```

### 12.2 SimulationCase

Representa una simulación definida pero no ejecutada.

```yaml
SimulationCase:
  simulation_case_id: simcase_001
  energy_model_id: energy_model_v1
  weather_profile_id: weather_vitoria_c040
  simulation_period: annual_or_custom
  timestep: 6
  output_requests: []
  engine_options: {}
```

### 12.3 CompiledEnergyPlusModel

Representa el artefacto que sí entiende EnergyPlus.

```yaml
CompiledEnergyPlusModel:
  compiled_model_id: compiled_epjson_001
  source_energy_model_id: energy_model_v1
  format: epJSON
  energyplus_version: 26.1.0
  artifact_path: runs/compiled/compiled_epjson_001/in.epJSON
  checksum: sha256
  schema_version: energyplus_schema_version
```

### 12.4 SimulationRun

Representa una ejecución concreta.

```yaml
SimulationRun:
  run_id: run_001
  simulation_case_id: simcase_001
  compiled_model_id: compiled_epjson_001
  status: completed
  started_at: timestamp
  finished_at: timestamp
  exit_code: 0
  output_directory: runs/simulations/run_001/
  diagnostics_id: diag_001
```

### 12.5 NormalizedSimulationResults

Representa los resultados ya tratados por Siamese.

```yaml
NormalizedSimulationResults:
  run_id: run_001
  zone_timeseries: []
  meter_timeseries: []
  hvac_timeseries: []
  comfort_metrics: []
  summary: {}
  quality_flags: []
```

---

## 13. Arquitectura interna sugerida del módulo EnergyPlus

El módulo EnergyPlus no debe ser un archivo único. Debe dividirse en componentes pequeños y testeables.

```text
siamese_energyplus/
│
├── model/
│   ├── domain.py
│   ├── geometry.py
│   ├── schedules.py
│   ├── loads.py
│   ├── hvac.py
│   └── outputs.py
│
├── compiler/
│   ├── to_epjson.py
│   ├── to_idf.py
│   ├── idf_writer.py
│   ├── epjson_writer.py
│   └── schema_mapping.py
│
├── validation/
│   ├── preflight.py
│   ├── geometry_checks.py
│   ├── construction_checks.py
│   ├── schedule_checks.py
│   ├── hvac_checks.py
│   └── output_checks.py
│
├── runner/
│   ├── command_runner.py
│   ├── api_runner.py
│   ├── job_queue.py
│   ├── sandbox.py
│   └── environment.py
│
├── results/
│   ├── raw_output_locator.py
│   ├── sql_parser.py
│   ├── csv_parser.py
│   ├── eso_parser.py
│   ├── meter_parser.py
│   └── normalized_results.py
│
├── diagnostics/
│   ├── err_parser.py
│   ├── warning_classifier.py
│   ├── failure_classifier.py
│   └── simulation_report.py
│
├── versioning/
│   ├── engine_version.py
│   ├── schema_version.py
│   └── compatibility.py
│
└── tests/
    ├── fixtures/
    ├── golden_idf/
    ├── golden_epjson/
    ├── golden_outputs/
    └── regression/
```

---

## 14. Validación previa a la ejecución

Siamese debe evitar lanzar simulaciones destinadas a fallar. Para ello debe validar antes de llamar a EnergyPlus.

Validaciones mínimas:

```text
Cada edificio tiene al menos una zona térmica.
Cada zona tiene geometría válida.
Cada superficie tiene tipo y condición de contorno.
Cada opening pertenece a una superficie.
Cada construction existe y referencia materiales válidos.
Cada schedule referenciado existe.
Cada carga interna tiene unidad y perfil temporal coherente.
Cada sistema HVAC básico está suficientemente definido.
El weather profile está disponible.
El periodo de simulación es válido.
Los outputs solicitados son compatibles con el modelo.
La versión de EnergyPlus es compatible con el formato generado.
```

Tipos de error:

```text
blocking_error:
  impide compilar o ejecutar.

warning:
  permite ejecutar pero advierte de baja calidad.

quality_issue:
  no impide ejecutar, pero reduce confianza del resultado.
```

Ejemplo:

```yaml
diagnostic:
  severity: blocking_error
  code: SURFACE_WITHOUT_ZONE
  message: Surface facade_south_03 is not assigned to any thermal zone.
  affected_entity: surface:facade_south_03
```

---

## 15. Resultados normalizados

Los resultados de EnergyPlus deben transformarse a contratos estables, no consumirse como archivos crudos.

### 15.1 Resultados por zona

```text
zone_air_temperature
zone_air_relative_humidity
zone_people_count
zone_heating_load
zone_cooling_load
zone_comfort_metrics
```

### 15.2 Resultados energéticos

```text
electricity_consumption
gas_consumption
heating_energy
cooling_energy
fans_energy
pumps_energy
lighting_energy
equipment_energy
```

### 15.3 Resultados HVAC

```text
supply_air_temperature
return_air_temperature
air_flow_rate
coil_load
boiler_load
chiller_load
pump_power
fan_power
```

### 15.4 Resultados para visualización

```text
thermal_map_values
surface_temperature_values
zone_comfort_status
sensor_vs_simulated_delta
alert_candidates
```

### 15.5 Resultados para calibración

```text
simulated_timeseries_aligned_to_sensor
error_metrics
residuals
calibration_objective_values
parameter_candidate_id
```

---

## 16. Conexión con OpenUSD

OpenUSD será la representación geométrica y semántica del edificio en Siamese. EnergyPlus no debe escribir USD directamente.

El flujo correcto:

```text
OpenUSD / AEC model
        ↓
USD → Energy Domain Mapper
        ↓
Siamese Energy Model
        ↓
EnergyPlus Compiler
        ↓
EnergyPlus Run
        ↓
Normalized Results
        ↓
Results → USD Visualization Mapper
        ↓
Omniverse Kit Viewport
```

USD debe contener:

```text
building hierarchy;
floors;
spaces;
surfaces;
openings;
materials metadata;
sensor metadata;
simulation result bindings;
visualization layers;
scenario layers;
collaboration metadata.
```

EnergyPlus debe contener:

```text
thermal zones;
constructions;
schedules;
loads;
HVAC;
simulation settings;
output requests.
```

El puente entre ambos debe ser explícito y versionado.

---

## 17. Conexión con Omniverse Kit

Omniverse Kit será la interfaz visual de ingeniería. Debe permitir:

```text
visualizar el modelo;
seleccionar zonas;
ver sensores;
lanzar simulaciones;
inspeccionar resultados;
comparar escenarios;
abrir paneles de diagnóstico;
ver mapas térmicos;
crear tareas agénticas asociadas a entidades del edificio.
```

Pero Kit no debe ejecutar lógica energética por su cuenta. Debe llamar a comandos o APIs:

```text
Kit UI
→ Siamese command/API
→ Backend EnergyPlus
→ Normalized results
→ Kit visualization layer
```

Ejemplo:

```text
Usuario selecciona Aula_3B en el viewport.
↓
Pulsa “Run thermal simulation”.
↓
Kit crea SimulationCase mediante API.
↓
Backend compila y ejecuta EnergyPlus.
↓
Resultados normalizados se enlazan a la zona.
↓
Kit muestra mapa térmico y gráficas.
```

---

## 18. Conexión con Nucleus

Nucleus puede servir como infraestructura colaborativa para USD y assets compartidos. EnergyPlus no debe depender de Nucleus para ejecutar simulaciones, pero Siamese puede usar Nucleus para coordinar:

```text
stages USD compartidos;
layers de diseño;
layers de resultados;
layers de escenarios;
permisos de colaboración;
revisión de geometría;
trabajo multiusuario.
```

Relación recomendada:

```text
Nucleus
→ almacena y sincroniza USD/assets.

Siamese Backend
→ almacena modelos energéticos normalizados, resultados, runs, calibraciones, datasets.

EnergyPlus
→ ejecuta simulaciones desde artefactos compilados controlados por backend.
```

No conviene guardar grandes series temporales dentro de USD. USD debe contener bindings, metadatos y capas visuales, mientras las series temporales viven en bases de datos o almacenamiento columnar.

---

## 19. Conexión con sensórica

EnergyPlus no ingiere sensores reales por sí solo en el flujo base de Siamese. La sensórica entra por una capa específica:

```text
Sensors / BMS
→ Ingestion Layer
→ Time-Series Storage
→ Sensor-Zone Mapping
→ Calibration / Comparison / Monitoring
```

EnergyPlus se conecta con los sensores mediante comparaciones:

```text
sensor data
vs
simulated data
```

Casos de uso:

```text
calibrar modelo;
validar simulación;
detectar desviaciones;
generar alertas;
medir performance del surrogate;
estimar valores cuando falla un sensor.
```

Ejemplo:

```yaml
SensorBinding:
  sensor_id: govee_3b_temp
  variable: zone_air_temperature
  zone_id: aula_3b
  calibration_role: target
  frequency: 10min
```

---

## 20. Conexión con calibración

La calibración es una de las razones principales para encapsular EnergyPlus correctamente.

Flujo:

```text
Modelo inicial
→ variables calibrables
→ sampling/optimización
→ compilación EnergyPlus
→ ejecución
→ comparación con sensores
→ métricas
→ nuevo candidato
→ modelo calibrado aprobado
```

EnergyPlus participa ejecutando cada candidato de simulación. Siamese controla:

```text
qué variables se modifican;
qué rangos son válidos;
qué sensores se usan como targets;
qué periodo temporal se calibra;
qué métrica se optimiza;
qué algoritmo se usa;
qué candidato se aprueba;
qué versión del modelo calibrado queda registrada.
```

El TFG ya demostró esta lógica de forma manual y semiautomatizada: sensores reales, modelo DesignBuilder, comparación sensor/simulación, métricas estadísticas y algoritmos genéticos para calibrar el modelo. Siamese debe convertir ese proceso en módulo reproducible.

---

## 21. Conexión con Dataset Factory

Una vez calibrado, el modelo EnergyPlus se vuelve una fuente de datos física para entrenar modelos rápidos.

Flujo:

```text
Modelo EnergyPlus calibrado
→ definición de espacio de escenarios
→ sampling
→ simulaciones masivas
→ extracción de outputs
→ dataset ML-ready
```

Siamese debe registrar:

```text
qué modelo calibrado se usó;
qué variables se samplearon;
qué rangos se usaron;
qué clima se usó;
qué outputs se generaron;
qué versión de EnergyPlus ejecutó la campaña;
qué checksums tienen los artefactos;
qué calidad tiene el dataset.
```

El output final no debe ser una carpeta de CSVs sueltos, sino un dataset versionado:

```text
DatasetManifest
├── metadata
├── schema
├── train/validation/test splits
├── feature definitions
├── target definitions
├── normalization stats
├── provenance
└── quality report
```

---

## 22. Conexión con modelos surrogados

EnergyPlus no se usa para inferencia rápida en operación. Para eso estarán los modelos surrogados.

Relación:

```text
EnergyPlus calibrado
→ genera datos físicos
→ entrena surrogate
→ surrogate hace inferencia rápida
→ EnergyPlus sigue como referencia física offline
```

Tipos de surrogate previstos:

```text
RC / grey-box;
LSTM / GRU;
Transformers temporales;
GNN multizona;
modelos híbridos físico-ML;
physics-informed neural networks;
modelos residuales sobre RC.
```

Siamese debe evitar vender esto como “IA genérica”. La formulación correcta:

```text
La IA no sustituye la física. La hace operativa.
```

EnergyPlus aporta la física calibrada; el surrogate aporta velocidad para predicción, recomendación y control.

---

## 23. Conexión con control y shadow mode

EnergyPlus puede validar estrategias de control offline, pero no debe ser el motor principal de control real-time.

Flujo recomendado:

```text
EnergyPlus calibrado
→ dataset
→ surrogate
→ controlador/recomendador
→ shadow mode
→ control supervisado
```

Uso de EnergyPlus:

```text
comparar escenarios;
validar políticas offline;
generar condiciones de entrenamiento;
evaluar acciones propuestas;
servir como referencia de alta fidelidad.
```

Uso del surrogate:

```text
predicción de estado futuro;
inferencia rápida;
estimación con sensores incompletos;
control MPC o políticas aprendidas;
shadow mode operativo.
```

---

## 24. Conexión con DSX Air / NetworkSim

EnergyPlus simula física energética. NVIDIA DSX Air o NetworkSim simularía infraestructura digital de operación:

```text
sensores;
gateways;
brokers MQTT;
latencia;
fallos de red;
BMS gateway;
servicio de inferencia;
control supervisado.
```

Relación:

```text
EnergyPlus / Surrogates
→ comportamiento térmico y energético.

DSX Air / NetworkSim
→ comunicación, latencia, fallos, infraestructura sensórica y HVAC.
```

Ambos son complementarios:

```text
Gemelo energético
+
Gemelo de red/operación
=
validación robusta antes de actuar sobre edificios reales.
```

---

## 25. Conexión con flujos agénticos Pepper/Hermes

La capa agéntica no debe escribir directamente archivos EnergyPlus. Debe usar herramientas gobernadas.

Ejemplo correcto:

```text
Calibration Agent
→ solicita crear CalibrationJob
→ backend valida permisos
→ backend crea SimulationCampaign
→ EnergyPlus Runner ejecuta candidatos
→ Metrics Evaluator calcula errores
→ Evidence Registry guarda resultados
→ Approval Gate pide revisión humana
```

Ejemplo incorrecto:

```text
Agente abre IDF
→ modifica líneas manualmente
→ ejecuta EnergyPlus por su cuenta
→ interpreta CSVs sin contrato
```

La integración agéntica debe apoyarse en:

```text
Tool Registry;
Policy Engine;
Evidence Registry;
Approval Gates;
Execution Inspector;
Roadmap Engine;
Kanban contextual;
Model Selector.
```

Cada acción sobre EnergyPlus debe tener:

```text
identidad;
input;
output;
evidencia;
permisos;
estado;
trazabilidad;
posible rollback;
validación.
```

---

## 26. Qué debe poder hacer un agente con EnergyPlus

Permitido:

```text
crear SimulationCase;
validar modelo;
pedir compilación IDF/epJSON;
lanzar simulación;
resumir diagnostics;
comparar resultados;
crear CalibrationJob;
crear DatasetCampaign;
generar informe técnico;
proponer siguiente tarea;
marcar bloqueo por datos insuficientes.
```

No permitido sin aprobación o sin herramienta gobernada:

```text
modificar modelo calibrado final;
aprobar calibración;
desplegar surrogate operativo;
activar control supervisado;
borrar resultados;
ignorar warnings críticos;
modificar datos reales;
modificar archivos del solver fuera del runner;
usar outputs crudos como autoridad final.
```

---

## 27. Versionado

EnergyPlus cambia con el tiempo. Siamese debe registrar siempre:

```text
energyplus_version;
input_format;
schema_version;
compiler_version;
weather_file_checksum;
compiled_input_checksum;
run_environment;
output_schema_version;
normalizer_version.
```

Sin esto, no habrá reproducibilidad.

Ejemplo:

```yaml
EnergyPlusRunProvenance:
  energyplus_version: 26.1.0
  input_format: epJSON
  schema_version: 26.1
  compiler_version: siamese-energy-compiler-0.3.0
  weather_checksum: sha256:...
  input_checksum: sha256:...
  normalizer_version: siamese-results-0.2.0
```

---

## 28. Licencia e integración comercial

EnergyPlus se distribuye bajo una licencia permisiva tipo BSD-3-like según su repositorio oficial. Esto lo hace mucho más favorable como dependencia estructural de Siamese que herramientas GPL como BESOS.

La estrategia recomendada:

```text
EnergyPlus puede ser dependencia estructural del producto.
BESOS debe ser referencia/investigación, no dependencia directa del core propietario.
```

Siamese debe incluir cumplimiento de licencias:

```text
registro de dependencias;
licencias asociadas;
versiones;
notices;
compatibilidad con distribución;
modo SaaS/on-premise.
```

---

## 29. MVP del módulo EnergyPlus

El MVP no debe intentar cubrir EnergyPlus completo. Debe demostrar el flujo robusto completo en vertical.

### 29.1 MVP funcional mínimo

```text
1 edificio;
varias zonas térmicas;
materiales/construcciones simples;
horarios básicos;
cargas internas básicas;
clima EPW;
simulación por línea de comandos;
outputs de temperatura, humedad y energía;
normalización de resultados;
diagnóstico de errores;
visualización básica en Siamese.
```

### 29.2 Primer caso de uso

```text
Crear/adoptar modelo simple del edificio.
Ejecutar simulación base.
Comparar una zona con sensores reales.
Generar primer reporte.
```

### 29.3 Criterio de éxito

El criterio no es “soportar todo EnergyPlus”. Es:

```text
Siamese puede controlar el ciclo completo:
modelo interno → compilación → ejecución → resultados normalizados → visualización/diagnóstico.
```

---

## 30. Evolución del módulo EnergyPlus

### Fase 1 — Solver baseline

```text
runner por CLI;
compilación mínima;
outputs básicos;
diagnósticos básicos.
```

### Fase 2 — Modelo multizona serio

```text
zonas;
superficies;
openings;
constructions;
schedules;
cargas;
ventilación;
HVAC simple.
```

### Fase 3 — Adopción de modelos existentes

```text
importar IDF;
importar epJSON;
leer outputs configurados;
generar Model Quality Report;
normalizar al dominio Siamese.
```

### Fase 4 — Calibración

```text
variables calibrables;
optimización;
comparación con sensores;
modelo calibrado versionado;
informes de calibración.
```

### Fase 5 — Dataset factory

```text
campaigns;
sampling;
paralelización;
manifest;
outputs ML-ready.
```

### Fase 6 — Runtime/API avanzada

```text
Python API;
callbacks;
actuadores;
control experimental;
co-simulación.
```

---

## 31. Riesgos técnicos

### Riesgo 1 — Convertirse en editor de IDF

Mitigación:

```text
modelo interno propio;
compilador explícito;
outputs normalizados.
```

### Riesgo 2 — Sobrecargar el MVP

Mitigación:

```text
vertical slice mínimo;
solo variables esenciales;
no intentar cubrir todo HVAC desde el inicio.
```

### Riesgo 3 — Mala calidad de modelos adoptados

Mitigación:

```text
Model Quality Report;
validación previa;
calibrabilidad;
señalar incertidumbre.
```

### Riesgo 4 — Resultados difíciles de interpretar

Mitigación:

```text
normalización;
visualización guiada;
diagnósticos;
resúmenes por zona y sistema.
```

### Riesgo 5 — Reproducibilidad débil

Mitigación:

```text
checksums;
versionado;
manifest de runs;
registro de engine/schema/compiler.
```

### Riesgo 6 — Agentes modificando demasiado

Mitigación:

```text
Tool Registry;
Policy Engine;
Approval Gates;
Execution Inspector;
no acceso directo a archivos críticos.
```

---

## 32. Ventajas estratégicas de usar EnergyPlus así

### 32.1 Rigor físico sin reinventar el solver

Siamese puede concentrarse en producto, operación, UX, datos, IA y colaboración, sin reimplementar física completa.

### 32.2 Compatibilidad con ecosistema existente

Adoptar modelos IDF/epJSON permite entrar en edificios ya modelados con DesignBuilder, OpenStudio u otros flujos basados en EnergyPlus.

### 32.3 Base para calibración real

EnergyPlus permite comparar datos simulados con sensores reales y ajustar variables del modelo.

### 32.4 Base para surrogates

El modelo calibrado puede generar datasets físicos sintéticos para entrenar inferencia rápida.

### 32.5 Base defendible ante expertos

Un sistema basado en EnergyPlus calibrado es más defendible que una IA genérica aplicada a sensores.

---

## 33. Relación con la narrativa comercial

EnergyPlus debe comunicarse como:

```text
el motor físico de Siamese;
la base de confianza;
la fuente de simulaciones calibrables;
el generador de datos físicos para IA;
la validación offline de estrategias.
```

No debe comunicarse como:

```text
el producto;
la interfaz;
la experiencia de usuario;
la solución completa.
```

Frase para presentación:

> No estamos reinventando la física del edificio. Estamos construyendo la capa que la conecta con datos reales, IA, visualización y operación.

Frase técnica:

> Siamese encapsula EnergyPlus detrás de un backend Python propio que valida modelos, compila entradas, ejecuta simulaciones, normaliza resultados y alimenta calibración, datasets, surrogates y control.

---

## 34. Relación con el TFG

El TFG demostró el problema:

```text
sensores reales;
modelo DesignBuilder;
calibración con datos reales;
algoritmos genéticos;
análisis de mejoras;
modelo finalmente archivado.
```

Siamese toma esa experiencia y la convierte en producto:

```text
sensores → ingesta estructurada;
DesignBuilder/EnergyPlus → backend propio;
calibración manual → módulo de calibración;
CSVs → time-series layer;
modelo archivado → gemelo vivo;
análisis puntual → operación continua;
algoritmos genéticos → calibración gobernada;
modelo calibrado → datasets y surrogates.
```

La diferencia fundamental:

```text
TFG:
modelo calibrado como entregable.

Siamese:
modelo calibrado como infraestructura viva.
```

---

## 35. Primeros tickets recomendados para este módulo

### EP-00 — EnergyPlus module vision

Crear documentación base del módulo EnergyPlus.

### EP-01 — EnergyPlus installation and execution spike

Validar ejecución local CLI con ejemplo oficial.

### EP-02 — SimulationCase contract

Definir DTOs internos para simulación.

### EP-03 — Minimal compiler to epJSON/IDF

Compilar un modelo mínimo Siamese a EnergyPlus.

### EP-04 — Command runner

Ejecutar EnergyPlus en sandbox controlado.

### EP-05 — Output locator and diagnostics parser

Localizar outputs y parsear `err`/warnings.

### EP-06 — Normalized zone results

Extraer resultados mínimos por zona.

### EP-07 — Golden fixture test

Crear fixture reproducible para regresión.

### EP-08 — USD-to-energy mapping stub

Definir el primer puente desde entidades USD/AEC hacia modelo energético.

### EP-09 — First Omniverse visualization binding

Mostrar resultado normalizado sobre una zona en Kit.

---

## 36. Decisión arquitectónica final

La decisión que debe guiar la implementación es:

```text
EnergyPlus será el solver físico de Siamese, no su modelo interno.
```

Todo lo demás deriva de ahí:

```text
Siamese tiene modelo de dominio propio.
Siamese valida antes de compilar.
Siamese compila a IDF/epJSON.
Siamese ejecuta EnergyPlus en jobs trazables.
Siamese normaliza outputs.
Siamese usa resultados para visualización, calibración, datasets, surrogates y control.
Siamese gobierna agentes mediante herramientas, permisos, evidencia y aprobación.
```

Esta frontera es necesaria para que Siamese pueda crecer de forma robusta, modular y escalable.

---

## 37. Referencias externas consultadas

- EnergyPlus Quick Start Guide — Command Line Interface.  
  https://energyplus.readthedocs.io/en/stable/quick_start/quick_start.html

- EnergyPlus Essentials — Command line usage, IDF/epJSON conversion and options.  
  https://energyplus.readthedocs.io/en/stable/essentials/essentials.html

- EnergyPlus EpJSON Input Schema.  
  https://energyplus.readthedocs.io/en/stable/schema.html

- EnergyPlus Python API.  
  https://energyplus.readthedocs.io/en/stable/api.html

- EnergyPlus Runtime API.  
  https://energyplus.readthedocs.io/en/v23.2.0/runtime.html

- EnergyPlus Data Transfer API.  
  https://energyplus.readthedocs.io/en/stable/datatransfer.html

- EnergyPlus GitHub repository / license note.  
  https://github.com/NREL/EnergyPlus

---

## 38. Referencias internas de proyecto

- `digital_twin_contexto_maestro.md` — visión general de Siamese, macroproyectos, arquitectura modular, principios EnergyPlus/Omniverse/USD/agentes.
- `Concienciación ambiental y optimización energética del CEP Divino Maestro.pdf` — origen narrativo y técnico: sensórica, DesignBuilder, calibración, algoritmos genéticos y limitación del modelo calibrado archivado.
