# Siamese — Módulo NVIDIA Omniverse Nucleus

**Documento:** Contexto técnico del módulo Nucleus dentro de Siamese  
**Proyecto:** Siamese — plataforma agéntica de gemelos digitales energéticos  
**Estado:** Documento de arquitectura conceptual previo a implementación  
**Versión:** 0.1  
**Propósito:** definir el papel de NVIDIA Omniverse Nucleus en Siamese como capa de colaboración, almacenamiento de assets OpenUSD, permisos, versionado, conexión entre herramientas mediante conectores y soporte para flujos multiusuario/agénticos.

---

## 1. Resumen ejecutivo

NVIDIA Omniverse Nucleus será la capa de colaboración y gestión de assets OpenUSD de Siamese.

No es el solver energético.  
No es el backend Python.  
No es la base de datos principal de sensores.  
No es el motor de calibración.  
No es el sistema de agentes.  

Su función es permitir que el gemelo energético exista como un activo digital compartido, versionado y conectado con diferentes herramientas de diseño, simulación y visualización.

La frase central del módulo:

> **Omniverse Kit es donde trabajas. OpenUSD es el formato común. Nucleus es la infraestructura que permite que ese trabajo viva, se comparta, se versione y se conecte con otras plataformas.**

En Siamese:

```text
OpenUSD
→ estructura geométrica y semántica del edificio

Omniverse Kit
→ interfaz visual y workspace de ingeniería

Nucleus
→ colaboración, almacenamiento, permisos, versionado y conectores
```

---

## 2. Qué es Nucleus dentro de Siamese

Nucleus debe entenderse como la infraestructura colaborativa para trabajar con assets OpenUSD.

Responsabilidades principales:

```text
almacenar stages USD;
almacenar layers USD;
servir assets a Omniverse Kit;
gestionar permisos;
facilitar colaboración multiusuario;
permitir versionado/checkpoints;
soportar live workflows cuando aplique;
conectar herramientas externas mediante Omniverse Connectors;
almacenar SimReady Energy Assets;
soportar Reference Designs;
proveer una base visual compartida para humanos y agentes.
```

No debe asumir responsabilidades de backend computacional.

Nucleus debe ser:

```text
asset collaboration layer
```

No:

```text
operational data layer
```

---

## 3. Por qué Nucleus es importante

Siamese no está pensado como una herramienta local de un único usuario. Un gemelo energético real implica múltiples perfiles:

```text
ingeniero energético;
arquitecto;
modelador AEC;
facility manager;
responsable de mantenimiento;
consultora energética;
cliente;
agentes IA;
desarrolladores;
proveedores externos;
auditores.
```

Cada perfil puede necesitar trabajar sobre distintas partes del gemelo:

```text
geometría;
materiales;
zonas térmicas;
sensores;
HVAC;
resultados visuales;
escenarios;
anotaciones;
revisiones;
capas de análisis;
propuestas de agentes.
```

Sin Nucleus o una capa equivalente, el flujo sería frágil:

```text
archivos locales;
versiones duplicadas;
envíos por correo;
modelos desactualizados;
exportaciones/importaciones manuales;
pérdida de trazabilidad;
dificultad para colaborar.
```

Con Nucleus:

```text
el stage USD vive en un servidor colaborativo;
los usuarios trabajan sobre la misma base visual;
los permisos delimitan quién puede editar;
los conectores traen datos desde otras herramientas;
las capas USD separan responsabilidades;
Kit visualiza e interactúa sobre assets compartidos.
```

---

## 4. Frontera arquitectónica

La frontera debe ser estricta.

### Nucleus debe guardar

```text
USD stages;
USD layers;
assets;
textures;
materials;
references;
payloads;
visualization layers;
scenario layers;
annotation layers;
SimReady Energy Assets;
building geometry;
openUSD reference designs.
```

### Nucleus no debe guardar como fuente principal

```text
series temporales grandes;
datasets ML completos;
logs crudos;
resultados masivos de EnergyPlus;
modelos surrogados pesados;
credenciales;
históricos operativos completos;
facturación;
jobs internos del backend;
permisos de negocio fuera del ámbito USD;
eventos de sensórica en bruto.
```

Regla:

```text
Nucleus = asset collaboration layer.
Backend Siamese = operational and computational authority.
```

---

## 5. Relación con OpenUSD

Nucleus es valioso porque el formato común de colaboración es OpenUSD.

OpenUSD permite representar el edificio como una composición de:

```text
prims;
atributos;
relaciones;
metadatos;
capas;
references;
payloads;
variants;
sublayers;
bindings;
schemas;
annotations.
```

Siamese puede representar entidades como:

```text
/World/Building
/World/Building/Floors/Floor_01
/World/Building/Spaces/Aula_3B
/World/Building/ThermalZones/Zone_Aula_3B
/World/Building/Sensors/Sensor_Aula_3B
/World/Building/HVAC/Radiator_Aula_3B
/World/Building/Results/ThermalMap_Run_001
/World/Building/Annotations/CalibrationIssue_004
```

Nucleus permite que ese stage se aloje, comparta y versiona para equipos humanos y agentes.

---

## 6. Capas USD recomendadas

Para que la colaboración sea robusta, Siamese no debe guardar todo en un único archivo USD monolítico.

Propuesta de capas:

```text
00_base_geometry.usd
→ geometría base del edificio.

01_aec_semantics.usd
→ spaces, surfaces, openings, materials.

02_energy_semantics.usd
→ thermal zones, constructions, schedules metadata.

03_hvac_semantics.usd
→ equipos HVAC, conexiones, actuadores, sistemas.

04_sensor_bindings.usd
→ sensores, ubicación, relaciones sensor-zona.

05_simulation_results.usd
→ capas visuales de resultados EnergyPlus.

06_calibration_results.usd
→ mapas de error, zonas calibradas, estado de calibración.

07_surrogate_predictions.usd
→ predicción actual/futura y confianza.

08_control_recommendations.usd
→ recomendaciones, shadow mode, acciones propuestas.

09_user_annotations.usd
→ notas, issues, revisiones, comentarios.

10_agent_annotations.usd
→ propuestas de agentes, tareas, evidencias visuales.
```

Esta separación permite gobernar edición y permisos por responsabilidad.

Ejemplo:

```text
arquitecto
→ edita 00/01.

ingeniero energético
→ edita 02/03.

equipo de sensores
→ edita 04.

backend
→ genera 05/06/07/08.

agente
→ escribe propuestas en 10.

cliente
→ lee y comenta en 09.
```

---

## 7. Permisos y roles

Nucleus debe utilizarse con una estrategia de permisos clara. Los permisos deben combinarse con la gobernanza interna de Siamese.

Roles propuestos:

```text
Owner / Admin
Energy Engineer
AEC Modeler
HVAC Engineer
Sensor Engineer
Facility Manager
Client Viewer
External Consultant
Agent
Auditor
Backend Service
```

### Matriz conceptual

```text
Owner / Admin
→ administra proyecto, permisos y capas.

AEC Modeler
→ edita geometría y semántica AEC.

Energy Engineer
→ edita zonas térmicas, construcciones y escenarios.

HVAC Engineer
→ edita sistemas HVAC y relaciones operativas.

Sensor Engineer
→ edita sensor bindings.

Facility Manager
→ revisa estado operativo, alertas, recomendaciones y comentarios.

Client Viewer
→ acceso read-only a modelo, resultados e informes.

External Consultant
→ permisos acotados por proyecto/capa.

Agent
→ escribe solo proposal/annotation layers.

Auditor
→ read-only sobre histórico, reports y evidence.

Backend Service
→ escribe capas generadas y metadata de resultados.
```

Regla crítica:

```text
Los agentes no editan capas fuente críticas.
Los agentes escriben propuestas.
La promoción requiere aprobación humana o backend autorizado.
```

---

## 8. Permisos por capa

El modelo de permisos debería ser por carpeta, archivo y tipo de layer.

Ejemplo:

```text
00_base_geometry.usd
→ write: AEC Lead / Admin
→ read: Energy Engineer, Client Viewer

02_energy_semantics.usd
→ write: Energy Engineer
→ read: AEC Modeler, Facility Manager

04_sensor_bindings.usd
→ write: Sensor Engineer + Energy Engineer
→ read: Facility Manager, Agent

05_simulation_results.usd
→ write: Backend Service
→ read: todos los roles técnicos

06_calibration_results.usd
→ write: Backend Service
→ approve: Energy Engineer

10_agent_annotations.usd
→ write: Agent
→ review: Human roles
```

Esto evita que un cambio visual destruya una geometría base o una semántica energética validada.

---

## 9. Live collaboration

Nucleus puede habilitar colaboración en tiempo real o sincronización live según la aplicación y el conector. Sin embargo, Siamese debe tratar esta funcionalidad con prudencia.

No se debe asumir que todos los conectores son:

```text
bidireccionales;
igual de maduros;
sin pérdida de metadata;
aptos para edición simultánea;
autoridad de datos.
```

Uso recomendado:

```text
colaboración visual;
revisión de geometría;
anotaciones;
sincronización de propuestas;
revisión multiusuario;
validación de diseño;
presentaciones con cliente;
sesiones de ingeniería.
```

No recomendado:

```text
actualizar modelos energéticos críticos sin validación;
promocionar cambios live directamente a EnergyPlus;
permitir que un conector externo sobrescriba capas validadas;
usar live sync como fuente de verdad sin control.
```

Patrón correcto:

```text
Live Sync / Connector
→ import/sync layer
→ validation
→ review
→ promotion
→ source layer
```

---

## 10. Conectores Omniverse

Una de las capacidades estratégicas de Nucleus es que puede actuar como punto de conexión entre plataformas mediante Omniverse Connectors.

Los conectores traducen entre aplicaciones nativas y OpenUSD, permitiendo que distintas herramientas colaboren sobre assets compartidos.

Herramientas relevantes:

```text
Revit;
Blender;
Unreal Engine;
Unity;
herramientas CAD/BIM;
herramientas de visualización;
apps propias;
conectores custom.
```

Esto evita que Siamese sea una isla. El gemelo puede vivir como activo OpenUSD conectado a herramientas existentes.

---

## 11. Revit Connector

Revit es crítico porque muchos edificios existentes tienen modelos BIM.

Flujo recomendado:

```text
Revit BIM
→ Omniverse Revit Connector
→ USD en Nucleus
→ Siamese Kit
→ enriquecimiento AEC/energético
→ backend EnergyPlus
→ simulación/calibración
```

Uso en Siamese:

```text
importar geometría BIM;
mantener referencia con modelo arquitectónico;
detectar espacios;
generar candidatos de zonas térmicas;
mapear sensores;
comparar cambios de diseño;
iniciar Adoption Model desde BIM.
```

Advertencia:

```text
Un modelo Revit no es automáticamente un modelo energético válido.
```

Siamese debe validar:

```text
zonificación;
cerramientos;
superficies;
openings;
materiales;
boundaries;
sombras;
calibrabilidad;
compatibilidad EnergyPlus.
```

---

## 12. Blender Connector

Blender puede ser útil para assets, limpieza visual y preparación de geometría.

Uso en Siamese:

```text
modelado auxiliar;
limpieza de assets;
creación de componentes;
preparación visual de SimReady Energy Assets;
edición de materiales;
assets HVAC o sensores;
demos visuales.
```

Ejemplo:

```text
radiador modelado en Blender
→ USD asset en Nucleus
→ Siamese añade metadata energética
→ asset reutilizable en proyectos
```

Regla:

```text
Blender puede ser fuente visual de assets.
No debe ser autoridad energética.
```

---

## 13. Unreal / Unity Connectors

Unreal y Unity pueden ser útiles para visualización inmersiva, demos comerciales y experiencias interactivas.

Uso:

```text
VR/AR;
demos cliente;
visualización externa;
formación;
experiencias interactivas;
entornos comerciales;
simulación visual simplificada.
```

No deben ser:

```text
backend energético;
fuente de verdad;
motor de calibración;
sistema de control.
```

Arquitectura:

```text
Siamese backend + USD/Nucleus
→ Unreal/Unity client
```

---

## 14. Conectores custom

Siamese probablemente necesitará conectores propios.

Posibles conectores:

```text
DesignBuilder → Siamese/OpenUSD;
OpenStudio → Siamese/OpenUSD;
IFC → Siamese/OpenUSD;
DXF/CAD → Siamese/OpenUSD;
EnergyPlus IDF/epJSON → Siamese;
BMS → Siamese Exchange;
Sensor platforms → Siamese;
Notion/Calendar/Gmail → Siamese workflows;
repository/agent tools → Siamese Operating Harness.
```

A futuro puede existir:

```text
Siamese Connector SDK
```

Objetivo:

```text
permitir que terceros conecten herramientas, datos o plataformas al gemelo energético.
```

---

## 15. Nucleus dentro del Siamese Adoption Model

Nucleus es especialmente importante para el modelo de adopción de activos existentes.

Adoptar un modelo no significa solo importar IDF. Puede incluir:

```text
Revit model;
IFC model;
Blender geometry;
Unreal scene;
DesignBuilder export;
OpenStudio model;
CAD/DXF plans;
USD assets;
assets HVAC de fabricantes;
modelos parciales existentes.
```

Flujo:

```text
Cliente sube o conecta modelo
→ Nucleus almacena USD/assets
→ Siamese analiza
→ genera Model Quality Report
→ crea roadmap de adopción
→ enriquece semántica
→ conecta EnergyPlus/sensores/calibración
→ convierte activo existente en gemelo vivo
```

Valor comercial:

> **Siamese no exige empezar de cero. Puede adoptar y revivir activos digitales existentes.**

---

## 16. Nucleus y agentes

Los agentes deben poder leer y proponer sobre Nucleus, pero no modificar capas críticas sin control.

### Permitido

```text
leer estructura del stage;
listar capas;
identificar assets;
crear anotaciones;
proponer cambios;
crear tareas;
generar capas de propuesta;
validar consistencia;
crear reportes;
detectar entidades sin metadata;
detectar sensores sin zona;
detectar cambios que requieren recalibración.
```

### No permitido sin aprobación

```text
modificar geometría base;
sobrescribir capas de ingeniería;
eliminar assets;
promocionar propuesta a fuente de verdad;
cambiar permisos;
publicar resultados como definitivos;
activar control operativo;
modificar capas de calibración aprobadas.
```

Patrón correcto:

```text
Agent writes proposal layer
→ human reviews
→ approval gate
→ backend/authorized command promotes
```

Ejemplo:

```text
Agent detecta que Aula_3B no tiene sensor asignado.
↓
Crea annotation en agent_annotations.usd.
↓
Crea task en roadmap.
↓
Propone binding sensor-zona.
↓
Sensor engineer aprueba.
↓
Backend actualiza sensor_bindings.usd.
```

---

## 17. Versionado y checkpoints

Nucleus debe aprovecharse para versionar assets y conservar estados históricos.

Casos:

```text
comparar geometría antes/después;
recuperar una versión estable;
auditar cambios;
separar ramas de diseño;
mantener versiones por cliente;
revisar antes de promover;
gestionar entregables;
comparar escenarios visuales.
```

Pero Nucleus versiona principalmente assets/stages. Siamese también debe versionar internamente:

```text
EnergyModel;
SimulationCase;
SimulationRun;
CalibrationJob;
DatasetCampaign;
SurrogateModel;
ControlPolicy;
Recommendation;
SensorDataset.
```

Relación:

```text
Nucleus checkpoint
→ versiona asset/stage USD.

Backend provenance
→ versiona cálculo, datos y decisiones.
```

Ambos deben enlazarse mediante IDs, URLs, checksums y metadata.

---

## 18. Arquitectura del módulo Nucleus

```text
Siamese Collaboration Layer
│
├── Nucleus Server / Cloud
│   ├── USD stages
│   ├── USD layers
│   ├── SimReady assets
│   ├── textures/materials
│   ├── scenario layers
│   └── annotation layers
│
├── Connectors
│   ├── Revit
│   ├── Blender
│   ├── Unreal
│   ├── Unity
│   ├── IFC/CAD future
│   └── Siamese custom connectors
│
├── Siamese Kit App
│   ├── viewport
│   ├── layer manager
│   ├── inspectors
│   ├── simulation overlays
│   └── agent panels
│
├── Siamese Backend
│   ├── model registry
│   ├── simulation registry
│   ├── sensor registry
│   ├── result registry
│   └── provenance mapping
│
└── Permission/Governance Layer
    ├── roles
    ├── ACLs
    ├── approval gates
    ├── promotion rules
    └── audit log
```

---

## 19. Relación con Omniverse Kit

Kit será el cliente visual principal de Nucleus.

Kit debe:

```text
abrir stages desde Nucleus;
mostrar layers;
permitir edición según permisos;
mostrar conflictos;
crear anotaciones;
visualizar resultados;
mostrar live state;
lanzar comandos backend;
crear tareas agénticas;
consultar approvals;
visualizar propuestas de agentes.
```

Kit no debe:

```text
saltarse permisos;
guardar cambios críticos sin validación;
mezclar resultados en geometría base;
tratar USD como única base de datos;
ejecutar simulaciones sin backend;
promocionar propuestas sin approval.
```

---

## 20. Relación con backend Python

El backend debe registrar la identidad de los assets Nucleus relevantes.

Ejemplo:

```yaml
BuildingAsset:
  building_id: building_001
  nucleus_stage_url: omniverse://server/projects/building_001/main.usd
  geometry_layer: 00_base_geometry.usd
  energy_layer: 02_energy_semantics.usd
  sensor_layer: 04_sensor_bindings.usd
  current_stage_version: checkpoint_abc
```

Cuando el backend ejecute una simulación, debe registrar:

```text
qué stage se usó;
qué layers estaban activos;
qué versión/checkpoint;
qué EnergyModel derivó;
qué compiler version;
qué EnergyPlus version;
qué outputs se generaron;
qué results layer se escribió.
```

Esto garantiza reproducibilidad.

---

## 21. Relación con EnergyPlus

EnergyPlus no debe leer directamente desde Nucleus.

Flujo correcto:

```text
Nucleus / USD stage
→ Siamese Kit or backend reads USD
→ USD-to-Energy mapper
→ Siamese EnergyModel
→ EnergyPlus compiler
→ EnergyPlus run
→ normalized results
→ Results-to-USD visualization layer
→ Nucleus
```

Nucleus aloja la escena y capas.  
Backend deriva modelo energético y ejecuta simulaciones.

---

## 22. Relación con sensórica

Los sensores pueden representarse en USD como prims, pero sus lecturas deben vivir fuera.

Ejemplo:

```yaml
SensorPrim:
  path: /World/Building/Sensors/Sensor_Aula_3B_Temp
  sensor_id: sensor_aula_3b_temp_01
  zone_id: aula_3b
  variable: zone_air_temperature
  timeseries_ref: tsdb://building_001/sensor_aula_3b_temp_01
```

Nucleus almacena:

```text
posición;
identidad;
binding;
metadata;
visual layer.
```

Timeseries DB almacena:

```text
lecturas históricas;
quality flags;
estado live;
datos agregados;
features.
```

---

## 23. Relación con calibración

La calibración puede generar capas visuales en Nucleus:

```text
calibration_error_map.usd;
calibrated_zones.usd;
pareto_candidate_annotations.usd;
sensor_vs_simulated_overlay.usd;
```

Pero las métricas completas deben vivir en backend:

```text
CVRMSE;
NMBE;
NMAE;
candidate parameters;
simulation runs;
calibration report;
approval status;
selected candidate;
calibrated model version.
```

Regla:

```text
Nucleus visualiza y comparte.
Backend gobierna y calcula.
```

---

## 24. Relación con resultados y visualización

El backend puede generar capas USD visuales para resultados:

```text
thermal_map_run_001.usd;
surface_temperature_run_001.usd;
comfort_status_run_001.usd;
prediction_layer_live.usd;
control_recommendations.usd;
```

Estas capas se guardan en Nucleus para que usuarios y herramientas las consuman.

Pero los datos completos permanecen en backend/storage:

```text
timeseries;
tables;
diagnostics;
logs;
reports;
normalized results.
```

---

## 25. Relación con Reference Designs

Los Siamese Reference Designs pueden distribuirse como paquetes USD/Nucleus.

Ejemplo:

```text
school_energy_twin_template/
├── base_stage.usd
├── layer_templates/
├── sensor_layout.usd
├── hvac_templates.usd
├── material_library.usd
├── simulation_presets.json
├── calibration_roadmap.json
└── documentation.md
```

Uso:

```text
nuevo colegio
→ crear proyecto desde School Reference Design
→ adaptar geometría
→ mapear sensores
→ calibrar
→ operar
```

Esto permite convertir metodología en producto.

---

## 26. Relación con SimReady Energy Assets

Nucleus será el repositorio natural de assets energéticos:

```text
assets/
├── hvac/
├── sensors/
├── construction/
├── renewables/
├── batteries/
├── controls/
└── templates/
```

Cada asset puede ser USD + metadata:

```text
visual geometry;
simulation metadata;
EnergyPlus template;
connector points;
control properties;
maintenance metadata;
versioning.
```

Ejemplo:

```text
assets/hvac/radiator_standard_v1.usd
assets/sensors/temp_humidity_sensor_v1.usd
assets/renewables/pv_panel_v1.usd
```

---

## 27. Arquitectura de proyecto en Nucleus

Estructura conceptual:

```text
omniverse://siamese-server/
│
├── projects/
│   └── building_001/
│       ├── stages/
│       │   ├── main.usd
│       │   └── variants/
│       ├── layers/
│       │   ├── 00_base_geometry.usd
│       │   ├── 01_aec_semantics.usd
│       │   ├── 02_energy_semantics.usd
│       │   ├── 03_hvac_semantics.usd
│       │   ├── 04_sensor_bindings.usd
│       │   ├── 05_simulation_results/
│       │   ├── 06_calibration_results/
│       │   ├── 07_surrogate_predictions/
│       │   ├── 08_control_recommendations/
│       │   ├── 09_user_annotations.usd
│       │   └── 10_agent_annotations.usd
│       ├── assets/
│       ├── references/
│       └── exports/
│
├── assets/
│   ├── hvac/
│   ├── sensors/
│   ├── materials/
│   ├── renewables/
│   └── templates/
│
└── reference_designs/
    ├── school/
    ├── hospital/
    ├── campus/
    └── office/
```

---

## 28. MVP del módulo Nucleus

### Objetivo MVP

Usar Nucleus para almacenar y compartir un stage USD del edificio con capas separadas y permisos básicos.

### Alcance MVP

```text
crear estructura de proyecto en Nucleus;
subir stage USD base;
abrir stage desde Siamese Kit;
crear layer de anotaciones;
crear layer de resultados;
definir roles básicos;
probar read/write/admin;
guardar referencia backend al stage;
probar export desde Blender o Revit si está disponible.
```

### Fuera del MVP

```text
live sync bidireccional completo;
conectores propios;
multiempresa avanzada;
control operativo;
workflow avanzado de aprobación;
SimReady library completa;
Reference Designs completos.
```

---

## 29. Evolución por fases

### Fase 1 — Nucleus Project Structure

```text
projects/
assets/
templates/
results/
annotations/
```

### Fase 2 — Layer Convention

```text
base geometry;
AEC semantics;
energy semantics;
HVAC;
sensors;
results;
annotations;
agent proposals.
```

### Fase 3 — Permissions MVP

```text
admin;
engineer;
viewer;
agent-proposal-only.
```

### Fase 4 — Kit Integration

```text
open stage;
layer manager;
save layer;
show permissions;
create annotation.
```

### Fase 5 — Backend Mapping

```text
stage URL;
layer IDs;
checkpoints;
model derivation;
run provenance.
```

### Fase 6 — Connectors Evaluation

```text
Revit;
Blender;
Unreal;
Unity;
IFC/CAD custom.
```

### Fase 7 — Agent Proposal Layers

```text
agent writes proposals;
human approves;
backend promotes.
```

### Fase 8 — Reference Designs / SimReady Assets

```text
templates;
asset libraries;
sector packages.
```

---

## 30. Primeros tickets recomendados

### NUC-00 — Nucleus module context

Crear documentación conceptual del módulo.

### NUC-01 — Nucleus project structure strategy

Definir estructura de carpetas/proyectos en Nucleus.

### NUC-02 — USD layer convention

Definir convención de capas Siamese.

### NUC-03 — Nucleus permission model

Definir roles y permisos por capa.

### NUC-04 — Backend Nucleus asset registry

Crear contrato `BuildingAsset` con `nucleus_stage_url`, layers y checkpoints.

### NUC-05 — Kit open stage from Nucleus

Abrir stage remoto desde la app Kit.

### NUC-06 — Annotation layer MVP

Crear capa de anotaciones de usuario.

### NUC-07 — Results layer MVP

Guardar capa visual de resultados generada por backend.

### NUC-08 — Agent proposal layer

Permitir que agentes escriban propuestas en layer separada.

### NUC-09 — Connector evaluation: Revit

Evaluar import/export/sync de Revit hacia USD/Nucleus.

### NUC-10 — Connector evaluation: Blender

Evaluar flujo Blender → USD asset → Nucleus → Siamese.

### NUC-11 — SimReady asset repository strategy

Diseñar repositorio de assets energéticos.

### NUC-12 — Reference design package structure

Diseñar estructura de paquetes por tipo de edificio.

---

## 31. Riesgos principales

### Riesgo 1 — Vendor dependency

Mitigación:

```text
USD válido;
export local;
backend independiente;
Nucleus adapter;
no guardar datos críticos solo en Nucleus.
```

### Riesgo 2 — Confundir live sync con colaboración perfecta

Mitigación:

```text
documentar dirección de sincronización por conector;
usar approval/promotion;
no asumir bidireccionalidad.
```

### Riesgo 3 — Permisos débiles

Mitigación:

```text
ACLs;
roles;
capas separadas;
agentes en proposal layers;
approval gates.
```

### Riesgo 4 — Meter datos pesados en USD

Mitigación:

```text
series temporales fuera;
datasets fuera;
USD como binding/visualización.
```

### Riesgo 5 — Romper el modelo energético con cambios geométricos

Mitigación:

```text
Model Quality Report;
diff de geometría;
validación antes de recalcular;
roadmap de actualización;
approval gates.
```

### Riesgo 6 — Conectores con pérdida semántica

Mitigación:

```text
validación post-import;
no asumir equivalencia energética;
mantener mapping explícito;
crear reportes de calidad.
```

---

## 32. Valor comercial

Nucleus permite contar una historia fuerte:

> **Siamese no es una herramienta cerrada. Es un workspace conectado al ecosistema OpenUSD.**

Beneficios para clientes:

```text
reutilizar modelos Revit;
preparar assets en Blender;
visualizar en Omniverse;
crear demos en Unreal/Unity;
colaborar sobre el mismo gemelo;
separar permisos por rol;
mantener trazabilidad visual;
adoptar activos digitales existentes;
trabajar con partners externos.
```

Esto reduce fricción de adopción. Siamese no obliga al cliente a abandonar sus herramientas actuales: conecta su stack existente mediante OpenUSD/Nucleus.

---

## 33. Frases de presentación

Frase principal:

> **Nucleus convierte el gemelo energético en un activo colaborativo.**

Frase técnica:

> **Siamese usa Nucleus para almacenar, versionar y compartir stages OpenUSD, gestionar permisos por capas y conectar herramientas como Revit, Blender, Unreal o Unity mediante conectores.**

Frase comercial:

> **El edificio no queda atrapado en una herramienta. Vive como un activo OpenUSD colaborativo, conectado al ecosistema de diseño, simulación y operación.**

---

## 34. Decisión arquitectónica final

La decisión central:

```text
Nucleus será la capa colaborativa de assets OpenUSD,
pero no será la autoridad computacional ni operativa de Siamese.
```

Arquitectura final:

```text
OpenUSD estructura.
Nucleus colabora.
Omniverse Kit interactúa.
Backend gobierna.
EnergyPlus calcula.
Sensórica observa.
Calibración ajusta.
Surrogates predicen.
Agentes orquestan.
```

Siamese debe ser:

```text
Nucleus-compatible,
OpenUSD-native,
backend-governed,
agent-safe,
not Nucleus-dependent for core computation.
```

---

## 35. Relación con documentos previos

Este módulo complementa:

```text
siamese_energyplus_context.md
→ EnergyPlus como solver físico.

siamese_python_backend_context.md
→ backend Python como capa de gobierno.

siamese_omniverse_kit_context.md
→ Omniverse Kit como interfaz visual y extensible.

siamese_calibration_module_context.md
→ calibración como puente modelo-realidad.

siamese_sensorics_module_context.md
→ sensórica como observación real.

siamese_dsx_ecosystem_context.md
→ DSX como referencia estratégica y ecosistema NVIDIA.

digital_twin_contexto_maestro.md
→ visión general modular del producto.
```

Y prepara:

```text
Siamese Adoption Model;
SimReady Energy Assets;
Reference Designs;
Collaboration & Deployment;
Agentic Workflow Engine;
Connector SDK.
```
