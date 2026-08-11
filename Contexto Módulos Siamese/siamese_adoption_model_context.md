# Siamese — Módulo Siamese Adoption Model

**Documento:** Contexto técnico y estratégico del módulo Siamese Adoption Model  
**Proyecto:** Siamese — plataforma agéntica de gemelos digitales energéticos  
**Estado:** Documento de arquitectura conceptual previo a implementación  
**Versión:** 0.1  
**Propósito:** definir cómo Siamese importará, traducirá, auditará y adoptará modelos, archivos, datos y activos existentes procedentes de EnergyPlus, DesignBuilder, OpenStudio, Revit, IFC, DXF, OpenUSD, CSV, plataformas externas y conectores personalizados.

---

## 1. Resumen ejecutivo

El **Siamese Adoption Model** es el módulo encargado de convertir activos digitales existentes en gemelos energéticos vivos dentro de Siamese.

Su función no es simplemente importar archivos. Importar es leer un activo. Adoptar es entenderlo, auditarlo, normalizarlo, enriquecerlo, conectarlo a Nucleus, prepararlo para EnergyPlus, vincularlo con sensores, calibrarlo y convertirlo en una infraestructura operativa.

La frase central del módulo es:

> **Siamese no obliga a empezar de cero: adopta modelos existentes y los convierte en gemelos vivos.**

Flujo conceptual:

```text
modelo existente / archivo / BIM / CAD / IDF / OSM / USD / CSV
        ↓
adopción controlada
        ↓
modelo Siamese normalizado
        ↓
validación de calidad
        ↓
enriquecimiento semántico
        ↓
calibración
        ↓
gemelo energético vivo
```

Este módulo es estratégico porque una gran parte del mercado ya tendrá activos previos:

```text
modelos DesignBuilder;
modelos OpenStudio;
archivos EnergyPlus IDF;
archivos epJSON;
modelos Revit;
modelos IFC;
geometría CAD/DXF;
modelos Blender;
escenas Unreal/Unity;
datos CSV de sensores;
informes energéticos antiguos;
auditorías previas;
modelos académicos;
gemelos digitales incompletos.
```

El Siamese Adoption Model permite transformar esos activos, que normalmente quedan archivados, en modelos conectados, calibrables, reutilizables y operativos.

---

## 2. Problema que resuelve

Muchos clientes no parten de cero. Pueden tener modelos creados para:

```text
auditorías energéticas;
certificaciones;
proyectos académicos;
TFGs/TFMs;
consultorías previas;
diseño BIM;
análisis de eficiencia;
informes de sostenibilidad;
reformas;
operación de mantenimiento.
```

Pero esos activos suelen estar:

```text
desconectados;
sin mantenimiento;
sin datos reales;
sin trazabilidad;
sin operación;
sin calibración actualizada;
sin integración con sensores;
sin visualización viva;
sin uso después del informe final.
```

El problema comercial:

```text
Ya pagué por un modelo, pero ahora está muerto.
```

La respuesta de Siamese:

```text
No pierdas lo que ya tienes.
Lo adoptamos, lo auditamos y lo convertimos en infraestructura viva.
```

---

## 3. Importar no es adoptar

### 3.1 Importar

Importar significa:

```text
leer un archivo;
abrirlo en una herramienta;
convertirlo parcialmente;
visualizarlo;
extraer algunos datos.
```

Ejemplo:

```text
Subir un IDF y ejecutarlo.
```

Eso es útil, pero insuficiente.

### 3.2 Adoptar

Adoptar significa:

```text
leer el activo;
entender qué contiene;
detectar qué falta;
mapearlo al dominio Siamese;
validarlo;
versionarlo;
conectarlo a USD/Nucleus;
prepararlo para EnergyPlus;
mapearlo a sensores;
calibrarlo;
hacerlo operativo.
```

Ejemplo:

```text
Subir un IDF de DesignBuilder,
analizar su calidad,
mapear zonas y superficies,
detectar HVAC simplificado,
conectar sensores históricos,
generar un roadmap de calibración
y convertirlo en un modelo Siamese versionado.
```

Frase clave:

> **Importar trae un archivo. Adoptar convierte ese archivo en un gemelo vivo.**

---

## 4. Relación con la historia original de Siamese

El origen de Siamese está directamente relacionado con este módulo.

En el TFG del C.E.P. Divino Maestro se creó un modelo del edificio en DesignBuilder, se instalaron sensores de temperatura y humedad, se calibró el modelo con datos reales y se analizaron mejoras energéticas. Sin embargo, después del proyecto, el modelo quedó archivado y no siguió conectado al edificio.

Siamese Adoption Model existe para evitar que eso ocurra.

Transformación:

```text
TFG:
modelo DesignBuilder calibrado
→ informe
→ archivo muerto

Siamese:
modelo existente
→ adopción
→ auditoría
→ recalibración
→ sensores
→ datasets
→ surrogates
→ operación continua
```

La propuesta comercial es clara:

> **Si tu edificio ya fue modelado, Siamese puede revivirlo.**

---

## 5. Arquitectura general

Arquitectura conceptual:

```text
External Assets
    ↓
Connector / Import Adapter
    ↓
Raw Asset Registry
    ↓
Parser / Reader
    ↓
Canonical Mapping
    ↓
Siamese Intermediate Model
    ↓
Quality Audit
    ↓
Semantic Enrichment
    ↓
Nucleus / OpenUSD Binding
    ↓
EnergyPlus Backend Compatibility
    ↓
Sensor Binding / Calibration Readiness
    ↓
Adopted Twin
```

Arquitectura detallada:

```text
DesignBuilder / IDF / epJSON / OSM / Revit / IFC / DXF / USD / CSV
        ↓
Siamese Adoption Connectors
        ↓
Raw Imported Artifact
        ↓
Format-specific parser
        ↓
Canonical Entity Extraction
        ↓
Siamese Domain Model
        ↓
Model Quality Report
        ↓
Repair / Enrichment Tasks
        ↓
OpenUSD/Nucleus Project
        ↓
EnergyPlus SimulationCase
        ↓
Calibration Roadmap
        ↓
Living Energy Twin
```

---

## 6. Entidades principales del módulo

El módulo necesita contratos propios para que cada adopción sea trazable.

Entidades principales:

```text
ImportedAsset
ImportJob
SourceFormat
ConnectorProfile
Parser
MappingReport
AdoptionCandidate
ModelQualityReport
RepairTask
SemanticEnrichmentTask
AdoptionRoadmap
AdoptedModel
```

### 6.1 ImportedAsset

Representa el activo original recibido.

```yaml
ImportedAsset:
  id: imported_asset_001
  source_type: designbuilder_export
  source_path: uploads/divino_maestro_model.idf
  format: idf
  uploaded_by: user
  created_at: timestamp
  checksum: sha256
  status: parsed
```

### 6.2 ImportJob

Representa el proceso de importación.

```yaml
ImportJob:
  id: import_job_001
  imported_asset_id: imported_asset_001
  connector_profile: designbuilder_idf_v1
  status: completed
  started_at: timestamp
  finished_at: timestamp
  mapping_report_id: mapping_report_001
  quality_report_id: quality_report_001
```

### 6.3 MappingReport

Describe cómo se tradujo el activo externo al dominio Siamese.

```yaml
MappingReport:
  id: mapping_report_001
  imported_asset_id: imported_asset_001
  mapped_entities:
    thermal_zones: 24
    surfaces: 312
    constructions: 18
    schedules: 11
    hvac_systems: 2
  unresolved_entities:
    - object_id: unknown_schedule_04
      reason: missing_reference
```

### 6.4 ModelQualityReport

Entregable central de la adopción.

```yaml
ModelQualityReport:
  id: quality_report_001
  imported_asset_id: imported_asset_001
  geometry_status: partial
  thermal_zones_status: valid
  constructions_status: incomplete
  schedules_status: valid
  hvac_status: simplified
  sensor_binding_status: missing
  calibration_readiness: medium
  blocking_issues:
    - missing_material_properties
  warnings:
    - simplified_hvac
    - no_sensor_mapping
```

### 6.5 AdoptedModel

Modelo ya registrado dentro de Siamese.

```yaml
AdoptedModel:
  id: adopted_model_001
  source_asset_id: imported_asset_001
  energy_model_id: energy_model_014
  nucleus_stage_url: omniverse://siamese/projects/building_001/stages/adopted_model_main.usd
  status: simulation_ready
  quality_report_id: quality_report_001
```

---

## 7. Relación con Nucleus

Nucleus es una pieza fundamental del Adoption Model.

El módulo de adopción debe usar Nucleus como espacio colaborativo para almacenar, revisar y enriquecer activos adoptados.

Flujo:

```text
activo externo
→ conversión/importación a USD/OpenUSD cuando aplique
→ almacenamiento en Nucleus
→ separación por layers
→ revisión colaborativa
→ enriquecimiento semántico
→ conexión con backend
```

Nucleus aporta:

```text
almacenamiento de stages USD;
layers separadas;
permisos;
conectores;
versionado;
colaboración;
revisión visual;
integración con Omniverse Kit;
assets compartidos.
```

Ejemplo de estructura en Nucleus:

```text
omniverse://siamese-server/projects/building_001/
├── imported/
│   ├── original_revit/
│   ├── original_idf/
│   ├── original_osm/
│   └── original_designbuilder/
├── stages/
│   └── adopted_model_main.usd
├── layers/
│   ├── 00_imported_geometry.usd
│   ├── 01_aec_semantics.usd
│   ├── 02_energy_semantics.usd
│   ├── 03_hvac_semantics.usd
│   ├── 04_sensor_bindings.usd
│   └── 09_adoption_annotations.usd
└── reports/
    └── model_quality_report.md
```

Frontera:

```text
Nucleus
→ activo visual, USD, colaboración, capas, conectores.

Backend Siamese
→ autoridad computacional, energética, operativa y agéntica.
```

---

## 8. Relación con Omniverse Connectors

Siamese puede adoptar activos externos apoyándose en conectores Omniverse/Nucleus.

Ejemplos:

```text
Revit → USD/Nucleus
Blender → USD/Nucleus
Unreal → USD/Nucleus
Unity → USD/Nucleus
CAD/BIM tools → USD/Nucleus
```

Flujo ideal:

```text
herramienta externa
→ Omniverse Connector
→ OpenUSD en Nucleus
→ Siamese Kit
→ Adoption Audit
→ Semantic Enrichment
→ EnergyPlus backend
```

Esto permite que Siamese no sea una herramienta aislada. El cliente puede seguir usando herramientas existentes y Siamese puede actuar como capa energética, operativa y agéntica sobre los activos adoptados.

---

## 9. Adopción desde IDF

El caso más directo es importar archivos **IDF** de EnergyPlus.

### 9.1 Qué puede contener un IDF

```text
building;
zones;
surfaces;
materials;
constructions;
schedules;
loads;
HVAC;
simulation settings;
output variables;
meters;
site/weather references.
```

### 9.2 Flujo de adopción

```text
IDF
→ parser
→ EnergyPlus object graph
→ Siamese EnergyModel
→ ModelQualityReport
→ optional USD geometry reconstruction
→ simulation readiness
```

### 9.3 Ventajas

```text
muy cercano a EnergyPlus;
útil para modelos exportados desde DesignBuilder/OpenStudio;
permite simulación relativamente directa;
contiene semántica energética;
es un formato extendido.
```

### 9.4 Riesgos

```text
nombres poco estructurados;
geometría difícil de visualizar directamente;
HVAC complejo;
objetos legacy;
dependencia de versión;
materiales incompletos;
outputs no configurados;
no contiene datos reales;
no contiene sensórica;
puede requerir limpieza.
```

### 9.5 Validación obligatoria

Un IDF importado no debe aceptarse automáticamente como modelo Siamese válido.

Debe pasar por:

```text
schema check;
reference check;
geometry check;
zone check;
construction check;
schedule check;
HVAC check;
output check;
simulation smoke test;
quality report.
```

---

## 10. Adopción desde epJSON

epJSON es más cómodo para herramientas programáticas que IDF.

### 10.1 Ventajas

```text
estructura JSON;
más fácil de parsear;
mejor para APIs;
mejor para validación automática;
más natural para backend Python;
útil como formato intermedio.
```

### 10.2 Riesgos

```text
dependiente de versión de EnergyPlus;
no siempre disponible en flujos externos;
puede requerir conversión desde IDF;
no debe convertirse en modelo interno final.
```

### 10.3 Uso recomendado

```text
IDF/epJSON import
→ normalizar a Siamese EnergyModel
→ registrar source artifact
→ generar quality report
→ usar backend EnergyPlus para validar
```

epJSON es un formato de intercambio, no la fuente de verdad interna de Siamese.

---

## 11. Adopción desde DesignBuilder

DesignBuilder es especialmente relevante para Siamese por el origen del proyecto.

DesignBuilder puede generar modelos basados en EnergyPlus/IDF y permite modelado 3D, horarios, materiales, HVAC simple, outputs y optimización. En el TFG se usó DesignBuilder para modelar el C.E.P. Divino Maestro, definir ocupación, ventilación, sombreado, calefacción, caldera, bomba, radiadores y realizar calibración manual y digital.

### 11.1 Qué debería poder hacer Siamese

```text
importar IDF exportado/generado desde DesignBuilder;
leer zonas;
leer superficies;
leer materiales;
leer schedules;
leer HVAC simplificado;
leer outputs relevantes;
leer variables críticas si están documentadas;
crear Model Quality Report;
mapear geometría a USD si es viable;
generar roadmap de calibración;
conectar sensores históricos;
recalibrar modelo.
```

### 11.2 Valor comercial

Muchos modelos DesignBuilder se usan para un proyecto concreto y después quedan archivados.

Propuesta de Siamese:

```text
Adopta tu modelo DesignBuilder.
Lo auditamos.
Lo conectamos con datos reales.
Lo recalibramos.
Lo convertimos en gemelo operativo.
```

### 11.3 Estrategia por fases

```text
Fase 1:
importar IDF exportado desde DesignBuilder.

Fase 2:
detectar patrones comunes de DesignBuilder.

Fase 3:
crear DesignBuilder Import Profile.

Fase 4:
soportar recalibración de modelos DesignBuilder.

Fase 5:
crear conector/adaptador específico si hay suficiente demanda.
```

### 11.4 Riesgos

```text
DesignBuilder añade su propia capa de abstracción;
objetos EnergyPlus generados pueden ser complejos;
puede haber diferencias entre versiones;
puede haber dependencia de scripts externos;
la geometría no siempre se reconstruye fácilmente;
los modelos pueden estar calibrados sin evidencia suficiente.
```

---

## 12. Adopción desde OpenStudio

OpenStudio es importante porque es open source y está conectado a EnergyPlus.

### 12.1 Formatos

```text
OSM;
IDF exportado;
measures;
model objects;
outputs EnergyPlus.
```

### 12.2 Aportes potenciales

```text
modelos EnergyPlus más estructurados;
ecosistema open source;
measures reutilizables;
referencia para arquitectura;
posible importación programática.
```

### 12.3 Flujo recomendado

Primera fase:

```text
OpenStudio export IDF
→ Siamese IDF import
```

Fase posterior:

```text
OSM
→ OpenStudio parser/SDK or export
→ Siamese EnergyModel
→ quality report
→ USD binding
→ EnergyPlus backend
```

### 12.4 Riesgos

```text
licencias y dependencias;
complejidad del SDK;
compatibilidad de versiones;
diferencia entre OpenStudio Model y EnergyPlus IDF;
measures con lógica propia.
```

### 12.5 Estrategia

```text
No depender del SDK OpenStudio en el core inicial.
Primero soportar IDF exportado.
Después evaluar OSM parser/adaptor.
Finalmente crear OpenStudio Adoption Profile.
```

---

## 13. Adopción desde Revit

Revit es clave para clientes con BIM.

### 13.1 Qué aporta Revit

```text
geometría;
plantas;
espacios;
muros;
puertas;
ventanas;
familias;
materiales BIM;
metadata arquitectónica;
documentación de proyecto.
```

### 13.2 Qué no aporta automáticamente

```text
modelo energético validado;
zonas térmicas correctas;
HVAC EnergyPlus listo;
schedules;
sensores;
calibración;
outputs;
control operativo.
```

### 13.3 Flujo vía Nucleus

```text
Revit
→ Omniverse Revit Connector
→ USD/Nucleus
→ Siamese Kit
→ AEC Semantic Audit
→ Energy Model Builder
→ EnergyPlus Backend
```

### 13.4 Validaciones necesarias

```text
espacios cerrados;
plantas correctas;
orientación;
unidades;
superficies exteriores;
huecos;
materiales;
nombres;
niveles;
zonas térmicas;
sombras;
geometría simplificable para EnergyPlus.
```

### 13.5 Valor

Revit permite entrar en proyectos AEC reales sin remodelar desde cero.

Frase clave:

> **Revit proporciona geometría/BIM. Siamese debe convertirla en modelo energético.**

---

## 14. Adopción desde IFC

IFC es relevante porque es un estándar abierto BIM.

### 14.1 Ventajas

```text
open standard;
interoperable;
presente en proyectos BIM;
menos dependiente de Autodesk;
útil para clientes públicos o europeos;
compatible con flujos openBIM.
```

### 14.2 Riesgos

```text
calidad variable;
geometría compleja;
semántica energética insuficiente;
materiales incompletos;
espacios mal definidos;
exportaciones inconsistentes;
dependencia de cómo se generó el IFC.
```

### 14.3 Flujo

```text
IFC
→ IFC parser
→ AEC entities
→ USD stage
→ Siamese EnergyModel
→ quality report
```

### 14.4 Estrategia

IFC debe formar parte del Adoption Model, pero no necesariamente del primer MVP.

---

## 15. Adopción desde DXF/CAD

DXF/CAD es útil cuando no hay modelo 3D, pero sí planos.

### 15.1 Uso

```text
planos de planta;
alzados;
referencias de medición;
croquizado;
snap;
reconstrucción AEC;
modelado desde cero asistido.
```

### 15.2 Flujo

```text
DXF
→ reference layer in USD
→ AEC sketching
→ spaces/surfaces
→ energy model
```

Aquí el Adoption Model no importa un gemelo completo. Importa una referencia para reconstruirlo.

### 15.3 Relación con TFG

En el TFG fue necesario conseguir planos del edificio desde distintas fuentes antes de modelar en DesignBuilder. Siamese debería convertir ese proceso en un flujo guiado:

```text
importar plano
→ escalar
→ usar como referencia
→ croquizar
→ generar espacios
→ validar geometría
→ crear EnergyModel
```

---

## 16. Adopción desde USD

Si el cliente ya tiene un asset USD, el proceso puede ser más directo, pero hay que distinguir tipos.

### 16.1 USD visual

```text
mallas;
materiales;
assets;
escena renderizable.
```

### 16.2 USD semántico

```text
building hierarchy;
spaces;
surfaces;
sensors;
metadata;
relationships;
layers.
```

Siamese necesita transformar USD visual en USD semántico energético cuando sea necesario.

Flujo:

```text
USD visual
→ semantic audit
→ entity extraction
→ add Siamese schemas/metadata
→ energy semantics layer
→ backend mapping
```

---

## 17. Adopción desde Blender / Unreal / Unity

Estos formatos suelen ser más visuales que energéticos.

### 17.1 Uso principal

```text
visualización;
assets;
demos;
materiales;
presentaciones;
VR/AR;
modelos conceptuales.
```

### 17.2 Flujo correcto

```text
Blender/Unreal/Unity
→ USD/Nucleus
→ visual asset
→ semantic enrichment
→ optional energy mapping
```

### 17.3 Regla

```text
Blender/Unreal/Unity pueden aportar activos visuales.
No deben ser autoridad energética.
```

Ejemplo:

```text
modelo visual de edificio en Blender
→ Siamese lo usa como referencia visual
→ se reconstruyen zonas energéticas
→ se genera EnergyModel propio
```

---

## 18. Adopción desde CSV y datos históricos

Adoption Model también debe poder adoptar datos, no solo modelos.

Fuentes:

```text
CSV de sensores;
Excel de horarios;
exports de BMS;
datos meteorológicos;
consumo de gas;
consumo eléctrico;
facturas energéticas;
inventarios HVAC;
listados de sensores;
mantenimientos.
```

Flujo:

```text
CSV/XLSX
→ schema detection
→ field mapping
→ normalization
→ Sensor Registry
→ Sensor-Zone Binding
→ Calibration Targets
→ Feature Builder
```

Esto conecta con el módulo de sensórica.

---

## 19. Traducción de archivos personalizados

Además de conectores estándar, Siamese debe permitir traductores personalizados.

Casos:

```text
CSV propio de sensores;
Excel de horarios;
JSON de BMS;
XML de software externo;
exports propios de DesignBuilder;
scripts de EnergyPlus;
archivos de mantenimiento;
listados de equipos HVAC;
planos con naming interno;
inventarios de sensores;
ficheros generados por consultoras.
```

### 19.1 CustomTranslator

Arquitectura:

```text
CustomTranslator
├── detect format
├── validate schema
├── map fields
├── transform units
├── create entities
├── emit warnings
└── produce adoption artifacts
```

Ejemplo:

```yaml
CustomTranslator:
  id: govee_csv_translator_v1
  input_format: csv
  maps:
    "Time" -> timestamp
    "Temperature" -> zone_air_temperature
    "Humidity" -> zone_air_relative_humidity
  output:
    SensorReading[]
```

Esto será esencial en pilotos, porque cada cliente traerá datos en formatos propios.

---

## 20. Conectores personalizados

A largo plazo, Siamese puede tener un sistema de conectores propio.

### 20.1 Tipos de conectores

```text
File connectors
→ IDF, epJSON, OSM, IFC, DXF, CSV, XLSX.

Application connectors
→ DesignBuilder, OpenStudio, Revit, Blender.

Platform connectors
→ Nucleus, Google Drive, SharePoint, Notion.

Operational connectors
→ BMS, MQTT, BACnet, Modbus, OPC-UA.

Workflow connectors
→ Notion, Calendar, Gmail, Jira, Linear.

Repository/agent connectors
→ Pepper, GitHub, Codex, Graphify.
```

### 20.2 Principio

Cada conector debe producir contratos internos de Siamese.

```text
Connector
→ ImportedAsset
→ MappingReport
→ SiameseModel entities
→ Evidence
```

No debe hacer esto:

```text
Connector
→ modificar backend directamente sin auditoría.
```

---

## 21. Model Quality Report

El **Model Quality Report** es el entregable central del módulo.

Debe responder:

```text
¿El modelo se puede simular?
¿Tiene geometría suficiente?
¿Tiene zonas térmicas?
¿Tiene materiales?
¿Tiene HVAC?
¿Tiene schedules?
¿Tiene sensores?
¿Está calibrado?
¿Qué falta?
¿Qué hay que corregir?
¿Qué riesgo tiene usarlo?
¿Puede pasar a EnergyPlus?
¿Puede pasar a calibración?
¿Puede pasar a dataset?
¿Puede pasar a surrogate?
¿Puede pasar a shadow mode?
```

### 21.1 Secciones recomendadas

```text
1. Source summary
2. Geometry completeness
3. AEC semantic quality
4. Energy semantic quality
5. HVAC completeness
6. Schedule completeness
7. Material/construction quality
8. Sensor readiness
9. Simulation readiness
10. Calibration readiness
11. Dataset readiness
12. Surrogate readiness
13. Shadow mode readiness
14. Blocking issues
15. Warnings
16. Recommended adoption roadmap
```

### 21.2 Readiness statuses

```text
not_ready;
partial;
ready_with_warnings;
ready;
approved.
```

---

## 22. Adoption Roadmap

Después del quality report, Siamese debe generar un roadmap de adopción.

### 22.1 Ejemplo: modelo DesignBuilder

```text
Roadmap: Adopt DesignBuilder model

1. Import IDF.
2. Parse EnergyPlus objects.
3. Validate zones and surfaces.
4. Reconstruct USD stage.
5. Map thermal zones to spaces.
6. Detect missing materials.
7. Import sensor CSV.
8. Bind sensors to zones.
9. Run baseline simulation.
10. Compare real vs simulated.
11. Launch calibration.
12. Approve calibrated model.
13. Generate dataset campaign.
14. Train surrogate.
15. Enter shadow mode.
```

### 22.2 Ejemplo: modelo Revit

```text
Roadmap: Adopt Revit BIM

1. Sync Revit to Nucleus.
2. Extract spaces and levels.
3. Validate geometry closure.
4. Generate thermal zones.
5. Assign constructions.
6. Add schedules.
7. Build EnergyModel.
8. Run EnergyPlus smoke test.
9. Add sensors.
10. Calibrate.
```

### 22.3 Relación con agentes

El roadmap debe dividirse en tareas ejecutables por humanos o agentes.

---

## 23. Relación con Agentic Workflow Engine

El Adoption Model debe producir tareas para agentes y humanos.

Agentes posibles:

```text
Import Agent
AEC Audit Agent
Energy Model Agent
Sensor Mapping Agent
Calibration Agent
Documentation Agent
QA Agent
Connector Agent
```

Ejemplo:

```text
Import Agent detecta que el modelo Revit no tiene espacios cerrados.
↓
Crea task:
"Revisar geometría de planta 2: 4 espacios abiertos."
↓
AEC Modeler corrige.
↓
Energy Model Agent vuelve a validar.
```

Regla:

```text
Los agentes pueden proponer y preparar.
La promoción de cambios críticos requiere aprobación.
```

---

## 24. Relación con EnergyPlus Backend

Adoption Model debe terminar generando o alimentando:

```text
Siamese EnergyModel;
SimulationCase;
CompiledEnergyPlusModel;
EnergyPlus Run;
NormalizedResults.
```

Flujo:

```text
imported IDF/OSM/Revit/USD
→ Siamese Domain Model
→ Validation Layer
→ EnergyPlus Compiler/Runner
```

Incluso si importamos un IDF listo, Siamese debe registrarlo, validarlo y versionarlo.

No debe ocurrir:

```text
IDF importado
→ EnergyPlus directo
→ resultados sin trazabilidad.
```

---

## 25. Relación con Calibración

Muchos modelos adoptados serán no calibrados o calibrados en otro contexto.

Siamese debe clasificarlos:

```text
uncalibrated;
manually calibrated;
digitally calibrated;
partially calibrated;
calibrated but stale;
calibration evidence missing;
calibration-ready;
not calibration-ready.
```

Ejemplo:

```text
DesignBuilder model from 2024
→ calibrated against one week of temperature data
→ no live sensors
→ calibration stale
→ recommend recalibration before surrogate training
```

Regla:

```text
Un modelo adoptado no debe pasar a surrogate operacional sin calibración suficiente.
```

---

## 26. Relación con Sensórica

Adoption Model debe permitir adoptar datos reales.

Fuentes:

```text
CSV histórico;
Govee exports;
BMS exports;
weather station CSV;
energy bills;
gas consumption files;
IoT platform exports.
```

El módulo debe conectar estos datos con:

```text
Sensor Registry;
Sensor-Zone Binding;
Calibration Targets;
Feature Builder;
Dataset Factory.
```

---

## 27. Relación con Dataset Factory y Surrogates

No se deben generar datasets ni entrenar surrogates operativos sobre modelos adoptados sin evaluar calidad.

Reglas:

```text
No quality report
→ no dataset campaign.

No calibrated model
→ no operational surrogate.

No sensor validation
→ no shadow mode.

No readiness gate
→ no control.
```

Readiness gates:

```text
simulation-ready;
calibration-ready;
dataset-ready;
surrogate-ready;
shadow-mode-ready;
control-ready.
```

---

## 28. Relación con SimReady Energy Assets

Los activos adoptados pueden convertirse en assets reutilizables.

Ejemplo:

```text
radiador importado desde Revit
→ asset visual
→ Siamese añade metadata energética
→ asset reutilizable
```

O:

```text
sensor modelado en Blender
→ USD asset
→ metadata de variable, protocolo, ubicación típica
→ asset de sensórica Siamese
```

Esto permite construir una librería de assets a partir de proyectos reales.

---

## 29. Arquitectura interna propuesta

```text
siamese_backend/adoption/
│
├── contracts/
│   ├── imported_asset.py
│   ├── import_job.py
│   ├── source_format.py
│   ├── connector_profile.py
│   ├── mapping_report.py
│   ├── quality_report.py
│   ├── adoption_roadmap.py
│   └── adopted_model.py
│
├── connectors/
│   ├── idf_connector.py
│   ├── epjson_connector.py
│   ├── designbuilder_connector.py
│   ├── openstudio_connector.py
│   ├── revit_connector.py
│   ├── ifc_connector.py
│   ├── dxf_connector.py
│   ├── usd_connector.py
│   └── csv_connector.py
│
├── parsers/
│   ├── idf_parser.py
│   ├── epjson_parser.py
│   ├── osm_parser.py
│   ├── ifc_parser.py
│   ├── dxf_parser.py
│   └── custom_parser.py
│
├── mapping/
│   ├── energyplus_to_domain.py
│   ├── bim_to_aec.py
│   ├── aec_to_energy.py
│   ├── usd_to_domain.py
│   ├── sensor_mapping.py
│   └── naming_resolution.py
│
├── quality/
│   ├── geometry_audit.py
│   ├── energy_audit.py
│   ├── hvac_audit.py
│   ├── schedule_audit.py
│   ├── material_audit.py
│   ├── sensor_audit.py
│   └── readiness_scoring.py
│
├── translators/
│   ├── translator_registry.py
│   ├── custom_translator.py
│   ├── schema_detection.py
│   └── field_mapping.py
│
├── nucleus/
│   ├── nucleus_import.py
│   ├── layer_writer.py
│   ├── connector_sync.py
│   └── asset_registry.py
│
├── roadmap/
│   ├── roadmap_generator.py
│   ├── repair_tasks.py
│   ├── enrichment_tasks.py
│   └── approval_gates.py
│
└── reports/
    ├── model_quality_report.py
    ├── adoption_summary.py
    └── migration_report.py
```

---

## 30. MVP del Adoption Model

### 30.1 Objetivo MVP

Adoptar un IDF/epJSON existente y convertirlo en un modelo Siamese validado mínimamente.

### 30.2 Alcance MVP

```text
IDF import;
epJSON import;
ImportedAsset registry;
basic parser;
basic EnergyModel mapping;
basic quality report;
EnergyPlus smoke test;
Nucleus stage/layer reference;
manual sensor CSV attachment;
adoption roadmap generated.
```

### 30.3 Fuera del MVP

```text
Revit connector completo;
OpenStudio OSM parser completo;
DesignBuilder-specific deep parsing;
IFC completo;
DXF reconstruction;
custom connector SDK;
automatic repair;
automatic calibration;
live connector sync.
```

### 30.4 Resultado esperado

```text
Siamese puede recibir un modelo EnergyPlus existente,
auditarlo,
registrarlo,
ejecutarlo,
mostrar qué falta,
y proponer los pasos para convertirlo en gemelo vivo.
```

---

## 31. Fases de evolución

### Fase 1 — IDF/epJSON Adoption

```text
parser;
quality report;
simulation smoke test.
```

### Fase 2 — DesignBuilder Adoption Profile

```text
patrones de IDF exportado;
schedules;
HVAC simple;
outputs;
variables críticas.
```

### Fase 3 — Sensor CSV Adoption

```text
importar datos históricos;
binding manual;
calibration readiness.
```

### Fase 4 — Nucleus/USD Adoption

```text
stage import;
layer conventions;
visual audit.
```

### Fase 5 — OpenStudio Adoption

```text
OSM support;
OpenStudio profile;
measures awareness.
```

### Fase 6 — Revit/IFC Adoption

```text
BIM to AEC;
geometry audit;
space extraction;
thermal zoning.
```

### Fase 7 — Custom Translators

```text
translator registry;
field mapping UI;
client-specific import profiles.
```

### Fase 8 — Agentic Adoption

```text
automatic roadmap;
repair tasks;
agent proposals;
approval gates.
```

---

## 32. Primeros tickets recomendados

### ADOPT-00 — Adoption Model context

Crear documentación conceptual del módulo.

### ADOPT-01 — ImportedAsset contracts

Definir `ImportedAsset`, `ImportJob`, `MappingReport`, `ModelQualityReport`.

### ADOPT-02 — IDF import spike

Leer un IDF existente y extraer entidades básicas.

### ADOPT-03 — epJSON import spike

Leer epJSON y mapear objetos básicos.

### ADOPT-04 — EnergyPlus smoke test

Ejecutar modelo importado con EnergyPlus y capturar diagnóstico.

### ADOPT-05 — Basic Model Quality Report

Generar informe de calidad inicial.

### ADOPT-06 — IDF to Siamese EnergyModel mapping

Traducir zonas, superficies, construcciones y schedules mínimos.

### ADOPT-07 — Nucleus imported asset structure

Definir estructura de carpetas/layers de activos importados en Nucleus.

### ADOPT-08 — Adoption Roadmap generator MVP

Generar roadmap de pasos pendientes a partir del quality report.

### ADOPT-09 — DesignBuilder import profile analysis

Analizar IDFs exportados desde DesignBuilder y patrones comunes.

### ADOPT-10 — Sensor CSV attachment

Permitir asociar CSV histórico a un modelo adoptado.

### ADOPT-11 — Revit connector evaluation

Evaluar flujo Revit → USD/Nucleus → Siamese.

### ADOPT-12 — Custom translator registry

Diseñar registro de traductores personalizados.

---

## 33. Riesgos principales

### Riesgo 1 — Prometer compatibilidad universal

Mitigación:

```text
adoption profiles;
quality report;
compatibility matrix;
import does not imply readiness.
```

### Riesgo 2 — Geometría visual no energética

Mitigación:

```text
semantic audit;
thermal zone generation;
EnergyPlus validation.
```

### Riesgo 3 — Pérdida semántica en conectores

Mitigación:

```text
mapping reports;
manual review;
layer separation;
metadata enrichment.
```

### Riesgo 4 — Modelos antiguos o malos

Mitigación:

```text
quality scoring;
repair roadmap;
do not silently accept invalid models.
```

### Riesgo 5 — Demasiados formatos al inicio

Mitigación:

```text
IDF/epJSON first;
DesignBuilder profile second;
Revit/IFC later.
```

### Riesgo 6 — Importar sin trazabilidad

Mitigación:

```text
ImportedAsset registry;
checksums;
mapping report;
quality report;
provenance.
```

---

## 34. Valor comercial

Este módulo es uno de los más importantes para vender Siamese.

Permite decir:

```text
No tienes que empezar de cero.
Siamese puede adoptar lo que ya tienes.
```

Casos comerciales:

```text
consultora con modelos DesignBuilder antiguos;
universidad con modelos EnergyPlus/OpenStudio;
hospital con BIM Revit;
cliente con CSVs de sensores;
facility manager con BMS exports;
proyecto público con IFC;
empresa con assets USD;
campus con modelos parciales por edificio.
```

Propuesta:

> **Siamese transforma modelos existentes en gemelos energéticos vivos.**

Esto reduce fricción de entrada, amplía mercado potencial y crea una vía natural para consultoría inicial.

---

## 35. Frases de presentación

Frase principal:

> **Siamese no obliga a empezar de cero: adopta modelos existentes y los convierte en gemelos vivos.**

Frase técnica:

> **El Adoption Model importa activos desde IDF, epJSON, DesignBuilder, OpenStudio, Revit, IFC, DXF, USD o CSV, los audita, los normaliza, los conecta a Nucleus y genera el roadmap necesario para simular, calibrar y operar el edificio.**

Frase comercial:

> **Si tu edificio ya fue modelado, Siamese puede revivirlo.**

---

## 36. Decisión arquitectónica final

La decisión central:

```text
El Adoption Model no es un importador de archivos.
Es una fábrica de transformación de activos existentes en gemelos energéticos vivos.
```

Arquitectura final:

```text
Connectors importan.
Translators traducen.
Quality Report audita.
Nucleus colabora.
Backend gobierna.
EnergyPlus valida.
Sensórica calibra.
Surrogates predicen.
Agentes orquestan.
```

Siamese debe soportar adopción progresiva:

```text
archivo importado
→ modelo entendible
→ modelo validado
→ modelo calibrado
→ modelo operativo
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
→ Nucleus como colaboración y conectores.

siamese_calibration_module_context.md
→ calibración como puente modelo-realidad.

siamese_sensorics_module_context.md
→ sensórica como observación real.

siamese_dsx_ecosystem_context.md
→ DSX como referencia estratégica.

digital_twin_contexto_maestro.md
→ visión modular general.
```

Y prepara:

```text
Connector SDK;
Reference Designs;
SimReady Energy Assets;
Agentic Workflow Engine;
Siamese Exchange;
Commercial onboarding workflows.
```
