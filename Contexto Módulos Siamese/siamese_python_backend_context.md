# Siamese — Backend Python sobre EnergyPlus

**Documento:** Contexto técnico del backend Python que envuelve EnergyPlus dentro de Siamese  
**Proyecto:** Siamese — plataforma agéntica de gemelos digitales energéticos  
**Estado:** Documento de arquitectura conceptual previo a implementación  
**Versión:** 0.1  
**Propósito:** definir con precisión qué es el backend Python de Siamese, qué responsabilidades tiene, cómo encapsula EnergyPlus, cómo se relaciona con Omniverse Kit, OpenUSD, Nucleus, sensórica, calibración, datasets, modelos surrogados, control y flujos agénticos, y cómo debe construirse para ser robusto, escalable y mantenible.

---

## 1. Resumen ejecutivo

El backend Python es la capa que convierte EnergyPlus en una plataforma de producto.

EnergyPlus aporta el cálculo físico, pero por sí solo no constituye Siamese. EnergyPlus trabaja mediante modelos de entrada, archivos climáticos, outputs crudos, logs, warnings y resultados que necesitan una capa superior para ser utilizables en una experiencia moderna, visual, colaborativa, trazable y posteriormente agéntica.

El backend Python debe actuar como la capa que:

```text
mantiene el modelo energético interno de Siamese;
valida modelos antes de ejecutar;
compila el modelo interno a IDF / epJSON;
ejecuta EnergyPlus de forma controlada;
parsea errores, warnings y resultados;
normaliza outputs;
gestiona jobs y artefactos;
expone APIs estables;
alimenta Omniverse Kit, calibración, datasets, surrogates, control y agentes.
```

La arquitectura conceptual es:

```text
Siamese Energy Model
        ↓
Validation Layer
        ↓
Energy Compiler → IDF / epJSON
        ↓
EnergyPlus Runner
        ↓
Raw EnergyPlus Outputs
        ↓
Results Normalizer
        ↓
APIs / Omniverse / Calibration / Datasets / Surrogates / Control / Agents
```

La frase clave es:

> EnergyPlus calcula. El backend Python convierte ese cálculo en producto.

---

## 2. Analogía con el backend OpenDSS del TFM

La forma correcta de entender este backend es compararlo con el backend construido en el TFM para trabajar con OpenDSS.

En un backend eléctrico tipo OpenDSS:

```text
modelo interno propio
→ validación
→ compilación a comandos/texto de entrada
→ ejecución OpenDSS
→ lectura de resultados
→ normalización
→ API / frontend
```

En Siamese:

```text
modelo energético interno propio
→ validación
→ compilación a IDF / epJSON
→ ejecución EnergyPlus
→ lectura de outputs crudos
→ normalización
→ API / Omniverse / calibración / IA / agentes
```

La analogía es importante porque evita una decisión peligrosa: convertir Siamese en una interfaz que escribe directamente objetos EnergyPlus.

Siamese debe trabajar con sus propias entidades:

```text
Building
Floor
Space
ThermalZone
Surface
Opening
Construction
Material
Schedule
InternalLoad
HVACSystem
SensorBinding
WeatherProfile
SimulationCase
SimulationRun
```

EnergyPlus recibe una compilación de esas entidades. No debe ser la fuente de verdad interna del producto.

---

## 3. Posición del backend Python dentro de Siamese

Siamese se compone de varias capas:

```text
Siamese Platform
│
├── Energy Twin Core
│   ├── modelo energético interno
│   ├── backend Python
│   ├── EnergyPlus solver
│   ├── validación
│   └── resultados normalizados
│
├── Visual Workspace
│   ├── Omniverse Kit
│   ├── OpenUSD
│   ├── viewport
│   ├── heatmaps
│   └── dashboards
│
├── Operational Intelligence
│   ├── calibración
│   ├── generación de datasets
│   ├── modelos surrogados
│   ├── inferencia
│   ├── optimización
│   └── recomendaciones/control
│
├── Sensor & Network Layer
│   ├── CSV
│   ├── MQTT
│   ├── REST
│   ├── BACnet
│   ├── Modbus
│   ├── BMS
│   └── NVIDIA DSX Air / NetworkSim
│
└── Agentic Workflow Engine
    ├── roadmaps
    ├── kanban
    ├── tareas
    ├── agentes
    ├── tool registry
    ├── approvals
    ├── evidence
    └── execution inspector
```

El backend Python pertenece al **Energy Twin Core**, pero conecta con todas las demás capas.

Su función no es solo lanzar EnergyPlus. Su función es mantener la coherencia entre el edificio digital, el solver físico, los datos reales, la visualización, la IA y los flujos agénticos.

---

## 4. Por qué el backend Python es imprescindible

Sin backend Python, Siamese correría el riesgo de convertirse en:

```text
una interfaz bonita;
un conjunto de scripts EnergyPlus;
un viewport 3D sin arquitectura de producto;
una colección de notebooks para calibración y datasets;
un sistema difícil de reproducir.
```

El backend Python es lo que permite que Siamese sea:

```text
producto;
plataforma;
API;
sistema multiusuario;
sistema trazable;
sistema agéntico;
sistema extensible;
sistema reproducible;
sistema escalable.
```

EnergyPlus no sabe qué usuario lanzó una simulación, qué roadmap la solicitó, qué sensor se usó para calibrar, qué modelo calibrado generó un dataset, qué surrogate fue entrenado, qué aprobación humana autorizó una acción o qué visualización debe actualizarse en Omniverse.

El backend Python sí debe saberlo.

---

## 5. Regla arquitectónica principal

La regla principal del backend debe ser:

```text
Ningún módulo importante de Siamese debe hablar directamente con EnergyPlus.
Todos deben pasar por contratos del backend.
```

Esto implica:

```text
Omniverse Kit no ejecuta EnergyPlus directamente.
El agente no edita IDF directamente.
La calibración no modifica archivos sin trazabilidad.
El módulo de datasets no parsea outputs por su cuenta.
El frontend no interpreta CSVs crudos.
El control no usa resultados sin normalizar.
Los usuarios no dependen de objetos EnergyPlus para trabajar.
```

Todo debe pasar por contratos como:

```text
EnergyModel
SimulationCase
CompiledEnergyPlusModel
SimulationRun
NormalizedSimulationResults
DiagnosticReport
CalibrationJob
DatasetCampaign
SurrogateTrainingJob
Recommendation
ApprovalGate
```

---

## 6. Responsabilidades del backend Python

El backend Python debe asumir, como mínimo, estas responsabilidades:

```text
1. Modelo de dominio energético propio.
2. Validación previa a EnergyPlus.
3. Compilación a IDF / epJSON.
4. Ejecución controlada de EnergyPlus.
5. Gestión de jobs y workers.
6. Parseo de errores, warnings y outputs.
7. Normalización de resultados.
8. Versionado y trazabilidad.
9. Exposición de APIs estables.
10. Integración con Omniverse Kit.
11. Integración con OpenUSD.
12. Integración con Nucleus.
13. Integración con sensórica.
14. Integración con calibración.
15. Integración con datasets.
16. Integración con modelos surrogados.
17. Integración con control y recomendaciones.
18. Integración con agentes y roadmaps.
19. Gestión de artefactos.
20. Diagnósticos comprensibles para usuarios y agentes.
```

No debe ser un wrapper fino del tipo:

```python
run_energyplus(idf_path, epw_path)
```

Eso puede existir como función interna del runner, pero no puede ser la arquitectura del backend.

---

## 7. Arquitectura general del backend

Una arquitectura inicial razonable sería:

```text
siamese_backend/
│
├── core/
│   ├── ids.py
│   ├── errors.py
│   ├── units.py
│   ├── time.py
│   ├── provenance.py
│   └── artifacts.py
│
├── energy_model/
│   ├── building.py
│   ├── floors.py
│   ├── spaces.py
│   ├── zones.py
│   ├── geometry.py
│   ├── surfaces.py
│   ├── openings.py
│   ├── materials.py
│   ├── constructions.py
│   ├── schedules.py
│   ├── loads.py
│   ├── hvac.py
│   ├── weather.py
│   └── sensors.py
│
├── energyplus/
│   ├── compiler/
│   ├── runner/
│   ├── results/
│   ├── diagnostics/
│   ├── validation/
│   └── compatibility/
│
├── simulations/
│   ├── cases.py
│   ├── jobs.py
│   ├── services.py
│   └── results_api.py
│
├── calibration/
│   ├── jobs.py
│   ├── parameters.py
│   ├── objectives.py
│   ├── metrics.py
│   ├── optimizers.py
│   └── reports.py
│
├── datasets/
│   ├── campaigns.py
│   ├── sampling.py
│   ├── extraction.py
│   ├── manifests.py
│   └── quality.py
│
├── surrogates/
│   ├── training.py
│   ├── registry.py
│   ├── validation.py
│   ├── inference.py
│   └── export.py
│
├── sensors/
│   ├── ingestion.py
│   ├── bindings.py
│   ├── quality.py
│   ├── timeseries.py
│   └── connectors/
│
├── control/
│   ├── recommendations.py
│   ├── shadow_mode.py
│   ├── policies.py
│   ├── safety.py
│   └── evaluation.py
│
├── agentic/
│   ├── tools.py
│   ├── policies.py
│   ├── evidence.py
│   ├── approvals.py
│   ├── roadmaps.py
│   └── execution.py
│
├── api/
│   ├── rest/
│   ├── schemas/
│   ├── auth.py
│   └── routes.py
│
└── workers/
    ├── simulation_worker.py
    ├── calibration_worker.py
    ├── dataset_worker.py
    └── training_worker.py
```

Esta estructura no implica implementarlo todo desde el inicio. Sirve para orientar el crecimiento modular.

---

## 8. Backend EnergyPlus vs Backend Siamese completo

Conviene distinguir dos niveles.

### 8.1 Backend EnergyPlus

Responsable de:

```text
compilar modelo energético;
ejecutar EnergyPlus;
parsear outputs;
normalizar resultados;
diagnosticar errores;
registrar artefactos de simulación.
```

### 8.2 Backend Siamese completo

Responsable de:

```text
proyectos;
usuarios;
edificios;
modelos;
sensores;
calibración;
datasets;
surrogates;
control;
agentes;
visualización;
colaboración;
roadmaps;
aprobaciones;
trazabilidad.
```

El backend EnergyPlus es una pieza dentro del backend Siamese.

---

## 9. Core Domain Model

El modelo de dominio es la fuente de verdad energética interna de Siamese.

Debe incluir entidades como:

```text
Building
Site
Floor
Space
ThermalZone
Surface
Opening
Construction
MaterialLayer
Schedule
OccupancyProfile
InternalLoad
VentilationProfile
InfiltrationProfile
HVACSystem
ControlSetpoint
WeatherProfile
SensorBinding
SimulationSettings
OutputRequest
```

La clave es que el modelo interno debe ser:

```text
más estable que IDF;
más usable que epJSON;
más cercano al lenguaje de ingeniería;
compatible con Omniverse/USD;
compatible con sensores;
compatible con calibración;
compatible con agentes.
```

Ejemplo conceptual:

```yaml
ThermalZone:
  id: zone_aula_3b
  name: Aula 3B
  floor_id: floor_01
  spaces:
    - space_aula_3b
  conditioning: heated
  sensor_bindings:
    - sensor_govee_3b_temp
    - sensor_govee_3b_rh
  schedules:
    occupancy: schedule_school_weekday
    heating: schedule_heating_winter
```

Esto se compila después a objetos EnergyPlus, pero Siamese no debe obligar al usuario a pensar en objetos EnergyPlus.

---

## 10. Validation Layer

Antes de compilar o ejecutar, el backend debe validar el modelo.

Tipos de validación:

```text
validación geométrica;
validación energética;
validación de horarios;
validación de materiales;
validación de cargas internas;
validación HVAC;
validación de sensores;
validación de outputs;
validación de compatibilidad con EnergyPlus;
validación de calibrabilidad.
```

Ejemplos:

```text
Una zona no tiene superficies.
Una ventana no pertenece a ninguna superficie.
Una construcción referencia un material inexistente.
Un schedule usado por ocupación no existe.
Un HVACSystem no tiene configuración mínima.
Un sensor está asignado a una zona inexistente.
Un OutputRequest no es compatible con el modelo.
El archivo EPW no está disponible.
```

Los diagnósticos deben ser estructurados:

```yaml
Diagnostic:
  severity: blocking_error
  code: ZONE_WITHOUT_SURFACES
  message: La zona Aula_3B no tiene superficies asociadas.
  entity_type: ThermalZone
  entity_id: zone_aula_3b
  suggested_fix: Asociar superficies válidas antes de compilar el modelo.
```

Categorías:

```text
blocking_error:
  impide compilar o ejecutar.

warning:
  permite ejecutar, pero indica posible baja calidad.

quality_issue:
  no impide ejecutar, pero afecta confianza del resultado.
```

---

## 11. Energy Compiler

El compilador traduce el modelo interno de Siamese a un artefacto ejecutable por EnergyPlus.

Formatos objetivo:

```text
IDF;
epJSON.
```

Flujo:

```text
EnergyModel
→ ValidationReport
→ EnergyCompiler
→ CompiledEnergyPlusModel
→ IDF / epJSON artifact
```

El compilador debe ser determinista: el mismo modelo, con la misma versión del compilador, debe generar el mismo artefacto.

Contrato:

```yaml
CompiledEnergyPlusModel:
  compiled_model_id: compiled_epjson_001
  source_energy_model_id: energy_model_v12
  format: epJSON
  energyplus_version: 26.1
  compiler_version: siamese-energy-compiler-0.1.0
  artifact_path: runs/compiled/compiled_epjson_001/in.epJSON
  checksum: sha256:...
  created_at: timestamp
```

Responsabilidades:

```text
mapear zonas;
mapear superficies;
mapear construcciones;
mapear materiales;
mapear schedules;
mapear cargas;
mapear HVAC;
mapear outputs solicitados;
generar archivos válidos;
registrar warnings de compilación.
```

No debe encargarse de:

```text
ejecutar EnergyPlus;
parsear resultados;
calibrar;
entrenar modelos;
visualizar.
```

---

## 12. EnergyPlus Runner

El runner ejecuta EnergyPlus de forma controlada.

Debe gestionar:

```text
ubicación del binario;
versión de EnergyPlus;
directorio de ejecución;
archivo IDF/epJSON;
archivo EPW;
argumentos CLI;
timeout;
stdout;
stderr;
exit code;
outputs generados;
limpieza;
fallos;
logs seguros.
```

Contrato:

```yaml
SimulationRun:
  run_id: run_001
  simulation_case_id: simcase_001
  compiled_model_id: compiled_epjson_001
  weather_profile_id: weather_vitoria_c040_v1
  status: completed
  started_at: timestamp
  finished_at: timestamp
  exit_code: 0
  output_directory: runs/simulations/run_001/
  diagnostics_id: diag_001
```

El runner debe soportar inicialmente modo CLI. Más adelante puede incorporar EnergyPlus Python API para co-simulación y control experimental.

---

## 13. Job Manager

Las simulaciones no siempre serán instantáneas. La calibración y la generación de datasets pueden requerir cientos o miles de ejecuciones.

Por eso el backend debe tener un sistema de jobs.

Tipos de jobs:

```text
SimulationJob
CalibrationJob
DatasetCampaignJob
SurrogateTrainingJob
InferenceDeploymentJob
ControlEvaluationJob
NetworkSimulationJob
```

Estados:

```text
created
queued
running
completed
failed
cancelled
blocked
requires_approval
```

Cada job debe registrar:

```text
inputs;
outputs;
estado;
progreso;
artefactos;
diagnósticos;
usuario/agente origen;
timestamps;
dependencias;
evidencia.
```

Ejemplo:

```yaml
Job:
  id: job_sim_001
  type: SimulationJob
  requested_by: user:pablo
  source: omniverse_kit
  status: running
  progress: 42
  related_entities:
    - simulation_case:simcase_001
    - building:building_divino_maestro
```

---

## 14. Results Parser

EnergyPlus produce outputs crudos. El backend debe localizarlos, leerlos y transformarlos.

Outputs posibles:

```text
ERR;
CSV;
SQL;
ESO;
MTR;
HTML/tabular reports;
logs.
```

El parser debe producir contratos estables:

```text
ZoneTimeseries;
MeterTimeseries;
HVACTimeseries;
ComfortMetrics;
EnergySummary;
DiagnosticReport;
VisualizationData;
CalibrationComparisonSeries.
```

Ejemplo:

```yaml
ZoneTimeseries:
  run_id: run_001
  zone_id: zone_aula_3b
  variable: zone_air_temperature
  unit: C
  timestep: 10min
  values:
    - timestamp: 2026-04-22T09:00:00
      value: 21.4
```

Ningún módulo superior debería leer directamente el CSV crudo de EnergyPlus.

---

## 15. Results Normalizer

El normalizador convierte resultados técnicos del solver en entidades de Siamese.

Responsabilidades:

```text
alinear timestamps;
convertir unidades;
asociar variables a zonas Siamese;
asociar meters a categorías;
calcular KPIs;
marcar quality flags;
preparar datos para visualización;
preparar series para calibración;
preparar outputs para datasets.
```

Ejemplo de output normalizado:

```yaml
NormalizedSimulationResults:
  run_id: run_001
  zones:
    - zone_id: zone_aula_3b
      metrics:
        mean_temperature: 22.1
        max_temperature: 24.3
        comfort_hours: 87.5
      timeseries:
        temperature: ts_zone_aula_3b_temperature
        relative_humidity: ts_zone_aula_3b_rh
  energy:
    heating_kwh: 12840.5
    electricity_kwh: 4430.2
```

---

## 16. Diagnostics Engine

El backend debe traducir los errores de EnergyPlus a mensajes comprensibles.

Tipos de diagnóstico:

```text
geometry_error;
construction_error;
schedule_error;
hvac_error;
weather_error;
output_error;
engine_runtime_error;
license_or_installation_error;
unknown_error.
```

Ejemplo:

```yaml
DiagnosticReport:
  id: diag_001
  run_id: run_001
  severity: severe
  category: geometry
  message: EnergyPlus rechazó una superficie por vértices no válidos.
  suggested_fix: Revisar orientación y coplanaridad de la superficie.
  linked_entity: surface:facade_south_03
```

Este módulo es clave para que Siamese pueda ser usado por clientes sin conocimiento profundo de EnergyPlus.

---

## 17. Artifact Registry

Cada artefacto debe tener identidad y trazabilidad.

Artefactos típicos:

```text
EnergyModel;
CompiledEnergyPlusModel;
WeatherProfile;
SimulationRun;
RawEnergyPlusOutputs;
NormalizedResults;
DiagnosticReport;
CalibrationCandidate;
CalibratedModel;
DatasetManifest;
SurrogateModel;
ControlPolicy;
Report;
USDVisualizationLayer.
```

Metadatos mínimos:

```yaml
Artifact:
  artifact_id: artifact_001
  type: CompiledEnergyPlusModel
  path: runs/compiled/compiled_epjson_001/in.epJSON
  checksum: sha256:...
  created_at: timestamp
  created_by: agent_or_user
  source_entities:
    - energy_model:energy_model_v12
  version: 1
```

Sin artifact registry, Siamese se convertiría en carpetas de resultados difíciles de auditar.

---

## 18. Provenance y reproducibilidad

Cada simulación debe ser reproducible.

Hay que registrar:

```text
versión de EnergyPlus;
versión del compilador Siamese;
versión del modelo energético;
versión del archivo climático;
checksum del input generado;
checksum del EPW;
outputs solicitados;
normalizer version;
runner version;
entorno de ejecución;
usuario/agente origen.
```

Ejemplo:

```yaml
SimulationProvenance:
  run_id: run_001
  energyplus_version: 26.1.0
  compiler_version: siamese-energy-compiler-0.1.0
  normalizer_version: siamese-results-0.1.0
  energy_model_id: energy_model_v12
  compiled_model_checksum: sha256:...
  weather_checksum: sha256:...
  requested_by: user:pablo
  launched_from: omniverse_kit
```

---

## 19. API REST / SDK

El backend debe exponer una API estable para Omniverse Kit, web dashboards, agentes y herramientas externas.

Endpoints mínimos para simulación:

```http
POST /api/v1/energy-models
GET  /api/v1/energy-models/{id}
POST /api/v1/simulation-cases
POST /api/v1/simulation-runs
GET  /api/v1/simulation-runs/{id}
GET  /api/v1/simulation-runs/{id}/results
GET  /api/v1/simulation-runs/{id}/diagnostics
```

Endpoints futuros:

```http
POST /api/v1/calibration-jobs
GET  /api/v1/calibration-jobs/{id}
POST /api/v1/dataset-campaigns
GET  /api/v1/dataset-campaigns/{id}
POST /api/v1/surrogate-training-jobs
GET  /api/v1/surrogate-models/{id}
POST /api/v1/recommendations
POST /api/v1/approvals
```

El SDK Python interno puede envolver esta API para scripts, tests y agentes.

---

## 20. Relación con Omniverse Kit

Omniverse Kit será un cliente avanzado del backend.

Kit debe poder:

```text
crear o editar entidades AEC/USD;
solicitar validación energética;
crear SimulationCase;
lanzar simulaciones;
consultar estado de jobs;
visualizar resultados;
mostrar diagnósticos;
abrir tareas agénticas;
crear approvals;
mostrar execution history.
```

Pero Kit no debe:

```text
ejecutar EnergyPlus directamente;
parsear outputs crudos;
contener la lógica energética principal;
escribir IDF directamente;
modificar modelos calibrados sin backend.
```

Flujo típico:

```text
Usuario selecciona Aula_3B en Omniverse.
↓
Kit llama al backend para consultar resultados.
↓
Backend devuelve NormalizedResults.
↓
Kit colorea la zona y muestra gráficas.
```

---

## 21. Relación con OpenUSD

OpenUSD representa geometría, jerarquía, semántica visual y capas colaborativas.

El backend debe mapear USD hacia el modelo energético interno:

```text
USD Stage
→ USD/AEC Mapper
→ Siamese EnergyModel
→ EnergyPlus Compiler
```

Y resultados hacia USD:

```text
NormalizedResults
→ Visualization Mapper
→ USD result layer / metadata binding
→ Omniverse viewport
```

USD debe guardar:

```text
geometría;
spaces;
surfaces;
openings;
material metadata;
sensor bindings;
result bindings;
visualization layers;
scenario layers.
```

El backend debe guardar:

```text
runs;
series temporales;
outputs normalizados;
calibraciones;
datasets;
surrogates;
jobs;
aprobaciones.
```

No conviene guardar grandes series temporales dentro de USD. USD debe contener bindings y capas visuales; los datos pesados deben vivir en backend storage.

---

## 22. Relación con Nucleus

Nucleus puede servir para colaboración sobre USD y assets.

Responsabilidad de Nucleus:

```text
stages USD compartidos;
layers colaborativos;
assets;
control de acceso a escenas;
versiones visuales;
trabajo multiusuario sobre el modelo.
```

Responsabilidad del backend:

```text
modelo energético normalizado;
runs;
resultados;
sensores;
calibración;
datasets;
surrogates;
jobs;
roadmaps;
trazabilidad.
```

Relación:

```text
Nucleus almacena el edificio visual/semántico.
Backend almacena la inteligencia energética y operacional.
```

---

## 23. Relación con sensórica

La sensórica entra al backend mediante conectores:

```text
CSV;
MQTT;
REST;
OPC-UA;
BACnet;
Modbus;
BMS;
simuladores.
```

Flujo:

```text
Sensors / BMS
→ Ingestion Service
→ Time-Series Storage
→ SensorBinding
→ Calibration / Visualization / Surrogate / Alerts
```

El backend debe poder comparar:

```text
medido;
simulado;
predicho;
estimado.
```

Ejemplo:

```yaml
ZoneOperationalState:
  zone_id: zone_aula_3b
  measured_temperature: 23.4
  simulated_temperature: 22.9
  predicted_temperature_30min: 24.1
  confidence: 0.86
```

El TFG demostró que el flujo sensor → CSV → tratamiento manual → comparación con simulación es potente pero frágil. Siamese debe hacer que ese flujo sea nativo.

---

## 24. Relación con calibración

La calibración usa el backend EnergyPlus como motor de simulaciones candidatas.

Flujo:

```text
CalibrationJob
→ CalibrationParameterSpace
→ CandidateGenerator / Optimizer
→ SimulationCases
→ EnergyPlus Runs
→ Result Normalization
→ Metric Evaluation
→ Candidate Ranking
→ CalibratedModel
```

Contrato conceptual:

```yaml
CalibrationJob:
  id: caljob_001
  energy_model_id: energy_model_v3
  target_period:
    start: 2026-04-22
    end: 2026-04-29
  target_sensors:
    - sensor_aula_3b_temp
    - sensor_aula_3b_rh
  variables:
    - infiltration_rate
    - glazing_u_value
    - occupancy_gain
    - heating_schedule_offset
  metrics:
    - CVRMSE
    - NMBE
    - NMAE
```

La calibración no debe ser un script externo. Debe ser un workflow trazable.

---

## 25. Relación con Dataset Factory

El backend debe generar datasets físicos sintéticos desde modelos calibrados.

Flujo:

```text
CalibratedEnergyModel
→ ScenarioSpace
→ SamplingPlan
→ SimulationCampaign
→ NormalizedResults
→ DatasetManifest
→ ML-ready dataset
```

El DatasetManifest debe registrar:

```text
modelo origen;
versión calibrada;
variables sampleadas;
rangos;
clima;
outputs;
features;
targets;
splits;
normalización;
checksums;
calidad;
provenance.
```

Esto evita que los datasets sean carpetas de CSVs sin trazabilidad.

---

## 26. Relación con Surrogate Factory

Los surrogates se entrenan a partir de datasets generados o datos reales normalizados.

Flujo:

```text
DatasetManifest
→ TrainingRecipe
→ TrainingJob
→ CandidateSurrogate
→ ValidationReport
→ ApprovedSurrogate
→ InferenceArtifact
```

Tipos de surrogate:

```text
RC / grey-box;
LSTM / GRU;
Transformers temporales;
GNN multizona;
híbridos físico-ML;
physics-informed neural networks;
modelos residuales sobre RC.
```

El backend debe registrar:

```text
dataset usado;
arquitectura;
hiperparámetros;
función de pérdida;
restricciones físicas;
métricas;
rollout;
incertidumbre;
artefacto exportado;
versión de runtime.
```

---

## 27. Relación con control y recomendaciones

El módulo de control debe usar estados normalizados, no datos crudos.

Flujo:

```text
Sensor state
+ Surrogate prediction
+ Constraints
+ Comfort targets
+ Energy/cost objective
→ Recommendation
→ Safety Layer
→ Shadow Mode / Approval / Supervised Control
```

El backend debe soportar modos:

```text
observation;
recommendation;
shadow_mode;
supervised_control;
limited_auto_control.
```

Al inicio, el modo correcto es:

```text
recomendación + shadow mode;
no control automático directo.
```

---

## 28. Relación con flujos agénticos Pepper/Hermes

El backend debe exponer tools gobernadas para agentes.

Ejemplos:

```text
CreateSimulationCase;
ValidateEnergyModel;
RunSimulation;
GetSimulationDiagnostics;
CreateCalibrationJob;
GenerateDatasetCampaign;
TrainSurrogate;
CreateRecommendation;
RequestApproval;
CreateRoadmapTask.
```

Un agente no debe:

```text
editar archivos IDF directamente;
lanzar EnergyPlus fuera del runner;
aprobar calibraciones finales;
desplegar surrogates operativos sin gate;
activar control HVAC sin autorización;
borrar resultados;
ignorar warnings críticos.
```

La capa agéntica debe apoyarse en:

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

---

## 29. Seguridad y permisos

El backend debe implementar permisos desde el inicio conceptual.

Acciones críticas:

```text
aprobar modelo calibrado;
desplegar surrogate;
activar shadow mode;
conectar BMS real;
enviar comandos HVAC;
borrar datos;
modificar modelo base;
publicar reporte a cliente.
```

Deben requerir:

```text
rol autorizado;
evidencia suficiente;
estado correcto del roadmap;
approval gate;
audit log;
rollback o plan de reversión cuando aplique.
```

Ejemplo:

```yaml
PolicyRule:
  action: DeploySurrogate
  requires:
    - surrogate.validation_status == approved
    - user.role in [EnergyEngineer, Admin]
    - approval_gate.status == approved
    - dataset.provenance.complete == true
```

---

## 30. Escalabilidad

El backend debe escalar en varios niveles.

### 30.1 Escalabilidad de simulaciones

EnergyPlus se puede ejecutar en paralelo por campañas:

```text
SimulationJob 1 → worker 1
SimulationJob 2 → worker 2
SimulationJob 3 → worker 3
...
```

### 30.2 Escalabilidad de edificios

El backend debe soportar:

```text
Organization
→ Portfolio
→ Site
→ Building
→ Floor
→ Zone
→ Sensor
→ Model
→ Dataset
→ Surrogate
```

### 30.3 Escalabilidad de producto

Cada nuevo edificio no debe requerir scripts nuevos. Debe usar:

```text
plantillas;
importadores;
wizards;
validadores;
roadmaps;
workflows;
reports;
APIs.
```

### 30.4 Escalabilidad de datos

Las series temporales deben almacenarse fuera de USD, en sistemas adecuados:

```text
PostgreSQL/TimescaleDB;
InfluxDB;
Parquet/Delta;
object storage;
metadata registry.
```

---

## 31. Testing

El backend debe tener tests por capas.

```text
unit tests:
  validadores, compiladores, parsers.

integration tests:
  modelo mínimo → EnergyPlus → resultados.

golden tests:
  mismo input produce mismo IDF/epJSON.

regression tests:
  outputs esperados no cambian accidentalmente.

contract tests:
  API y DTOs estables.

worker tests:
  jobs y estados.

agent tool tests:
  permisos, evidence y approvals.
```

Fixtures recomendadas:

```text
modelo mínimo una zona;
modelo multizona simple;
modelo con ventana;
modelo con schedule;
modelo con HVAC simple;
modelo inválido por geometría;
modelo inválido por material;
run EnergyPlus exitoso;
run EnergyPlus fallido.
```

---

## 32. MVP del backend Python

El MVP debe ser un vertical slice robusto.

### Objetivo

Demostrar que Siamese puede controlar el ciclo completo:

```text
modelo interno → validación → compilación → ejecución EnergyPlus → resultados normalizados → API → visualización.
```

### Alcance MVP

```text
EnergyModel mínimo;
ThermalZone;
Surface básica;
Construction simple;
Schedule básico;
WeatherProfile EPW;
SimulationCase;
EnergyPlus CLI runner;
ERR parser;
CSV/SQL parser mínimo;
NormalizedResults;
API mínima;
primer binding con Omniverse.
```

### Fuera del MVP

```text
HVAC detallado;
calibración completa;
generación masiva de datasets;
surrogates avanzados;
control;
DSX Air;
agentes autónomos;
multiusuario completo.
```

---

## 33. Roadmap de construcción

### Fase 1 — Fundamentos

```text
Core IDs;
Artifact model;
EnergyModel mínimo;
SimulationCase;
WeatherProfile;
```

### Fase 2 — EnergyPlus Runner

```text
detectar EnergyPlus;
validar versión;
ejecutar CLI;
crear sandbox;
capturar outputs;
parsear errores.
```

### Fase 3 — Compilador mínimo

```text
EnergyModel → epJSON/IDF;
golden fixtures;
checksum;
compiled model artifact.
```

### Fase 4 — Resultados normalizados

```text
leer outputs;
extraer temperatura zona;
extraer consumo;
crear NormalizedResults;
API de consulta.
```

### Fase 5 — Omniverse binding

```text
selección de zona;
run status;
heatmap mínimo;
grilla temporal simple;
diagnósticos en panel.
```

### Fase 6 — Calibración inicial

```text
sensor binding;
comparación sensor vs simulado;
metric evaluator;
primer CalibrationJob simple.
```

### Fase 7 — Dataset campaign MVP

```text
sampling básico;
batch de SimulationCases;
DatasetManifest;
export Parquet/CSV.
```

---

## 34. Riesgos de diseño

### Riesgo 1 — Wrapper demasiado fino

Si el backend solo ejecuta EnergyPlus, no habrá producto.

Mitigación:

```text
contratos, validación, normalización y jobs desde el inicio.
```

### Riesgo 2 — Sobrediseño prematuro

Si se intenta cubrir todo EnergyPlus desde el día uno, el proyecto se bloqueará.

Mitigación:

```text
vertical slice mínimo y extensible.
```

### Riesgo 3 — Lógica energética en Omniverse

Si Kit contiene lógica del solver, el sistema será difícil de mantener.

Mitigación:

```text
Kit como cliente del backend.
```

### Riesgo 4 — Outputs no gobernados

Si cada módulo lee CSVs por su cuenta, habrá inconsistencias.

Mitigación:

```text
NormalizedResults como contrato único.
```

### Riesgo 5 — Agentes con acceso directo

Si los agentes editan archivos o lanzan scripts, habrá riesgo operativo.

Mitigación:

```text
tools gobernadas;
policy engine;
evidence registry;
approval gates;
execution inspector.
```

---

## 35. Ventajas estratégicas

El backend Python propio aporta:

```text
abstracción sobre EnergyPlus;
experiencia usable para novatos;
profundidad para expertos;
compatibilidad con modelos existentes;
reproducibilidad;
trazabilidad;
escalabilidad;
capacidad de calibración;
generación de datasets;
base para surrogates;
base para control;
integración visual;
integración agéntica.
```

La ventaja comercial no es decir:

```text
Siamese usa EnergyPlus.
```

La ventaja es decir:

```text
Siamese convierte EnergyPlus en una plataforma operativa conectada a datos reales, IA, visualización y workflows agénticos.
```

---

## 36. Relación con la narrativa del producto

En una presentación, este módulo se puede explicar así:

> EnergyPlus aporta la física. El backend Python de Siamese convierte esa física en una plataforma: valida modelos, compila entradas, ejecuta simulaciones, normaliza resultados y alimenta calibración, datasets, IA, visualización y control.

Versión corta:

> EnergyPlus calcula. El backend Siamese lo convierte en producto.

Versión para inversores:

> No estamos vendiendo una interfaz sobre un solver. Estamos construyendo la capa de producto que transforma simulaciones físicas en operación continua.

---

## 37. Relación con el TFG

El TFG demostró el flujo manual:

```text
sensores reales;
CSV;
DesignBuilder;
modelo 3D;
calibración;
algoritmos genéticos;
comparación sensor/simulación;
análisis de mejoras;
modelo finalmente archivado.
```

Siamese convierte ese flujo en arquitectura:

```text
sensores reales → ingestion layer;
CSV manual → time-series storage;
DesignBuilder/EnergyPlus → backend propio;
calibración artesanal → CalibrationJob;
algoritmos genéticos → optimizer module;
comparación manual → metrics evaluator;
modelo archivado → gemelo vivo;
análisis puntual → operación continua.
```

La diferencia fundamental:

```text
TFG:
modelo calibrado como entregable.

Siamese:
modelo calibrado como infraestructura viva.
```

---

## 38. Primeros tickets recomendados

### BEP-00 — Backend Python vision

Crear documento de visión y fronteras del backend Python.

### BEP-01 — Core contracts

Definir `EnergyModel`, `SimulationCase`, `CompiledEnergyPlusModel`, `SimulationRun`, `NormalizedResults` y `DiagnosticReport`.

### BEP-02 — EnergyPlus CLI runner spike

Detectar EnergyPlus instalado y ejecutar una simulación mínima en sandbox.

### BEP-03 — Minimal epJSON compiler

Compilar un modelo interno mínimo a epJSON.

### BEP-04 — Diagnostics parser

Parsear archivo ERR y clasificar errores/warnings.

### BEP-05 — Normalized zone results

Extraer una serie de temperatura por zona y exponerla como contrato estable.

### BEP-06 — Simulation API MVP

Crear endpoints para SimulationCase, SimulationRun, status, results y diagnostics.

### BEP-07 — Golden regression fixture

Crear fixture reproducible para detectar cambios accidentales del compilador.

### BEP-08 — USD/AEC mapper stub

Definir primer contrato de mapeo desde entidades USD/AEC al EnergyModel.

### BEP-09 — Omniverse result binding MVP

Mostrar un resultado normalizado en una zona del viewport.

### BEP-10 — Sensor comparison stub

Comparar una serie de sensor contra una serie simulada para preparar calibración.

---

## 39. Decisión arquitectónica final

La decisión que debe guiar este módulo es:

```text
El backend Python es la capa de producto que gobierna EnergyPlus.
```

De esta decisión derivan las demás:

```text
Siamese tiene modelo interno propio.
EnergyPlus es solver externo.
Omniverse Kit es cliente visual.
OpenUSD representa geometría y semántica.
Nucleus facilita colaboración sobre USD.
Los sensores entran por ingestion layer.
La calibración usa jobs trazables.
Los datasets tienen manifiestos.
Los surrogates tienen registry.
El control pasa por safety y approvals.
Los agentes actúan mediante tools gobernadas.
```

Sin este backend, Siamese sería una suma de tecnologías. Con este backend, Siamese puede convertirse en una plataforma.

---

## 40. Referencias internas de proyecto

- `digital_twin_contexto_maestro.md` — visión general de Siamese, macroproyectos, arquitectura modular y principios EnergyPlus/Omniverse/USD/agentes.
- `siamese_energyplus_context.md` — documento específico sobre EnergyPlus como solver físico dentro de Siamese.
- `Concienciación ambiental y optimización energética del CEP Divino Maestro.pdf` — origen narrativo y técnico: sensórica, DesignBuilder, calibración, algoritmos genéticos y limitación del modelo calibrado archivado.
