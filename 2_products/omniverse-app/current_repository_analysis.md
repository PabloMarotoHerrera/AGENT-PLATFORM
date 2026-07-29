# current_repository_analysis.md

# Proyecto 0 — Análisis del repositorio actual

**Macroproyecto:** Estructura repo/carpeta  
**Repositorio analizado:** `C:\kit-app-template`  
**Estado:** análisis inicial para reorganización arquitectónica segura  
**Fecha:** 2026-05-23  

---

## 1. Objetivo del documento

Este documento recoge el análisis inicial del repositorio actual usado como base para la plataforma de gemelos digitales energéticos con NVIDIA Omniverse Kit, OpenUSD, EnergyPlus e IA.

El objetivo no es rediseñar todavía el repositorio, sino documentar el estado actual, identificar riesgos, separar lo que pertenece al template de Kit de lo que pertenece al producto propio, detectar deuda estructural y dejar una base sólida para los siguientes documentos:

- `repository_architecture.md`
- `repository_tree_contract.md`
- `external_resources_policy.md`
- `kit_extension_boundaries.md`
- `repository_access_policy.md`

---

## 2. Resumen ejecutivo

El repositorio actual parte de `kit-app-template` de NVIDIA Omniverse y conserva buena parte de su estructura original. Sobre esa base se han añadido extensiones propias AEC, visualización térmica, agente IA, documentación del proyecto y una instalación local de EnergyPlus.

La situación actual no es un caos total. El repositorio ya contiene una arquitectura funcional implícita:

```text
source/apps/
source/extensions/
docs/
tools/
EnergyPlusV24-2-0/
_build/
_compiler/
templates/
```

También existen módulos propios con una separación conceptual bastante clara:

```text
custom.aec.sketch
custom.aec.extrude
custom.aec.primitive_mesh
custom.aec.modeling
custom.aec.thermal_viz
dt.energy.agent
```

El problema principal no es la ausencia de arquitectura, sino la mezcla de niveles:

```text
código fuente propio
+ estructura gestionada por Kit App Template
+ artefactos generados
+ runtime/build
+ vendor binaries
+ instalación completa de EnergyPlus
+ documentación de proyecto
+ outputs/cachés Python
```

La prioridad inmediata debe ser **documentar boundaries y políticas**, no mover archivos todavía.

---

## 3. Principio de cautela: `source/` es zona compatible con Kit

La carpeta `source/` no debe tratarse como una carpeta genérica. Fue creada por el flujo oficial de Kit App Template y contiene:

```text
source/apps/
source/extensions/
```

Actualmente la app se encuentra en:

```text
source/apps/my_own_software.kit
```

Las extensiones propias se encuentran en:

```text
source/extensions/
```

Por tanto, cualquier migración de `source/apps` o `source/extensions` debe considerarse delicada, porque puede afectar a:

- `repo.bat`
- `repo.toml`
- `premake5.lua`
- configuración de build
- búsqueda de extensiones
- paths generados en `_build/`
- launch de la app Kit
- configuración de VSCode generada

Decisión provisional:

```text
source/apps/ y source/extensions/ se mantienen inicialmente.
No se deben mover hasta tener repository_architecture.md, repository_tree_contract.md y un plan de migración validado.
```

---

## 4. Inventario top-level actual

A partir del árbol del repo y del inventario de tamaños, se identifican las siguientes carpetas y archivos relevantes en la raíz:

```text
.github/
.vscode/
docs/
EnergyPlusV24-2-0/
readme-assets/
_build/
_compiler/
_repo/
source/
templates/
tools/

.editorconfig
.gitattributes
.gitignore
.omniverse_eula_accepted.txt
00_PROJECT_CONTEXT.txt
01_RULES_AND_LIMITATIONS.txt
02_TASKS_BACKLOG.txt
03_USD_CONVENTIONS.txt
04_CODEX_WORKFLOW.txt
05_MIGRATION_MAP.txt
06_EXTENSION_PLAYBOOK.txt
07_PROFESIONAL_VISUALIZATION.txt
CHANGELOG.md
CustomPrimitiveMesh.zip
digital_twin_contexto_maestro.md
LICENSE
premake5.lua
PRODUCT_TERMS_OMNIVERSE
README.md
repo.bat
repo.sh
repo.toml
repo_tools.toml
SECURITY.md
```

---

## 5. Clasificación inicial de carpetas

### 5.1 Código fuente propio / editable con cautela

```text
source/apps/
source/extensions/custom.aec.extrude/
source/extensions/custom.aec.modeling/
source/extensions/custom.aec.primitive_mesh/
source/extensions/custom.aec.sketch/
source/extensions/custom.aec.thermal_viz/
source/extensions/dt.energy.agent/
docs/
```

Estas carpetas contienen el código o documentación propia del producto.

### 5.2 Template / scaffolding NVIDIA

```text
templates/
tools/
repo.bat
repo.sh
repo.toml
repo_tools.toml
premake5.lua
source/extensions/my_company.my_usd_composer_setup_extension/
```

Estas zonas proceden del Kit App Template o están muy acopladas a él.

No deben tratarse como código de producto puro hasta entender completamente su papel en build, launch y packaging.

### 5.3 Vendor / recursos externos

```text
EnergyPlusV24-2-0/
PRODUCT_TERMS_OMNIVERSE
LICENSE
```

La instalación completa de EnergyPlus está actualmente dentro del repo. Es el mayor elemento externo y el mayor riesgo estructural.

### 5.4 Generado / runtime / cachés

```text
_build/
_compiler/
__pycache__/
*.pyc
```

Estas carpetas y archivos no deberían formar parte de la fuente de verdad del proyecto.

### 5.5 Documentación contextual propia

```text
00_PROJECT_CONTEXT.txt
01_RULES_AND_LIMITATIONS.txt
02_TASKS_BACKLOG.txt
03_USD_CONVENTIONS.txt
04_CODEX_WORKFLOW.txt
05_MIGRATION_MAP.txt
06_EXTENSION_PLAYBOOK.txt
07_PROFESIONAL_VISUALIZATION.txt
digital_twin_contexto_maestro.md
docs/07_USD_MODELING_CONVENTIONS.md
```

Esta documentación es valiosa, pero conviene migrarla gradualmente a una estructura documental más formal dentro de `docs/`.

---

## 6. Inventario de apps Kit

Actualmente se detectan:

```text
source/apps/my_own_software.kit
source/apps/my_own_software.kit.before_extension_cleanup
```

Interpretación:

- `my_own_software.kit` es la app activa.
- `my_own_software.kit.before_extension_cleanup` parece un backup o snapshot anterior.

Riesgo:

```text
No está formalizado qué archivo .kit es fuente activa y cuál es histórico.
```

Recomendación:

- Mantener ambos de momento.
- Documentar cuál se usa para launch.
- Mover backups históricos a una política clara más adelante, por ejemplo `docs/archive/` o `archive/`, si procede.
- No eliminar el backup hasta validar launch/build.

---

## 7. Inventario de extensiones existentes

Extensiones propias detectadas:

```text
source/extensions/custom.aec.extrude/
source/extensions/custom.aec.modeling/
source/extensions/custom.aec.primitive_mesh/
source/extensions/custom.aec.sketch/
source/extensions/custom.aec.thermal_viz/
source/extensions/dt.energy.agent/
source/extensions/my_company.my_usd_composer_setup_extension/
```

Extensiones template detectadas dentro de `templates/`:

```text
templates/extensions/basic_cpp/
templates/extensions/basic_python/
templates/extensions/basic_python_binding/
templates/extensions/python_ui/
templates/extensions/service.setup/
templates/extensions/usd_composer.setup/
templates/extensions/usd_explorer.setup/
templates/extensions/usd_viewer.messaging/
templates/extensions/usd_viewer.setup/
```

Clasificación preliminar:

| Extensión | Tipo | Estado preliminar |
|---|---|---|
| `custom.aec.sketch` | Authoring / sketching | Propia |
| `custom.aec.extrude` | Authoring / geometry generation | Propia |
| `custom.aec.primitive_mesh` | Geometry prototype | Propia |
| `custom.aec.modeling` | Semantic AEC core | Propia crítica |
| `custom.aec.thermal_viz` | Visualization / telemetry | Propia |
| `dt.energy.agent` | Agent / tools / orchestration | Propia crítica |
| `my_company.my_usd_composer_setup_extension` | App setup / template-derived | Revisar |
| `templates/extensions/*` | Template/scaffolding | Read-only / inspect-only |

---

## 8. Arquitectura funcional implícita

El repositorio ya sugiere una arquitectura por capas:

```text
App Kit
  ↓
AEC authoring extensions
  ↓
AEC semantic modeling
  ↓
Thermal visualization / telemetry
  ↓
Energy agent / tools / future backend
```

Más concretamente:

```text
custom.aec.sketch
custom.aec.extrude
custom.aec.primitive_mesh
    ↓
custom.aec.modeling
    ↓
custom.aec.thermal_viz
    ↓
dt.energy.agent
```

Esta arquitectura implícita debe conservarse, pero necesita formalizarse.

---

## 9. Análisis de `custom.aec.modeling`

Ruta:

```text
source/extensions/custom.aec.modeling/
```

Archivos principales:

```text
api.py
extension.py
opening_specs.py
partition_specs.py
rebuild.py
rebuild_polygon.py
```

Interpretación:

`custom.aec.modeling` no es solo una extensión visual. Contiene lógica de dominio AEC:

- API pública
- openings
- partitions
- rebuild
- polygon-aware rebuild
- lógica semántica del modelo

Conclusión:

```text
custom.aec.modeling es el núcleo semántico actual del sistema.
```

Riesgo:

Al vivir dentro de una extensión Kit, parte de la lógica de dominio puede quedar acoplada a Omniverse y ser difícil de testear en modo headless.

Recomendación futura:

- Extraer gradualmente lógica pura a `packages/dt_aec/`.
- Mantener la extensión como capa Kit/UI/comandos.
- Evitar que backend, agente o tests dependan de internals de extensión si puede existir API pública.

---

## 10. Análisis de authoring geométrico

Extensiones:

```text
custom.aec.sketch
custom.aec.extrude
custom.aec.primitive_mesh
```

Archivos relevantes:

```text
custom.aec.extrude/custom_aec/extrude/mesh_builder.py
custom.aec.primitive_mesh/custom_aec/primitive_mesh/mesh_builder.py
custom.aec.sketch/custom/aec/sketch/extension.py
```

Interpretación:

Estas extensiones representan la capa de creación geométrica:

- sketches
- extrusión
- generación de mallas
- primitives
- interacción inicial con viewport/stage

Riesgo:

Puede existir duplicación entre `primitive_mesh` y `extrude`.

Recomendación futura:

- Auditar `mesh_builder.py` de ambas extensiones.
- Determinar si `primitive_mesh` es prototipo histórico, feature activa o base reutilizable.
- Definir si la geometría pura debe vivir en `packages/dt_aec_geometry/` o dentro de `dt_aec`.

---

## 11. Análisis de `custom.aec.thermal_viz`

Ruta:

```text
source/extensions/custom.aec.thermal_viz/
```

Archivos principales:

```text
data_sources.py
model_access.py
mqtt_client.py
plot_widget.py
signals.py
thermal_style.py
timeseries.py
ui_telemetry.py
viewport_renderer.py
viewport_viz.py
```

Interpretación:

Esta extensión ya mezcla varias responsabilidades:

- visualización térmica
- acceso al modelo
- telemetría
- MQTT
- series temporales
- UI
- viewport rendering

Conclusión:

```text
custom.aec.thermal_viz es una extensión avanzada, pero contiene lógica que en el futuro debería separarse.
```

Posible separación futura:

```text
packages/dt_results/
packages/dt_sensors/
packages/dt_visualization/
extensions/custom.aec.thermal_viz/
```

Donde:

- `packages/dt_sensors` gestiona MQTT y datos reales/sintéticos.
- `packages/dt_results` normaliza resultados y series temporales.
- `packages/dt_visualization` define contratos visuales.
- `custom.aec.thermal_viz` solo implementa UI/viewport dentro de Kit.

---

## 12. Análisis de `dt.energy.agent`

Ruta:

```text
source/extensions/dt.energy.agent/
```

Estructura observada:

```text
dt/energy/agent/
├── extension.py
├── core/
│   ├── action_router.py
│   ├── agent_controller.py
│   ├── message_types.py
│   └── safety.py
├── llm/
│   ├── base_provider.py
│   ├── intent_parser.py
│   ├── mock_provider.py
│   └── nvidia_nim_provider.py
├── mcp/
│   └── tool_schema.py
├── tools/
│   ├── aec_inspection.py
│   ├── aec_modeling_tools.py
│   ├── dxf_tools.py
│   ├── geometry_tools.py
│   ├── idf_tools.py
│   ├── registry.py
│   ├── results.py
│   ├── scene_tools.py
│   ├── simulation_tools.py
│   ├── sketching_tools.py
│   ├── thermal_sync_tools.py
│   └── thermal_tools.py
└── ui/
    └── chat_window.py
```

Interpretación:

Esta extensión ya contiene una arquitectura de agente seria:

- core orchestration
- safety
- typed messages
- LLM provider layer
- mock provider
- NVIDIA NIM provider
- MCP schema
- tool registry
- UI chat
- herramientas AEC, IDF, simulación, thermal, scene

Conclusión:

```text
dt.energy.agent es conceptualmente un servicio/orquestador, aunque físicamente viva como extensión Kit.
```

Riesgo:

El agente está muy cerca de convertirse en una capa transversal de plataforma. Si sigue creciendo dentro de `source/extensions`, puede acoplarse demasiado a Kit.

Recomendación futura:

Separar en:

```text
packages/dt_ai/
packages/dt_tools/
packages/dt_mcp/
extensions/dt.energy.agent/
```

O mantener físicamente la extensión en `source/extensions/dt.energy.agent`, pero extraer progresivamente la lógica pura a packages.

Regla crítica:

```text
El agente no debe crear geometría, compilar IDF ni parsear resultados directamente si existen APIs públicas.
Debe orquestar comandos/tools validados.
```

---

## 13. Análisis de EnergyPlusV24-2-0

Ruta:

```text
EnergyPlusV24-2-0/
```

Tamaño aproximado:

```text
0,69 GB
```

Contiene:

```text
energyplus.exe
energyplusapi.dll
Energy+.idd
EnergyPlusComplete.idd
Energy+.schema.epJSON
ExampleFiles/
Documentation/
DataSets/
PreProcess/
PostProcess/
WeatherData/
pyenergyplus/
python_lib/
dlls y ejecutables Windows
```

Interpretación:

Es una instalación completa de EnergyPlus dentro del repo.

Riesgos:

- Aumenta mucho el tamaño del repositorio.
- Mezcla vendor binary con código fuente.
- Puede generar problemas de licencia/distribución.
- Dificulta CI y clonados.
- Dificulta GitHub.
- Puede confundir a Codex y herramientas de búsqueda.
- Contiene miles de archivos que no son código propio.
- Contiene `python_lib`, ejemplos y documentación que contaminan inventarios.

Decisión recomendada:

```text
EnergyPlusV24-2-0 debe considerarse vendor/read-only y no código propio.
```

Recomendación futura:

Evaluar moverlo a una de estas opciones:

```text
external/EnergyPlusV24-2-0/      # si se mantiene dentro del workspace pero no como source
third_party/EnergyPlusV24-2-0/   # si se versiona con mucho cuidado
local_tools/EnergyPlusV24-2-0/   # si es instalación local no versionada
C:\EnergyPlusV24-2-0\            # instalación fuera del repo
```

La decisión final debe definirse en:

```text
external_resources_policy.md
energyplus_backend_repository_structure.md
generated_files_policy.md
```

---

## 14. Análisis de `tools/`

Ruta:

```text
tools/
```

Estructura observada:

```text
tools/
├── package.bat
├── package.sh
├── VERSION.md
├── deps/
│   ├── host-deps.packman.xml
│   ├── kit-sdk-deps.packman.xml
│   ├── kit-sdk.packman.xml
│   ├── pip.toml
│   ├── repo-deps.packman.xml
│   └── user.toml
├── packman/
└── repoman/
```

Interpretación:

Esta carpeta pertenece principalmente al tooling del template NVIDIA:

- packman
- repoman
- dependencias Kit SDK
- packaging

No debe confundirse con futuros scripts propios de plataforma.

Decisión provisional:

```text
tools/ actual = Kit template tooling / NVIDIA tooling.
```

Riesgo:

Si en el futuro se añaden scripts propios aquí, se mezclará tooling de NVIDIA con tooling de producto.

Recomendación futura:

Crear separación clara:

```text
tools/                 # si se mantiene para NVIDIA/repoman/packman
scripts/               # scripts propios del proyecto
tools/internal/         # opcional, solo si se decide centralizar
```

O bien:

```text
kit_tools/             # tooling heredado de Kit
tools/                 # tooling propio
```

Esta decisión se tomará en `repository_architecture.md`.

---

## 15. Análisis de `templates/`

Ruta:

```text
templates/
```

Contiene templates oficiales o derivados del Kit App Template:

```text
templates/extensions/basic_cpp/
templates/extensions/basic_python/
templates/extensions/basic_python_binding/
templates/extensions/python_ui/
templates/extensions/service.setup/
templates/extensions/usd_composer.setup/
templates/extensions/usd_explorer.setup/
templates/extensions/usd_viewer.messaging/
templates/extensions/usd_viewer.setup/
```

Interpretación:

`templates/` parece formar parte del scaffolding del Kit App Template.

Decisión provisional:

```text
templates/ = inspect-only / read-only salvo que se esté modificando el sistema de templates.
```

No debe mezclarse con ejemplos o plantillas propias de edificios, modelos EnergyPlus o workflows. Para eso deberían existir carpetas futuras como:

```text
examples/
assets/templates/
data/templates/
docs/examples/
```

---

## 16. Análisis de documentación actual

Documentación detectada:

```text
docs/07_USD_MODELING_CONVENTIONS.md
00_PROJECT_CONTEXT.txt
01_RULES_AND_LIMITATIONS.txt
02_TASKS_BACKLOG.txt
03_USD_CONVENTIONS.txt
04_CODEX_WORKFLOW.txt
05_MIGRATION_MAP.txt
06_EXTENSION_PLAYBOOK.txt
07_PROFESIONAL_VISUALIZATION.txt
digital_twin_contexto_maestro.md
README.md
CHANGELOG.md
SECURITY.md
```

Interpretación:

Existe documentación útil, pero aún no está normalizada dentro de una estructura documental madura.

Problemas:

- Documentos importantes viven en root.
- Algunos documentos duplican función con `docs/`.
- Hay mezcla entre contexto del proyecto, reglas, backlog, convenciones y playbooks.
- Falta estructura `docs/architecture`, `docs/design`, `docs/analysis`, `docs/development`, etc.

Recomendación futura:

Migrar progresivamente a:

```text
docs/
├── README.md
├── project/
├── architecture/
├── design/
├── analysis/
├── development/
├── codex/
├── roadmap/
├── adr/
├── research/
└── archive/
```

No mover todavía sin plan.

---

## 17. Archivos generados y cachés detectados

Se detectan múltiples carpetas `__pycache__` dentro de extensiones:

```text
source/extensions/*/**/__pycache__/
```

También archivos `.pyc`:

```text
*.cpython-312.pyc
```

Interpretación:

Son artefactos generados por Python y no deberían estar versionados.

Acción recomendada futura:

- Añadir o confirmar reglas en `.gitignore`.
- Limpiar cachés del working tree.
- Añadir script de cleanup seguro.
- Evitar que Codex los lea como fuente.

---

## 18. Identificación preliminar de carpetas read-only

Propuesta inicial:

```text
EnergyPlusV24-2-0/
templates/
tools/packman/
tools/repoman/
_build/
_compiler/
_repo/
```

Matices:

- `_build/`, `_compiler/`, `_repo/` no son exactamente read-only: son generated/runtime. Codex no debería modificarlos manualmente.
- `tools/packman` y `tools/repoman` deben tratarse como vendor/template tooling.
- `EnergyPlusV24-2-0` debe tratarse como vendor/read-only hasta definir política externa.

---

## 19. Identificación preliminar de carpetas editables por Codex

Con scope explícito, Codex podría modificar:

```text
docs/
source/extensions/custom.aec.extrude/
source/extensions/custom.aec.modeling/
source/extensions/custom.aec.primitive_mesh/
source/extensions/custom.aec.sketch/
source/extensions/custom.aec.thermal_viz/
source/extensions/dt.energy.agent/
source/apps/my_own_software.kit
```

Pero con restricciones:

- No tocar app `.kit` sin ticket explícito.
- No tocar `premake5.lua` sin ticket explícito.
- No modificar `repo.toml` sin ticket explícito.
- No modificar tooling NVIDIA sin ticket explícito.
- No tocar EnergyPlus salvo lectura.
- No tocar `_build` ni `_compiler`.

---

## 20. Identificación preliminar de módulos mezclados

### 20.1 `custom.aec.thermal_viz`

Mezcla:

```text
visualización + datos + MQTT + timeseries + acceso a modelo
```

Debe separarse progresivamente.

### 20.2 `dt.energy.agent`

Mezcla:

```text
extensión Kit + UI + core agent + LLM + MCP + tools + IDF + simulation + AEC tools
```

Arquitectura conceptual correcta, pero físicamente demasiado concentrada.

### 20.3 `custom.aec.modeling`

Mezcla posible:

```text
domain logic + Kit extension + USD operations
```

Debe auditarse para extraer lógica pura a package interno.

### 20.4 Root docs

Mezcla:

```text
contexto + backlog + reglas + playbooks + migración + visión
```

Debe normalizarse en `docs/`.

---

## 21. Identificación preliminar de duplicaciones

Posibles duplicaciones a revisar:

```text
custom.aec.extrude/mesh_builder.py
custom.aec.primitive_mesh/mesh_builder.py
```

Posible solapamiento entre:

```text
03_USD_CONVENTIONS.txt
docs/07_USD_MODELING_CONVENTIONS.md
digital_twin_contexto_maestro.md
```

Posible duplicación conceptual entre:

```text
custom.aec.thermal_viz/model_access.py
dt.energy.agent/tools/thermal_sync_tools.py
dt.energy.agent/tools/thermal_tools.py
```

Posible duplicación de herramientas AEC:

```text
dt.energy.agent/tools/aec_modeling_tools.py
dt.energy.agent/tools/geometry_tools.py
dt.energy.agent/tools/sketching_tools.py
custom.aec.modeling/api.py
```

Estas duplicaciones deben confirmarse leyendo código, no solo estructura.

---

## 22. Deuda estructural principal

La deuda estructural se resume en:

1. EnergyPlus instalado dentro del repo.
2. Lógica de dominio viviendo dentro de extensiones Kit.
3. Agente IA físicamente concentrado dentro de una extensión.
4. Thermal visualization mezclando datos, MQTT, UI y rendering.
5. Artefactos generados `__pycache__` dentro de source.
6. Root con demasiados documentos propios.
7. Falta de carpeta `packages/` para lógica Python reusable.
8. Falta de carpeta `backend/` para EnergyPlus backend propio.
9. Falta de carpeta `schemas/` para contratos.
10. Falta de separación formal entre vendor, generated, source, runtime y docs.
11. Dependencia fuerte del layout generado por Kit App Template.
12. Ausencia de política formal Codex por carpeta.

---

## 23. Riesgos de migración

Riesgos altos:

```text
Mover source/apps/
Mover source/extensions/
Modificar repo.toml
Modificar premake5.lua
Modificar layout de extensión sin actualizar extension.toml
Eliminar my_company.my_usd_composer_setup_extension
Eliminar backups .kit sin validar launch
Eliminar EnergyPlus sin adaptar paths
```

Riesgos medios:

```text
Mover docs root a docs/
Separar thermal_viz en packages
Separar dt.energy.agent core en packages
Renombrar custom.aec.* a dt.aec.*
Limpiar __pycache__
```

Riesgos bajos:

```text
Crear docs/architecture/
Crear docs/analysis/
Crear docs/design/
Crear scripts/ propios
Crear schemas/
Crear packages/ vacío
Crear backend/ vacío
Crear tests/ vacío
Actualizar .gitignore
```

---

## 24. Recomendaciones inmediatas

### 24.1 No mover código todavía

Antes de migrar:

```text
1. current_repository_analysis.md
2. repository_architecture.md
3. repository_tree_contract.md
4. repository_access_policy.md
5. external_resources_policy.md
```

### 24.2 Congelar `source/` como zona Kit-managed

Definir provisionalmente:

```text
source/apps/       = Kit app source
source/extensions/ = Kit extension source
```

No mover hasta comprobar build/launch.

### 24.3 Crear documentación estructural

Primera estructura documental recomendada:

```text
docs/
├── analysis/
│   └── current_repository_analysis.md
├── architecture/
├── design/
├── development/
├── codex/
└── roadmap/
```

### 24.4 Definir política EnergyPlus

EnergyPlus debe convertirse en vendor/read-only o salir del repo.

### 24.5 Limpiar generados

A corto plazo:

```text
__pycache__/
*.pyc
```

deben ignorarse y limpiarse.

### 24.6 Separar packages a medio plazo

Futuros candidatos a package:

```text
packages/dt_aec/
packages/dt_energy/
packages/dt_energyplus/
packages/dt_results/
packages/dt_sensors/
packages/dt_ai/
packages/dt_visualization/
```

---

## 25. Estado de madurez por área

| Área | Estado actual | Madurez | Riesgo |
|---|---|---:|---:|
| Kit app | Existe y arranca presumiblemente | Media | Medio |
| Extensiones AEC | Existen varias | Media | Medio |
| AEC semantic core | Existe en `custom.aec.modeling` | Media-alta | Alto si se acopla |
| Thermal visualization | Bastante avanzada | Media | Alto por mezcla |
| Agent IA | Arquitectura avanzada | Media-alta | Alto por acoplamiento |
| Backend EnergyPlus propio | No separado | Baja | Alto |
| EnergyPlus vendor | Instalado dentro repo | Baja estructural | Alto |
| Docs | Útiles pero dispersos | Media-baja | Medio |
| Tests | Parciales en extensiones | Baja | Medio |
| Runtime/build separation | Insuficiente | Baja | Alto |
| Codex governance | Conceptual, no formalizada en repo | Media-baja | Alto |

---

## 26. Decisiones preliminares

### Decisión 1

```text
No se migrará source/apps ni source/extensions en el Proyecto 0.
```

Motivo: son carpetas generadas/esperadas por Kit App Template y pueden estar acopladas al sistema de build.

### Decisión 2

```text
EnergyPlusV24-2-0 se considera vendor/read-only provisional.
```

Motivo: es una instalación externa completa, no código propio.

### Decisión 3

```text
custom.aec.modeling se considera candidato principal a core semántico.
```

Motivo: contiene API, openings, partitions y rebuild.

### Decisión 4

```text
dt.energy.agent se considera extensión de UI/runtime con core extraíble a package futuro.
```

Motivo: contiene lógica transversal de agente, LLM, MCP y tools.

### Decisión 5

```text
custom.aec.thermal_viz se considera extensión de visualización con lógica de datos extraíble.
```

Motivo: mezcla MQTT, timeseries, UI y viewport rendering.

---

## 27. Próximos documentos recomendados

Orden recomendado:

```text
1. repository_architecture.md
2. repository_tree_contract.md
3. external_resources_policy.md
4. kit_extension_boundaries.md
5. internal_packages_architecture.md
6. generated_files_policy.md
7. repository_access_policy.md
```

---

## 28. Siguiente ticket Codex recomendado

```text
# Ticket 002 — Crear repository_architecture.md

## Objetivo
Definir la arquitectura objetivo del repositorio respetando la compatibilidad con Kit App Template.

## Alcance
Crear `docs/architecture/repository_architecture.md`.

## Restricción crítica
No mover archivos ni modificar código.

## Resultado esperado
Documento que defina:
- capas del repositorio
- source vs generated vs vendor vs runtime
- rol de `source/`
- rol de `packages/`
- rol de `backend/`
- rol de `docs/`
- rol de `scripts/`
- dependency directions
- boundaries
- decisiones provisionales
```

---

## 29. Conclusión

El repositorio actual no debe verse como un desorden sin valor, sino como un prototipo avanzado construido sobre Kit App Template que ya contiene una arquitectura implícita potente.

La prioridad no es reescribir ni mover, sino formalizar:

```text
qué es fuente
qué es generado
qué es vendor
qué es runtime
qué es extensión
qué es package
qué es backend
qué puede tocar Codex
qué debe permanecer read-only
```

La dirección recomendada es evolucionar hacia un monorepo modular manteniendo inicialmente la compatibilidad con Omniverse Kit App Template.

