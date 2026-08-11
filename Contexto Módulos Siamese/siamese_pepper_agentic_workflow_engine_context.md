# Siamese — Módulo Agentic Workflow Engine / Pepper

**Documento:** Contexto técnico y estratégico del módulo Agentic Workflow Engine / Pepper dentro de Siamese  
**Proyecto:** Siamese — plataforma agéntica de gemelos digitales energéticos  
**Estado:** Documento de arquitectura conceptual previo a implementación  
**Versión:** 0.1  
**Propósito:** definir cómo Pepper actuará como infraestructura agéntica horizontal de Siamese, conectando todos los módulos, aceptando entradas humanas bidireccionales, generando workflows, recomendaciones, acciones, tareas, evidencias, aprobaciones y control gobernado sobre un ecosistema energético vivo e inmersivo.

---

## 1. Resumen ejecutivo

**Pepper** es el **Agentic Workflow Engine** de Siamese.

No es solo un chat.  
No es solo un kanban.  
No es solo una capa de automatización.  
No es solo un asistente IA.

Pepper es la infraestructura horizontal que conecta todos los módulos de Siamese y permite que humanos y agentes colaboren sobre un gemelo energético vivo.

La frase central del módulo es:

> **Pepper convierte Siamese en un ecosistema vivo de trabajo energético.**

Pepper conecta:

```text
EnergyPlus
Backend Python
Omniverse Kit
Nucleus
Sensórica
Calibración
Adoption Model
Dataset Factory
Surrogate Models
Optimización y Control
DSX / NetworkSim
BMS / HVAC
Informes humanos
Tareas
Aprobaciones
Evidencias
Reglas operativas
```

Su función es convertir capacidades técnicas en workflows gobernados:

```text
módulos técnicos
→ tools gobernadas
→ agentes especializados
→ tareas
→ recomendaciones
→ evidencias
→ aprobación
→ acción / shadow mode / informe
```

Decisión central:

> **Pepper debe poder leer todo lo necesario, editar solo lo permitido, ejecutar solo mediante tools gobernadas y promocionar cambios solo con evidencia y aprobación.**

---

## 2. Qué es Pepper dentro de Siamese

Pepper es el motor agéntico y de workflows de Siamese.

Opera como sistema nervioso del producto:

```text
Siamese tiene módulos técnicos.
Pepper convierte esos módulos en trabajo coordinado.
```

Pepper permite que modelos, sensores, simulaciones, calibraciones, datasets, surrogates, optimizaciones, recomendaciones, tareas, aprobaciones, informes, decisiones humanas, restricciones, evidencias y reglas operativas estén conectados mediante workflows auditables.

Frase conceptual:

> **Pepper es el sistema nervioso operativo de Siamese.**

---

## 3. Relación con Hermes

Pepper se construye a partir de la estructura personalizada derivada de **Hermes**.

Hermes aporta la base conceptual y operativa de:

```text
workflows;
approvals;
execution inspector;
agent orchestration;
task coordination;
controlled runtime;
governance;
evidence;
tool execution boundaries.
```

Pepper es la evolución orientada a Siamese.

Evolución prevista:

```text
Fase 1
Pepper externo
→ se usa para construir Siamese.

Fase 2
Pepper compatible
→ Siamese expone tools, contracts, jobs y módulos accesibles.

Fase 3
Pepper embebido
→ Siamese integra kanban, roadmaps, approvals, agents, evidence, execution inspector.

Fase 4
Pepper nativo
→ Siamese es una plataforma agéntica energética completa.
```

Regla:

```text
No meter todo Pepper dentro de Siamese desde el día uno.
Sí diseñar Siamese para que Pepper pueda integrarse sin romper arquitectura.
```

---

## 4. Qué problema resuelve

Sin Pepper, Siamese tendría módulos potentes pero relativamente aislados:

```text
EnergyPlus ejecuta simulaciones.
Sensórica ingiere datos.
Calibración ajusta modelos.
Surrogates predicen.
Control recomienda acciones.
Omniverse visualiza.
Nucleus colabora.
```

Pero el producto necesita coordinar preguntas como:

```text
¿Qué falta para calibrar este edificio?
¿Qué sensor impide pasar a shadow mode?
¿Qué modelo surrogate está aprobado?
¿Qué recomendación puede ejecutarse?
¿Qué informe humano cambia los horarios de ocupación?
¿Qué tarea debe crear el agente?
¿Qué módulo tiene autoridad sobre este dato?
¿Qué puede editarse y qué solo puede leerse?
¿Qué evidencia justifica esta acción?
¿Qué decisión humana cambió una constraint?
```

Pepper resuelve esto creando una capa común de workflows, tareas, agentes, tools, políticas, aprobaciones, evidencia, memoria operativa, human input y action governance.

---

## 5. Pepper no es solo IA hacia el humano

Pepper no debe funcionar solo así:

```text
Siamese analiza
→ agente recomienda al humano
```

Debe funcionar también así:

```text
humano informa
→ agente interpreta
→ sistema actualiza contexto operativo
→ workflows se ajustan
```

La interacción debe ser bidireccional.

### 5.1 Del sistema hacia el humano

Ejemplos:

```text
“El sensor del aula 3B lleva 45 minutos sin datos.”
“El surrogate no puede usarse para control porque no supera el rollout de 60 min.”
“Hay riesgo de sobrecalentamiento a las 11:30.”
“Recomiendo adelantar el apagado de calefacción 30 minutos.”
“El modelo adoptado desde DesignBuilder no tiene materiales suficientes.”
“El control está bloqueado porque el sensor principal está stale.”
```

Pepper debe entregar recomendación, razón, evidencia, impacto esperado, riesgo, confianza, estado de aprobación y siguiente acción.

### 5.2 Del humano hacia el sistema

Ejemplos:

```text
“Hoy el aula 3B estará vacía de 11:00 a 13:00.”
“Esta semana hay exámenes y no queremos cambios de temperatura agresivos.”
“Los profesores suelen abrir ventanas después del recreo.”
“La calefacción no debe apagarse antes de las 15:00.”
“El viernes hay jornada reducida.”
“Ferrovial recomienda no tocar la bomba sin revisión.”
“El cliente prefiere mantener 22 ºC aunque el consumo suba.”
“Se ha cambiado un sensor de posición.”
“Los viernes por la tarde hay actividades extraescolares en la segunda planta.”
```

Pepper debe convertir estos inputs en entidades operativas:

```text
HumanObservation;
OccupancyOverride;
ScheduleChange;
HVACUsageRule;
OperationalConstraint;
MaintenanceNote;
BuildingPolicy;
Task;
Approval;
Exception;
Evidence;
ModelUpdateProposal.
```

Esto convierte al humano en fuente estructurada de conocimiento operativo.

---

## 6. El humano como fuente de datos

En Siamese, el humano no es solo usuario final.

También es fuente de observaciones, normas de uso, horarios especiales, restricciones, prioridades, incidencias, informes técnicos, decisiones, aprobaciones, rechazos, preferencias de confort, cambios de ocupación, mantenimiento y experiencia del edificio.

Ejemplo:

```text
Facility manager:
“El aula 4A suele tener más ocupación real los martes por la tarde.”

Pepper:
→ crea HumanObservation
→ propone actualizar OccupancyProfile
→ marca que requiere validación
→ recalcula predicción de surrogate
→ genera tarea de revisión de horario
```

Otro ejemplo:

```text
Ingeniero:
“No usar ventilación natural en días de lluvia.”

Pepper:
→ crea OperationalRule
→ aplica constraint al módulo de control
→ bloquea recomendaciones de ventilación natural si weather.rain = true
```

Esto es crítico porque muchos detalles reales de operación no vendrán de sensores ni de EnergyPlus. Vendrán de personas.

---

## 7. Arquitectura general

```text
                 ┌────────────────────────────┐
                 │          Human UI           │
                 │  chat / kanban / approvals  │
                 └─────────────▲──────────────┘
                               │
                               │ bidirectional input/output
                               │
┌──────────────────────────────┴──────────────────────────────┐
│                         Pepper Engine                         │
│                                                               │
│  Agents / Workflows / Roadmaps / Tasks / Evidence / Policies │
│                                                               │
│  Tool Registry │ Policy Engine │ Approval Gates │ Memory      │
└───────────────▲───────────────▲───────────────▲──────────────┘
                │               │               │
                │ governed tool calls            │ contextual evidence
                │               │               │
┌───────────────┴───────────────┴───────────────┴──────────────┐
│                       Siamese Modules                         │
│                                                               │
│ EnergyPlus │ Sensors │ Calibration │ Datasets │ Surrogates    │
│ Control    │ Nucleus │ Omniverse   │ Adoption │ DSX/NetworkSim│
└───────────────────────────────────────────────────────────────┘
```

Pepper no sustituye a los módulos. Los orquesta.

---

## 8. Pepper como sistema operativo de workflows

Pepper debe transformar trabajo complejo en:

```text
Macroproject
→ Project
→ Task
→ Tool call
→ Evidence
→ Review
→ Approval
→ Promotion
```

Aplicado al dominio energético:

```text
Macroproyecto:
Crear gemelo energético del Hospital X

Proyecto:
Adoptar modelo Revit

Tareas:
1. Importar Revit vía Nucleus.
2. Validar geometría.
3. Extraer spaces.
4. Crear thermal zones.
5. Generar Model Quality Report.
6. Crear EnergyModel.
7. Ejecutar EnergyPlus smoke test.
8. Proponer sensores necesarios.
9. Crear roadmap de calibración.
```

---

## 9. Entidades principales

Pepper necesita contratos propios.

Entidades:

```text
WorkUnit;
Roadmap;
Project;
Task;
HumanObservation;
OperationalRule;
Recommendation;
Approval;
Evidence;
AgentEvent;
ToolCall;
PolicyDecision;
MemoryItem;
Exception;
PromotionRequest;
ExecutionTrace.
```

### 9.1 WorkUnit

Entidad genérica de trabajo.

```yaml
WorkUnit:
  id: work_001
  type: task
  title: Revisar sensor Aula 3B
  status: open
  priority: medium
  related_entity:
    type: sensor
    id: sensor_aula_3b_temp_01
  created_by: agent:sensor_agent
  requires_approval: false
```

Estados posibles:

```text
open;
in_progress;
blocked;
waiting_approval;
approved;
rejected;
completed;
cancelled;
archived.
```

### 9.2 Roadmap

```yaml
Roadmap:
  id: roadmap_calibration_building_001
  title: Calibración multizona del edificio
  status: in_progress
  projects:
    - sensor_audit
    - model_quality_review
    - calibration_job
    - validation_report
```

Uso:

```text
adopción de edificio;
calibración;
sensor deployment;
dataset generation;
surrogate training;
shadow mode;
control readiness;
BMS integration.
```

### 9.3 HumanObservation

```yaml
HumanObservation:
  id: obs_001
  source: facility_manager
  content: El aula 3B estará vacía de 11:00 a 13:00.
  affected_entities:
    - zone:aula_3b
  validity:
    start: 2026-07-24T11:00:00
    end: 2026-07-24T13:00:00
  status: pending_interpretation
```

Estados:

```text
pending_interpretation;
classified;
linked;
converted_to_rule;
converted_to_task;
rejected;
expired.
```

### 9.4 OperationalRule

```yaml
OperationalRule:
  id: rule_001
  title: No ventilar en días de lluvia
  scope:
    building_id: building_001
  condition:
    weather.rain: true
  action_constraint:
    block: natural_ventilation_recommendation
  authority: human_policy
  approved_by: facility_manager
```

Tipos:

```text
comfort_rule;
hvac_rule;
maintenance_rule;
schedule_rule;
safety_rule;
client_preference;
temporary_exception;
energy_policy.
```

### 9.5 Recommendation

```yaml
Recommendation:
  id: rec_001
  source_module: optimization_control
  proposed_by: control_agent
  action: lower_heating_setpoint
  target: zone:aula_3b
  expected_effect:
    energy_saving_kwh: 4.2
    comfort_risk: low
  status: pending_review
```

Estados:

```text
draft;
pending_review;
allowed_for_shadow;
blocked;
approved;
rejected;
executed;
expired;
superseded.
```

### 9.6 Approval

```yaml
Approval:
  id: approval_001
  target_type: recommendation
  target_id: rec_001
  status: approved
  approved_by: facility_manager
  timestamp: 2026-07-24T10:30:00
```

Estados:

```text
pending_review;
approved;
rejected;
needs_revision;
expired;
auto_blocked.
```

### 9.7 Evidence

```yaml
Evidence:
  id: evidence_001
  type: simulation_result
  source_module: energyplus
  linked_to:
    - recommendation:rec_001
  summary: La simulación predice confort mantenido con menor consumo.
  raw_access_policy: restricted
```

Tipos:

```text
simulation_result;
sensor_data_quality_report;
calibration_report;
surrogate_validation_report;
control_shadow_report;
human_observation;
operational_rule;
network_simulation_report;
model_quality_report;
approval_decision;
agent_reasoning_summary;
external_document;
nucleus_layer_reference.
```

---

## 10. Tipos de agentes

Pepper no debe tener un único agente genérico. Debe tener agentes especializados.

Agentes principales:

```text
Energy Model Agent;
Sensor Agent;
Calibration Agent;
Dataset Agent;
Surrogate Agent;
Control Agent;
Adoption Agent;
Nucleus / Collaboration Agent;
DSX / Network Agent;
Documentation / Reporting Agent;
QA / Validation Agent;
Security / Policy Agent.
```

---

## 11. Agentes especializados

### 11.1 Energy Model Agent

Opera sobre:

```text
EnergyModel;
IDF/epJSON;
SimulationCase;
EnergyPlus diagnostics;
Model Quality Report.
```

Puede:

```text
detectar problemas de modelo;
proponer reparaciones;
crear tareas de modelado;
explicar warnings de EnergyPlus;
solicitar simulaciones.
```

No puede editar modelo calibrado final sin aprobación, promocionar cambios críticos, ignorar errores severos ni modificar IDF directamente fuera del backend.

### 11.2 Sensor Agent

Opera sobre sensores, quality flags, sensor health, coverage, bindings, CSV/MQTT/BMS y Feature Builder.

Puede detectar sensores fallidos, proponer nuevos sensores, crear tareas de revisión, bloquear calibración si faltan datos y explicar calidad de datos.

No puede falsear readings, sobrescribir raw data ni marcar estimaciones como medidas reales.

### 11.3 Calibration Agent

Opera sobre CalibrationJob, parámetros, métricas, Pareto front, candidate models y validation report.

Puede proponer variables calibrables, seleccionar periodos candidatos, resumir resultados, detectar overfitting y proponer aprobación.

No puede aprobar modelo calibrado final sin humano ni cambiar criterios de aceptación sin approval.

### 11.4 Dataset Agent

Opera sobre DatasetCampaign, sampling, features, targets, quality report, manifest y splits.

Puede crear campañas, detectar huecos, validar splits, generar dataset report y proponer nueva campaña.

No puede entrenar modelos con dataset sin manifest ni mezclar datos de clientes sin política explícita.

### 11.5 Surrogate Agent

Opera sobre training jobs, model registry, validation reports, drift, inference status y PredictionResult.

Puede comparar modelos, proponer retraining, explicar baja confianza, crear model cards y detectar drift.

No puede aprobar modelo para control sin approval, ignorar validation failure ni desplegar modelo operativo sin gate.

### 11.6 Control Agent

Opera sobre recommendations, shadow mode, MPC, PPO/Recurrent PPO, safety decisions y control readiness.

Puede proponer acciones, comparar estrategias, explicar trade-offs, crear shadow logs, detectar bloqueo por seguridad y solicitar approval.

No puede enviar comandos HVAC sin permisos, activar control automático, saltarse safety layer ni promocionar política RL.

### 11.7 Adoption Agent

Opera sobre IDF, epJSON, DesignBuilder, OpenStudio, Revit, IFC, USD, CSV y Model Quality Report.

Puede importar activos, generar quality report, crear roadmap de adopción, proponer tareas de reparación e identificar formato.

No puede declarar modelo simulation-ready sin validación ni promocionar importación como modelo final sin review.

### 11.8 Nucleus / Collaboration Agent

Opera sobre Nucleus, USD layers, permissions, connectors, annotations y proposal layers.

Puede listar capas, detectar conflictos, crear propuesta en agent layer, avisar de permisos incorrectos y vincular evidencia visual.

No puede cambiar ACLs críticas sin admin, sobrescribir source layers ni promocionar proposal layers sin approval.

### 11.9 DSX / Network Agent

Opera sobre DSX Air, NetworkSim, MQTT, gateways, latency y BMS ack/nack.

Puede crear escenarios de fallo, validar shadow mode, bloquear control si la red no es fiable y generar network readiness report.

### 11.10 Documentation / Reporting Agent

Opera sobre informes, presentaciones, model cards, calibration reports, client summaries y control reports.

Puede generar informe ejecutivo, resumir evidencia, crear documentación técnica y preparar entregables.

Debe respetar confidencialidad, raw data restrictions, customer boundaries y source code privacy.

---

## 12. Tool Registry

Pepper necesita un registro de herramientas gobernadas.

Los agentes no deben manipular módulos directamente.

Patrón:

```text
Agent intent
→ Tool Registry
→ Policy Engine
→ Tool execution
→ Evidence
→ Result
```

Ejemplos de tools:

```text
CreateSimulationCase;
RunEnergyPlusSimulation;
GetSimulationDiagnostics;
CreateCalibrationJob;
GetCalibrationReport;
CreateDatasetCampaign;
TrainSurrogateModel;
GetSurrogatePrediction;
CreateRecommendation;
RunShadowModeEvaluation;
CreateSensorBinding;
ImportIDF;
ImportRevitStage;
WriteNucleusAnnotation;
CreateWorkTask;
RequestApproval;
GenerateReport.
```

Cada tool debe tener input schema, output schema, permissions, allowed roles, side effects, evidence policy, approval requirement, rollback if applicable y confidentiality level.

---

## 13. Policy Engine

El Policy Engine decide qué puede hacer cada agente.

Evalúa:

```text
quién llama;
qué entidad toca;
qué módulo afecta;
si modifica estado;
si requiere aprobación;
si hay datos confidenciales;
si la acción es reversible;
si el sistema está en modo analysis/recommendation/shadow/control;
qué evidencia existe;
qué permisos tiene el usuario/agente.
```

Ejemplo:

```text
Control Agent pide enviar setpoint a BMS.

Policy Engine:
- ¿control supervisado habilitado? no
- ¿approval humano existe? no
- ¿surrogate aprobado para control? no

Resultado:
blocked
```

Otro ejemplo:

```text
Sensor Agent quiere crear tarea de revisar sensor.

Policy Engine:
- no modifica datos críticos
- no actúa sobre BMS
- task creation permitted

Resultado:
allowed
```

---

## 14. Approval Gates

Pepper debe tener puertas de aprobación explícitas.

Acciones que requieren aprobación:

```text
aprobar modelo calibrado;
aprobar dataset para training;
aprobar surrogate para shadow mode;
aprobar surrogate para control;
cambiar operational rules;
enviar comando BMS;
promocionar agent proposal layer;
modificar geometry/energy source layers;
compartir informe externo;
exportar datos de cliente;
cambiar permisos;
activar control supervisado;
activar limited auto-control.
```

Un Approval Gate debe guardar quién lo solicitó, qué evidencia aportó, qué decisión se tomó, quién aprobó, cuándo, qué consecuencias tiene y qué versión del estado fue aprobada.

---

## 15. Evidence Registry

Pepper debe guardar evidencia de cada decisión.

Tipos:

```text
simulation result;
sensor data quality report;
calibration report;
surrogate validation report;
control shadow report;
human observation;
operational rule;
network simulation report;
model quality report;
approval decision;
agent reasoning summary;
external document;
Nucleus layer reference.
```

Niveles de acceso:

```text
public_summary;
technical_summary;
restricted_raw;
confidential;
source_code_private;
credentials_forbidden.
```

Ejemplo:

```yaml
EvidenceAccessPolicy:
  evidence_id: evidence_001
  summary_access: all_project_members
  technical_access: engineers
  raw_access: backend_service_only
  confidential: true
```

---

## 16. Acceso total no significa edición total

Los agentes deben poder acceder a todos los detalles necesarios del ecosistema, pero no deben poder modificarlo todo.

Modelo:

```text
Read access
→ amplio, pero gobernado.

Write access
→ limitado por módulo, rol, fase y aprobación.

Execute access
→ solo mediante tools.

Promote access
→ solo con approval.
```

Ejemplo:

```text
Agente puede leer:
- estado de sensores;
- diagnóstico de EnergyPlus;
- resultado de calibración;
- validación surrogate;
- recomendación de control;
- tareas;
- reglas operativas;
- summaries de evidencia.

Agente no puede editar:
- datos raw;
- modelo calibrado aprobado;
- reglas de seguridad;
- permisos;
- credenciales;
- código fuente confidencial;
- datos de otros clientes.
```

---

## 17. Confidencialidad y seguridad

Pepper debe definir qué no se expone.

### 17.1 Código fuente

Niveles:

```text
source_code_private;
source_code_summary;
api_contracts;
tool_contracts;
module_docs;
runtime_state.
```

Para un agente operativo de edificio normalmente basta:

```text
tool contracts;
module capabilities;
runtime state;
evidence summaries;
allowed actions.
```

No necesita:

```text
código fuente interno;
secrets;
licencias privadas;
credenciales;
implementaciones propietarias;
datos de otros clientes.
```

### 17.2 Datos de cliente

Proteger:

```text
ocupación;
horarios;
consumo;
planos;
BMS;
sensores;
informes;
costes;
recomendaciones;
incidencias;
contratos;
permisos.
```

### 17.3 Credenciales

Prohibido exponer:

```text
tokens;
API keys;
passwords;
BMS credentials;
Nucleus admin tokens;
MQTT credentials;
cloud credentials.
```

Los agentes deben pedir acciones mediante tools. No deben recibir secretos.

---

## 18. Context Engine

Pepper necesita un motor de contexto.

Debe ensamblar información relevante según la tarea:

```text
selected building;
selected floor;
selected zone;
selected sensor;
active simulation;
latest calibration;
surrogate status;
control mode;
human rules;
current tasks;
permissions;
evidence;
recent changes;
network state;
approval state.
```

Ejemplo:

```text
Usuario selecciona Aula 3B y pregunta:
“¿Por qué se va a sobrecalentar?”

Context Engine reúne:
- geometría/zona;
- sensores Aula 3B;
- predicción surrogate;
- simulación EnergyPlus;
- ocupación prevista;
- horarios HVAC;
- reglas humanas;
- recomendaciones previas;
- safety decision.
```

---

## 19. Memory / Knowledge Layer

Pepper necesita memoria gobernada.

Tipos:

```text
project memory;
building memory;
zone memory;
sensor memory;
model memory;
client preferences;
operational rules;
historical incidents;
approved decisions;
rejected decisions;
lessons learned.
```

Ejemplo:

```text
“En este edificio no se recomienda ventilación natural en días de lluvia.”
```

Eso debe convertirse en regla operativa, no quedarse como nota suelta.

---

## 20. Knowledge Graph / Graphify / G-Brain

A futuro, Pepper debería apoyarse en una capa de grafo para relaciones.

Ejemplo de grafo:

```text
Building contains Floor
Floor contains Zone
Zone has Sensor
Zone has ThermalSurface
Sensor measures Variable
SimulationRun uses EnergyModel
CalibrationJob produces CalibratedModel
SurrogateModel trained_on Dataset
Recommendation based_on Prediction
Approval approves Recommendation
OperationalRule constrains ControlAction
```

Esto permite que los agentes naveguen el sistema sin búsquedas frágiles.

Uso:

```text
localizar dependencias;
explicar impacto de cambios;
detectar qué módulos se ven afectados;
ensamblar contexto;
validar readiness;
hacer auditoría.
```

---

## 21. Relación con Omniverse Kit

Pepper debe integrarse en Kit como experiencia nativa.

Componentes UI:

```text
Agent Chat;
Roadmap Panel;
Kanban Board;
Approval Inbox;
Execution Inspector;
Tool Inspector;
Evidence Viewer;
Recommendation Panel;
Human Report Input;
Operational Rules Panel;
Model Status Panel.
```

Debe ser contextual:

```text
Seleccionas Aula 3B
→ Pepper muestra tareas, sensores, predicciones, recomendaciones, reglas y evidencias de esa zona.

Seleccionas un sensor
→ Pepper muestra estado, histórico, calidad, tareas, calibraciones afectadas.

Seleccionas una recomendación
→ Pepper muestra surrogate, safety decision, expected effect, approval status.
```

---

## 22. Relación con Nucleus

Pepper debe trabajar con Nucleus mediante capas de propuesta.

Patrón:

```text
Agent writes proposal layer
→ human reviews
→ approval gate
→ backend promotes
```

Ejemplo:

```text
Agent crea:
10_agent_annotations.usd

Propone:
“Este sensor debería vincularse a Aula 3B.”

Humano aprueba.
Backend actualiza:
04_sensor_bindings.usd
```

Los agentes no deben sobrescribir capas fuente.

---

## 23. Relación con EnergyPlus

Pepper no debe compilar ni editar EnergyPlus directamente.

Debe llamar tools:

```text
CreateSimulationCase;
ValidateEnergyModel;
RunEnergyPlusSimulation;
GetSimulationDiagnostics;
CompareSimulationResults.
```

Incorrecto:

```text
agente abre IDF;
agente edita líneas;
agente ejecuta EnergyPlus por su cuenta.
```

Correcto:

```text
agente pide SimulationCase;
backend valida;
runner ejecuta;
results normalizer procesa;
evidence registry guarda.
```

---

## 24. Relaciones con módulos funcionales

### Sensórica

Pepper puede consultar estado de sensores, detectar fallos, crear tareas de revisión, proponer sensor bindings, bloquear workflows por datos insuficientes y aceptar observaciones humanas sobre sensores.

No puede modificar datos raw, inventar readings ni marcar estimaciones como mediciones reales.

### Calibración

Pepper orquesta calibration roadmap, calibration jobs, parameter review, metric review, candidate comparison y approval of calibrated model.

No puede aprobar modelo calibrado final sin gate, ignorar métricas fuera de rango ni ocultar incertidumbre.

### Dataset Factory

Pepper orquesta dataset campaign, sampling review, feature/target selection, quality report y dataset approval for training.

Regla:

```text
No DatasetManifest
→ no surrogate training.
```

### Surrogate Models

Pepper puede consultar predicción, comparar modelos, detectar drift, crear retraining task, solicitar ValidationReport, explicar incertidumbre y pedir approval para shadow mode.

No puede promover surrogate a shadow mode sin approval, promover surrogate a control sin approval ni ignorar validation failure.

### Optimización y Control

Pepper convierte una recomendación de control en workflow.

Flujo:

```text
Control Module genera Recommendation
→ Pepper recibe Recommendation
→ Policy Engine evalúa modo
→ Evidence Registry vincula predicción/safety
→ Approval Gate si aplica
→ UI muestra al humano
→ humano aprueba/rechaza/comenta
→ Pepper actualiza estado
→ backend ejecuta si permitido
```

También procesa entradas humanas:

```text
Humano:
“Hoy no aplicar recomendaciones de apagado temprano.”

Pepper:
→ crea OperationalRule temporal
→ Control Module recibe constraint
→ recomendaciones se recalculan o bloquean
```

---

## 25. Relación con informes humanos

Pepper debe aceptar informes humanos estructurados o semiestructurados.

Ejemplos:

```text
informe de uso HVAC;
informe de ventilación;
reporte de mantenimiento;
cambio de horarios;
observación de ocupación;
normas del edificio;
preferencias del cliente;
incidencia técnica;
comentario del profesor;
nota del facility manager.
```

El sistema debe convertirlos en:

```text
HumanObservation;
OperationalRule;
ScheduleOverride;
MaintenanceEvent;
Constraint;
Task;
Approval;
Evidence;
ModelUpdateProposal.
```

Ejemplo:

```text
Informe humano:
“Durante enero, las aulas de la segunda planta se usan también de 17:00 a 19:00 para actividades extraescolares.”

Pepper:
→ crea ScheduleOverride
→ marca periodo de validez
→ actualiza OccupancyProfile candidate
→ pide aprobación
→ recalcula predicciones
→ genera tarea de validar sensores.
```

---

## 26. Human-in-the-loop real

Human-in-the-loop no significa solo aprobar un botón.

Significa:

```text
humano enseña al sistema;
humano corrige al sistema;
humano aporta contexto;
humano aprueba;
humano rechaza;
humano define normas;
humano reporta excepciones;
humano valida evidencia.
```

Pepper debe registrar todo eso como datos operativos.

---

## 27. Arquitectura interna propuesta

```text
siamese_backend/agentic/
│
├── contracts/
│   ├── work_unit.py
│   ├── roadmap.py
│   ├── task.py
│   ├── recommendation.py
│   ├── approval.py
│   ├── evidence.py
│   ├── human_observation.py
│   ├── operational_rule.py
│   └── agent_event.py
│
├── agents/
│   ├── base_agent.py
│   ├── energy_model_agent.py
│   ├── sensor_agent.py
│   ├── calibration_agent.py
│   ├── dataset_agent.py
│   ├── surrogate_agent.py
│   ├── control_agent.py
│   ├── adoption_agent.py
│   ├── nucleus_agent.py
│   ├── network_agent.py
│   └── reporting_agent.py
│
├── tools/
│   ├── registry.py
│   ├── schemas.py
│   ├── permissions.py
│   ├── execution.py
│   └── results.py
│
├── policies/
│   ├── policy_engine.py
│   ├── access_control.py
│   ├── confidentiality.py
│   ├── action_scope.py
│   └── safety_policy.py
│
├── approvals/
│   ├── approval_gate.py
│   ├── approval_queue.py
│   ├── approval_history.py
│   └── promotion.py
│
├── evidence/
│   ├── evidence_registry.py
│   ├── evidence_linker.py
│   ├── access_policy.py
│   └── summaries.py
│
├── context/
│   ├── context_engine.py
│   ├── context_assembler.py
│   ├── context_filters.py
│   └── entity_context.py
│
├── memory/
│   ├── memory_store.py
│   ├── operational_rules.py
│   ├── human_observations.py
│   └── lessons_learned.py
│
├── workflows/
│   ├── roadmap_engine.py
│   ├── kanban.py
│   ├── workflow_templates.py
│   ├── task_generator.py
│   └── dependency_graph.py
│
├── human_input/
│   ├── report_parser.py
│   ├── schedule_change_parser.py
│   ├── rule_extractor.py
│   ├── observation_classifier.py
│   └── approval_comment_parser.py
│
├── ui/
│   ├── chat_adapter.py
│   ├── kanban_adapter.py
│   ├── approval_inbox.py
│   ├── evidence_viewer.py
│   └── report_input_panel.py
│
└── audit/
    ├── audit_log.py
    ├── agent_trace.py
    ├── decision_log.py
    └── compliance_export.py
```

---

## 28. Pepper dentro del producto

A nivel de producto, Pepper aparece como:

```text
Agent Chat;
Roadmap;
Kanban;
Approval Inbox;
Execution Inspector;
Evidence Viewer;
Operational Rules;
Human Reports;
Model Status;
Recommendation Center.
```

Pero internamente es una capa horizontal:

```text
Pepper
├── controla tools
├── controla workflows
├── controla aprobaciones
├── controla evidencia
├── recibe inputs humanos
├── conecta módulos
└── mantiene memoria operativa
```

---

## 29. Ejemplos completos

### 29.1 Cambio de ocupación

Usuario dice:

```text
“El viernes el aula 3B no se usará por la tarde.”
```

Pepper:

```text
1. Clasifica mensaje como ScheduleOverride.
2. Identifica entidad: Aula 3B.
3. Identifica periodo: viernes tarde.
4. Crea HumanObservation.
5. Propone OccupancyScheduleChange.
6. Solicita aprobación si afecta control.
7. Actualiza contexto operativo.
8. Lanza predicción surrogate con nueva ocupación.
9. Control Module recalcula recomendaciones.
10. Genera recomendación:
   “adelantar apagado de calefacción 90 min”.
11. Muestra impacto esperado.
12. Si está en shadow mode, registra qué habría hecho.
```

### 29.2 Informe de HVAC

Humano informa:

```text
“Ferrovial indica que la bomba no debe operar por debajo del 40% de caudal nominal.”
```

Pepper:

```text
1. Clasifica como HVAC Operational Constraint.
2. Extrae entidad: pump / HVAC system.
3. Crea OperationalRule candidate.
4. Marca fuente: Ferrovial / human report.
5. Solicita aprobación de Energy/HVAC Engineer.
6. Si se aprueba, Control Module recibe nueva constraint.
7. Recomendaciones futuras respetan caudal mínimo.
8. Evidence Registry guarda informe original.
```

### 29.3 Recomendación de surrogate + control

Sistema detecta:

```text
Surrogate predice sobrecalentamiento en Aula 3B a las 11:30.
```

Pepper:

```text
1. Surrogate Agent recibe PredictionResult.
2. Control Agent solicita acciones candidatas.
3. Control Module evalúa:
   - mantener;
   - bajar setpoint;
   - apagar antes;
   - ventilar.
4. Safety Layer bloquea ventilación por lluvia.
5. Recomendación válida:
   bajar setpoint 1 ºC durante 90 min.
6. Evidence Registry vincula:
   - predicción;
   - sensor state;
   - surrogate validation;
   - safety decision.
7. Approval Inbox muestra recomendación.
8. Humano aprueba o rechaza.
9. En shadow mode, solo se registra.
```

---

## 30. MVP recomendado

El MVP de Pepper dentro de Siamese no debe intentar crear todos los agentes.

### Objetivo MVP

Crear una capa agéntica mínima que conecte recomendaciones, tareas, aprobaciones y observaciones humanas.

### Alcance MVP

```text
WorkUnit contract;
Task contract;
HumanObservation contract;
OperationalRule contract;
Recommendation intake;
ApprovalGate básico;
EvidenceRegistry básico;
ToolRegistry básico;
PolicyEngine básico;
Agent Chat contextual;
Kanban simple;
Approval Inbox;
integración con módulo de control en modo recomendación/shadow;
input humano para cambios de horario/ocupación.
```

### Fuera del MVP

```text
agentes autónomos complejos;
control real;
multiempresa;
Graphify completo;
memoria avanzada;
RAG completo;
herramientas externas completas;
edición automática de Nucleus layers;
PPO autonomous policy;
full BMS execution.
```

### Resultado esperado

```text
Siamese puede recibir una observación humana,
convertirla en contexto operativo,
generar o modificar recomendaciones,
crear tareas,
pedir aprobación
y guardar evidencia.
```

---

## 31. Fases de evolución

### Fase 1 — Workflow Core

```text
WorkUnits;
Tasks;
Roadmaps;
Kanban;
statuses.
```

### Fase 2 — Human Input

```text
HumanObservation;
ScheduleOverride;
OperationalRule;
report ingestion.
```

### Fase 3 — Tool Registry

```text
tools por módulo;
schemas;
permissions.
```

### Fase 4 — Evidence Registry

```text
evidencia vinculada;
resúmenes;
access policy.
```

### Fase 5 — Approval Gates

```text
aprobaciones;
promotion;
approval history.
```

### Fase 6 — Module Agents

```text
Sensor Agent;
Calibration Agent;
Surrogate Agent;
Control Agent.
```

### Fase 7 — Omniverse Native UI

```text
chat;
kanban;
approval inbox;
evidence viewer;
roadmaps contextualizados.
```

### Fase 8 — Nucleus Proposal Layers

```text
agent annotations;
human review;
backend promotion.
```

### Fase 9 — Advanced Memory / Graph

```text
knowledge graph;
operational memory;
building-specific rules.
```

### Fase 10 — Full Agentic Operation

```text
multi-agent workflows;
parallel tasks;
control readiness;
client workflows;
auditable automation.
```

---

## 32. Primeros tickets recomendados

### PEPPER-00 — Pepper module context

Crear documentación conceptual del módulo.

### PEPPER-01 — Agentic core contracts

Definir `WorkUnit`, `Task`, `Roadmap`, `AgentEvent`.

### PEPPER-02 — HumanObservation contract

Crear contrato para observaciones humanas.

### PEPPER-03 — OperationalRule contract

Crear contrato para reglas operativas del edificio.

### PEPPER-04 — Recommendation intake

Aceptar recomendaciones desde módulo de control.

### PEPPER-05 — Evidence Registry MVP

Registrar y vincular evidencia.

### PEPPER-06 — Approval Gate MVP

Crear flujo básico de aprobación.

### PEPPER-07 — Policy Engine MVP

Permitir/bloquear acciones según rol, modo y scope.

### PEPPER-08 — Tool Registry MVP

Registrar tools por módulo con schemas y permisos.

### PEPPER-09 — Human report parser MVP

Convertir texto humano en observación/regla/tarea candidata.

### PEPPER-10 — Context Engine MVP

Ensamblar contexto por edificio/zona/sensor/recomendación.

### PEPPER-11 — Kanban / Roadmap UI

Mostrar tareas y roadmaps en Kit/web.

### PEPPER-12 — Approval Inbox UI

Mostrar aprobaciones pendientes.

### PEPPER-13 — Recommendation Center

Mostrar recomendaciones con evidencia y safety decision.

### PEPPER-14 — Nucleus proposal layer policy

Definir cómo agentes escriben capas de propuesta.

### PEPPER-15 — Confidentiality policy

Definir niveles de acceso a raw data, source code, credentials y datos cliente.

---

## 33. Riesgos principales

### Riesgo 1 — Agentes con demasiado poder

Mitigación:

```text
Tool Registry;
Policy Engine;
Approval Gates;
read/write separation;
no direct file edits.
```

### Riesgo 2 — Chat sin estructura

Mitigación:

```text
convertir inputs a entidades:
HumanObservation, Rule, Task, Approval, Evidence.
```

### Riesgo 3 — Exponer información confidencial

Mitigación:

```text
access levels;
raw data restrictions;
source code privacy;
credential isolation;
customer isolation.
```

### Riesgo 4 — Recomendaciones sin evidencia

Mitigación:

```text
Evidence Registry obligatorio;
RecommendationReport;
SafetyDecision;
ValidationReport.
```

### Riesgo 5 — Automatización prematura

Mitigación:

```text
recommendation first;
shadow mode;
human approval;
limited actions.
```

### Riesgo 6 — Fragmentar Pepper y Siamese

Mitigación:

```text
Pepper externo al inicio;
contratos compatibles;
migración nativa planificada;
tool interfaces estables.
```

### Riesgo 7 — Humanos aportan información ambigua

Mitigación:

```text
HumanObservation pending_interpretation;
clarification tasks;
approval before operational rule;
validity window.
```

---

## 34. Valor comercial

Este módulo es muy diferenciador.

Herramientas clásicas pueden simular. Siamese puede ofrecer:

```text
un gemelo energético que trabaja contigo;
un sistema que recuerda normas del edificio;
un asistente que entiende sensores, modelos, predicciones y tareas;
un flujo de trabajo auditable;
un copiloto para facility managers;
un sistema que aprende de informes humanos;
un software que no muere tras el informe.
```

Frase comercial:

> **Siamese no entrega un modelo. Entrega un sistema vivo que organiza, recuerda, recomienda y coordina la operación energética del edificio.**

---

## 35. Frases de presentación

Frase principal:

> **Pepper convierte Siamese en un ecosistema vivo de trabajo energético.**

Frase técnica:

> **Pepper es el motor agéntico que conecta módulos, tools, evidencias, tareas, aprobaciones, observaciones humanas y recomendaciones operativas bajo políticas de seguridad y trazabilidad.**

Frase comercial:

> **El edificio no solo se simula: se gestiona, se aprende y se opera con agentes.**

Frase estratégica:

> **Siamese no es un software con un chatbot. Es una plataforma energética agent-native.**

Frase de seguridad:

> **Los agentes leen contexto, proponen acciones y ejecutan tools gobernadas; no editan ni controlan sin permisos, evidencia y aprobación.**

---

## 36. Decisión arquitectónica final

La arquitectura final:

```text
EnergyPlus calcula.
Calibración ajusta.
Sensórica observa.
Surrogates predicen.
Control recomienda.
Nucleus colabora.
Omniverse visualiza.
Pepper orquesta.
```

La decisión clave:

```text
Pepper es la capa horizontal de orquestación, contexto, tareas, evidencia,
aprobaciones, human input y herramientas gobernadas.
```

Pepper debe:

```text
leer todo lo necesario;
editar solo lo permitido;
ejecutar solo mediante tools;
promocionar solo con approval;
exponer solo información permitida;
registrar evidencia;
respetar modos operativos;
aceptar inputs humanos como datos operativos.
```

No debe:

```text
sustituir módulos técnicos;
editar código fuente confidencial;
exponer credenciales;
actuar sobre HVAC sin safety/approval;
convertirse en un chat sin estructura;
ocultar incertidumbre o falta de evidencia.
```

---

## 37. Relación con documentos previos

Este documento complementa:

```text
siamese_energyplus_context.md
→ EnergyPlus como solver físico.

siamese_python_backend_context.md
→ backend Python como capa de gobierno.

siamese_omniverse_kit_context.md
→ Omniverse Kit como interfaz visual.

siamese_nucleus_module_context.md
→ colaboración y assets OpenUSD.

siamese_calibration_module_context.md
→ calibración como puente modelo-realidad.

siamese_sensorics_module_context.md
→ sensórica como observación real.

siamese_adoption_model_context.md
→ adopción de modelos existentes.

siamese_surrogate_models_context.md
→ predicción operativa.

siamese_optimization_control_context.md
→ recomendaciones y control gobernado.

siamese_dsx_ecosystem_context.md
→ referencia estratégica NVIDIA/DSX.

digital_twin_contexto_maestro.md
→ visión modular general.
```

Y prepara:

```text
Siamese native agentic UI;
Control readiness workflows;
Human-in-the-loop operations;
BMS supervised control;
Knowledge graph / G-Brain integration;
Multi-agent operation;
Client-facing digital twin workflows;
Auditable building operations.
```
