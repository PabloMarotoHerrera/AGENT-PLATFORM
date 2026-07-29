# Contexto maestro — Plataforma de Gemelos Digitales Energéticos

**Proyecto:** Digital Twin energético con NVIDIA Omniverse Kit + OpenUSD + EnergyPlus + IA.  
**Propósito:** dejar un contexto reutilizable para abrir nuevos chats dentro del mismo proyecto y que el asistente entienda rápidamente qué estamos construyendo, qué decisiones se han tomado, cómo trabajamos con Codex y cómo estructuraremos los macroproyectos en proyectos/tickets.

---

## 1. Visión general del producto

El objetivo es construir una **plataforma modular de gemelos digitales energéticos para edificios**. No es solo una extensión de Omniverse ni un exportador IDF: es una plataforma completa que combina modelado AEC, simulación, calibración, datos reales, IA, optimización, visualización y despliegue.

Componentes principales previstos:

- **NVIDIA Omniverse Kit + OpenUSD** como runtime visual, colaborativo y semántico.
- **AEC-USD Modelling** para crear y editar edificios: sketches, bloques, spaces, surfaces, openings, materials, metadata.
- **Backend EnergyPlus** como solver backend robusto, equivalente en filosofía al backend OpenDSS del TFM.
- **Calibración** del modelo simulado contra otro modelo o contra un edificio real.
- **Generación de datasets físicos sintéticos** con simulaciones masivas EnergyPlus.
- **Surrogate models**: RC, LSTM, GRU, Transformers, GNN, híbridos físico-ML, foundation models.
- **Control y optimización**: MPC, Recurrent PPO, safe RL, optimización clásica, cuOpt y QUBO/quantum-inspired futuro.
- **Sensórica e ingesta de datos reales**: CSV, MQTT, REST, OPC-UA, BACnet, Modbus, BMS.
- **NVIDIA Air / NetworkSim IoT-HVAC** para simular red, latencias, gateways, actuadores y robustez del control.
- **Visualización avanzada**: Room Stats, Surface Stats, Sensor Stats, HVAC Stats, ThermalViz, dashboards, real/sim/pred/control, point clouds y heatmaps volumétricos.
- **Agente IA interno y agentes externos vía MCP**, con tool calling y comandos nativos.
- **Colaboración y despliegue**: Nucleus, USD layers, permisos, packaging, backend remoto/HPC, releases.
- **Economía, gestión empresarial y marketing** para preparar producto comercial futuro.

Flujo conceptual:

```text
Modelo USD/AEC
→ Modelo energético abstracto
→ Backend EnergyPlus
→ Simulación / calibración / datasets
→ Surrogates / control
→ Visualización / sensórica / agente
→ Producto colaborativo y desplegable
```

---

## 2. Principios arquitectónicos clave

### 2.1 EnergyPlus es solver, no modelo interno

EnergyPlus debe tratarse igual que OpenDSS en el TFM: un motor externo. La plataforma debe tener su propio modelo de dominio, validación, compilador y resultados normalizados.

```text
Modelo interno propio
→ Validación
→ Compilador/exportador EnergyPlus
→ Engine runner
→ Resultados normalizados
```

### 2.2 Omniverse Kit no es el backend

Kit debe ser UI, viewport, comandos, extensiones y visualización. La lógica fuerte debe vivir en paquetes/backend.

### 2.3 OpenUSD es fuente geométrica y semántica

USD representa Building, Blocks, Spaces, Surfaces, Sketches, Openings, Materials, Energy metadata, Sensors, Simulation result metadata y Visualization layers. Las series temporales grandes se guardarán preferentemente fuera del USD, con metadata/bindings dentro del stage.

### 2.4 El agente IA no modela por su cuenta

Regla central:

```text
Agente = orquestador
Comandos nativos = acciones reales
Módulos core = lógica de dominio
USD/backend = fuentes de verdad
```

Prohibido:

```text
dt.energy.agent crea geometría propia
dt.energy.agent compila IDF directamente
dt.energy.agent parsea resultados directamente
dt.energy.agent calcula control directamente
```

Permitido:

```text
dt.energy.agent interpreta intención
→ llama AEC.CreateSketch
→ llama AEC.ExtrudeSketchToBlock
→ llama Energy.RunSimulation
→ llama Viz.ColorByTemperature
```

### 2.5 Primero comandos, contratos y backend; después IA avanzada

Antes de usar Nemotron/NIM o agentes multimodales tipo SyncTwin, necesitamos APIs públicas, comandos nativos, validación, mappers, tests y contratos de datos.

---

## 3. Contexto inicial y evolución

La visión inicial tenía 10 partes:

1. Modelado y representación en Omniverse/USD.
2. Exportador USD → EnergyPlus/IDF.
3. Simulación y orquestación.
4. Ingesta de datos reales.
5. Calibración.
6. Modelos rápidos / surrogates.
7. Reinforcement learning / Recurrent PPO.
8. Interfaz visual en Omniverse Kit.
9. Operación en tiempo real.
10. Infraestructura y colaboración.

Durante el desarrollo se decidió que los bloques 2 y 3 deben convertirse en un **Backend EnergyPlus completo**, no solo un exportador. Calibración, datasets, surrogates y control dependen de ese backend. Visualización, sensórica, agentes, NVIDIA Air, CUDA-X, colaboración, economía y marketing se tratan como macroproyectos separados.

---

## 4. Estado actual del prototipo Omniverse/AEC

Se ha trabajado exploratoriamente sobre una app basada en Kit App Template.

Extensiones/módulos explorados:

- `custom.aec.modeling`
- `custom.aec.primitive_mesh`
- `custom.aec.extrude`
- `dt.energy.agent`
- herramientas de ThermalViz / sync energético

Avances técnicos:

- Bloques paramétricos bajo `/World/Building/Block_XX`.
- Jerarquía con `Mass`, `Spaces/Space_01/Surfaces`, `Partitions`, `Metadata`, `_AEC/PartitionSpecs`.
- Sketches bajo `/World/Building/Sketches`.
- Relación `aec:sourceCurveRel` desde bloque a sketch.
- Extrusión de sketches rectangulares y poligonales.
- Modificación de sketch y rebuild asociado.
- Búsqueda de bloques asociados a sketch.
- Polygon-aware rebuild.
- Corrección de floors/ceilings cóncavos mediante triangulación ear clipping.
- Debug tool tipo `inspect_surface_geometry`.
- Sincronización ThermalViz para bloques AEC, evitando que solo los bloques creados por agente tengan metadata térmica.

Decisión clave: el agente no debe crear estructuras paralelas; debe usar AEC Modelling, idealmente mediante comandos nativos Kit.

Arquitectura objetivo:

```text
AEC API pública
→ comandos Kit nativos
→ UI / Agente / Hotkeys / MCP / scripts
```

No:

```text
dt.energy.agent crea geometría por su cuenta
```

Pendientes relevantes:

- Importación DXF como referencia.
- Snap sobre vértices/líneas del DXF.
- Croquizado interactivo en viewport.
- Particiones/openings robustos sobre footprints arbitrarios.
- Interpretación futura de planos para detectar muros exteriores y particiones.

---

## 5. Flujo de trabajo con Codex

Queremos usar Codex como **sistema de ejecución de tickets**, no como chat genérico.

Flujo operativo:

1. Definir macroproyecto.
2. Dividir en proyectos.
3. Dividir proyectos en tareas.
4. Convertir cada tarea en ticket Codex.
5. Codex inspecciona repo y docs.
6. Codex modifica solo el scope permitido.
7. Codex ejecuta validación.
8. Codex reporta archivos inspeccionados, modificados, comandos, tests, decisiones, limitaciones y siguiente ticket.
9. Se revisa diff.
10. Se hace commit.
11. Se actualiza Notion.

Reglas para Codex:

- Leer documentación base antes de actuar.
- No modificar `references/`, `third_party/`, binarios, manuales u outputs.
- No tocar `.git/`.
- No mezclar macroproyectos en un mismo ticket.
- No implementar más de lo pedido.
- No duplicar lógica si ya hay API/comando público.
- Añadir tests cuando aplique.
- Ejecutar build/test/launch si corresponde.
- Limpiar `__pycache__` si lo genera.
- Reportar limitaciones con honestidad.

---

## 6. Plantilla recomendada de ticket Codex

```text
# Ticket XXX — <título>

## 0. Contexto obligatorio
<qué debe saber Codex antes de actuar>

## 1. Tipo
Documentación / Arquitectura / Implementación / Refactor / Test / Bugfix

## 2. Objetivo
<resultado concreto esperado>

## 3. Alcance permitido
<archivos/carpetas que puede tocar>

## 4. Alcance prohibido
<archivos/carpetas que no puede tocar>

## 5. Tareas
1. ...
2. ...
3. ...

## 6. Criterios de aceptación
- ...

## 7. Validación requerida
Comandos a ejecutar:
- ...

## 8. Formato de respuesta esperado
### Summary
### Files inspected
### Files modified
### Tests/commands run
### Decisions made
### Limitations
### Recommended next ticket

## 9. Restricciones importantes
- No ampliar scope.
- No modificar carpetas read-only.
- No implementar features no solicitadas.
```

---

## 7. Organización en Notion

Se creó un Área llamada **Digital Twin**.

Estructura conceptual:

```text
Área Digital Twin
→ Objetivos / Macroproyectos
→ Proyectos
→ Tareas
→ Tickets Codex
```

Cada macroproyecto debe tratarse como un proyecto completo tipo TFM, no como una simple lista de funcionalidades.

---

## 8. Macroproyectos actuales

Lista de macroproyectos definidos:

1. Estructura del repo/carpeta.
2. Configuración CODEX.
3. Backend EnergyPlus.
4. Calibración.
5. Generación Dataset.
6. Surrogate Models.
7. Control y Optimización.
8. Análisis de extensiones existentes / ecosistema Omniverse NVIDIA/partners.
9. Análisis CUDA-X / librerías GPU.
10. Plataforma Omniverse Kit.
11. AEC-USD Modelling.
12. Integración Backend EnergyPlus ↔ Omniverse Kit.
13. Sensórica e ingesta de datos.
14. NVIDIA Air / Simulación red IoT-HVAC.
15. Visualización Avanzada.
16. Agente IA.
17. Colaboración y despliegue.
18. Economía y gestión empresarial.
19. Marketing.

---

## 9. Estructuración resumida de los macroproyectos

### 9.1 Estructura del repo/carpeta

Objetivo: que la estructura del repo refleje la arquitectura del producto.

Proyectos:

```text
Proyecto 0 — Análisis del repositorio actual
Proyecto 1 — Diseño de arquitectura de repositorio
Proyecto 2 — Estructura base propuesta del repositorio
Proyecto 3 — Separación entre código propio y recursos externos
Proyecto 4 — Separación entre extensiones Kit y librerías core
Proyecto 5 — Diseño de paquetes Python internos
Proyecto 6 — Estructura específica del backend EnergyPlus
Proyecto 7 — Estructura específica de Omniverse Kit
Proyecto 8 — Estructura de documentación
Proyecto 9 — Estructura de tests
Proyecto 10 — Estructura de ejemplos y demos
Proyecto 11 — Estructura de datos, outputs y runs
Proyecto 12 — Estructura de schemas y contratos
Proyecto 13 — Estructura de scripts y herramientas internas
Proyecto 14 — Política .gitignore y archivos generados
Proyecto 15 — Migración segura del repositorio actual
Proyecto 16 — Reglas de acceso de Codex por carpeta
Proyecto 17 — Validación final de estructura
```

Estructura conceptual:

```text
digital-twin-platform/
├── apps/
├── extensions/
├── packages/
├── backend/
├── docs/
├── references/
├── assets/
├── data/
├── runs/
├── scripts/
├── tools/
├── notebooks/
├── schemas/
├── configs/
├── README.md
└── .gitignore
```

### 9.2 Configuración CODEX

Objetivo: convertir Codex en infraestructura de desarrollo asistido.

Proyectos:

```text
Proyecto 0 — Análisis de capacidades actuales de Codex
Proyecto 1 — Gobernanza Codex del Área Digital Twin
Proyecto 2 — Estructura documental para tickets Codex
Proyecto 3 — Contexto permanente del proyecto para Codex
Proyecto 4 — Organización de repositorios para trabajo con Codex
Proyecto 5 — Flujo Git y control de cambios con Codex
Proyecto 6 — Configuración de entorno local para Codex
Proyecto 7 — Sistema de validación automática para Codex
Proyecto 8 — MCP strategy para Codex
Proyecto 9 — MCP propio para Omniverse Kit
Proyecto 10 — MCP propio para EnergyPlus backend
Proyecto 11 — Skills / playbooks reutilizables para Codex
Proyecto 12 — Automations y tareas recurrentes
Proyecto 13 — Chronicle / validación visual asistida
Proyecto 14 — Integración Codex ↔ Notion
Proyecto 15 — Seguridad, permisos y límites de Codex
Proyecto 16 — Métricas de productividad y calidad con Codex
Proyecto 17 — Flujo operativo diario con Codex
Proyecto 18 — Validación final de configuración Codex
```

### 9.3 Backend EnergyPlus

Objetivo: backend robusto tipo OpenDSS TFM.

Proyectos:

```text
Proyecto 0 — Formación EnergyPlus y análisis inicial
Proyecto 1 — Arquitectura y backend MVP EnergyPlus
Proyecto 2 — Geometry / Thermal Zone vertical slice
Proyecto 3 — Materials & Constructions vertical slice
Proyecto 4 — Openings, windows and boundary conditions
Proyecto 5 — Internal loads, schedules and operation
Proyecto 6 — HVAC MVP vertical slice
Proyecto 7 — Weather, location and simulation settings
Proyecto 8 — Results, analytics and diagnostics
Proyecto 9 — Batch simulation and parametric workflows
Proyecto 10 — Calibration architecture
Proyecto 11 — Synthetic dataset generation
Proyecto 12 — Surrogate models backend
Proyecto 13 — Control and optimization backend
Proyecto 14 — API / SDK consolidation
Proyecto 15 — REST API backend
Proyecto 16 — Omniverse integration readiness
Proyecto 17 — Validación y benchmarking EnergyPlus
Proyecto 18 — Documentación, memoria técnica y demo
```

### 9.4 Calibración

Objetivo: calibrar modelo simulado contra otro modelo o datos reales.

Proyectos:

```text
Proyecto 0 — Formación y análisis inicial de calibración
Proyecto 1 — Arquitectura general del módulo de calibración
Proyecto 2 — Modelo de datos de calibración
Proyecto 3 — Fuentes de referencia para calibración
Proyecto 4 — Variables calibrables y parametrización del modelo
Proyecto 5 — Edición programática de IDF / modelo interno
Proyecto 6 — Métricas estadísticas de calibración
Proyecto 7 — Targets y objetivos de calibración
Proyecto 8 — Pipeline de simulación para calibración
Proyecto 9 — Paralelización local
Proyecto 10 — Paralelización HPC / servidor
Proyecto 11 — Optimización genética básica
Proyecto 12 — NSGA-II y calibración multiobjetivo
Proyecto 13 — Optimización bayesiana y reducción de búsqueda
Proyecto 14 — Surrogate-assisted calibration
Proyecto 15 — Calibración IDF vs IDF
Proyecto 16 — Calibración contra datos reales
Proyecto 17 — Gestión de incertidumbre y robustez
Proyecto 18 — Resultados, reporting y trazabilidad
Proyecto 19 — Persistencia y versionado de modelos calibrados
Proyecto 20 — Integración con generación de datasets
Proyecto 21 — Integración con Omniverse
Proyecto 22 — API / SDK de calibración
Proyecto 23 — Validación y benchmarking del módulo de calibración
Proyecto 24 — Documentación y casos de uso
```

### 9.5 Generación Dataset

Objetivo: generar datasets físicos sintéticos reproducibles y ML-ready.

Proyectos:

```text
Proyecto 0 — Formación y análisis inicial de datasets energéticos
Proyecto 1 — Arquitectura general del módulo de generación de datasets
Proyecto 2 — Modelo de datos del dataset
Proyecto 3 — Definición del objetivo del dataset
Proyecto 4 — Selección de features y targets
Proyecto 5 — Modelos base y fuentes de simulación
Proyecto 6 — Espacio de escenarios y domain randomization
Proyecto 7 — Sampling strategy y tamaño del dataset
Proyecto 8 — Configuración de simulaciones para dataset
Proyecto 9 — Ejecución local de generación dataset
Proyecto 10 — Ejecución en servidor / HPC / clusters
Proyecto 11 — Gestión de batches y chunks
Proyecto 12 — Extracción y normalización de resultados EnergyPlus
Proyecto 13 — Construcción de series temporales ML-ready
Proyecto 14 — Formatos de almacenamiento
Proyecto 15 — Metadata, manifest y trazabilidad
Proyecto 16 — Quality checks del dataset
Proyecto 17 — Splits train / validation / test
Proyecto 18 — Normalización y escalado
Proyecto 19 — Data loaders para entrenamiento
Proyecto 20 — Dataset para modelos RC
Proyecto 21 — Dataset para LSTM / Deep Learning
Proyecto 22 — Dataset para RL / control
Proyecto 23 — Dataset multizona y multi-edificio
Proyecto 24 — Dataset de sensores sintéticos
Proyecto 25 — Integración con calibración
Proyecto 26 — Integración con Surrogate Models
Proyecto 27 — Integración con Omniverse
Proyecto 28 — API / SDK de generación dataset
Proyecto 29 — Validación y benchmarking dataset generation
Proyecto 30 — Documentación y casos de uso
```

### 9.6 Surrogate Models

Objetivo: modelos rápidos que aproximan la dinámica térmica/energética.

Proyectos:

```text
Proyecto 0 — Formación y análisis inicial de surrogate models energéticos
Proyecto 1 — Arquitectura general del módulo Surrogate Models
Proyecto 2 — Modelo de datos de surrogate models
Proyecto 3 — Definición de problemas de predicción
Proyecto 4 — Contrato Dataset ↔ Surrogate Models
Proyecto 5 — Preprocesado para entrenamiento
Proyecto 6 — Baselines simples
Proyecto 7 — Modelos grey-box RC
Proyecto 8 — RNN / GRU / LSTM models
Proyecto 9 — Transformer temporal models
Proyecto 10 — Modelos híbridos físico-ML
Proyecto 11 — Physics-informed models
Proyecto 12 — Graph Neural Networks para multizona
Proyecto 13 — Foundation models y transfer learning
Proyecto 14 — Entrenamiento y experiment tracking
Proyecto 15 — Hyperparameter optimization
Proyecto 16 — Evaluación y métricas
Proyecto 17 — Rollout y estabilidad temporal
Proyecto 18 — Incertidumbre y confianza
Proyecto 19 — Model Registry y artefactos
Proyecto 20 — Exportación e inferencia
Proyecto 21 — Integración con calibración
Proyecto 22 — Integración con control y optimización
Proyecto 23 — Integración con Omniverse
Proyecto 24 — SDK/API de surrogate models
Proyecto 25 — Validación y benchmarking surrogate models
Proyecto 26 — Documentación y casos de uso
```

### 9.7 Control y Optimización

Objetivo: sistema activo de decisión, recomendación y control.

Proyectos:

```text
Proyecto 0 — Formación y análisis inicial de control energético
Proyecto 1 — Arquitectura general del módulo de control
Proyecto 2 — Modelo de datos de control
Proyecto 3 — Definición de estados del sistema
Proyecto 4 — Definición de acciones de control
Proyecto 5 — Restricciones de confort, seguridad y operación
Proyecto 6 — Funciones objetivo, coste y reward
Proyecto 7 — Entorno de simulación para control
Proyecto 8 — Integración con EnergyPlus para control offline
Proyecto 9 — Integración con surrogate models como entorno rápido
Proyecto 10 — Controladores baseline
Proyecto 11 — Control predictivo MPC
Proyecto 12 — Optimización clásica de estrategias
Proyecto 13 — Reinforcement Learning básico
Proyecto 14 — Recurrent PPO
Proyecto 15 — Offline RL y aprendizaje desde datasets
Proyecto 16 — Safe RL y control seguro
Proyecto 17 — Multiobjetivo y Pareto control
Proyecto 18 — Forecasting para control predictivo
Proyecto 19 — Demand response y tarifas energéticas
Proyecto 20 — Evaluación de políticas de control
Proyecto 21 — Rollout, robustez y generalización
Proyecto 22 — Entrenamiento local y HPC
Proyecto 23 — Experiment tracking y model registry
Proyecto 24 — Exportación de políticas e inferencia
Proyecto 25 — Shadow mode
Proyecto 26 — Operación en tiempo real
Proyecto 27 — Integración con sensores/BMS
Proyecto 28 — Integración con Omniverse
Proyecto 29 — API / SDK de control
Proyecto 30 — Validación y benchmarking de control
Proyecto 31 — Documentación y casos de uso
```

### 9.8 Análisis de extensiones existentes / ecosistema NVIDIA

Objetivo: decidir qué reutilizar, adaptar, estudiar, copiar como patrón o descartar.

Proyectos:

```text
Proyecto 0 — Inventario inicial del ecosistema Omniverse
Proyecto 1 — Criterios de evaluación y matriz de decisión
Proyecto 2 — Análisis Cadence Reality / Cadence Reality DC Design
Proyecto 3 — Análisis Patch Manager Extension
Proyecto 4 — Análisis Point Clouds / Reality Capture
Proyecto 5 — Análisis BIM Explorer / Revit / IFC workflows
Proyecto 6 — Análisis IoT Samples / Room Stats / Digital Twin Data Visualization
Proyecto 7 — Análisis OmniUI Plot / DAQ / gráficos en Kit
Proyecto 8 — Análisis Omniverse Flow / Fluid Dynamics / CFD-like visualization
Proyecto 9 — Análisis Clash Detection / validación geométrica
Proyecto 10 — Análisis NVIDIA Air / DSX Air y red IoT-HVAC
Proyecto 11 — Análisis SyncTwin
Proyecto 12 — Búsqueda de conferencia / grabación GTC / TAMU HPRC
Proyecto 13 — Investigación de la extensión de visualización de datos “DB”
Proyecto 14 — Análisis DesignBuilder / EnergyPlus / Omniverse interoperability
Proyecto 15 — Análisis Omniverse Replicator / Synthetic Data
Proyecto 16 — Análisis Isaac Sim / sensores sintéticos / ROS2
Proyecto 17 — Análisis NVIDIA Modulus / Physics-ML
Proyecto 18 — Análisis NVIDIA Cosmos / AI world models
Proyecto 19 — Análisis Nemotron / NIM / Agentic AI en Omniverse
Proyecto 20 — Análisis Omniverse Connectors relevantes
Proyecto 21 — Análisis de apps partner / industrial digital twins
Proyecto 22 — Instalación y pruebas controladas de extensiones candidatas
Proyecto 23 — Matriz de utilidad para nuestra plataforma
Proyecto 24 — Plan de contactos externos
Proyecto 25 — Extracción de patrones arquitectónicos reutilizables
Proyecto 26 — Decisiones de integración en nuestro roadmap
Proyecto 27 — Documentación final y recomendaciones
```

### 9.9 Análisis CUDA-X / librerías GPU

Objetivo: aceleración opcional, benchmarkeada y con fallback CPU.

Proyectos:

```text
Proyecto 0 — Formación y análisis inicial CUDA-X para Digital Twin energético
Proyecto 1 — Arquitectura general de aceleración GPU
Proyecto 2 — Inventario de librerías NVIDIA útiles
Proyecto 3 — Estrategia cuOpt para optimización energética
Proyecto 4 — cuOpt para MPC y control predictivo
Proyecto 5 — cuOpt para optimización de schedules y operación
Proyecto 6 — cuOpt para calibración y selección de candidatos
Proyecto 7 — RAPIDS cuDF para datasets grandes
Proyecto 8 — RAPIDS cuML para modelos y análisis rápido
Proyecto 9 — cuGraph para modelos multizona / grafos
Proyecto 10 — cuDSS / sparse solvers para modelos RC y optimización
Proyecto 11 — TensorRT / ONNX Runtime GPU para inferencia surrogate
Proyecto 12 — PyTorch CUDA para entrenamiento surrogate/RL
Proyecto 13 — CUDA/Numba/CuPy para kernels propios
Proyecto 14 — GPU para métricas de calibración masiva
Proyecto 15 — GPU para generación y procesamiento de datasets
Proyecto 16 — GPU para simulaciones paralelas indirectas
Proyecto 17 — GPU/HPC execution architecture
Proyecto 18 — Benchmarking global CPU vs GPU
Proyecto 19 — API / SDK de aceleración GPU
Proyecto 20 — Seguridad, reproducibilidad y dependencias GPU
Proyecto 21 — Integración con Omniverse Kit
Proyecto 22 — Documentación y casos de uso
Proyecto 23 — Validación final del macroproyecto GPU/CUDA-X
```

### 9.10 Plataforma Omniverse Kit

Objetivo: app Kit propia como runtime visual del Digital Twin.

Proyectos:

```text
Proyecto 0 — Formación y análisis inicial de Omniverse Kit
Proyecto 1 — Arquitectura general de la app Kit
Proyecto 2 — Configuración base de la aplicación Kit
Proyecto 3 — Sistema de extensiones propio
Proyecto 4 — Sistema de comandos nativos Kit
Proyecto 5 — Estructura visual y experiencia de usuario base
Proyecto 6 — Sistema visual / tema premium
Proyecto 7 — Sistema de settings y configuración de usuario
Proyecto 8 — Gestión de proyecto digital twin dentro de Kit
Proyecto 9 — Gestión USD y stage conventions
Proyecto 10 — Gestión de layers y variantes USD
Proyecto 11 — Integración con AEC Modeling
Proyecto 12 — Integración con Backend EnergyPlus
Proyecto 13 — Integración con resultados y datos temporales
Proyecto 14 — Sistema de visualización personalizada
Proyecto 15 — Gráficos y dashboards en Kit
Proyecto 16 — Sistema de sensórica en Kit
Proyecto 17 — Integración del agente IA en Kit
Proyecto 18 — MCP para interacción externa con Kit
Proyecto 19 — Conexión con Codex y agentes externos
Proyecto 20 — Sistema de logging, diagnostics y feedback
Proyecto 21 — Sistema de progreso y jobs
Proyecto 22 — Interacción viewport avanzada
Proyecto 23 — Importación y conectores de datos
Proyecto 24 — Gestión de recursos y assets
Proyecto 25 — Plantillas de edificios y workflows guiados
Proyecto 26 — Sistema de permisos y modos de usuario
Proyecto 27 — Performance y escalabilidad de la app
Proyecto 28 — Testing de extensiones Kit
Proyecto 29 — Packaging y distribución de la app
Proyecto 30 — Documentación y demo de la plataforma Kit
```

### 9.11 AEC-USD Modelling

Objetivo: fuente de verdad geométrica AEC sobre OpenUSD.

Proyectos:

```text
Proyecto 0 — Formación y análisis inicial AEC / OpenUSD / Omniverse
Proyecto 1 — Arquitectura general del módulo AEC-USD Modelling
Proyecto 2 — Modelo de dominio AEC
Proyecto 3 — Convenciones USD para AEC
Proyecto 4 — API pública y comandos nativos AEC
Proyecto 5 — Bloques paramétricos MVP
Proyecto 6 — Croquizado básico
Proyecto 7 — Extrusión de sketches a bloques AEC
Proyecto 8 — Polygon-aware rebuild
Proyecto 9 — Particiones interiores
Proyecto 10 — Spaces y zoning
Proyecto 11 — Superficies AEC y superficies térmicas
Proyecto 12 — Openings, ventanas y puertas
Proyecto 13 — Materiales, construcciones y metadata energética básica
Proyecto 14 — Importación DXF como referencia
Proyecto 15 — Snap sobre DXF y geometría existente
Proyecto 16 — Croquizado interactivo en viewport
Proyecto 17 — Modificación geométrica y rebuild seguro
Proyecto 18 — Niveles, plantas y edificios multipiso
Proyecto 19 — Plantillas paramétricas de edificios
Proyecto 20 — Validación geométrica AEC
Proyecto 21 — Inspección, debug y diagnostics
Proyecto 22 — Interoperabilidad BIM / IFC / Revit
Proyecto 23 — Compatibilidad con EnergyPlus Backend
Proyecto 24 — Compatibilidad con ThermalViz
Proyecto 25 — Integración con agente IA
Proyecto 26 — Floorplan-to-sketch futuro
Proyecto 27 — Performance y escalabilidad geométrica
Proyecto 28 — Testing AEC-USD Modelling
Proyecto 29 — Packaging y documentación de extensión AEC
Proyecto 30 — Validación final del macroproyecto AEC
```

### 9.12 Integración Backend EnergyPlus ↔ Omniverse Kit

Objetivo: puente formal entre USD/AEC y backend EnergyPlus.

Proyectos:

```text
Proyecto 0 — Formación y análisis inicial de integración Kit ↔ Backend
Proyecto 1 — Arquitectura general de integración
Proyecto 2 — Contrato de datos USD/AEC → Backend
Proyecto 3 — Mapper AEC-USD → modelo energético backend
Proyecto 4 — Validación previa desde Kit
Proyecto 5 — Comandos nativos de integración
Proyecto 6 — Modos de conexión backend
Proyecto 7 — Ejecución local directa del backend
Proyecto 8 — Ejecución como proceso externo
Proyecto 9 — Ejecución mediante REST API
Proyecto 10 — SimulationCase desde escena USD
Proyecto 11 — Gestión de configuración de simulación en Kit
Proyecto 12 — Panel de validación energética
Proyecto 13 — Generación y depuración de IDF desde Kit
Proyecto 14 — Sistema de jobs de simulación en Kit
Proyecto 15 — Progress reporting y logs
Proyecto 16 — Recepción y normalización de resultados en Kit
Proyecto 17 — Mapper Backend Results → USD
Proyecto 18 — Estrategia de almacenamiento de resultados
Proyecto 19 — Visualización inicial de resultados
Proyecto 20 — Room Stats / Space Stats Panel
Proyecto 21 — Surface Stats Panel
Proyecto 22 — Time controller y playback
Proyecto 23 — Integración con ThermalViz avanzada
Proyecto 24 — Integración con agente IA
Proyecto 25 — Comparación de simulaciones
Proyecto 26 — Flujo USD/Omniverse → EnergyPlus → Omniverse end-to-end
Proyecto 27 — Manejo de errores EnergyPlus desde Kit
Proyecto 28 — Integración con workflows batch/calibración/dataset
Proyecto 29 — Seguridad, límites y permisos
Proyecto 30 — Performance y escalabilidad
Proyecto 31 — Testing de integración
Proyecto 32 — API/SDK de integración para otros módulos
Proyecto 33 — Documentación y casos de uso
Proyecto 34 — Validación final del macroproyecto
```

### 9.13 Sensórica e ingesta de datos

Objetivo: capturar, normalizar, almacenar y mapear datos reales/históricos.

Proyectos:

```text
Proyecto 0 — Formación y análisis inicial de sensórica/BMS/IoT
Proyecto 1 — Arquitectura general de sensórica e ingesta
Proyecto 2 — Modelo de datos de sensórica
Proyecto 3 — Catálogo de sensores y variables
Proyecto 4 — Contrato de datos temporales
Proyecto 5 — Mapeo sensores ↔ edificio digital
Proyecto 6 — Conector CSV / archivos históricos
Proyecto 7 — Conector MQTT
Proyecto 8 — Conector REST/API
Proyecto 9 — Conector OPC-UA
Proyecto 10 — Conector BACnet
Proyecto 11 — Conector Modbus
Proyecto 12 — Ingesta en tiempo real
Proyecto 13 — Ingesta histórica / batch
Proyecto 14 — Normalización temporal y limpieza
Proyecto 15 — Validación de calidad de datos
Proyecto 16 — Almacenamiento de datos temporales
Proyecto 17 — SensorData API / SDK
Proyecto 18 — Sensores sintéticos y virtuales
Proyecto 19 — Simulación de red, latencia y fallos
Proyecto 20 — NVIDIA Air / DSX Air research line
Proyecto 21 — Integración con Omniverse Kit
Proyecto 22 — Integración con USD
Proyecto 23 — Visualización de datos reales
Proyecto 24 — Integración con calibración
Proyecto 25 — Integración con generación de datasets
Proyecto 26 — Integración con surrogate models
Proyecto 27 — Integración con control y optimización
Proyecto 28 — Alertas y detección de anomalías
Proyecto 29 — Seguridad, permisos y credenciales
Proyecto 30 — Performance y escalabilidad
Proyecto 31 — Testing y simuladores de sensores
Proyecto 32 — Documentación y casos de uso
Proyecto 33 — Validación final del macroproyecto
```

### 9.14 NVIDIA Air / Simulación red IoT-HVAC

Objetivo: simular infraestructura de comunicación entre sensores, gateways, BMS y HVAC.

Proyectos:

```text
Proyecto 0 — Formación y análisis inicial NVIDIA Air / DSX Air
Proyecto 1 — Arquitectura general del macroproyecto NVIDIA Air IoT-HVAC
Proyecto 2 — Modelo de dominio red IoT-HVAC
Proyecto 3 — Topologías de red para edificios inteligentes
Proyecto 4 — Contrato de mensajes sensor/control
Proyecto 5 — Integración con MQTT y brokers simulados
Proyecto 6 — Modelo de fallos de red
Proyecto 7 — Escenarios sintéticos de red
Proyecto 8 — Orquestación Air / simulador de red
Proyecto 9 — Simulación local alternativa si Air no cubre IoT directamente
Proyecto 10 — Integración con sensórica e ingesta
Proyecto 11 — Integración con control HVAC
Proyecto 12 — Impacto de red en calibración
Proyecto 13 — Impacto de red en surrogate models
Proyecto 14 — Impacto de red en control predictivo/RL
Proyecto 15 — Edge controller y fallback local
Proyecto 16 — Métricas de red e impacto energético
Proyecto 17 — Dataset de red sintética para robustez
Proyecto 18 — Visualización en Omniverse Kit
Proyecto 19 — Network Stats Panel
Proyecto 20 — Integración con agente IA
Proyecto 21 — Seguridad y políticas de red
Proyecto 22 — Integración con NVIDIA Air real
Proyecto 23 — API / SDK del módulo Air/NetworkSim
Proyecto 24 — Testing y validación
Proyecto 25 — Benchmarking de escenarios de red
Proyecto 26 — Documentación y casos de uso
Proyecto 27 — Validación final del macroproyecto
```

### 9.15 Visualización Avanzada

Objetivo: experiencia visual energética avanzada dentro de Kit.

Proyectos:

```text
Proyecto 0 — Formación y análisis inicial de visualización energética
Proyecto 1 — Arquitectura general de Visualización Avanzada
Proyecto 2 — Modelo de datos de visualización
Proyecto 3 — Contrato de datos para visualización
Proyecto 4 — Binding visual con USD
Proyecto 5 — Sistema de variables visualizables
Proyecto 6 — Time Controller y playback temporal
Proyecto 7 — Sistema de colormaps y leyendas
Proyecto 8 — ThermalViz por zonas
Proyecto 9 — ThermalViz por superficies
Proyecto 10 — Room Stats Panel
Proyecto 11 — Surface Stats Panel
Proyecto 12 — Sensor Stats Panel
Proyecto 13 — HVAC Stats Panel
Proyecto 14 — Gráficas y dashboards en Kit
Proyecto 15 — Comparación Real vs Simulado vs Predicho
Proyecto 16 — Visualización de calibración
Proyecto 17 — Visualización de datasets
Proyecto 18 — Visualización de surrogate models
Proyecto 19 — Visualización de control y optimización
Proyecto 20 — Visualización de red IoT-HVAC / NVIDIA Air
Proyecto 21 — Point cloud / NavVis-like visualization
Proyecto 22 — Heatmaps volumétricos / CFD-like visualization
Proyecto 23 — Visualización de flujos de aire / HVAC
Proyecto 24 — Visualización de coste, carbono y energía
Proyecto 25 — Alertas, anomalías y diagnóstico visual
Proyecto 26 — Reportes visuales y exportación
Proyecto 27 — Presets de visualización y workspaces
Proyecto 28 — Interacción viewport avanzada
Proyecto 29 — Performance y escalabilidad visual
Proyecto 30 — API / SDK de visualización
Proyecto 31 — Integración con agente IA
Proyecto 32 — Testing de visualización
Proyecto 33 — Documentación y casos de uso
Proyecto 34 — Validación final del macroproyecto
```

### 9.16 Agente IA

Objetivo: agente interno y agentes externos vía MCP.

Proyectos:

```text
Proyecto 0 — Formación y análisis inicial de agentes IA para software técnico
Proyecto 1 — Arquitectura general del sistema de agentes
Proyecto 2 — Modelo de dominio del agente
Proyecto 3 — Separación agente interno / agente externo
Proyecto 4 — UI del agente interno en Omniverse Kit
Proyecto 5 — Experiencia de input en lenguaje natural
Proyecto 6 — Intent parser inicial / MockLLM
Proyecto 7 — Provider layer para LLMs
Proyecto 8 — NVIDIA Nemotron / NIM integration
Proyecto 9 — Tool Registry del agente
Proyecto 10 — Estándar de resultados de tools
Proyecto 11 — Safety layer y permisos
Proyecto 12 — Agente y comandos nativos Kit
Proyecto 13 — Tools AEC Modelling
Proyecto 14 — Tools EnergyPlus Backend
Proyecto 15 — Tools de integración Kit ↔ Backend
Proyecto 16 — Tools de visualización avanzada
Proyecto 17 — Tools de sensórica
Proyecto 18 — Tools de calibración
Proyecto 19 — Tools de generación de datasets
Proyecto 20 — Tools de surrogate models
Proyecto 21 — Tools de control y optimización
Proyecto 22 — Tools NVIDIA Air / NetworkSim
Proyecto 23 — Tools CUDA-X / optimización GPU
Proyecto 24 — Agent Planner
Proyecto 25 — Plan validation y guardrails
Proyecto 26 — Context Engine del agente
Proyecto 27 — Memoria del agente
Proyecto 28 — RAG/documentación técnica para agente
Proyecto 29 — MCP Server para Omniverse Kit
Proyecto 30 — MCP Server para Backend EnergyPlus
Proyecto 31 — MCP Server para proyecto/repositorio/Codex
Proyecto 32 — MCP Client / external agent compatibility
Proyecto 33 — Agent ↔ Codex developer workflow
Proyecto 34 — Agent observability / tracing
Proyecto 35 — Confirmaciones, undo y rollback
Proyecto 36 — Evaluación del agente
Proyecto 37 — Seguridad, privacidad y límites
Proyecto 38 — Agent UX avanzado
Proyecto 39 — Agente generativo tipo SyncTwin / Edify3D
Proyecto 40 — Voice / multimodal / visión futura
Proyecto 41 — API / SDK del agente
Proyecto 42 — Performance y escalabilidad del agente
Proyecto 43 — Testing del agente y MCP
Proyecto 44 — Documentación y casos de uso
Proyecto 45 — Validación final del macroproyecto
```

### 9.17 Colaboración y despliegue

Objetivo: plataforma desplegable, colaborativa, versionada y mantenible.

Proyectos:

```text
Proyecto 0 — Formación y análisis inicial de colaboración/despliegue
Proyecto 1 — Arquitectura general de colaboración y despliegue
Proyecto 2 — Modos de despliegue del producto
Proyecto 3 — Gestión de repositorios y ramas
Proyecto 4 — Versionado del software
Proyecto 5 — Gestión de entornos de desarrollo
Proyecto 6 — Build system y scripts de desarrollo
Proyecto 7 — Packaging de la aplicación Omniverse Kit
Proyecto 8 — Distribución de extensiones Kit
Proyecto 9 — Packaging del backend EnergyPlus
Proyecto 10 — Backend como servicio
Proyecto 11 — Despliegue con Docker / contenedores
Proyecto 12 — Despliegue HPC / servidor de simulaciones
Proyecto 13 — Despliegue cloud / remoto
Proyecto 14 — Omniverse Nucleus y colaboración USD
Proyecto 15 — Estrategia de USD layers colaborativas
Proyecto 16 — Gestión de proyectos digitales compartidos
Proyecto 17 — Roles, usuarios y permisos
Proyecto 18 — Seguridad del despliegue
Proyecto 19 — Gestión de datos, outputs y almacenamiento
Proyecto 20 — Base de datos / registro de artefactos
Proyecto 21 — CI/CD básico
Proyecto 22 — Testing de despliegue
Proyecto 23 — Observabilidad, logs y monitorización
Proyecto 24 — Gestión de jobs distribuidos
Proyecto 25 — Colaboración con agentes externos / MCP
Proyecto 26 — Gestión de releases
Proyecto 27 — Instalador / distribución para usuarios
Proyecto 28 — Licencias y dependencias externas
Proyecto 29 — Documentación de despliegue y operación
Proyecto 30 — Backup, restore y recuperación
Proyecto 31 — Multiusuario y resolución de conflictos
Proyecto 32 — Performance y escalabilidad del despliegue
Proyecto 33 — Entornos de demo, staging y producción
Proyecto 34 — Soporte, mantenimiento y troubleshooting
Proyecto 35 — Validación final del macroproyecto
```

### 9.18 Economía y gestión empresarial

Objetivo: gestionar viabilidad económica, clientes, suscripciones, costes, pricing, métricas y planificación.

Proyectos:

```text
Proyecto 0 — Formación y análisis inicial de economía SaaS/software
Proyecto 1 — Arquitectura general de gestión económica
Proyecto 2 — Modelo de negocio y estrategia comercial
Proyecto 3 — Catálogo de productos, módulos y planes
Proyecto 4 — Pricing y estrategia de precios
Proyecto 5 — Gestión de clientes y cuentas
Proyecto 6 — Licencias y suscripciones
Proyecto 7 — Facturación e ingresos
Proyecto 8 — Gestión de gastos y costes
Proyecto 9 — Unit economics y rentabilidad
Proyecto 10 — Métricas SaaS y KPIs
Proyecto 11 — Forecast financiero
Proyecto 12 — Presupuesto y planificación económica
Proyecto 13 — Costes cloud, HPC y GPU
Proyecto 14 — Pricing basado en uso computacional
Proyecto 15 — CRM mínimo y pipeline comercial
Proyecto 16 — Propuestas, presupuestos y contratos
Proyecto 17 — Gestión de soporte y éxito de cliente
Proyecto 18 — Roadmap económico del producto
Proyecto 19 — Analítica de uso del software
Proyecto 20 — Dashboard económico en Notion / Excel
Proyecto 21 — Automatización económica
Proyecto 22 — Integración con herramientas externas
Proyecto 23 — Fiscalidad, forma jurídica y cumplimiento
Proyecto 24 — Plan de financiación e inversión
Proyecto 25 — Gestión de riesgos económicos
Proyecto 26 — Métricas para decidir si crear empresa
Proyecto 27 — Gestión de pilotos y primeros clientes
Proyecto 28 — Reporting mensual de negocio
Proyecto 29 — API / base de datos interna de negocio
Proyecto 30 — Validación final del macroproyecto
```

### 9.19 Marketing

Pendiente de estructurar. Debe cubrir previsiblemente:

```text
posicionamiento
marca
web
portfolio
contenido técnico
demos
casos de uso
ventas B2B
comunidad
LinkedIn
documentación comercial
landing pages
captación de leads
estrategia de lanzamiento
```

---

## 10. Decisiones sobre DesignBuilder, HVAC y módulos futuros

EnergyPlus aporta cálculo; DesignBuilder aporta workflow.

DesignBuilder ofrece sobre EnergyPlus:

```text
modelador 3D
abstracción IDF
UI de materiales/construcciones/schedules
HVAC gráfico
gestión de resultados
visualización
optimización
CFD
daylighting
librerías y plantillas
scripting/API propia
flujo de trabajo completo
```

La plataforma debe mejorar ese concepto con:

```text
Omniverse/OpenUSD
colaboración
sensores reales
IA/agentes
GPU/cuOpt
surrogates
control predictivo
visualización avanzada
```

Módulos adicionales identificados para futuro:

```text
HVAC-USD Modelling
Energy Libraries & Templates
Cost, Carbon & LCA
Daylighting & Lighting
CFD / Airflow / Thermal Fields
Diagnostics & Fault Detection
Compliance & Certification
Quantum / QUBO HVAC Optimization
```

El más importante a corto-medio plazo es **HVAC-USD Modelling**, porque para controlar un edificio real hay que modelar su sistema HVAC real, sensores, actuadores, límites y lógica.

QUBO/quantum-inspired HVAC optimization es interesante para problemas discretos:

```text
on/off de equipos
modos HVAC
setpoints discretos
schedules
secuenciación de equipos
unit commitment HVAC simplificado
```

Pero inicialmente MPC, MILP, cuOpt, GA, NSGA-II y RL probablemente serán más prácticos.

---

## 11. Qué hemos hecho hasta ahora en esta conversación

- Replantear el proyecto desde exploración tecnológica a arquitectura modular.
- Definir macroproyectos como objetivos de Notion.
- Estructurar casi todos los macroproyectos en proyectos internos.
- Alinear el método con el TFM OpenDSS: backend-first, contratos, DTOs, validación, tests, tickets Codex.
- Definir que cada macroproyecto se trata como proyecto completo tipo TFM.
- Revisar DesignBuilder vs EnergyPlus.
- Identificar la necesidad de HVAC detallado, CUDA-X/cuOpt, NVIDIA Air, agentes IA, visualización avanzada, economía y marketing.
- Preparar este documento como contexto maestro para futuros chats.

---

## 12. Qué es lo siguiente

El siguiente paso práctico será comenzar el macroproyecto:

```text
Estructura del repo/carpeta
```

Primeros tickets probables:

```text
Ticket 001 — Analizar repositorio actual y proponer estructura modular
Ticket 002 — Crear repository_architecture.md
Ticket 003 — Crear repository_tree_contract.md
Ticket 004 — Crear repository_access_policy.md
Ticket 005 — Crear .gitignore robusto
Ticket 006 — Plan de migración segura
```

Antes de código, conviene crear o consolidar documentación base:

```text
docs/PROJECT_VISION.md
docs/CODEX_RULES.md
docs/CODEX_TICKET_TEMPLATE.md
docs/architecture/
docs/design/
docs/analysis/
docs/roadmap/
```

---

## 13. Orden estratégico recomendado

```text
1. Estructura repo/carpeta
2. Configuración Codex
3. Documentación base de visión/arquitectura
4. Backend EnergyPlus
5. AEC-USD Modelling
6. Integración Backend ↔ Omniverse
7. Visualización MVP
8. Calibración
9. Dataset Generation
10. Surrogates
11. Control
12. Sensórica
13. Agente avanzado
14. NVIDIA Air / red
15. Colaboración/despliegue
16. Economía/marketing
```

Aunque ya existan prototipos Omniverse, el desarrollo robusto debe reorganizarse desde arquitectura y repo.

---

## 14. Advertencias para futuros chats

- No asumir que el objetivo inmediato es programar.
- Primero identificar macroproyecto.
- Luego identificar proyecto.
- Luego transformar en tareas/tickets.
- Cada macroproyecto tiene escala grande, tipo TFM.
- El usuario trabaja con Notion para planificación y Codex para ejecución.
- El usuario busca estructura detallada, paso a paso, orientada a Codex.
- Evitar iteraciones caóticas.
- Mantener arquitectura backend-first y separación de responsabilidades.
- En temas técnicos cambiantes de NVIDIA/OpenAI/Codex, verificar web antes de afirmar.

---

## 15. Resumen ultra corto para pegar en otro chat

```text
Estamos construyendo una plataforma modular de gemelos digitales energéticos con Omniverse Kit/OpenUSD + Backend EnergyPlus + IA. El objetivo es superar un workflow tipo DesignBuilder mediante AEC-USD modelling, backend robusto, calibración, generación de datasets, surrogates, control predictivo/RL, sensórica real, visualización avanzada, agente IA y despliegue colaborativo.

Trabajamos con Notion y Codex. Cada objetivo se trata como macroproyecto completo tipo TFM, dividido en proyectos y tareas/tickets Codex. Codex debe ejecutar tickets controlados, con scope claro, validación, tests y reporte final. No debe actuar como chat genérico.

Principios clave:
- EnergyPlus es solver, no modelo interno.
- Omniverse Kit es runtime/UI, no backend.
- OpenUSD es fuente geométrica/semántica.
- El agente IA ejecuta comandos nativos, no duplica lógica.
- ThermalViz visualiza, no es fuente de verdad.
- La estructura del repo debe reflejar la arquitectura del producto.

Siguiente paso: empezar macroproyecto “Estructura del repo/carpeta”, generando documentos base y tickets Codex para analizar el repo actual, diseñar estructura modular, separar code/references/runs/docs/extensions/backend/packages y definir reglas de acceso para Codex.
```
