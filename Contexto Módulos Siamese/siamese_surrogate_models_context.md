# Siamese — Módulo Surrogate Models

**Documento:** Contexto técnico y estratégico del módulo de modelos surrogados dentro de Siamese  
**Proyecto:** Siamese — plataforma agéntica de gemelos digitales energéticos  
**Estado:** Documento de arquitectura conceptual previo a implementación  
**Versión:** 0.1  
**Propósito:** definir cómo Siamese entrenará, validará, registrará y desplegará modelos surrogados a partir de EnergyPlus, modelos calibrados, datasets físicos, sensórica real, physics-informed machine learning, PINNs, BESOS y flujos de inferencia/control.

---

## 1. Resumen ejecutivo

El módulo de **Surrogate Models** convierte Siamese de una plataforma de simulación/calibración en una plataforma de **operación predictiva**.

EnergyPlus aporta simulación física de alta fidelidad. La calibración ajusta el modelo al comportamiento real del edificio. La sensórica aporta observación. El Dataset Factory genera datos estructurados. El módulo de modelos surrogados utiliza todo eso para entrenar modelos rápidos capaces de predecir el estado futuro del edificio y evaluar estrategias de operación.

La frase central del módulo es:

> **EnergyPlus da rigor físico. Los surrogates dan velocidad operativa.**

Flujo conceptual:

```text
Modelo EnergyPlus calibrado
        ↓
Simulaciones masivas
        ↓
Dataset físico sintético
        ↓
Entrenamiento surrogate
        ↓
Validación contra simulación y sensores reales
        ↓
Inferencia rápida
        ↓
Predicción / shadow mode / recomendaciones / control supervisado
```

Un surrogate no sustituye a EnergyPlus. Lo complementa.

EnergyPlus sigue siendo la referencia física de alta fidelidad. El surrogate es el modelo rápido que permite predicción operativa, evaluación de acciones, sensor masking, shadow mode y control supervisado.

---

## 2. Qué es un surrogate model en Siamese

Un **modelo surrogado** es un modelo aproximado, normalmente mucho más rápido que un solver físico completo, entrenado para reproducir una parte del comportamiento energético, térmico u operativo del edificio.

En Siamese, un surrogate puede aprender:

```text
temperatura futura por zona;
humedad futura por zona;
demanda térmica;
consumo energético;
respuesta a setpoints;
respuesta a ventilación;
respuesta del edificio a ocupación;
inercia térmica;
riesgo de disconfort;
estado estimado cuando falla un sensor;
efecto de acciones HVAC.
```

El surrogate trabaja sobre el estado actual y pasado del edificio:

```text
sensores;
clima;
ocupación;
horarios;
estado HVAC;
setpoints;
zona;
propiedades físicas;
outputs EnergyPlus;
datos reales.
```

Y devuelve predicciones rápidas:

```text
T_zona(t + 15 min)
T_zona(t + 30 min)
HR_zona(t + 30 min)
carga térmica prevista
riesgo de sobrecalentamiento
acción candidata
confianza de predicción
```

---

## 3. Por qué Siamese necesita modelos surrogados

EnergyPlus es adecuado para:

```text
simulación detallada;
calibración;
análisis de escenarios;
generación de datasets;
validación offline;
comparación de mejoras;
auditoría técnica;
benchmark de modelos rápidos.
```

Pero EnergyPlus no es ideal como motor operativo principal para:

```text
inferencia cada pocos minutos;
control predictivo en tiempo real;
evaluar miles de acciones rápidamente;
shadow mode operativo;
optimización continua;
sensor masking;
estimación de estados;
respuesta interactiva en Omniverse Kit;
copiloto operativo del facility manager.
```

Problema:

```text
EnergyPlus puede simular con rigor,
pero no siempre con la velocidad necesaria para operar.
```

Solución:

```text
EnergyPlus calibrado genera conocimiento físico.
El surrogate lo comprime en un modelo rápido.
```

---

## 4. Posición del módulo en la arquitectura Siamese

El módulo de surrogates depende de módulos previos.

```text
EnergyPlus Backend
→ genera simulaciones y resultados normalizados.

Calibración
→ produce modelos calibrados.

Sensórica
→ aporta datos reales e inferencia live.

Dataset Factory
→ crea datasets ML-ready.

Feature Builder
→ produce features consistentes.

Model Registry
→ gobierna modelos entrenados.

Inference Runtime
→ ejecuta predicciones.

Control / Recommendations
→ usa predicciones para recomendar acciones.

Omniverse Kit
→ visualiza predicciones, incertidumbre y shadow mode.

Agentic Workflow Engine
→ orquesta entrenamiento, validación, aprobación y despliegue.
```

Arquitectura global:

```text
EnergyPlus Runner
        ↓
Dataset Factory
        ↓
Surrogate Factory
        ↓
Model Registry
        ↓
Inference Runtime
        ↓
Control / Visualization / Agents
```

---

## 5. Relación con EnergyPlus

EnergyPlus será la fuente física principal para generar datos de entrenamiento.

Flujo:

```text
CalibratedEnergyModel
        ↓
Scenario Sampling
        ↓
EnergyPlus Batch Simulation
        ↓
Normalized Results
        ↓
Surrogate Training Dataset
```

EnergyPlus se usa como:

```text
fuente de datos físicos sintéticos;
benchmark de validación;
simulador de alta fidelidad;
oráculo offline para acciones;
base para generar escenarios;
referencia para comparar el surrogate.
```

Regla:

```text
EnergyPlus no desaparece cuando entrenamos un surrogate.
EnergyPlus queda como referencia física, validador y generador de datos.
```

---

## 6. Relación con BESOS

BESOS es una referencia importante para este módulo.

BESOS significa **Building and Energy Simulation, Optimization and Surrogate-modelling**. Su valor principal para Siamese es que valida un pipeline similar:

```text
definir parámetros;
definir objetivos;
samplear el espacio de diseño/operación;
ejecutar EnergyPlus muchas veces;
guardar resultados estructurados;
entrenar un surrogate;
usar surrogate para explorar, optimizar o acelerar análisis.
```

Conceptos de BESOS que interesan:

```text
Parameters;
Objectives;
Problem;
Evaluators;
Sampling;
Optimizers;
Surrogate modelling workflows.
```

Equivalencias con Siamese:

```text
BESOS Parameters
→ Siamese ParameterSpace

BESOS Objectives
→ Siamese OutputRequest / ObjectiveSet

BESOS EvaluatorEP
→ Siamese EnergyPlus Runner + SimulationCampaign

BESOS Sampling
→ Siamese Dataset Factory Sampling

BESOS Optimizers
→ Siamese Calibration / Optimization Engine

BESOS surrogate examples
→ Siamese Surrogate Factory
```

---

## 7. Qué tomar de BESOS

BESOS es útil como referencia para:

```text
parametrización de modelos EnergyPlus;
sampling;
ejecución batch;
análisis paramétrico;
optimización;
uso de DataFrames;
entrenamiento de modelos ML;
flujo investigador reproducible.
```

Siamese debe aprender de BESOS en:

```text
cómo definir parámetros calibrables;
cómo lanzar campañas de simulación;
cómo relacionar inputs/outputs;
cómo estructurar experimentos;
cómo entrenar modelos rápidos sobre datos simulados.
```

---

## 8. Qué NO copiar directamente de BESOS

BESOS está más orientado a investigación, notebooks y experimentación. Siamese debe ser una plataforma producto.

Siamese necesita:

```text
multiusuario;
UI profesional;
Omniverse Kit;
OpenUSD/Nucleus;
sensórica real;
model registry;
dataset registry;
permisos;
approval gates;
shadow mode;
control readiness;
trazabilidad empresarial;
agentes gobernados;
runtime de inferencia;
operación conectada.
```

Además, BESOS tiene licencia GPL. Por tanto, no conviene copiar código de BESOS al core propietario de Siamese sin análisis legal específico.

Decisión:

```text
BESOS = referencia arquitectónica y experimental.
Siamese = implementación propia, modular, gobernada y productizable.
```

Regla:

```text
Estudiar patrones de BESOS.
No copiar código GPL al core propietario.
```

---

## 9. Tipos de modelos surrogados en Siamese

Siamese debe tener una **Surrogate Factory**, no un único modelo.

Familias:

```text
modelos estadísticos clásicos;
modelos grey-box RC;
MLP;
Random Forest;
Gradient Boosting;
Gaussian Processes;
LSTM;
GRU;
Temporal Transformers;
Graph Neural Networks;
hybrid RC + neural residual;
physics-informed neural networks;
physics-informed surrogate models;
foundation/transfer models futuros.
```

La elección depende de:

```text
cantidad de datos;
nivel de calibración;
objetivo de predicción;
horizonte temporal;
necesidad de interpretabilidad;
uso operativo;
coste computacional;
riesgo tolerable;
número de zonas;
tipo de edificio.
```

---

## 10. Modelos estadísticos clásicos

Ejemplos:

```text
Linear Regression;
Ridge;
Lasso;
Random Forest;
Gradient Boosting;
Gaussian Processes;
Support Vector Regression.
```

Uso en Siamese:

```text
baseline;
primeras comparaciones;
pocos datos;
modelos simples por zona;
validación inicial;
aproximaciones rápidas.
```

Ventajas:

```text
rápidos;
fáciles de entrenar;
fáciles de comparar;
buenos como baseline;
menor coste computacional;
más interpretables que deep learning.
```

Limitaciones:

```text
capturan mal dinámicas temporales largas;
pueden fallar fuera del dominio entrenado;
pueden no representar bien inercia térmica;
no siempre sirven para rollout multistep.
```

Decisión:

```text
Deben ser la primera familia de modelos para establecer baseline.
```

---

## 11. Modelos grey-box RC

Los modelos RC representan el edificio mediante analogías térmicas:

```text
R = resistencia térmica
C = capacidad térmica
```

Ejemplo conceptual:

```text
temperatura exterior
→ resistencia envolvente
→ nodo térmico de zona
→ capacidad térmica
→ cargas internas / HVAC
```

Ventajas:

```text
interpretables;
físicamente razonables;
rápidos;
útiles para MPC;
defendibles ante ingenieros;
buen equilibrio entre física y simplicidad.
```

Limitaciones:

```text
pueden ser demasiado simplificados;
requieren identificación de parámetros;
pueden no capturar geometrías complejas;
pueden requerir modelos distintos por zona/tipo de edificio.
```

Uso recomendado:

```text
primer surrogate operativo serio;
baseline físico;
modelo para MPC;
comparación con ML black-box.
```

---

## 12. MLP

Un MLP puede ser útil para aprender relaciones no lineales entre features y targets.

Entradas:

```text
temperatura actual;
clima;
ocupación;
setpoint;
estado HVAC;
radiación;
zona;
propiedades físicas.
```

Salidas:

```text
temperatura futura;
demanda;
consumo;
riesgo de confort.
```

Ventajas:

```text
simple;
rápido;
entrenamiento relativamente directo;
exportable a ONNX.
```

Limitaciones:

```text
no modela temporalidad por sí solo;
requiere features con lags y ventanas;
puede fallar en rollout.
```

Uso:

```text
baseline no lineal.
```

---

## 13. LSTM / GRU

Modelos recurrentes para series temporales.

Entradas típicas:

```text
temperatura actual;
temperaturas pasadas;
humedad;
clima;
ocupación;
estado HVAC;
setpoints;
radiación solar;
hora del día;
día de semana.
```

Salidas:

```text
temperatura futura;
humedad futura;
demanda térmica;
estado de confort;
consumo previsto.
```

Ventajas:

```text
capturan dinámica temporal;
útiles para predicción multistep;
compatibles con datos de sensores;
maduros;
buenos para inercia térmica.
```

Limitaciones:

```text
pueden ser caja negra;
pueden acumular error en rollouts largos;
necesitan buena alineación temporal;
pueden sufrir drift;
requieren Feature Builder robusto.
```

Decisión:

```text
Fase natural después de baselines y RC.
```

---

## 14. Temporal Transformers

Modelos basados en atención para secuencias temporales.

Ventajas:

```text
capturan dependencias largas;
manejan múltiples variables;
pueden trabajar con ventanas grandes;
útiles para patrones complejos.
```

Limitaciones:

```text
más pesados;
requieren más datos;
más difíciles de validar;
riesgo de sobreajuste en un solo edificio;
mayor coste de entrenamiento e inferencia.
```

Uso recomendado:

```text
fase posterior;
multi-edificio;
múltiples años;
datasets grandes;
transfer learning.
```

No deben ser MVP.

---

## 15. Graph Neural Networks multizona

Un edificio multizona puede representarse como un grafo.

```text
nodos
→ zonas térmicas, espacios, sensores, equipos.

aristas
→ adyacencias, paredes, puertas, flujos, conexiones HVAC.

atributos
→ orientación, volumen, área, materiales, sensores, setpoints.
```

Ventajas:

```text
representan relaciones espaciales;
encajan con edificios multizona;
pueden capturar transferencia entre zonas;
encajan con OpenUSD;
pueden generalizar entre edificios similares;
útiles para zonas sin sensor.
```

Limitaciones:

```text
más complejas;
requieren grafo bien definido;
necesitan datasets grandes;
validación más difícil;
requieren buen mapping USD/AEC/energy graph.
```

Uso futuro:

```text
multizona avanzada;
edificios grandes;
campus;
predicción espacial;
sensor masking;
control por zonas.
```

---

## 16. Physics-informed surrogate models

Los modelos physics-informed incorporan conocimiento físico en el entrenamiento o arquitectura.

No se entrenan solo con:

```text
error = predicho - real
```

También penalizan o restringen:

```text
balance energético;
transferencia de calor;
humedad;
inercia térmica;
restricciones HVAC;
límites físicos;
conservación;
rango de actuadores;
plausibilidad térmica.
```

Esto es especialmente importante porque:

```text
un modelo puramente data-driven puede predecir bien en test
pero violar física en operación.
```

Siamese debe posicionarse así:

```text
No IA genérica.
No caja negra pura.
Surrogates informados por física calibrada.
```

---

## 17. PINNs dentro de Siamese

Un PINN puro es más adecuado cuando tenemos ecuaciones diferenciales explícitas, condiciones de contorno claras y un dominio físico relativamente bien formulado.

En edificios reales, EnergyPlus contiene muchos submodelos. No es realista meter todo EnergyPlus directamente dentro de una loss function.

En Siamese, el enfoque más sensato es:

```text
physics-informed surrogate
```

más que:

```text
PINN puro para todo el edificio
```

Esto significa incorporar física parcial:

```text
balance térmico de zona;
inercia térmica;
ganancias internas;
transferencia por envolvente;
ventilación/infiltración;
acción HVAC;
humedad simplificada;
restricciones de confort;
límites de actuadores.
```

---

## 18. Physics-informed loss

Ejemplo conceptual:

```text
Loss total =
  α · error_temperatura
+ β · error_humedad
+ γ · error_consumo
+ δ · residual_balance_térmico
+ ε · penalización_acciones_físicamente_imposibles
+ ζ · penalización_fuera_de_rango
```

Donde:

```text
error_temperatura
→ diferencia predicción/simulación/sensor.

residual_balance_térmico
→ penalización si el modelo viola un balance físico simplificado.

penalización_acciones_físicamente_imposibles
→ setpoints, caudales o potencias fuera de rango.

penalización_fuera_de_rango
→ temperatura, humedad o demanda no plausibles.
```

Esto permite que el surrogate aprenda de datos sin perder coherencia física.

---

## 19. Balance térmico simplificado

Para una zona:

```text
Cz · dTz/dt =
    Q_hvac
  + Q_internal
  + Q_solar
  + Q_ventilation
  + Q_infiltration
  + Σ U_i A_i (T_adj_i - Tz)
```

El surrogate puede predecir:

```text
Tz(t+1)
```

Pero durante entrenamiento se penaliza si la predicción viola demasiado ese balance.

El modelo aprende:

```text
inercia térmica;
respuesta al clima;
efecto de ocupación;
efecto de HVAC;
transferencia entre zonas;
efecto de ventilación.
```

---

## 20. Modelos híbridos RC + neural residual

Una arquitectura muy recomendable para Siamese:

```text
T_pred = RC_model(state, action, weather) + NN_residual(features)
```

Interpretación:

```text
RC_model
→ captura física principal.

NN_residual
→ corrige efectos no modelados, errores, patrones reales.
```

Ventajas:

```text
más interpretable que deep learning puro;
más flexible que RC puro;
mejor coherencia física;
útil para control;
defendible ante usuarios técnicos.
```

Debe ser una línea prioritaria a medio plazo.

---

## 21. Relación con Dataset Factory

El módulo de surrogates depende totalmente de Dataset Factory.

No hay surrogate serio sin dataset serio.

El dataset debe incluir:

### Inputs

```text
temperatura exterior;
humedad exterior;
radiación solar;
viento si aplica;
ocupación;
horarios;
setpoints;
estado HVAC;
temperatura actual;
humedad actual;
historial temporal;
zona;
orientación;
planta;
propiedades físicas;
sensores reales si existen.
```

### Targets

```text
temperatura futura;
humedad futura;
demanda calefacción/refrigeración;
consumo;
confort;
carga térmica;
respuesta a acción.
```

### Metadata

```text
train/validation/test split;
splits temporales;
splits por escenario;
splits por zona;
normalización;
quality report;
provenance;
modelo EnergyPlus origen;
modelo calibrado origen;
versión EnergyPlus;
versión compiler;
versión dataset.
```

Regla:

```text
No DatasetManifest
→ no SurrogateTrainingJob.
```

---

## 22. Relación con calibración

Los surrogates deben entrenarse preferentemente sobre modelos calibrados.

Sin calibración:

```text
surrogate aprende un edificio teórico.
```

Con calibración:

```text
surrogate aprende un edificio parecido al real.
```

La calidad del surrogate depende de:

```text
calidad del modelo EnergyPlus;
calidad de calibración;
calidad de sensores;
calidad de sampling;
calidad de variables objetivo;
calidad de features;
cobertura de escenarios.
```

Regla de madurez:

```text
uncalibrated_model
→ analysis surrogate only

calibrated_for_prediction
→ prediction surrogate

calibrated_for_shadow_mode
→ shadow surrogate

calibrated_for_control
→ supervised control candidate
```

---

## 23. Relación con sensórica

La sensórica alimenta a los surrogates en dos momentos.

### 23.1 Entrenamiento y validación

Datos reales para:

```text
validar surrogate;
fine-tuning;
corregir sesgos;
detectar drift;
comparar contra EnergyPlus;
crear residual models;
evaluar generalización.
```

### 23.2 Inferencia live

Datos vivos para construir features:

```text
temperatura actual;
humedad actual;
CO₂;
ocupación;
HVAC state;
clima actual;
forecast;
setpoints;
quality flags.
```

Flujo:

```text
SensorReadings
→ cleaning
→ quality flags
→ latest state
→ Feature Builder
→ Surrogate Inference
```

Regla:

```text
El surrogate no consume datos crudos.
Consume FeatureVectors versionados.
```

---

## 24. Relación con Feature Builder

El Feature Builder es crítico. Debe garantizar que entrenamiento e inferencia usan las mismas features.

Debe controlar:

```text
orden de features;
unidades;
normalización;
lags;
ventanas temporales;
quality flags;
datos faltantes;
estimaciones;
no uso de datos futuros;
misma versión de schema.
```

Contrato:

```yaml
FeatureSchema:
  id: feature_schema_v01
  features:
    - zone_temp_t0
    - zone_temp_t_minus_10
    - zone_temp_t_minus_30
    - outdoor_temp
    - outdoor_humidity
    - solar_radiation
    - occupancy_estimate
    - heating_status
    - setpoint
    - hour_sin
    - hour_cos
```

Regla:

```text
No FeatureSchema estable
→ no inferencia operativa.
```

---

## 25. Relación con Siamese Adoption Model

Muchos clientes llegarán con modelos existentes.

Adoption Model puede producir:

```text
modelo DesignBuilder adoptado;
IDF importado;
OpenStudio OSM adoptado;
Revit → EnergyModel;
sensor CSV histórico;
Model Quality Report.
```

Pero el surrogate solo debe entrenarse si el modelo supera gates:

```text
simulation-ready;
calibration-ready;
dataset-ready;
surrogate-ready.
```

Flujo:

```text
IDF exportado de DesignBuilder
→ Siamese Adoption Model
→ Quality Report
→ Calibration Roadmap
→ Calibrated Model
→ Dataset Campaign
→ Surrogate Training
```

Esto permite revivir modelos antiguos y convertirlos en sistemas predictivos.

---

## 26. Relación con Omniverse Kit

Omniverse Kit debe visualizar y operar los surrogates, pero no entrenarlos.

Debe mostrar:

```text
modelo surrogate activo;
horizonte de predicción;
confianza;
zona seleccionada;
predicción temporal;
comparativa real/simulado/predicho;
zonas de mayor incertidumbre;
drift;
estado de inferencia;
recomendaciones derivadas;
quality flags.
```

Ejemplo de panel:

```text
Surrogate Inference & Control

Model: lstm_zone_v04
Status: running
Horizon: 30 min
Zone: Aula 3B

Current: 22.3 °C
Predicted 30 min: 24.1 °C
Confidence: 0.82
Risk: overheating
Recommended action: reduce heating earlier
```

---

## 27. Relación con Nucleus / OpenUSD

Nucleus y OpenUSD pueden representar:

```text
surrogate prediction layers;
prediction heatmaps;
confidence maps;
zones with high uncertainty;
surrogate metadata binding;
model status annotations.
```

Pero no deben almacenar el modelo ML completo ni las series temporales grandes.

Nucleus almacena:

```text
visualization layers;
bindings;
metadata;
annotations.
```

Backend / Model Registry almacena:

```text
model artifact;
metrics;
dataset;
training job;
validation report;
provenance.
```

---

## 28. Relación con control y optimización

El surrogate es el motor rápido para control.

Control necesita evaluar:

```text
si bajo setpoint 1 ºC, qué ocurre;
si ventilo 10 minutos, qué ocurre;
si retraso calefacción, qué ocurre;
si cambio horario, qué ocurre;
si limito potencia, qué ocurre.
```

Flujo:

```text
current state
→ surrogate rollout
→ candidate actions
→ predicted comfort/energy
→ safety constraints
→ recommendation
→ shadow mode
→ supervised control
```

Regla:

```text
Surrogate predicts.
Safety layer decides.
Human/policy approves.
```

El surrogate nunca debe saltarse la safety layer.

---

## 29. Relación con DSX / NetworkSim

DSX Air o NetworkSim no entrenan el surrogate térmico. Sirven para probar si el surrogate puede operar bajo condiciones reales de red.

Escenarios:

```text
sensor llega tarde;
feature incompleta;
MQTT broker falla;
gateway offline;
inference service tiene latencia;
BMS no confirma acción.
```

NetworkSim valida:

```text
latencia sensor → feature builder;
latencia feature → inference;
latencia inference → recommendation;
robustez con datos faltantes;
bloqueo de acciones con datos stale.
```

Esto es necesario antes de control supervisado.

---

## 30. Arquitectura interna propuesta

```text
siamese_backend/surrogates/
│
├── contracts/
│   ├── surrogate_model.py
│   ├── training_job.py
│   ├── inference_job.py
│   ├── model_signature.py
│   ├── prediction_result.py
│   ├── validation_report.py
│   └── deployment_status.py
│
├── datasets/
│   ├── dataset_loader.py
│   ├── feature_schema.py
│   ├── target_schema.py
│   ├── splits.py
│   └── normalization.py
│
├── models/
│   ├── baselines.py
│   ├── rc_model.py
│   ├── sklearn_models.py
│   ├── mlp.py
│   ├── lstm.py
│   ├── gru.py
│   ├── temporal_transformer.py
│   ├── graph_neural_network.py
│   ├── physics_informed.py
│   └── hybrid_rc_nn.py
│
├── training/
│   ├── trainer.py
│   ├── loss_functions.py
│   ├── physics_losses.py
│   ├── callbacks.py
│   ├── hyperparameter_search.py
│   └── experiment_tracking.py
│
├── validation/
│   ├── metrics.py
│   ├── rollout_validation.py
│   ├── temporal_split_validation.py
│   ├── zone_validation.py
│   ├── physics_consistency.py
│   ├── uncertainty.py
│   └── drift_detection.py
│
├── registry/
│   ├── model_registry.py
│   ├── artifact_store.py
│   ├── versioning.py
│   └── approval.py
│
├── inference/
│   ├── feature_builder_adapter.py
│   ├── inference_runtime.py
│   ├── batch_inference.py
│   ├── live_inference.py
│   ├── onnx_export.py
│   ├── triton_adapter.py
│   └── confidence.py
│
├── control/
│   ├── rollout_engine.py
│   ├── candidate_action_evaluator.py
│   └── shadow_mode_adapter.py
│
└── reports/
    ├── training_report.py
    ├── validation_report.py
    ├── deployment_report.py
    └── model_card.py
```

---

## 31. Contratos principales

### 31.1 SurrogateTrainingJob

```yaml
SurrogateTrainingJob:
  id: train_job_001
  dataset_id: dataset_calibrated_building_001_v04
  model_family: lstm
  target_variables:
    - zone_air_temperature
    - zone_relative_humidity
  horizon_minutes: 30
  input_window_minutes: 120
  status: running
  created_by: user_or_agent
```

### 31.2 FeatureSchema

```yaml
FeatureSchema:
  id: feature_schema_v01
  features:
    - zone_temp_t0
    - zone_temp_t_minus_10
    - zone_temp_t_minus_30
    - outdoor_temp
    - outdoor_humidity
    - solar_radiation
    - occupancy_estimate
    - heating_status
    - setpoint
    - hour_sin
    - hour_cos
```

### 31.3 SurrogateModel

```yaml
SurrogateModel:
  id: surrogate_lstm_building_001_v03
  model_family: LSTM
  trained_on_dataset: dataset_001
  calibrated_model_id: calibrated_model_v04
  target: zone_air_temperature
  horizon: 30min
  status: validated_for_shadow_mode
  artifact_path: models/surrogates/lstm_v03.onnx
```

### 31.4 PredictionResult

```yaml
PredictionResult:
  model_id: surrogate_lstm_building_001_v03
  zone_id: aula_3b
  timestamp: 2026-07-23T10:30:00Z
  horizon: 30min
  predictions:
    zone_air_temperature: 24.1
    relative_humidity: 42
  confidence: 0.82
  quality:
    measured_input_ratio: 0.87
    estimated_input_ratio: 0.13
```

### 31.5 ValidationReport

```yaml
ValidationReport:
  model_id: surrogate_lstm_building_001_v03
  metrics:
    MAE_temperature: 0.34
    RMSE_temperature: 0.52
    rollout_error_60min: 0.88
    physics_residual_score: 0.91
  validation_status: passed_for_shadow_mode
  limitations:
    - low confidence during holidays
    - not validated for summer cooling
```

---

## 32. Métricas de validación

No basta con MSE.

Siamese debe validar:

### 32.1 Error puntual

```text
MAE;
RMSE;
MAPE si aplica;
NMAE;
CVRMSE.
```

### 32.2 Rollout error

```text
error 15 min;
error 30 min;
error 60 min;
error 2 h;
error acumulado.
```

Un modelo puede predecir bien un paso y fallar en varios pasos.

### 32.3 Error por zona

```text
aulas sur;
aulas norte;
pasillos;
zonas bajo cubierta;
zonas con sensor;
zonas sin sensor.
```

### 32.4 Error por régimen

```text
mañana;
tarde;
noche;
ocupado;
vacío;
calefacción on;
calefacción off;
ventilación;
fines de semana;
eventos anómalos.
```

### 32.5 Consistencia física

```text
no predecir temperaturas imposibles;
respetar inercia térmica;
respetar límites HVAC;
no crear energía artificial;
no violar tendencias básicas.
```

### 32.6 Incertidumbre y confianza

```text
intervalos de predicción;
confidence score;
out-of-distribution detection;
quality of inputs;
drift.
```

---

## 33. Model Registry

Cada surrogate debe quedar registrado con trazabilidad completa.

Debe incluir:

```text
modelo base EnergyPlus;
modelo calibrado origen;
dataset usado;
features;
targets;
arquitectura;
hiperparámetros;
métricas;
periodo de entrenamiento;
periodo de validación;
limitaciones;
estado de aprobación;
artifact path;
formato de exportación;
versión;
responsable;
fecha;
evidencia.
```

Estados:

```text
draft;
trained;
validated;
rejected;
approved_for_analysis;
approved_for_prediction;
approved_for_shadow_mode;
approved_for_supervised_control;
deprecated.
```

Regla:

```text
Ningún modelo pasa a operación sin ValidationReport y ApprovalGate.
```

---

## 34. Inference Runtime

El runtime de inferencia debe soportar varios modos.

### 34.1 Batch inference

Uso:

```text
replay de semana pasada;
validar surrogate;
comparar contra sensores;
generar informes;
benchmark.
```

### 34.2 Live inference

Uso:

```text
cada 5 min;
cada 15 min;
horizonte 30-60 min;
actualización de Omniverse;
shadow mode;
alertas.
```

### 34.3 Edge inference

Uso:

```text
inferencia local;
fallback si cloud cae;
menor latencia;
privacy;
operación robusta.
```

### 34.4 Cloud inference

Uso:

```text
muchos edificios;
entrenamiento centralizado;
modelos más pesados;
dashboards remotos;
fleet analytics.
```

---

## 35. ONNX, Triton y TensorRT

No conviene empezar con dependencia fuerte de NVIDIA para inferencia.

Orden recomendado:

```text
PyTorch / sklearn local
→ ONNX export
→ ONNX Runtime CPU
→ ONNX Runtime GPU
→ Triton Inference Server
→ TensorRT optimization
```

Principio:

```text
NVIDIA-compatible,
not NVIDIA-dependent.
```

Siamese puede usar aceleración NVIDIA más adelante, pero los modelos deben tener un camino portable.

---

## 36. Surrogate-assisted calibration

Línea avanzada.

Problema:

```text
calibrar con EnergyPlus puede requerir cientos o miles de simulaciones.
```

Solución:

```text
entrenar surrogate aproximado del espacio de parámetros
→ usarlo para explorar rápido
→ seleccionar candidatos prometedores
→ validar candidatos con EnergyPlus
```

Flujo:

```text
initial sampling
→ EnergyPlus runs
→ provisional surrogate
→ candidate search
→ EnergyPlus validation
→ update surrogate
→ repeat
```

Uso:

```text
acelerar calibración;
reducir coste computacional;
explorar espacios de búsqueda grandes;
mejorar NSGA-II / Bayesian optimization.
```

No debe ser MVP.

---

## 37. Sensor masking

Cuando falla un sensor, el surrogate puede estimar el estado de la zona.

Caso:

```text
sensor Aula_3B offline
```

Inputs disponibles:

```text
zonas vecinas;
temperatura exterior;
humedad exterior;
horario;
ocupación;
estado HVAC;
histórico;
surrogate;
modelo calibrado.
```

Output:

```yaml
EstimatedReading:
  zone_id: aula_3b
  timestamp: 2026-07-23T10:30:00Z
  variable: zone_air_temperature
  value: 22.7
  unit: C
  quality_flag: estimated
  source: surrogate_estimation
  confidence: 0.78
```

Regla:

```text
valor estimado ≠ valor medido.
```

Debe mostrarse explícitamente en UI y bloquear control si la confianza no es suficiente.

---

## 38. Shadow mode

Shadow mode es el primer uso operativo serio.

Flujo:

```text
datos reales
→ surrogate predice
→ recommendation engine propone acción
→ acción no se aplica
→ Siamese registra qué habría recomendado
→ compara contra evolución real
```

Shadow mode permite validar:

```text
precisión;
seguridad;
ahorro potencial;
riesgos;
confianza;
latencia;
fallos de sensores;
quality flags;
robustez de recomendaciones.
```

Regla:

```text
Antes de control real,
Siamese debe acumular evidencia en shadow mode.
```

---

## 39. Relación con agentes

Los agentes pueden orquestar el módulo de surrogates, pero no saltarse los gates.

Agentes posibles:

```text
Dataset Agent;
Surrogate Training Agent;
Validation Agent;
Inference Monitor Agent;
Drift Detection Agent;
Control Recommendation Agent;
Documentation Agent.
```

Permitido:

```text
crear TrainingJob;
seleccionar dataset candidato;
comparar modelos;
resumir ValidationReport;
detectar drift;
proponer retraining;
crear tareas de mejora;
generar Model Card.
```

No permitido sin aprobación:

```text
aprobar modelo para shadow mode;
aprobar modelo para control supervisado;
desplegar modelo operativo;
ignorar fallos de validación;
usar dataset sin quality report;
sobrescribir modelos aprobados.
```

---

## 40. MVP recomendado

### 40.1 Objetivo MVP

Entrenar un surrogate simple para predecir temperatura de una zona usando datos generados por EnergyPlus calibrado.

### 40.2 Alcance MVP

```text
1 edificio;
1 zona tipo;
temperatura como target;
horizonte 30 min;
dataset generado por EnergyPlus;
features básicas;
baseline Random Forest o Gradient Boosting;
MLP simple o LSTM simple;
validación contra EnergyPlus;
si hay sensores, validación secundaria contra sensor;
Model Registry básico;
PredictionResult contract;
visualización simple en Omniverse.
```

### 40.3 Fuera del MVP

```text
GNN;
Transformers;
PINNs completos;
control real;
Triton/TensorRT;
surrogate-assisted calibration;
multi-edificio;
sensor masking avanzado;
fine-tuning real;
deployment edge.
```

### 40.4 Resultado esperado

```text
Siamese puede entrenar un modelo rápido,
validarlo,
registrarlo,
hacer inferencia
y mostrar predicción por zona.
```

---

## 41. Evolución por fases

### Fase 1 — Baselines

```text
Random Forest;
Gradient Boosting;
MLP;
validación básica.
```

### Fase 2 — LSTM/GRU

```text
ventanas temporales;
rollout;
horizontes 15/30/60 min.
```

### Fase 3 — RC / Grey-box

```text
modelo interpretable;
MPC-ready;
comparación con ML.
```

### Fase 4 — Physics-informed loss

```text
balance térmico;
restricciones;
penalización física.
```

### Fase 5 — Hybrid RC + Neural Residual

```text
RC base;
red residual;
mayor robustez;
mejor interpretabilidad.
```

### Fase 6 — Multizona

```text
varias zonas;
relaciones espaciales;
transferencias;
zonas sin sensor.
```

### Fase 7 — GNN

```text
grafo térmico del edificio;
adyacencias;
relaciones HVAC;
OpenUSD graph mapping.
```

### Fase 8 — Shadow mode

```text
predicción live;
recomendaciones no aplicadas;
evidencia.
```

### Fase 9 — Control supervised

```text
surrogate como entorno rápido;
safety layer;
approval gates.
```

### Fase 10 — Acceleration

```text
ONNX;
Triton;
TensorRT;
edge inference;
GPU.
```

---

## 42. Primeros tickets recomendados

### SURR-00 — Surrogate module context

Crear documentación conceptual del módulo.

### SURR-01 — Surrogate contracts

Definir `SurrogateModel`, `TrainingJob`, `PredictionResult`, `ValidationReport`.

### SURR-02 — DatasetManifest dependency

Definir dependencia obligatoria Dataset → Surrogate.

### SURR-03 — FeatureSchema MVP

Crear contrato de features para predicción de temperatura.

### SURR-04 — Baseline model training

Entrenar Random Forest / Gradient Boosting sobre dataset EnergyPlus.

### SURR-05 — MLP baseline

Entrenar MLP simple.

### SURR-06 — LSTM spike

Entrenar LSTM con ventana temporal.

### SURR-07 — Validation metrics

Implementar MAE, RMSE, CVRMSE, rollout error.

### SURR-08 — Model Registry MVP

Registrar modelo, artefacto, métricas y estado.

### SURR-09 — PredictionResult API

Exponer predicción por zona/horizonte.

### SURR-10 — Omniverse prediction overlay

Visualizar predicción simple en Kit.

### SURR-11 — Physics-informed loss research

Diseñar primer residual físico simple.

### SURR-12 — BESOS architecture review

Documentar patrones reutilizables sin copiar código GPL.

### SURR-13 — ONNX export spike

Exportar modelo simple a ONNX.

### SURR-14 — Shadow mode readiness gate

Diseñar estados y criterios para pasar de predicción a shadow mode.

---

## 43. Riesgos principales

### Riesgo 1 — Modelo caja negra poco fiable

Mitigación:

```text
physics-informed losses;
RC baselines;
explainability;
validation reports;
uncertainty.
```

### Riesgo 2 — Entrenar sobre modelo no calibrado

Mitigación:

```text
calibration gate;
dataset-ready gate;
surrogate-ready gate.
```

### Riesgo 3 — Overfitting a un edificio o semana

Mitigación:

```text
splits temporales;
validación por escenarios;
dataset variado;
domain randomization;
real-data validation.
```

### Riesgo 4 — Error acumulado en rollout

Mitigación:

```text
multi-step validation;
closed-loop simulation;
horizon-specific metrics.
```

### Riesgo 5 — Features inconsistentes entre entrenamiento e inferencia

Mitigación:

```text
FeatureSchema versionado;
Feature Builder único;
normalización compartida.
```

### Riesgo 6 — Uso incompatible de BESOS

Mitigación:

```text
estudiar arquitectura;
no copiar código GPL al core;
implementar contratos propios;
evaluar integración externa si procede.
```

### Riesgo 7 — Desplegar demasiado pronto

Mitigación:

```text
Model Registry;
ValidationReport;
ApprovalGate;
Shadow mode antes de control.
```

---

## 44. Valor comercial

El valor comercial no es decir:

```text
La IA controla edificios automáticamente.
```

Eso sería peligroso y poco creíble.

La propuesta correcta:

```text
Siamese convierte modelos energéticos calibrados en modelos predictivos rápidos,
capaces de anticipar condiciones futuras y evaluar recomendaciones antes de actuar.
```

Valor para clientes:

```text
predecir sobrecalentamiento;
anticipar disconfort;
evaluar acciones antes de aplicarlas;
reducir consumo sin perder confort;
detectar sensores fallidos;
comparar operación real contra comportamiento esperado;
crear shadow mode antes de control;
justificar recomendaciones;
convertir modelos calibrados en sistemas operativos.
```

Frase comercial:

> **El modelo calibrado deja de ser un informe y se convierte en un sistema predictivo.**

---

## 45. Frases de presentación

Frase principal:

> **Los surrogates convierten la física calibrada en predicción operativa.**

Frase técnica:

> **Siamese entrena modelos rápidos a partir de simulaciones EnergyPlus calibradas y datos reales, incorporando restricciones físicas para predecir temperatura, humedad, demanda y confort en tiempo real.**

Frase comercial:

> **EnergyPlus entiende el edificio. El surrogate permite actuar a tiempo.**

Frase estratégica:

> **No sustituimos la física por IA. Convertimos la física calibrada en inferencia rápida.**

---

## 46. Decisión arquitectónica final

La decisión central:

```text
Los modelos surrogados serán una capa rápida de inferencia,
no una sustitución del modelo físico ni una caja negra autónoma.
```

Arquitectura final:

```text
EnergyPlus genera física.
Calibración ajusta realidad.
Dataset Factory estructura datos.
Surrogate Factory entrena modelos rápidos.
Model Registry gobierna versiones.
Inference Runtime predice.
Control Engine recomienda.
Omniverse visualiza.
Agentes orquestan.
```

Siamese debe aprender de BESOS, pero ir más allá:

```text
BESOS demuestra el workflow académico:
sampling → EnergyPlus → surrogate.

Siamese lo convierte en producto:
modelo adoptado → calibrado → dataset → surrogate → inferencia → shadow mode → operación supervisada.
```

---

## 47. Relación con documentos previos

Este documento complementa:

```text
siamese_energyplus_context.md
→ EnergyPlus como solver físico.

siamese_python_backend_context.md
→ backend Python como capa de gobierno.

siamese_calibration_module_context.md
→ calibración como puente modelo-realidad.

siamese_sensorics_module_context.md
→ sensórica como observación real.

siamese_adoption_model_context.md
→ adopción de modelos existentes.

siamese_omniverse_kit_context.md
→ visualización e interacción.

siamese_nucleus_module_context.md
→ colaboración y assets OpenUSD.

siamese_dsx_ecosystem_context.md
→ referencia estratégica NVIDIA/DSX.

digital_twin_contexto_maestro.md
→ visión modular general.
```

Y prepara:

```text
Dataset Factory;
Control and Optimization;
Siamese Exchange;
Shadow Mode;
Supervised Control;
Model Registry;
Agentic Workflow Engine;
CUDA-X / Triton / TensorRT acceleration.
```
