# Siamese — Módulo Optimización y Control

**Documento:** Contexto técnico y estratégico del módulo de optimización y control dentro de Siamese  
**Proyecto:** Siamese — plataforma agéntica de gemelos digitales energéticos  
**Estado:** Documento de arquitectura conceptual previo a implementación  
**Versión:** 0.1  
**Propósito:** definir cómo Siamese transformará simulaciones, modelos calibrados, sensórica y surrogates en recomendaciones operativas, shadow mode, control supervisado y, en fases avanzadas, políticas de control con MPC, optimización clásica, GPU/CUDA-X, PPO y Recurrent PPO.

---

## 1. Resumen ejecutivo

El módulo de **optimización y control** es la capa que convierte a Siamese en una plataforma capaz de pasar de la observación y predicción a la **decisión operativa**.

Hasta este punto, Siamese dispone de:

```text
EnergyPlus
→ simulación física de alta fidelidad.

Backend Python
→ gobierno, validación, compilación, ejecución y resultados normalizados.

Calibración
→ ajuste del modelo energético al comportamiento real del edificio.

Sensórica
→ observación real del edificio.

Dataset Factory
→ generación de datasets físicos y ML-ready.

Surrogate Models
→ inferencia rápida del comportamiento térmico/energético.

Omniverse Kit / Nucleus
→ visualización, colaboración y operación espacial.

DSX / NetworkSim
→ validación de red, latencia, BMS, gateways y robustez operacional.

Agentic Workflow Engine
→ roadmaps, tareas, aprobaciones, evidencias y gobernanza.
```

El módulo de control utiliza todo lo anterior para responder:

```text
¿Qué conviene hacer ahora?
¿Qué acción reduce consumo sin perder confort?
¿Qué acción es segura?
¿Qué acción debe bloquearse?
¿Qué habría pasado si hubiéramos actuado?
Cuándo hay evidencia suficiente para pasar de recomendación a control supervisado?
```

La frase central del módulo es:

> **Predice primero. Recomienda después. Actúa solo cuando hay evidencia.**

---

## 2. Qué es el módulo de optimización y control

El módulo de optimización y control es el sistema encargado de generar, evaluar, filtrar, explicar y registrar decisiones operativas sobre el edificio.

Trabaja con:

```text
estado actual del edificio;
predicción surrogate;
modelo calibrado;
restricciones de confort;
restricciones HVAC;
precio energético;
ocupación;
clima;
forecast;
señales de red;
calidad de sensores;
políticas de seguridad;
permisos;
modo operativo.
```

Produce:

```text
recomendaciones;
setpoints;
horarios optimizados;
estrategias de ventilación;
acciones de demand response;
planes de operación;
shadow-mode logs;
acciones supervisadas;
reportes de control;
readiness gates.
```

Su función no es simplemente “aplicar IA”.  
Su función es **tomar decisiones energéticas trazables y seguras**.

---

## 3. Principio fundamental

El módulo no debe empezar con control autónomo.

Arquitectura progresiva:

```text
simulación
→ calibración
→ surrogate validado
→ predicción
→ recomendación
→ shadow mode
→ control supervisado
→ control limitado
```

No:

```text
modelo IA
→ acción directa sobre HVAC
```

Regla central:

```text
No direct control before shadow evidence.
```

Y más estrictamente:

```text
No RL policy directly to HVAC.
```

---

## 4. Por qué este módulo es necesario

Sin optimización/control, Siamese puede decir:

```text
esta zona se va a sobrecalentar;
este edificio consume demasiado;
este sensor está fallando;
este modelo está calibrado;
esta predicción tiene baja confianza.
```

Con optimización/control, Siamese puede decir:

```text
si reduces este setpoint 1 ºC ahora, mantienes confort y ahorras energía;
si retrasas calefacción 45 minutos, el aula seguirá en rango a las 9:00;
si ventilas ahora, perderás calor innecesariamente;
si esperas 20 minutos, la inercia térmica mantiene el confort;
si el precio sube a las 18:00, conviene precalentar antes;
si el sensor principal está stale, la acción debe bloquearse.
```

Esto convierte Siamese en:

```text
diagnóstico
→ recomendación defendible
→ operación asistida
```

---

## 5. Relación con módulos previos

### 5.1 EnergyPlus

EnergyPlus valida física y escenarios offline.

Uso en control:

```text
validar estrategias;
comparar políticas;
generar datasets para surrogates;
hacer benchmarking de acciones;
auditar resultados.
```

EnergyPlus no debe ser el motor de control en tiempo real.

### 5.2 Calibración

El control solo tiene sentido si el modelo representa razonablemente el edificio real.

Regla:

```text
No calibrated model
→ no operational control.
```

### 5.3 Surrogate Models

Los surrogates permiten evaluar rápidamente acciones candidatas.

```text
estado actual
→ surrogate rollout
→ predicción bajo acción candidata
→ coste/confort/riesgo
```

### 5.4 Sensórica

La sensórica aporta estado real y calidad de datos.

```text
sensor valid
→ recomendación posible

sensor stale/offline
→ menor confianza o bloqueo
```

### 5.5 Dataset Factory

Permite entrenar y evaluar políticas, surrogates y entornos de control.

### 5.6 Omniverse Kit

Visualiza:

```text
recomendaciones;
riesgo;
horizonte;
zonas afectadas;
predicción;
shadow mode;
acciones bloqueadas;
confianza.
```

### 5.7 Nucleus

Puede almacenar capas visuales de recomendaciones, resultados y anotaciones.

### 5.8 DSX / NetworkSim

Valida robustez de comunicación:

```text
latencia sensor → inferencia;
fallos de gateway;
BMS ack/nack;
shadow mode bajo fallos;
bloqueo por datos stale.
```

### 5.9 Agentic Workflow Engine

Orquesta:

```text
tareas;
recomendaciones;
aprobaciones;
evidencia;
control readiness;
informes.
```

---

## 6. Modos de operación

Siamese debe tener niveles de madurez operativa.

### 6.1 Analysis Mode

Solo análisis offline.

```text
simular escenarios;
comparar consumos;
comparar confort;
evaluar reformas;
generar informes.
```

Uso:

```text
consultoría inicial;
diseño energético;
validación de hipótesis;
adoption model;
análisis de mejoras.
```

### 6.2 Recommendation Mode

Siamese propone, pero no actúa.

```text
recomendación visible;
impacto esperado;
confianza;
riesgo;
evidencia;
explicación.
```

Ejemplo:

```text
Reducir consigna de calefacción en Aula 3B de 22.5 ºC a 21.5 ºC entre 11:00 y 13:00.
Impacto esperado: menor sobrecalentamiento y menor consumo.
Riesgo: bajo.
```

### 6.3 Shadow Mode

Siamese calcula qué habría hecho, pero no lo aplica.

```text
acción recomendada;
no enviada al HVAC;
resultado esperado;
comparación posterior con realidad;
acumulación de evidencia.
```

Este modo es obligatorio antes de cualquier control real.

### 6.4 Supervised Control

Siamese propone y un humano aprueba.

```text
Siamese recomienda
→ facility manager revisa
→ humano aprueba
→ acción enviada
→ sistema registra resultado
```

### 6.5 Limited Auto-Control

Solo para acciones acotadas, seguras y reversibles.

```text
acciones dentro de límites;
zonas no críticas;
horarios definidos;
rollback;
monitorización;
bloqueo automático ante anomalías.
```

No debe ser una fase temprana.

---

## 7. Qué optimiza Siamese

El problema de control en edificios es multiobjetivo.

### 7.1 Confort térmico

```text
temperatura dentro de rango;
PMV;
PPD;
humedad relativa;
asimetrías térmicas;
horas fuera de confort;
estabilidad térmica.
```

### 7.2 Energía

```text
kWh;
demanda pico;
gas;
electricidad;
calefacción;
refrigeración;
bombas;
ventiladores;
auxiliares.
```

### 7.3 Coste

```text
precio horario;
tarifa dinámica;
potencia contratada;
penalizaciones por demanda;
coste operativo diario;
coste operativo semanal.
```

### 7.4 Emisiones

```text
kg CO₂;
factor de emisión horario;
mix eléctrico;
gas natural;
autoconsumo fotovoltaico;
emisiones evitadas.
```

### 7.5 Calidad del aire

```text
CO₂;
ventilación mínima;
renovaciones/hora;
humedad;
ocupación;
filtración.
```

### 7.6 Robustez

```text
mantener confort aunque falle un sensor;
evitar acciones con baja confianza;
evitar acciones con datos stale;
mantener operación segura;
fallback disponible.
```

Objetivo real:

```text
minimizar consumo
sin perder confort
sin violar seguridad
sin depender de datos malos
sin actuar fuera de límites HVAC.
```

---

## 8. Variables de decisión

### 8.1 Setpoints

```text
temperatura calefacción;
temperatura refrigeración;
humedad objetivo;
CO₂ objetivo.
```

### 8.2 Horarios

```text
inicio calefacción;
apagado calefacción;
ventilación;
ocupación prevista;
modo vacaciones;
preheating;
precooling.
```

### 8.3 HVAC

```text
fan speed;
caudal;
posición de válvula;
modo equipo;
temperatura de impulsión;
bomba on/off;
UTA on/off;
economizer;
recirculación.
```

### 8.4 Envolvente y operación pasiva

```text
persianas;
ventanas;
sombreamiento;
ventilación natural.
```

### 8.5 Energía distribuida

```text
batería;
fotovoltaica;
EV charging;
bomba de calor;
demand response.
```

Para MVP:

```text
setpoints;
horarios;
ventilación;
acciones recomendadas.
```

---

## 9. Restricciones

El control energético sin restricciones es peligroso.

Siamese debe imponer límites duros:

```text
temperatura mínima/máxima permitida;
rango de humedad;
CO₂ máximo;
tiempo mínimo entre cambios;
máximo cambio de setpoint por intervalo;
zonas críticas;
horarios ocupados;
prioridad de confort;
límites de equipos;
no actuar con sensor crítico offline;
no actuar si surrogate está fuera de dominio;
no actuar sin aprobación en fases tempranas;
no repetir comandos si no hay confirmación;
rollback obligatorio para control supervisado.
```

Ejemplo:

```text
No bajar calefacción si:
- zona ocupada;
- sensor principal está stale;
- surrogate confidence < 0.75;
- PMV previsto cae fuera de rango;
- no hay rollback definido.
```

---

## 10. Arquitectura general

Arquitectura conceptual:

```text
Current Building State
        ↓
Feature Builder
        ↓
Surrogate Inference
        ↓
Candidate Action Generator
        ↓
Optimizer / Policy
        ↓
Safety Layer
        ↓
Recommendation Engine
        ↓
Approval / Shadow / Supervised Control
        ↓
Monitoring & Feedback
```

Arquitectura detallada:

```text
Sensors / BMS / Weather / Occupancy / Tariffs
        ↓
State Estimator
        ↓
Prediction Model
        ↓
Control Problem Builder
        ↓
Optimization Engine
        ↓
Safety & Constraint Checker
        ↓
Action Proposal
        ↓
Human Approval / Shadow Log / BMS Gateway
        ↓
Outcome Evaluation
        ↓
Policy Improvement
```

---

## 11. Familias de métodos

Orden recomendado:

```text
1. Rule-based recommendations
2. Heuristic optimization
3. Classical optimization
4. MPC
5. Multiobjective optimization
6. Safe RL
7. PPO / Recurrent PPO
8. Hybrid agentic control
```

No empezar por PPO.

---

## 12. Rule-based recommendations

Primera capa operativa.

Ejemplos:

```text
si zona supera 23 ºC y calefacción está activa
→ recomendar bajar setpoint.

si CO₂ alto y zona ocupada
→ recomendar ventilación.

si sensor stale
→ bloquear recomendación operativa.

si predicción muestra sobrecalentamiento
→ recomendar anticipar apagado.

si zona vacía y calefacción activa
→ recomendar modo ahorro.
```

Ventajas:

```text
simple;
explicable;
seguro;
útil para MVP;
ideal para facility managers;
buen fallback.
```

Limitaciones:

```text
poco óptimo;
no explora combinaciones complejas;
requiere reglas manuales;
puede no adaptarse a edificios complejos.
```

Debe existir siempre como fallback.

---

## 13. Heurísticas y algoritmos evolutivos

Útiles para escenarios offline o semiautomáticos.

Casos:

```text
optimizar horarios;
optimizar setpoints;
optimizar estrategias de ventilación;
comparar configuraciones;
buscar soluciones Pareto;
definir estrategias semanales.
```

Métodos:

```text
genetic algorithms;
NSGA-II;
particle swarm;
simulated annealing;
bayesian optimization.
```

Relación con la experiencia previa:

```text
En el TFG se usaron algoritmos genéticos y frente de Pareto para calibrar variables críticas.
En Siamese, el mismo patrón puede aplicarse a operación:
- calibración busca parámetros del modelo;
- control busca acciones óptimas.
```

---

## 14. Optimización clásica

### 14.1 LP / QP

Útiles para problemas continuos:

```text
reparto de potencia;
minimización de coste;
suavizado de setpoints;
balance energético simplificado;
control con penalización cuadrática.
```

### 14.2 MILP

Útil para variables discretas:

```text
equipo on/off;
modo calefacción/refrigeración;
bomba activada;
horarios discretos;
ventanas de operación;
prioridad por zonas;
demand response.
```

### 14.3 QP para MPC

MPC suele formularse como:

```text
minimizar error de confort + consumo + cambios bruscos
sujeto a dinámica térmica y restricciones.
```

Puede convertirse en QP o MILP dependiendo del modelo.

---

## 15. MPC — Model Predictive Control

MPC debe ser uno de los métodos principales antes de RL.

Idea:

```text
1. Observar estado actual.
2. Predecir próximos estados.
3. Evaluar acciones futuras.
4. Elegir la primera acción óptima.
5. Repetir en el siguiente intervalo.
```

Flujo:

```text
estado actual
→ surrogate / RC model
→ horizonte 1-6 h
→ optimización
→ primera acción
→ siguiente ciclo
```

Ventajas:

```text
explicable;
basado en restricciones;
apto para ingeniería;
bueno para confort;
más fácil de validar que RL;
compatible con control supervisado;
natural para edificios.
```

Limitaciones:

```text
requiere modelo rápido fiable;
puede ser costoso con muchos estados;
depende de forecast;
requiere buena formulación;
requiere constraints bien definidas.
```

En Siamese, MPC debería usar:

```text
modelo RC;
surrogate validado;
hybrid RC + NN residual.
```

No EnergyPlus directo en tiempo real.

---

## 16. PPO

PPO, **Proximal Policy Optimization**, es un algoritmo de reinforcement learning que aprende políticas mediante interacción con un entorno simulado.

En Siamese puede servir para aprender una política:

```text
estado del edificio
→ acción HVAC
→ reward
```

Ejemplo de estado:

```text
temperaturas por zona;
humedad;
ocupación;
clima;
forecast;
estado HVAC;
precio energía;
hora;
quality flags.
```

Ejemplo de acción:

```text
setpoint calefacción;
setpoint refrigeración;
ventilación;
modo equipo;
fan speed;
válvula.
```

Reward conceptual:

```text
reward =
  - consumo energético
  - penalización por disconfort
  - penalización por CO₂ alto
  - penalización por cambios bruscos
  - penalización por acciones inseguras
```

PPO podría aprender políticas no triviales.

Pero:

```text
PPO no es MVP.
PPO no debe conectarse directamente al HVAC.
PPO debe entrenarse offline.
```

---

## 17. Recurrent PPO

Recurrent PPO añade memoria temporal mediante políticas recurrentes, normalmente LSTM.

Es especialmente interesante para edificios porque:

```text
la temperatura actual no basta;
la historia térmica importa;
la inercia térmica importa;
la ocupación pasada importa;
el HVAC pasado importa;
la ventilación pasada importa;
los sensores pueden ser incompletos.
```

Recurrent PPO puede aprender de secuencias:

```text
T(t-60), T(t-30), T(t)
HVAC(t-60), HVAC(t-30), HVAC(t)
occupancy(t)
weather(t)
```

Ventaja frente a PPO normal:

```text
mejor gestión de memoria térmica;
mejor en sistemas parcialmente observables;
mejor cuando faltan sensores;
mejor para dinámica lenta.
```

Riesgos:

```text
más difícil de entrenar;
más difícil de validar;
más difícil de explicar;
más peligroso si se despliega sin safety layer;
más sensible a datos fuera de distribución.
```

Uso recomendado:

```text
fase avanzada;
offline;
shadow mode;
comparación contra MPC;
nunca directo a HVAC sin safety/approval.
```

---

## 18. Por qué PPO/Recurrent PPO no son MVP

Riesgos de RL:

```text
puede aprender estrategias raras;
puede explotar errores del surrogate;
puede violar confort;
puede generalizar mal;
puede ser difícil de explicar;
puede requerir muchos datos;
puede fallar fuera del dominio de entrenamiento;
puede proponer acciones no aceptables para un facility manager.
```

Flujo seguro:

```text
EnergyPlus calibrado
→ surrogate validado
→ entorno simulado
→ entrenamiento RL offline
→ evaluación offline
→ stress tests
→ shadow mode
→ comparación contra MPC/reglas
→ control supervisado limitado
```

Regla:

```text
No RL policy directly to HVAC.
```

---

## 19. Entorno RL de Siamese

Para PPO/Recurrent PPO se necesita un entorno tipo Gymnasium.

```text
SiameseControlEnv
```

### 19.1 Observation

```yaml
observation:
  zone_temperatures: [...]
  zone_humidity: [...]
  occupancy: [...]
  outdoor_temperature: ...
  outdoor_humidity: ...
  solar_radiation: ...
  hvac_state: ...
  setpoints: [...]
  energy_price: ...
  time_features: ...
  sensor_quality: [...]
```

### 19.2 Action

Continuo:

```text
setpoint_delta;
fan_speed;
valve_position;
ventilation_rate;
supply_temperature.
```

Discreto:

```text
increase_setpoint;
decrease_setpoint;
keep;
ventilate;
preheat;
shutdown_zone.
```

### 19.3 Reward

```text
reward =
  - energy_cost
  - comfort_penalty
  - co2_penalty
  - action_smoothness_penalty
  - unsafe_action_penalty
```

### 19.4 Episode

```text
un día;
una semana;
periodo frío;
periodo cálido;
semana ocupada;
escenario con sensor failure;
escenario con tarifa dinámica;
escenario con ocupación atípica.
```

---

## 20. Safe RL

Si Siamese usa RL, debe ser **safe RL**.

No basta con maximizar reward.

Se necesitan:

```text
constraints;
action masks;
shielding;
fallback;
policy validation;
human approval;
rollback;
runtime monitors.
```

Ejemplo:

```text
PPO propone bajar calefacción.
Safety layer evalúa:
- zona ocupada;
- predicción PMV;
- temperatura mínima;
- confianza surrogate;
- sensor quality;
- acción anterior;
- límites HVAC.

Si falla:
→ bloquea acción.
```

Patrón correcto:

```text
RL Policy
→ Safety Shield
→ Recommendation
→ Approval / Shadow / Control
```

Nunca:

```text
RL Policy
→ HVAC
```

---

## 21. CUDA-X y librerías NVIDIA

El módulo de optimización puede beneficiarse de GPU, pero de forma selectiva.

Tecnologías relevantes:

```text
cuOpt;
cuDF;
cuML;
cuGraph;
CuPy;
PyTorch CUDA;
ONNX Runtime GPU;
Triton;
TensorRT;
cuDSS / sparse solvers;
custom CUDA kernels en fases avanzadas.
```

Principio:

```text
GPU-accelerated when useful.
CPU fallback always.
```

Siamese debe ser:

```text
NVIDIA-compatible,
not NVIDIA-dependent.
```

---

## 22. NVIDIA cuOpt

cuOpt es relevante para problemas de optimización acelerada por GPU, especialmente LP, QP, MILP y problemas de scheduling/routing.

Aplicaciones potenciales en Siamese:

```text
optimización de horarios HVAC;
optimización de setpoints;
demand response;
asignación de cargas;
scheduling de equipos;
operación de baterías;
cargadores EV;
problemas MILP/QP grandes;
multi-zona;
multi-edificio;
campus.
```

Ejemplo:

```text
Minimizar coste energético diario
sujeto a:
- temperatura dentro de rango;
- potencia máxima;
- horarios de ocupación;
- estado de batería;
- limitaciones HVAC.
```

No usar en MVP.

Arquitectura recomendada:

```text
OptimizationBackend:
  - scipy/cvxpy local
  - pyomo/pulp
  - cuOpt adapter
  - external solver adapter
```

---

## 23. RAPIDS cuDF / cuML

### 23.1 cuDF

Uso:

```text
datasets grandes de simulación;
series temporales masivas;
agregaciones;
feature engineering;
procesado de datos de sensores.
```

### 23.2 cuML

Uso:

```text
modelos baseline;
clustering de perfiles térmicos;
regresores surrogate;
detección de anomalías;
reducción dimensional;
clasificación de zonas.
```

Flujo posible:

```text
Dataset Factory masivo
→ cuDF para procesado
→ cuML para baselines
→ PyTorch para deep surrogates/RL
```

No debe ser dependencia inicial.

---

## 24. PyTorch CUDA, ONNX, Triton y TensorRT

Para RL y modelos neuronales:

```text
PyTorch CUDA
→ entrenamiento PPO, Recurrent PPO, LSTM, GNN.

ONNX
→ formato portable de inferencia.

ONNX Runtime GPU
→ inferencia acelerada sin lock-in fuerte.

Triton
→ serving de modelos a escala.

TensorRT
→ optimización NVIDIA avanzada.
```

Orden recomendado:

```text
PyTorch local
→ ONNX export
→ ONNX Runtime CPU
→ ONNX Runtime GPU
→ Triton
→ TensorRT
```

---

## 25. cuDSS / sparse solvers

Para MPC grande, problemas QP/NLP y modelos multizona, los solvers dispersos pueden ser importantes.

Uso futuro:

```text
MPC multizona;
QP grandes;
NLP con restricciones;
sistemas RC grandes;
optimización de campus;
matrices dispersas.
```

Estado:

```text
interesante a futuro;
no MVP;
requiere investigación específica;
requiere benchmarking.
```

---

## 26. Arquitectura interna propuesta

```text
siamese_backend/control/
│
├── contracts/
│   ├── control_state.py
│   ├── control_action.py
│   ├── control_policy.py
│   ├── optimization_problem.py
│   ├── recommendation.py
│   ├── safety_decision.py
│   └── control_result.py
│
├── state/
│   ├── state_estimator.py
│   ├── feature_adapter.py
│   ├── sensor_quality_adapter.py
│   └── occupancy_estimator.py
│
├── objectives/
│   ├── comfort_objective.py
│   ├── energy_objective.py
│   ├── cost_objective.py
│   ├── carbon_objective.py
│   └── multiobjective.py
│
├── constraints/
│   ├── comfort_constraints.py
│   ├── hvac_constraints.py
│   ├── safety_constraints.py
│   ├── sensor_constraints.py
│   └── approval_constraints.py
│
├── optimizers/
│   ├── rule_based.py
│   ├── heuristic.py
│   ├── genetic.py
│   ├── nsga2.py
│   ├── mpc.py
│   ├── scipy_optimizer.py
│   ├── cvxpy_optimizer.py
│   ├── cuopt_adapter.py
│   └── rl_policy_adapter.py
│
├── rl/
│   ├── env.py
│   ├── reward.py
│   ├── ppo_training.py
│   ├── recurrent_ppo_training.py
│   ├── policy_registry.py
│   └── offline_evaluation.py
│
├── safety/
│   ├── safety_layer.py
│   ├── action_shield.py
│   ├── fallback_policy.py
│   ├── rollback.py
│   └── runtime_monitor.py
│
├── shadow/
│   ├── shadow_mode.py
│   ├── shadow_logger.py
│   ├── counterfactual_eval.py
│   └── shadow_report.py
│
├── execution/
│   ├── bms_gateway.py
│   ├── command_dispatcher.py
│   ├── ack_monitor.py
│   └── command_history.py
│
└── reports/
    ├── recommendation_report.py
    ├── control_policy_report.py
    ├── shadow_mode_report.py
    └── control_readiness_report.py
```

---

## 27. Contratos principales

### 27.1 ControlState

```yaml
ControlState:
  building_id: building_001
  timestamp: 2026-07-23T10:30:00Z
  zones:
    aula_3b:
      temperature: 22.3
      humidity: 43
      occupancy: 0.72
      sensor_quality: valid
  outdoor:
    temperature: 16.1
    humidity: 42
  hvac:
    heating_status: on
    supply_temp: 45
  energy:
    price_eur_kwh: 0.18
```

### 27.2 ControlAction

```yaml
ControlAction:
  id: action_001
  type: setpoint_update
  target: zone:aula_3b
  value:
    heating_setpoint: 21.5
  duration: 2h
```

### 27.3 ControlObjective

```yaml
ControlObjective:
  comfort_weight: 0.55
  energy_weight: 0.25
  cost_weight: 0.15
  carbon_weight: 0.05
```

### 27.4 Recommendation

```yaml
Recommendation:
  id: rec_001
  action_id: action_001
  expected_effect:
    energy_saving_kwh: 4.2
    comfort_risk: low
    predicted_temp_min: 20.8
  confidence: 0.82
  mode: shadow
  approval_required: true
```

### 27.5 SafetyDecision

```yaml
SafetyDecision:
  recommendation_id: rec_001
  status: allowed_for_shadow
  blocked_for_direct_control: true
  reasons:
    - supervised_control_not_enabled
    - model_not_approved_for_control
```

---

## 28. Control readiness gates

### 28.1 Prediction-ready

```text
surrogate validado;
FeatureSchema estable;
sensores suficientes;
confidence score disponible;
inputs sin datos críticos stale.
```

### 28.2 Recommendation-ready

```text
objetivos definidos;
constraints definidos;
safety layer activa;
explicación generada;
recomendación trazable.
```

### 28.3 Shadow-ready

```text
logging completo;
comparación posterior;
no escritura en BMS;
monitorización;
counterfactual evaluation.
```

### 28.4 Supervised-control-ready

```text
BMS gateway validado;
aprobación humana;
rollback;
DSX/NetworkSim o prueba local;
control limitado por zona/acción;
ack/nack handling;
permisos.
```

### 28.5 Limited-auto-ready

```text
histórico shadow positivo;
policy estable;
safety monitor;
fallos probados;
SLA operacional;
permisos;
auditoría;
rollback validado.
```

---

## 29. Relación con DSX Ecosystem

DSX MaxLPS / Max-Q inspira:

```text
maximizar confort útil por kWh;
maximizar bienestar por coste;
minimizar emisiones manteniendo servicio.
```

DSX Flex inspira:

```text
señales de red;
tarifas dinámicas;
demand response;
fotovoltaica;
baterías;
cargadores EV.
```

DSX Air / NetworkSim valida:

```text
latencia sensor → inferencia;
fallos de gateway;
BMS ack/nack;
robustez de shadow mode;
bloqueo ante datos stale.
```

Conclusión:

```text
EnergyPlus valida física.
Surrogates permiten inferencia.
Control decide acciones.
DSX/NetworkSim valida operación bajo fallos.
```

---

## 30. Relación con agentes

Un **Control Agent** puede:

```text
analizar recomendaciones;
comparar estrategias;
crear OptimizationJob;
resumir trade-offs;
detectar riesgos;
crear tareas;
generar reportes;
proponer shadow mode;
explicar por qué se bloqueó una acción;
comparar reglas, MPC y RL.
```

No puede:

```text
activar control automático;
saltarse safety layer;
aprobar política RL;
enviar comandos BMS sin permiso;
ignorar sensores stale;
modificar constraints críticas;
cambiar permisos.
```

Patrón:

```text
Agent proposes.
Optimizer evaluates.
Safety filters.
Human approves.
Backend executes.
```

---

## 31. Relación con Omniverse Kit

Omniverse Kit debe mostrar:

```text
acción recomendada;
zona afectada;
horizonte;
impacto esperado;
riesgo;
confianza;
por qué se recomienda;
por qué se bloquea;
modo actual;
shadow log;
comparación posterior;
approval status.
```

Visualizaciones:

```text
heatmap de riesgo;
trayectoria prevista de temperatura;
zonas bajo recomendación;
acciones bloqueadas;
timeline de decisiones;
panel de control readiness.
```

---

## 32. Relación con Nucleus / OpenUSD

Nucleus puede almacenar capas visuales:

```text
control_recommendations.usd;
shadow_mode_annotations.usd;
blocked_actions.usd;
comfort_risk_map.usd;
control_readiness_layer.usd.
```

Pero no debe almacenar:

```text
políticas RL completas;
logs masivos;
series temporales completas;
credenciales BMS;
comandos operativos como fuente única.
```

Backend gobierna. Nucleus visualiza y colabora.

---

## 33. MVP recomendado

No empezar con PPO.

### 33.1 Objetivo MVP

Generar recomendaciones seguras de operación sobre una zona usando surrogate + reglas + optimización simple.

### 33.2 Alcance MVP

```text
1 edificio;
1 zona tipo;
surrogate validado para temperatura;
acciones discretas simples:
  - mantener
  - bajar setpoint
  - subir setpoint
  - adelantar apagado
  - ventilar/no ventilar
horizonte 30-60 min;
restricciones básicas de confort;
recommendation report;
shadow mode sin control real;
visualización en Omniverse.
```

### 33.3 Fuera del MVP

```text
PPO;
Recurrent PPO;
control real;
cuOpt;
BMS real;
multiobjetivo avanzado;
MILP complejo;
demand response;
baterías;
multi-edificio.
```

### 33.4 Resultado esperado

```text
Siamese recomienda acciones,
explica por qué,
estima impacto,
las registra en shadow mode
y compara después contra la realidad.
```

---

## 34. Evolución por fases

### Fase 1 — Rule-based recommendations

```text
reglas claras;
safety layer;
explicación;
shadow logging.
```

### Fase 2 — Heuristic optimization

```text
comparar acciones candidatas;
usar surrogate para rollout;
elegir mejor acción.
```

### Fase 3 — MPC con RC/surrogate

```text
horizonte predictivo;
restricciones;
optimización continua.
```

### Fase 4 — Multiobjective / Pareto

```text
confort vs energía;
coste vs emisiones;
riesgo vs ahorro.
```

### Fase 5 — cuOpt / GPU optimization

```text
MILP/QP grande;
multi-zona;
tarifas;
baterías;
demand response.
```

### Fase 6 — PPO offline

```text
entorno simulado;
surrogate como environment;
evaluación contra MPC/reglas.
```

### Fase 7 — Recurrent PPO

```text
memoria temporal;
parcial observabilidad;
fallos de sensores;
operación compleja.
```

### Fase 8 — Shadow RL

```text
RL recomienda sin actuar;
comparación con realidad;
safety report.
```

### Fase 9 — Supervised control

```text
humano aprueba;
BMS simulado primero;
BMS real después.
```

### Fase 10 — Limited auto-control

```text
acciones acotadas;
rollback;
monitorización continua;
solo tras evidencia suficiente.
```

---

## 35. Primeros tickets recomendados

### CTRL-00 — Control module context

Crear documentación conceptual del módulo.

### CTRL-01 — Control contracts

Definir `ControlState`, `ControlAction`, `ControlObjective`, `Recommendation`, `SafetyDecision`.

### CTRL-02 — Rule-based recommendation MVP

Implementar primeras reglas explicables.

### CTRL-03 — Safety layer MVP

Bloquear acciones por sensor stale, baja confianza y límites de confort.

### CTRL-04 — Candidate action generator

Generar acciones discretas simples.

### CTRL-05 — Surrogate rollout evaluator

Evaluar acciones usando predicción surrogate.

### CTRL-06 — Recommendation report

Crear reporte con impacto, riesgo, confianza y explicación.

### CTRL-07 — Shadow mode logger

Registrar acciones recomendadas pero no aplicadas.

### CTRL-08 — Counterfactual evaluation

Comparar recomendación shadow con evolución real.

### CTRL-09 — MPC research note

Diseñar formulación inicial MPC con RC/surrogate.

### CTRL-10 — RL environment design

Diseñar `SiameseControlEnv`.

### CTRL-11 — PPO offline spike

Entrenar PPO en entorno simulado, sin operación real.

### CTRL-12 — Recurrent PPO research

Evaluar necesidad de memoria temporal.

### CTRL-13 — cuOpt feasibility

Evaluar cuOpt para horarios/setpoints/MILP.

### CTRL-14 — Control readiness gates

Definir gates de prediction, recommendation, shadow, supervised y limited-auto.

### CTRL-15 — Omniverse control panel

Visualizar recomendaciones y estados de seguridad.

---

## 36. Riesgos principales

### Riesgo 1 — Control prematuro

Mitigación:

```text
recommendation first;
shadow mode;
approval gates;
no direct HVAC control.
```

### Riesgo 2 — PPO antes de tiempo

Mitigación:

```text
rules → MPC → RL offline → shadow RL.
```

### Riesgo 3 — Surrogate explotado por el optimizador

Mitigación:

```text
constraints;
EnergyPlus validation;
out-of-distribution detection;
safety layer.
```

### Riesgo 4 — Recomendaciones poco explicables

Mitigación:

```text
RecommendationReport;
trade-off summary;
human-readable reasons.
```

### Riesgo 5 — Datos malos

Mitigación:

```text
sensor quality flags;
confidence score;
blocking rules.
```

### Riesgo 6 — BMS/Red no fiable

Mitigación:

```text
DSX/NetworkSim;
ack/nack handling;
fallback;
rollback.
```

### Riesgo 7 — Dependencia GPU/NVIDIA

Mitigación:

```text
CPU fallback;
abstract OptimizationBackend;
cuOpt optional;
ONNX portable.
```

---

## 37. Valor comercial

No vender como:

```text
IA autónoma para controlar edificios.
```

Vender como:

```text
Siamese convierte predicciones físicas en recomendaciones operativas seguras.
```

Valor para clientes:

```text
menos consumo;
menos sobrecalentamiento;
mejor confort;
menos decisiones manuales;
menos dependencia de intuición;
mejor trazabilidad;
shadow mode antes de riesgo;
control supervisado gradual;
justificación de acciones.
```

Frase comercial:

> **Antes de actuar sobre el edificio, Siamese simula, predice, compara y justifica cada decisión.**

---

## 38. Frases de presentación

Frase principal:

> **El control de Siamese no empieza actuando. Empieza demostrando qué habría hecho.**

Frase técnica:

> **Siamese combina surrogates, MPC, optimización clásica y, en fases avanzadas, PPO/Recurrent PPO, siempre bajo restricciones físicas, safety layer, aprobación humana y shadow mode.**

Frase comercial:

> **Predice primero. Recomienda después. Actúa solo cuando hay evidencia.**

Frase estratégica:

> **La IA no gobierna el edificio. Siamese gobierna la IA.**

---

## 39. Decisión arquitectónica final

La decisión central:

```text
El módulo de control debe ser ambicioso,
pero escalonado y gobernado.
```

Arquitectura recomendada:

```text
Rule-based
→ Heuristic
→ MPC
→ Multiobjective optimization
→ GPU acceleration
→ PPO
→ Recurrent PPO
→ Safe supervised control
```

No:

```text
PPO desde el día uno.
```

Decisión clave:

> **PPO y Recurrent PPO son herramientas futuras para políticas avanzadas; el núcleo inicial debe ser MPC, reglas, constraints, shadow mode y explicabilidad.**

---

## 40. Relación con documentos previos

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

siamese_surrogate_models_context.md
→ modelos rápidos para predicción operativa.

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
Siamese Flex;
Demand Response;
BMS Gateway;
Shadow Mode;
Supervised Control;
RL Policy Registry;
cuOpt integration;
Control Readiness Gates;
Agentic Control Workflows.
```
