# Siamese — Omniverse Kit como interfaz gráfica, semántica y extensible

**Documento:** Contexto técnico del módulo Omniverse Kit dentro de Siamese  
**Proyecto:** Siamese — plataforma agéntica de gemelos digitales energéticos  
**Estado:** Documento de arquitectura conceptual previo a implementación  
**Versión:** 0.1  
**Propósito:** definir con precisión qué papel cumple NVIDIA Omniverse Kit en Siamese, qué responsabilidades tiene, qué responsabilidades no debe asumir, cómo se relaciona con el backend Python, EnergyPlus, OpenUSD, Nucleus, RTX, sensórica, visualización, módulos agénticos y extensiones propias.

---

## 1. Resumen ejecutivo

Omniverse Kit será la **interfaz gráfica avanzada** de Siamese: el entorno visual, modular y extensible donde el usuario crea, inspecciona, visualiza y opera el gemelo energético del edificio.

Su función no es sustituir al backend Python ni al solver EnergyPlus. Su función es convertir el sistema energético en una experiencia espacial, semántica y navegable.

La frontera arquitectónica clave es:

```text
EnergyPlus calcula.
Backend Python gobierna.
OpenUSD estructura.
Omniverse Kit visualiza e interactúa.
Nucleus colabora.
Agentes orquestan.
Siamese convierte todo en un gemelo energético vivo.
```

Omniverse Kit debe funcionar como el **workspace técnico premium** de Siamese: una aplicación propia construida sobre extensiones, comandos, paneles, viewport RTX, semántica USD y conexión con el backend.

---

## 2. Qué es Omniverse Kit para Siamese

Omniverse Kit será el runtime sobre el que se construirá la app visual de Siamese.

En Siamese, Kit debe aportar:

```text
viewport 3D;
interfaz gráfica modular;
extensiones propias;
extensiones existentes reutilizables;
comandos nativos;
visualización RTX;
semántica OpenUSD;
paneles técnicos;
inspector contextual;
visualización de sensores;
visualización de simulaciones;
visualización de calibración;
visualización de predicción;
visualización de control/recomendaciones;
chat agéntico contextual;
roadmaps y kanban embebidos;
approval inbox;
execution inspector.
```

Pero Kit no debe ser:

```text
backend energético;
solver de simulación;
base de datos principal;
sistema de ingesta de sensores;
motor de calibración;
runtime de entrenamiento IA;
sistema de control directo;
source of truth completo del producto.
```

La interfaz debe estar profundamente integrada con Siamese, pero la lógica fuerte debe seguir viviendo en backend y paquetes core.

---

## 3. Por qué usar Omniverse Kit

La razón estratégica no es solamente visual. Siamese necesita una interfaz capaz de trabajar con entidades espaciales y técnicas a la vez:

```text
edificios 3D;
plantas;
aulas;
zonas térmicas;
superficies;
ventanas;
materiales;
sistemas HVAC;
sensores;
resultados de simulación;
mapas de calor;
predicciones;
recomendaciones;
tareas agénticas;
validaciones;
aprobaciones.
```

Una interfaz web tradicional puede servir para dashboards y reporting, pero no ofrece de forma natural un workspace espacial donde entender la relación entre:

```text
geometría física
→ zona térmica
→ sensor
→ simulación
→ calibración
→ surrogate
→ predicción
→ recomendación
→ decisión operativa.
```

Omniverse Kit permite que Siamese sea una herramienta de ingeniería, no solo un panel de datos.

---

## 4. Arquitectura general

La arquitectura recomendada es:

```text
┌──────────────────────────────────────────────┐
│              Omniverse Kit App               │
│                                              │
│  Viewport RTX / USD Stage / UI Panels        │
│  Extensions / Commands / Tools / Agent UI    │
└──────────────────────▲───────────────────────┘
                       │
                       │ API / Commands / Events
                       │
┌──────────────────────┴───────────────────────┐
│             Siamese Backend Python            │
│                                              │
│  Energy Model / Simulation / Calibration      │
│  Datasets / Surrogates / Control / Jobs       │
└──────────────────────▲───────────────────────┘
                       │
                       │ IDF / epJSON / EPW
                       │
┌──────────────────────┴───────────────────────┐
│                 EnergyPlus                    │
│              Physical Solver                  │
└──────────────────────────────────────────────┘
```

Omniverse Kit es cliente visual y superficie de interacción. El backend Python es la autoridad energética y operacional. EnergyPlus es el solver físico.

---

## 5. Principios arquitectónicos

### 5.1 Kit no es el backend

La lógica energética no debe vivir dentro de la app Kit.

Regla:

```text
Kit muestra, edita e interactúa.
El backend valida, ejecuta, persiste y normaliza.
```

### 5.2 Kit no habla directamente con EnergyPlus

No debe existir este flujo:

```text
Omniverse Kit
→ genera IDF suelto
→ lanza EnergyPlus directamente
→ parsea CSVs directamente
```

Debe existir este flujo:

```text
Omniverse Kit
→ comando/API Siamese
→ backend Python
→ EnergyPlus Runner
→ resultados normalizados
→ capa visual en Kit
```

### 5.3 USD contiene semántica, no datos masivos

USD debe contener geometría, relaciones, metadatos, bindings y capas visuales. No debe contener grandes series temporales, datasets, logs o modelos ML completos.

### 5.4 Las acciones se ejecutan mediante comandos gobernados

La UI, los agentes y los scripts deben llamar comandos o APIs estables, no modificar datos críticos de forma libre.

### 5.5 La interfaz debe ser modular

Cada gran capacidad de Siamese debe encapsularse como extensión, panel o workspace independiente.

---

## 6. OpenUSD como base semántica

OpenUSD debe actuar como la representación geométrica y semántica del edificio.

En Siamese, el edificio no debe ser una simple malla 3D. Debe estar compuesto por entidades identificables:

```text
Building;
Floor;
Space;
ThermalZone;
Surface;
Opening;
Construction;
Material;
Sensor;
HVACElement;
SimulationResultLayer;
CalibrationLayer;
PredictionLayer;
RecommendationLayer;
AgentAnnotation.
```

Ejemplo conceptual de jerarquía:

```text
/World/Building
/World/Building/Floors/Floor_01
/World/Building/Spaces/Aula_3B
/World/Building/ThermalZones/Zone_Aula_3B
/World/Building/Surfaces/Fachada_Sur_03
/World/Building/Sensors/Sensor_Govee_3B
/World/Building/Results/Simulation_Run_001
/World/Building/Visualization/ThermalMap_Run_001
```

La ventaja de OpenUSD es que permite trabajar con composición, capas, referencias, variantes, payloads, relaciones y metadatos. Esto permite que Siamese represente múltiples dimensiones del gemelo sin duplicar ni destruir la geometría base.

---

## 7. USD como semántica energética

En Siamese, una superficie no debe ser solo una cara gráfica. Debe poder representar:

```text
una superficie arquitectónica;
una frontera térmica;
una parte de una zona;
un elemento de la envolvente;
un soporte de material/construcción;
un objeto de simulación EnergyPlus;
un receptor de resultados;
un elemento seleccionable en la UI;
un objeto sobre el que un agente puede razonar.
```

Ejemplo de metadata conceptual:

```yaml
Prim: /World/Building/Surfaces/Fachada_Sur_03
Type: SiameseThermalSurface
Metadata:
  zone_id: aula_3b
  boundary_condition: outdoors
  construction_id: wall_brick_uninsulated_v1
  energyplus_surface_id: ep_surface_104
  latest_surface_temperature_result: result_run_001
```

Este enfoque permite que una selección visual tenga significado energético y operativo.

---

## 8. Capas USD recomendadas

La escena debe componerse mediante capas diferenciadas.

Ejemplo:

```text
building_base.usd
→ geometría base del edificio

aec_model.usd
→ espacios, superficies, openings y materiales

energy_semantics.usd
→ zonas térmicas, relaciones energéticas y metadatos

sensor_bindings.usd
→ sensores y relación sensor-zona

simulation_results_run_001.usd
→ visualización de resultados de simulación

calibration_results_v03.usd
→ errores, métricas y estado de calibración

surrogate_prediction_live.usd
→ predicción actual y próximos estados

control_recommendations.usd
→ recomendaciones y estados de control

agent_annotations.usd
→ comentarios, tareas, evidencias y marcas visuales no destructivas
```

Ventajas:

```text
separación de responsabilidades;
comparación de escenarios;
trabajo colaborativo;
versionado visual;
carga diferida de contenido pesado;
mejor rendimiento;
trazabilidad.
```

---

## 9. RTX como herramienta de ingeniería

El renderer RTX no debe usarse como decoración visual. En Siamese debe cumplir una función de comunicación técnica:

```text
lectura espacial clara;
visualización premium;
inspección del edificio;
materialidad entendible;
mapas térmicos legibles;
presentaciones comerciales;
demos de alto impacto;
comprensión inmediata de zonas críticas.
```

La dirección visual debe ser:

```text
premium;
minimalista;
profesional;
sobria;
blancos, negros y grises;
acento cian/turquesa Siamese;
sin estética neón excesiva;
sin sobrecarga de datos.
```

El viewport debe priorizar:

```text
modelo del edificio;
zonas coloreadas por variable;
sensores discretos;
leyenda limpia;
panel contextual mínimo;
comparación real/simulado/predicho.
```

---

## 10. Sistema de extensiones

Las extensiones serán la unidad modular principal de la app Kit.

Siamese debería organizar sus capacidades visuales y de interacción como extensiones independientes.

Propuesta inicial:

```text
extensions/
├── siamese.app.shell/
├── siamese.ui.theme/
├── siamese.usd.schema/
├── siamese.aec.modeling/
├── siamese.energy.modeling/
├── siamese.energyplus.bridge/
├── siamese.visualization.thermal/
├── siamese.visualization.timeseries/
├── siamese.sensors.mapping/
├── siamese.calibration.workspace/
├── siamese.datasets.workspace/
├── siamese.surrogates.workspace/
├── siamese.control.workspace/
├── siamese.agent.chat/
├── siamese.agent.roadmaps/
├── siamese.agent.kanban/
├── siamese.agent.approvals/
├── siamese.agent.execution_inspector/
└── siamese.collaboration.nucleus/
```

Cada extensión debe tener una responsabilidad acotada.

---

## 11. Extensiones propias y existentes

### 11.1 Extensiones base de Omniverse

Se usarán como infraestructura:

```text
viewport;
USD stage;
selection;
layers;
properties;
materials;
renderer;
UI toolkit;
asset browser;
commands;
collaboration.
```

### 11.2 Extensiones existentes candidatas

Deben evaluarse caso por caso:

```text
layer widgets;
viewport tools;
plotting components;
property panels;
asset management;
point cloud visualization;
live collaboration;
material tools;
scene inspection tools.
```

Criterios de adopción:

```text
licencia;
estabilidad;
compatibilidad con Kit;
calidad de API;
extensibilidad;
capacidad de mantenerse a futuro;
valor frente a implementación propia.
```

### 11.3 Extensiones propias Siamese

Aquí está la diferenciación:

```text
AEC-USD Modelling;
Thermal Zone Editor;
EnergyPlus Run Panel;
Calibration Workspace;
Sensor Mapping;
ThermalViz;
Surrogate Monitor;
Control Recommendations;
Agentic Roadmaps;
Kanban;
Approval Inbox;
Execution Inspector.
```

---

## 12. Comandos nativos Kit

Los comandos serán la forma controlada de ejecutar acciones desde la UI, hotkeys, scripts o agentes.

Ejemplos:

```text
AEC.CreateSpace
AEC.ExtrudeSketchToBlock
AEC.AssignThermalZone
AEC.CreateOpening
AEC.AssignConstruction
Energy.CreateSimulationCase
Energy.RunSimulation
Viz.ApplyThermalMap
Sensor.BindSensorToZone
Calibration.CreateJob
Dataset.CreateCampaign
Surrogate.DeployPredictionLayer
Control.CreateRecommendation
Agent.CreateRoadmapTask
Agent.RequestApproval
```

Regla:

```text
UI, agente y scripts llaman comandos.
Los comandos llaman backend o modifican USD de forma controlada.
```

Ventajas:

```text
trazabilidad;
tests;
undo/redo cuando aplique;
seguridad;
consistencia;
integración agéntica;
registro de evidencias;
menor duplicación de lógica.
```

---

## 13. App shell y estructura visual

La interfaz debería organizarse en un shell estable.

Propuesta:

```text
Top Bar:
- proyecto activo;
- edificio activo;
- estado live;
- hora/clima;
- usuario;
- notificaciones;
- modo operacional.

Left Sidebar:
- Overview;
- Building;
- Systems;
- Energy;
- Environment;
- Analytics;
- Simulation;
- Calibration;
- Surrogates;
- Control;
- Alarms;
- Agent Roadmaps;
- Settings.

Center:
- RTX viewport;
- USD stage;
- heatmaps;
- sensores;
- overlays;
- selección espacial.

Right Inspector:
- entidad seleccionada;
- zona;
- sensor;
- superficie;
- sistema HVAC;
- simulación;
- calibración;
- surrogate;
- recomendación;
- tarea.

Bottom Panel:
- timeline;
- jobs;
- execution inspector;
- gráficas temporales;
- comparación real/simulado/predicho.

Agent Dock:
- chat contextual;
- tareas;
- approvals;
- acciones propuestas.
```

---

## 14. Inspector contextual

El inspector contextual será una pieza clave.

Cuando el usuario seleccione una zona, Siamese debe mostrar:

```text
identidad de zona;
planta;
superficie;
sensores asociados;
temperatura real;
humedad real;
CO₂ si existe;
temperatura simulada;
temperatura predicha;
error de calibración;
estado de confort;
recomendaciones activas;
tareas abiertas;
historial de simulaciones.
```

Ejemplo:

```yaml
Selected: Aula_3B
Type: ThermalZone
Current:
  measured_temperature: 22.8 °C
  simulated_temperature: 22.5 °C
  predicted_30min: 23.4 °C
  comfort_status: within_range
  sensor_health: operational
OpenTasks:
  - revisar horario de ocupación
  - validar estrategia de ventilación
```

---

## 15. Relación con el backend Python

Omniverse Kit debe comunicarse con el backend mediante APIs, comandos y eventos.

Ejemplo de flujo de simulación:

```text
Usuario pulsa Run Simulation en Kit
↓
Kit ejecuta Energy.RunSimulation
↓
El comando crea SimulationCase en backend
↓
Backend valida y compila
↓
Backend ejecuta EnergyPlus
↓
Backend publica estado de job
↓
Kit muestra progreso
↓
Backend devuelve resultados normalizados
↓
Kit aplica capa visual sobre USD
```

Esto evita que Kit se convierta en backend y mantiene la arquitectura limpia.

---

## 16. Relación con EnergyPlus

EnergyPlus no debe saber que Omniverse existe.

La cadena debe ser:

```text
OpenUSD / AEC Model
        ↓
USD-to-Energy Mapper
        ↓
Siamese Energy Model
        ↓
EnergyPlus Compiler
        ↓
EnergyPlus Run
        ↓
Normalized Results
        ↓
Results-to-USD Visualization Mapper
        ↓
Omniverse Kit
```

Esta separación permite que:

```text
EnergyPlus siga siendo solver;
backend mantenga trazabilidad;
Kit visualice sin parsear outputs crudos;
agentes actúen mediante herramientas gobernadas.
```

---

## 17. Relación con Nucleus

Nucleus puede aportar colaboración sobre escenas, assets y capas USD.

Usos esperados:

```text
almacenar stages USD compartidos;
gestionar assets;
trabajar con capas colaborativas;
coordinar revisiones de geometría;
permitir sesiones live;
comparar alternativas visuales;
compartir modelos entre usuarios;
crear un entorno multiusuario.
```

Pero Nucleus no debe sustituir al backend.

Relación recomendada:

```text
Nucleus:
USD, assets, layers, colaboración visual.

Siamese Backend:
modelos energéticos, simulaciones, resultados, sensores, calibraciones, datasets, surrogates, permisos, jobs, trazabilidad.
```

---

## 18. Qué datos deben vivir en USD

### 18.1 Deben vivir en USD

```text
geometría;
jerarquía espacial;
plantas;
espacios;
zonas térmicas;
superficies;
openings;
metadata de materiales;
ubicación de sensores;
bindings a datos externos;
capas visuales;
escenarios;
anotaciones;
relaciones espaciales.
```

### 18.2 No deben vivir en USD

```text
series temporales completas;
datasets masivos;
outputs crudos de EnergyPlus;
modelos ML completos;
logs extensos;
credenciales;
datos sensibles de clientes;
históricos operativos completos;
registros de facturación;
colas de jobs;
permisos críticos.
```

USD debe referenciar estos datos mediante identificadores y metadata.

Ejemplo:

```yaml
SensorPrim:
  path: /World/Building/Sensors/Sensor_3B_Temp
  sensor_id: sensor_3b_temp_01
  zone_id: aula_3b
  timeseries_ref: tsdb://building_001/sensor_3b_temp_01
```

---

## 19. Relación con sensórica

Kit debe visualizar sensórica, no ingerirla directamente.

Flujo:

```text
sensor/BMS
→ backend ingestion
→ time-series storage
→ normalized sensor state
→ Kit visualization
```

Kit muestra:

```text
sensores colocados espacialmente;
estado online/offline;
última lectura;
temperatura;
humedad;
CO₂;
alertas;
comparación sensor vs simulación;
comparación sensor vs predicción;
zonas sin sensor;
sensores degradados.
```

La visualización debe ser espacial y sobria:

```text
sensor como punto cian discreto;
tooltip técnico;
línea fina hacia panel de datos;
icono de estado;
alertas sin saturar el viewport.
```

---

## 20. Relación con calibración

Kit debe ayudar a entender y revisar la calibración.

Debe mostrar:

```text
zonas calibradas;
zonas con error alto;
comparación real vs simulado;
variables calibrables;
progreso de jobs;
métricas;
curvas;
modelo calibrado aprobado;
historial de intentos;
zonas bloqueadas por datos insuficientes.
```

Ejemplo de panel:

```yaml
Calibration Workspace:
  target_zone: Aula_3B
  period: 2026-04-22/2026-04-29
  metrics:
    CVRMSE: 8.4
    NMBE: -1.2
    NMAE: 3.1
  status: requires_human_approval
```

Kit no calcula la calibración. La hace comprensible, revisable y aprobable.

---

## 21. Relación con Dataset Factory

Kit debe visualizar campañas de generación de datasets.

Debe poder mostrar:

```text
modelo calibrado usado;
variables sampleadas;
escenarios generados;
simulaciones completadas;
calidad del dataset;
zona/edificio cubierto;
features;
targets;
splits;
manifest.
```

El objetivo no es que el usuario vea miles de archivos. Debe ver la lógica del dataset.

---

## 22. Relación con Surrogate Factory

Kit debe convertir los modelos surrogados en elementos interpretables.

Debe mostrar:

```text
modelo activo;
horizonte de predicción;
variables predichas;
zonas cubiertas;
confianza;
error histórico;
rollout stability;
comparación real/sim/pred;
estado de despliegue;
versión del modelo.
```

Ejemplo:

```yaml
Surrogate:
  model_id: surrogate_aula3b_lstm_pi_v04
  horizon: 30min
  target: zone_air_temperature
  status: approved_for_shadow_mode
  last_validation_rmse: 0.42 °C
```

---

## 23. Relación con control y recomendaciones

Kit debe evitar una UI peligrosa de control directo.

No debe existir una experiencia tipo:

```text
Botón grande: Optimizar edificio automáticamente
```

Debe existir:

```text
recomendación;
evidencia;
impacto esperado;
modo operativo;
riesgo;
aprobación humana;
rollback;
historial.
```

Ejemplo:

```yaml
Recommendation:
  zone: Aula_3B
  action: reduce_heating_setpoint
  value: -1.0 °C
  window: 10:30-12:00
  expected_effect:
    comfort: maintained
    energy: reduced
    overheating: reduced
  mode: shadow
  approval_required: true
```

Estados recomendados:

```text
observation;
recommendation;
shadow mode;
supervised control;
limited auto control.
```

---

## 24. Relación con flujos agénticos

El motor agéntico derivado de Pepper/Hermes debe integrarse en Kit de forma nativa, pero como capa sobre comandos y entidades Siamese.

Módulos visuales:

```text
Agent Chat;
Roadmap Panel;
Kanban Panel;
Approval Inbox;
Execution Inspector;
Tool Inspector;
Model Selector;
Evidence Viewer.
```

Ejemplo:

```text
Usuario selecciona Aula_3B.
↓
Pregunta al chat: ¿Por qué se sobrecalienta?
↓
Agente consulta sensores, simulaciones, calibración y orientación.
↓
Agente responde con evidencia.
↓
Agente propone una tarea de simulación alternativa.
↓
Usuario aprueba crear la tarea.
```

El agente no debe inventar acciones ni modificar archivos directamente. Debe operar mediante herramientas gobernadas.

---

## 25. Roadmaps dentro de Kit

Siamese debe poder representar proyectos de gemelo energético como roadmaps.

Ejemplos:

```text
Crear gemelo desde cero;
Adoptar modelo existente;
Diseñar sensórica;
Calibrar modelo multizona;
Generar dataset;
Entrenar surrogate;
Activar shadow mode;
Preparar control supervisado.
```

Cada roadmap se divide en:

```text
macroproyectos;
proyectos;
tareas;
agentes;
evidencias;
gates;
aprobaciones.
```

Kit debe permitir ver ese roadmap junto al edificio, no en una herramienta externa desconectada.

---

## 26. Colaboración y roles

Siamese debe soportar colaboración entre perfiles:

```text
ingeniero energético;
arquitecto;
facility manager;
consultora;
cliente;
mantenedor;
investigador;
agente IA.
```

Cada perfil debe tener permisos distintos.

Ejemplo:

```text
Arquitecto:
puede modificar geometría en layer de diseño.

Ingeniero energético:
puede aprobar zonas térmicas, materiales y calibración.

Facility manager:
puede revisar sensores, alertas y recomendaciones.

Agente:
puede proponer tareas y ejecutar herramientas permitidas.

Cliente:
puede ver dashboards e informes, pero no modificar modelo físico.
```

---

## 27. Personalización de la interfaz

Omniverse Kit permite que Siamese tenga una interfaz adaptada a distintos perfiles.

Workspaces posibles:

```text
Consultor energético;
Facility manager;
Investigador;
Desarrollador;
Cliente/inversor;
Operador HVAC;
Modo demo.
```

Cada workspace puede activar/desactivar:

```text
paneles;
capas;
variables;
colormaps;
extensiones;
herramientas;
detalle técnico;
permisos;
modo novato/experto.
```

Ejemplo:

```text
Modo facility manager:
- sensores;
- alertas;
- confort;
- recomendaciones;
- tareas.

Modo investigador:
- datasets;
- surrogates;
- métricas;
- experiment tracking.

Modo desarrollador:
- schemas;
- commands;
- API;
- execution inspector.
```

---

## 28. Sistema visual Siamese

La identidad visual debe heredar la estética del logo:

```text
blanco;
negro;
grises;
cian/turquesa de los ojos;
minimalismo;
precisión;
elegancia;
alto contraste;
uso moderado del color;
amplio espacio negativo.
```

Reglas:

```text
no usar neones saturados;
no sobrecargar paneles;
no mostrar todos los datos a la vez;
no convertir el viewport en un videojuego;
priorizar jerarquía visual;
mostrar solo lo necesario para decidir.
```

Color primario:

```text
Siamese cyan / turquoise
```

Uso recomendado:

```text
estado activo;
selección;
trazas de sensores;
series principales;
indicadores de live/inference;
call-to-action técnico.
```

---

## 29. MVP recomendado de Omniverse Kit

El primer MVP debe demostrar una conexión vertical real:

```text
1. Cargar edificio USD.
2. Seleccionar zona térmica.
3. Mostrar metadata energética.
4. Crear SimulationCase desde Kit.
5. Lanzar simulación vía backend.
6. Consultar estado del job.
7. Recibir resultados normalizados.
8. Aplicar mapa térmico simple.
9. Mostrar gráfica básica por zona.
10. Crear tarea agéntica asociada a la zona.
```

No incluir todavía:

```text
control HVAC real;
surrogates completos;
colaboración multiusuario avanzada;
roadmaps complejos;
Nucleus completo;
calibración multizona avanzada;
plugins externos de productividad.
```

Criterio de éxito:

```text
Kit puede actuar como cliente visual real del backend Siamese.
```

---

## 30. Fases de construcción

### Fase 1 — App shell

```text
tema Siamese;
layout principal;
sidebar;
viewport;
inspector;
settings;
estado de proyecto.
```

### Fase 2 — USD/AEC base

```text
cargar stage;
jerarquía building/floors/spaces;
selección de entidades;
metadata básica;
capas iniciales.
```

### Fase 3 — Energy bridge

```text
crear SimulationCase;
lanzar simulación;
mostrar estado;
recibir resultados.
```

### Fase 4 — ThermalViz MVP

```text
colorear zonas;
leyenda;
timeline básico;
gráfica simple.
```

### Fase 5 — Sensor mapping

```text
colocar sensores;
mapear sensores a zonas;
mostrar datos reales;
estado de sensores.
```

### Fase 6 — Calibration workspace

```text
comparar real vs simulado;
mostrar métricas;
visualizar error;
aprobar modelo calibrado.
```

### Fase 7 — Surrogates/control

```text
predicción;
shadow mode;
recomendaciones;
alertas;
validación visual.
```

### Fase 8 — Agentic workflow

```text
chat contextual;
roadmaps;
kanban;
approvals;
execution inspector;
tool inspector.
```

---

## 31. Riesgos técnicos

### Riesgo 1 — Convertir Kit en el núcleo

Mitigación:

```text
backend independiente;
APIs estables;
Kit como cliente.
```

### Riesgo 2 — Sobrecargar la interfaz

Mitigación:

```text
workspaces;
progressive disclosure;
modo experto;
minimalismo visual.
```

### Riesgo 3 — Dependencia excesiva de NVIDIA

Mitigación:

```text
backend usable sin Kit;
web dashboard alternativo;
formatos abiertos;
exportación;
contratos independientes.
```

### Riesgo 4 — Visualización sin decisión

Mitigación:

```text
cada vista debe responder:
qué pasa;
por qué pasa;
qué evidencia hay;
qué acción procede.
```

### Riesgo 5 — Datos masivos dentro de USD

Mitigación:

```text
series temporales fuera de USD;
USD solo metadata, bindings y capas visuales.
```

### Riesgo 6 — Agentes modificando escena sin control

Mitigación:

```text
comandos gobernados;
policy engine;
approval gates;
evidence registry;
execution inspector.
```

---

## 32. Ventajas estratégicas

### 32.1 Diferenciación visual

Siamese puede presentarse como una herramienta de ingeniería premium, no como un dashboard genérico.

### 32.2 Semántica espacial

El usuario entiende el edificio desde su geometría, no desde tablas aisladas.

### 32.3 Modularidad

El sistema de extensiones permite crecer por módulos.

### 32.4 Colaboración

Con Nucleus y USD layers se abre la puerta a workflows colaborativos.

### 32.5 Interoperabilidad

USD puede actuar como tejido semántico para conectar geometría, datos, simulación y visualización.

### 32.6 Integración agéntica

Los agentes pueden operar sobre entidades seleccionadas, roadmaps, tareas y comandos.

### 32.7 Narrativa comercial

La interfaz permite explicar la propuesta de valor de forma inmediata: el edificio real, el modelo, los sensores y la predicción se ven en un mismo lugar.

---

## 33. Relación con la narrativa comercial

Omniverse Kit debe comunicarse como:

```text
la interfaz espacial de Siamese;
el workspace donde el gemelo energético se vuelve visible;
el entorno donde sensores, simulaciones, predicciones y recomendaciones se entienden sobre el edificio;
la capa visual premium que diferencia Siamese de dashboards e interfaces tradicionales.
```

No debe comunicarse como:

```text
el solver;
el backend;
la IA;
el producto completo;
una demo visual sin profundidad técnica.
```

Frase para presentación:

> Omniverse Kit convierte Siamese en un workspace visual de ingeniería: una interfaz modular sobre OpenUSD donde el edificio, los sensores, la simulación, la IA y los flujos agénticos se vuelven navegables.

Frase corta:

> Omniverse Kit es donde el gemelo energético se vuelve visible, editable y operable.

Frase para inversores:

> No construimos solo un dashboard. Construimos una interfaz espacial para operar inteligencia energética sobre edificios reales.

---

## 34. Relación con otros módulos de Siamese

```text
EnergyPlus:
  Kit no lo ejecuta directamente; visualiza sus resultados normalizados.

Backend Python:
  Kit es cliente avanzado mediante APIs y comandos.

OpenUSD:
  Kit lo usa como escena geométrica y semántica.

Nucleus:
  Kit lo usa para colaboración, assets y layers.

Sensórica:
  Kit visualiza sensores normalizados por backend.

Calibración:
  Kit muestra errores, métricas y aprobación visual.

Datasets:
  Kit muestra campañas, manifest y cobertura.

Surrogates:
  Kit muestra predicciones, confianza y validación.

Control:
  Kit muestra recomendaciones, impacto y approval gates.

Agentes:
  Kit aloja chat, roadmaps, kanban, approvals y execution inspector.
```

---

## 35. Primeros tickets recomendados

### KIT-00 — Omniverse Kit module vision

Crear la documentación base del módulo Kit.

### KIT-01 — App shell architecture

Definir layout principal, navegación, tema visual y workspaces.

### KIT-02 — USD stage conventions

Definir convenciones iniciales para Building, Floors, Spaces, ThermalZones, Surfaces y Sensors.

### KIT-03 — Extension structure baseline

Crear estructura mínima de extensiones Siamese.

### KIT-04 — Theme system MVP

Crear estilo visual Siamese: blanco, negro, grises y acento cian.

### KIT-05 — Selection and inspector MVP

Seleccionar entidades USD y mostrar metadata contextual.

### KIT-06 — Backend API bridge MVP

Crear cliente Kit para consultar backend Siamese.

### KIT-07 — Simulation run panel MVP

Permitir crear SimulationCase y consultar estado del job.

### KIT-08 — ThermalViz MVP

Visualizar resultados normalizados como capa térmica por zona.

### KIT-09 — Sensor mapping MVP

Representar sensores y su relación con zonas.

### KIT-10 — Agentic panel placeholder

Reservar espacio para chat, roadmap, kanban y approvals sin activar automatización avanzada.

---

## 36. Decisión arquitectónica final

La decisión que debe guiar la implementación es:

```text
Omniverse Kit será la interfaz gráfica modular y semántica de Siamese, no su backend.
```

Todo lo demás deriva de ahí:

```text
Kit visualiza;
Kit permite interacción;
Kit aloja extensiones;
Kit trabaja sobre USD;
Kit se conecta al backend;
Kit no ejecuta lógica energética crítica;
Kit no almacena datos masivos;
Kit no sustituye al motor agéntico;
Kit presenta y gobierna acciones mediante comandos, permisos y evidencias.
```

Esta frontera permitirá que Siamese crezca como una plataforma robusta, escalable y verdaderamente agéntica.

---

## 37. Referencias externas consultadas

- NVIDIA Omniverse Kit — Overview.  
  https://docs.omniverse.nvidia.com/kit/docs/kit-manual/latest/guide/kit_overview.html

- NVIDIA Omniverse Kit — Architecture.  
  https://docs.omniverse.nvidia.com/kit/docs/kit-manual/109.0.6/guide/kit_architecture.html

- NVIDIA Omniverse Extensions — Overview.  
  https://docs.omniverse.nvidia.com/extensions/latest/overview.html

- NVIDIA Omniverse Kit — Kit SDK Extensions.  
  https://docs.omniverse.nvidia.com/kit/docs/kit-manual/latest/guide/kit_exts.html

- NVIDIA Omniverse Kit — USD Schema Extensions.  
  https://docs.omniverse.nvidia.com/kit/docs/kit-manual/latest/guide/extensions_usd_schema.html

- NVIDIA Omniverse — Developing with OpenUSD.  
  https://docs.omniverse.nvidia.com/dev-guide/latest/dev-usd.html

- NVIDIA Omniverse — Live Session Management.  
  https://docs.omniverse.nvidia.com/extensions/latest/ext_core/ext_live/sessions.html

- NVIDIA Omniverse — OmniLive.  
  https://docs.omniverse.nvidia.com/extensions/latest/ext_core/ext_live.html

---

## 38. Referencias internas de proyecto

- `digital_twin_contexto_maestro.md` — visión general de Siamese, macroproyectos, arquitectura modular, principios EnergyPlus/Omniverse/USD/agentes.
- `siamese_energyplus_context.md` — EnergyPlus como solver físico.
- `siamese_python_backend_context.md` — backend Python como capa que convierte EnergyPlus en producto.
- Presentación Siamese — narrativa del TFG, modelo muerto y nacimiento de Siamese como Living Energy Twin.
