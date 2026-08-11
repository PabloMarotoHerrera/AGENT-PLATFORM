# Siamese — Módulo de Calibración

**Documento:** Contexto técnico del módulo de calibración dentro de Siamese  
**Proyecto:** Siamese — plataforma agéntica de gemelos digitales energéticos  
**Estado:** Documento de arquitectura conceptual previo a implementación  
**Versión:** 0.1  
**Propósito:** definir qué es el módulo de calibración de Siamese, qué problema resuelve, cómo se relaciona con EnergyPlus, el backend Python, Omniverse Kit, OpenUSD, sensórica, datasets, modelos surrogados, control, optimización y flujos agénticos.

---

## 1. Resumen ejecutivo

El módulo de calibración es el componente que transforma un modelo energético teórico en un modelo que representa de forma aproximada el comportamiento real de un edificio observado.

En Siamese, calibrar significa comparar datos simulados con datos reales —sensores, consumos, BMS, horarios reales o datos operativos— y ajustar variables físicas, operativas y de sistema hasta reducir el error entre ambos mundos.

La idea central es:

```text
Modelo energético base
+ datos reales del edificio
+ optimización
= modelo energético calibrado
```

Sin calibración, Siamese puede simular. Con calibración, Siamese empieza a crear un gemelo energético vivo.

La calibración es el puente entre:

```text
edificio real
↓
sensores / consumos / BMS
↓
datos reales
```

Y:

```text
modelo EnergyPlus / Siamese
↓
simulación
↓
datos simulados
```

La salida principal del módulo es un **CalibratedModel**: una versión del modelo energético con parámetros ajustados, métricas de error, trazabilidad, estado de aprobación y evidencia suficiente para ser usado en análisis de escenarios, generación de datasets, entrenamiento de modelos surrogados y, progresivamente, shadow mode o control supervisado.

---

## 2. Principio fundamental

La regla central del módulo es:

```text
Un modelo sin calibrar representa un edificio supuesto.
Un modelo calibrado representa un edificio observado.
```

EnergyPlus aporta rigor físico, pero su precisión depende directamente de la calidad de los datos de entrada.

En edificios existentes, muchos datos no se conocen con precisión:

```text
composición real de muros;
aislamento efectivo;
infiltraciones;
horarios reales;
ocupación real;
uso de ventanas;
estado real del sistema HVAC;
consignas reales;
intervenciones de mantenimiento;
ganancias internas;
comportamiento de usuarios.
```

La calibración no elimina toda la incertidumbre, pero permite reducirla de forma medible y trazable.

---

## 3. Por qué la calibración es crítica en Siamese

Siamese no quiere ser solo una herramienta de diseño energético. Su objetivo es conectar simulación, datos reales, predicción y operación.

Ese objetivo no puede alcanzarse con modelos no calibrados.

Flujo sin calibración:

```text
modelo energético
→ simulación
→ resultado teórico
→ informe
```

Flujo con calibración:

```text
modelo energético
→ comparación con datos reales
→ calibración
→ modelo calibrado
→ datasets físicos
→ surrogate models
→ predicción
→ recomendaciones
→ operación asistida
```

La calibración es, por tanto, el punto donde Siamese pasa de ser una plataforma de análisis a una plataforma de gemelo vivo.

---

## 4. Origen conceptual desde el TFG

El TFG del C.E.P. Divino Maestro ya contenía la semilla técnica de este módulo:

```text
1. Se instaló sensórica real de temperatura y humedad.
2. Se modeló el edificio en DesignBuilder.
3. Se compararon datos reales con datos simulados.
4. Se ajustaron variables del modelo.
5. Se utilizaron algoritmos genéticos para mejorar el calibrado.
6. Se analizaron escenarios de mejora.
```

El problema fue que ese proceso era manual y fragmentado:

```text
sensores → CSV;
DesignBuilder → exportación de resultados;
scripts → comparación;
algoritmos genéticos → calibración;
informe → modelo archivado.
```

Siamese convierte esa experiencia en un módulo sistemático:

```text
sensores → ingesta estructurada;
modelo EnergyPlus → backend propio;
CSV manual → time-series layer;
comparación manual → Calibration Engine;
algoritmos genéticos aislados → optimizadores gobernados;
modelo archivado → CalibratedModel versionado;
calibración puntual → base de datasets, surrogates y operación.
```

---

## 5. Qué es calibrar en Siamese

Calibrar consiste en encontrar un conjunto de parámetros del modelo que minimicen la diferencia entre las salidas simuladas y las observadas.

Formalmente, Siamese parte de:

```text
Modelo base M
Parámetros calibrables θ
Datos reales Y_real
Solver EnergyPlus E(M, θ)
Métrica de error f(Y_sim, Y_real)
```

Y busca:

```text
θ* = argmin f(E(M, θ), Y_real)
```

En la práctica, no debe presentarse al usuario como una ecuación, sino como un proceso de ingeniería:

```text
Seleccionar datos reales
→ seleccionar variables calibrables
→ definir rangos físicos
→ ejecutar simulaciones candidatas
→ comparar con datos reales
→ evaluar métricas
→ seleccionar modelo calibrado
→ validar y aprobar
```

---

## 6. Qué variables puede calibrar Siamese

### 6.1 Parámetros físicos de envolvente

```text
U-value equivalente de muros;
U-value de cubierta;
U-value de suelo;
U-value de ventanas;
factor solar del acristalamiento;
transmitancia térmica equivalente;
capacidad térmica efectiva;
masa térmica efectiva;
conductividad equivalente;
absorptancia solar;
emisividad.
```

Estos parámetros son especialmente importantes cuando no se conocen los materiales reales del edificio.

### 6.2 Parámetros de infiltración y ventilación

```text
air changes per hour;
infiltration rate;
ventilation rate;
ventilation schedule;
window opening factor;
natural ventilation setpoint;
mechanical ventilation flow;
fan operation schedule.
```

En edificios existentes, la infiltración y la ventilación real suelen ser fuentes importantes de error.

### 6.3 Parámetros de ocupación

```text
horarios reales de ocupación;
densidad de ocupación;
multiplicador de ocupación;
ganancias metabólicas;
actividad;
uso irregular de aulas o espacios;
periodos de recreo;
periodos sin actividad.
```

La ocupación afecta tanto a temperatura como a humedad, CO₂ y cargas internas.

### 6.4 Parámetros de cargas internas

```text
iluminación;
equipos eléctricos;
ordenadores;
cocinas/comedor;
equipamiento especial;
cargas por aula;
cargas por horario;
multiplicadores de potencia.
```

### 6.5 Parámetros HVAC

```text
horario de calefacción;
horario de refrigeración;
consignas;
temperatura de impulsión;
potencia efectiva de radiadores;
eficiencia de caldera;
eficiencia de bomba de calor;
curvas de operación;
caudales;
válvulas;
bombas;
ventiladores;
controladores.
```

### 6.6 Parámetros operativos

```text
persianas;
sombreamiento;
apertura de ventanas;
intervenciones manuales;
modo vacaciones;
modo fin de semana;
acciones de mantenimiento;
programación de centralita;
setpoints horarios.
```

---

## 7. Arquitectura general del módulo

La arquitectura conceptual del módulo es:

```text
Reference Data
    ↓
Calibration Data Adapter
    ↓
Calibration Target Builder
    ↓
Parameter Space
    ↓
Optimizer
    ↓
EnergyPlus Simulation Campaign
    ↓
Metrics Evaluator
    ↓
Candidate Ranking / Pareto Front
    ↓
Calibrated Model Registry
    ↓
Validation Report + Approval Gate
```

Componentes principales:

```text
CalibrationJob
CalibrationTarget
CalibrationParameter
ParameterSpace
CalibrationCandidate
SimulationCampaign
MetricsEvaluator
Optimizer
ParetoAnalyzer
CalibrationReport
CalibratedModelRegistry
ApprovalGate
```

---

## 8. Entradas del módulo

### 8.1 Modelo base

El modelo base puede proceder de:

```text
modelo creado en Siamese;
modelo adoptado desde DesignBuilder;
IDF importado;
epJSON importado;
OpenStudio / OSM;
modelo generado desde OpenUSD;
modelo reconstruido desde planos;
modelo simplificado grey-box.
```

### 8.2 Datos reales

Fuentes posibles:

```text
sensores de temperatura;
sensores de humedad;
CO₂;
ocupación;
contadores eléctricos;
contadores de gas;
BMS;
BACnet;
Modbus;
OPC-UA;
MQTT;
REST;
CSV histórico;
datos meteorológicos;
datos de mantenimiento;
horarios reales.
```

### 8.3 Datos climáticos

El clima debe estar alineado con el periodo de calibración:

```text
EPW;
CSV meteorológico;
estación cercana;
API meteorológica;
datos medidos in situ;
correcciones locales.
```

### 8.4 Periodo de calibración

No todos los periodos sirven. Deben seleccionarse periodos representativos:

```text
semana tipo;
periodo frío;
periodo cálido;
periodo con HVAC activo;
periodo con buena cobertura de sensores;
periodo sin fallos relevantes;
periodo con ocupación conocida;
periodo estable para análisis.
```

También deben existir periodos de validación independientes.

---

## 9. Salidas del módulo

El módulo de calibración debe producir:

```text
modelo calibrado versionado;
valores calibrados de parámetros;
métricas de error;
informe de calibración;
curvas real vs simulado;
mapa de error por zona;
frente de Pareto;
ranking de candidatos;
diagnóstico de incertidumbre;
calibration quality score;
recomendaciones de sensores adicionales;
estado de aprobación;
evidencia para agentes y usuarios.
```

Salida principal:

```yaml
CalibratedModel:
  calibrated_model_id: calibrated_model_v03
  base_model_id: energy_model_v12
  calibration_job_id: cal_job_001
  selected_candidate_id: candidate_027
  target_period: 2026-04-22/2026-04-29
  status: pending_approval
  metrics:
    CVRMSE_temperature: 8.7
    NMBE_temperature: 2.1
    NMAE_temperature: 5.4
```

---

## 10. Métricas de calibración

### 10.1 CVRMSE

Métrica habitual para medir la dispersión relativa del error.

Uso:

```text
comparar ajuste general;
validar calidad de calibración;
evaluar candidatos;
comparar zonas.
```

### 10.2 NMBE

Métrica que indica sesgo medio. Permite saber si el modelo tiende a sobreestimar o subestimar.

Uso:

```text
identificar sesgo sistemático;
detectar modelos que parecen buenos pero están desplazados;
equilibrar ajuste.
```

### 10.3 NMAE

Error absoluto medio normalizado. Útil para interpretar error medio de forma directa.

### 10.4 RMSE / MAE

Métricas generales útiles para temperatura, humedad, consumo y variables HVAC.

### 10.5 Métricas temporales avanzadas

Siamese debe añadir métricas que midan forma dinámica, no solo error medio:

```text
error de picos;
error en fase temporal;
error en arranque HVAC;
error en apagado;
error nocturno;
error diurno;
error en transitorios;
error de pendiente;
error en inercia térmica;
error ante cambios de ocupación.
```

Estas métricas son esenciales si el modelo calibrado se usará para surrogates y control.

---

## 11. Tipos de calibración

### 11.1 Calibración manual asistida

El usuario o ingeniero ajusta variables con ayuda del sistema.

Uso inicial:

```text
MVP;
validación de flujo;
casos pequeños;
aprendizaje experto.
```

### 11.2 Calibración automática monoobjetivo

Un optimizador busca minimizar una función objetivo.

Ejemplo:

```text
minimizar CVRMSE de temperatura de zona.
```

### 11.3 Calibración multiobjetivo

Se optimizan varios objetivos simultáneamente:

```text
error de temperatura;
error de humedad;
error de consumo;
penalización física;
coherencia entre zonas;
estabilidad temporal.
```

### 11.4 Calibración multizona

Calibra múltiples zonas y niveles jerárquicos de parámetros.

### 11.5 Calibración contra consumo

Usa consumos reales de electricidad, gas, calefacción o refrigeración.

### 11.6 Calibración contra BMS

Usa datos operativos del sistema HVAC.

### 11.7 Recalibración

Actualiza un modelo previamente calibrado ante drift o cambios del edificio.

### 11.8 Calibración asistida por surrogate

Usa modelos rápidos para reducir el número de simulaciones EnergyPlus necesarias.

---

## 12. Algoritmos genéticos

Los algoritmos genéticos son una familia de optimización inspirada en evolución. Son adecuados para calibración energética porque EnergyPlus actúa como una caja negra: se prueban parámetros, se ejecuta simulación y se mide el error.

### 12.1 Conceptos

```text
Individuo = conjunto de parámetros calibrables.
Población = conjunto de individuos.
Fitness = calidad del individuo según métricas.
Generación = iteración del algoritmo.
Crossover = combinación de parámetros de individuos.
Mutación = cambio aleatorio controlado.
Selección = elección de mejores candidatos.
```

### 12.2 Flujo

```text
1. Crear población inicial.
2. Compilar cada candidato.
3. Ejecutar EnergyPlus.
4. Comparar con datos reales.
5. Calcular fitness.
6. Seleccionar candidatos.
7. Cruzar y mutar.
8. Crear nueva generación.
9. Repetir hasta convergencia o límite.
```

### 12.3 Encaje con Siamese

```text
Calibration Engine
→ genera candidatos
→ Backend EnergyPlus ejecuta simulaciones
→ Metrics Evaluator calcula error
→ Optimizer crea nueva generación
→ Registry guarda candidatos y evidencia
```

### 12.4 Ventajas

```text
no requiere gradientes;
funciona con EnergyPlus como caja negra;
explora espacios complejos;
soporta variables continuas y discretas;
puede paralelizar evaluaciones.
```

### 12.5 Limitaciones

```text
coste computacional alto;
convergencia lenta;
riesgo de overfitting;
soluciones físicamente absurdas si no hay restricciones;
variabilidad entre ejecuciones;
difícil interpretación si hay demasiadas variables.
```

---

## 13. NSGA-II

NSGA-II es un algoritmo evolutivo multiobjetivo. En lugar de buscar una única solución, busca un conjunto de soluciones de compromiso llamado frente de Pareto.

### 13.1 Por qué es útil

La calibración real rara vez tiene un único objetivo. Siamese puede querer minimizar simultáneamente:

```text
CVRMSE de temperatura;
NMBE de temperatura;
error de humedad;
error de consumo;
penalización de parámetros no plausibles;
diferencia entre zonas similares;
complejidad del modelo.
```

NSGA-II permite no forzar todos los objetivos en una única métrica artificial.

### 13.2 Frente de Pareto

Una solución pertenece al frente de Pareto si no hay otra solución mejor en todos los objetivos al mismo tiempo.

Ejemplo:

```text
Candidato A: muy bueno en temperatura, peor en consumo.
Candidato B: bueno en consumo, peor en temperatura.
Candidato C: equilibrio razonable.
```

El usuario puede elegir según criterio técnico.

### 13.3 Pipeline NSGA-II en Siamese

```text
1. Definir objetivos.
2. Definir parámetros y bounds.
3. Crear población inicial.
4. Ejecutar simulaciones.
5. Calcular vector de objetivos.
6. Ordenar por dominancia.
7. Mantener diversidad con crowding distance.
8. Cruzar y mutar.
9. Repetir.
10. Presentar Pareto front.
11. Seleccionar candidato.
12. Crear CalibratedModel.
```

### 13.4 Ejemplo de objetivos

```yaml
objectives:
  - minimize: CVRMSE_temperature
  - minimize: abs_NMBE_temperature
  - minimize: CVRMSE_humidity
  - minimize: gas_consumption_error
  - minimize: physical_parameter_penalty
```

---

## 14. Otros algoritmos relevantes

### 14.1 Random search

Útil como baseline simple.

### 14.2 Latin Hypercube Sampling

Útil para explorar el espacio de variables de forma más uniforme.

### 14.3 Optimización bayesiana

Puede reducir simulaciones cuando cada evaluación EnergyPlus es cara.

### 14.4 CMA-ES

Puede ser útil para espacios continuos complejos.

### 14.5 Surrogate-assisted calibration

Entrena un modelo aproximado del error para proponer candidatos sin ejecutar EnergyPlus siempre.

### 14.6 Optimización híbrida

Combinación recomendada:

```text
screening inicial;
random/LHS;
GA o NSGA-II;
refinamiento local;
validación cruzada;
aprobación humana.
```

---

## 15. Calibración multizona

La calibración multizona es un objetivo estratégico de Siamese.

Un edificio real no es una colección de zonas aisladas. Las zonas interactúan mediante:

```text
particiones internas;
pasillos;
plantas;
transferencia térmica;
ventilación;
HVAC común;
ocupación;
radiación solar;
inercia térmica;
sombreamiento;
uso real.
```

Por ello, calibrar una zona de forma aislada puede producir inconsistencias globales.

---

## 16. Estrategia multizona jerárquica

Siamese debe calibrar por niveles:

```text
Nivel global
→ parámetros comunes del edificio.

Nivel grupo
→ parámetros de familias de zonas.

Nivel local
→ ajustes específicos por zona.
```

### 16.1 Parámetros globales

```text
envolvente general;
eficiencia del sistema;
infiltración base;
horarios generales;
clima;
setpoints comunes.
```

### 16.2 Parámetros por grupo

```text
aulas sur;
aulas norte;
pasillos;
despachos;
comedores;
zonas bajo cubierta;
zonas sin uso.
```

### 16.3 Parámetros locales

```text
ocupación de Aula_3B;
ventilación manual de Aula_4A;
sensor offset de Dirección;
radiador particular;
sombreamiento local.
```

---

## 17. Zonas tipo

Para escalar, Siamese debe identificar zonas representativas.

Criterios:

```text
orientación;
uso;
planta;
exposición solar;
tipo de envolvente;
ocupación;
presencia de sensor;
comportamiento térmico;
relación con HVAC;
calidad de datos.
```

Ejemplo:

```text
Aula sur con alta radiación;
aula norte;
despacho;
pasillo;
comedor;
zona bajo cubierta;
zona no ocupada.
```

Estas zonas tipo permiten calibrar de forma eficiente y transferir parámetros a zonas similares.

---

## 18. Calibración contra temperatura, humedad y consumo

### 18.1 Temperatura

Variable inicial más directa y útil para confort e inercia térmica.

### 18.2 Humedad

Más compleja, pero importante para confort, ventilación y calidad ambiental.

### 18.3 Consumo

Necesario para calibración energética global.

### 18.4 BMS/HVAC

Crítico para pasar de análisis a operación.

Siamese debe permitir calibraciones progresivas:

```text
primero temperatura;
después humedad;
después consumo;
después HVAC;
después multizona y control.
```

---

## 19. Data quality

La calibración depende de datos reales. Por tanto, el módulo debe incluir checks de calidad:

```text
huecos temporales;
outliers;
sensores congelados;
drift;
desfase horario;
unidades incorrectas;
sensores mal ubicados;
periodos no representativos;
fallos de estación meteorológica;
datos duplicados;
ruido excesivo.
```

Cada fuente debe tener un score de confianza.

Ejemplo:

```yaml
ReferenceDataQuality:
  sensor_id: aula_3b_temp
  completeness: 0.94
  outlier_rate: 0.02
  drift_suspected: false
  time_alignment: valid
  usable_for_calibration: true
```

---

## 20. Overfitting y validación cruzada

Un modelo puede calibrarse muy bien contra un periodo concreto y fallar en otro.

Siamese debe separar:

```text
periodo de calibración;
periodo de validación;
periodo de test operativo.
```

También debe mostrar:

```text
calibration error;
validation error;
gap between both;
overfitting warning.
```

Ejemplo:

```yaml
CalibrationQuality:
  calibration_CVRMSE: 7.8
  validation_CVRMSE: 14.2
  overfitting_risk: high
```

---

## 21. Penalizaciones físicas

El optimizador puede encontrar soluciones matemáticamente buenas pero físicamente absurdas.

Siamese debe incluir penalizaciones:

```text
valores fuera de rango plausible;
diferencias excesivas entre zonas similares;
inercia térmica imposible;
consumos no realistas;
respuestas HVAC irreales;
parámetros que contradicen documentación disponible;
cambios bruscos injustificados.
```

Esto es esencial para que la calibración sea defendible ante ingenieros.

---

## 22. Relación con EnergyPlus

EnergyPlus ejecuta cada candidato.

Flujo:

```text
CalibrationCandidate
→ modificar parámetros del EnergyModel
→ compilar a IDF/epJSON
→ ejecutar EnergyPlus
→ normalizar resultados
→ calcular métricas
```

EnergyPlus no decide qué calibrar. Eso lo decide Siamese.

EnergyPlus no compara contra sensores. Eso lo hace Calibration Engine.

EnergyPlus no aprueba modelos. Eso lo hace Siamese mediante validación y aprobación humana.

---

## 23. Relación con backend Python

El módulo de calibración vive sobre el backend Python.

Depende de:

```text
EnergyModel;
SimulationCase;
EnergyPlus Runner;
NormalizedResults;
SensorData;
WeatherProfile;
Artifact Registry;
Job Manager;
Diagnostics;
Approval Gates.
```

No debe tener lógica duplicada de ejecución EnergyPlus. Debe usar el backend EnergyPlus existente.

---

## 24. Relación con Omniverse Kit

Omniverse Kit visualiza el proceso.

Debe mostrar:

```text
zonas calibradas;
zonas con error alto;
curvas real vs simulado;
frente de Pareto;
parámetros calibrados;
calidad de datos;
estado del job;
modelo calibrado seleccionado;
aprobaciones pendientes.
```

Kit no calcula la calibración. La hace entendible.

---

## 25. Relación con OpenUSD

USD puede representar:

```text
zonas;
sensores;
metadatos de calibración;
mapas de error;
capas visuales de candidatos;
anotaciones;
estado de aprobación.
```

No debe almacenar:

```text
todas las simulaciones crudas;
todos los resultados temporales pesados;
todos los candidatos completos;
logs masivos;
datasets.
```

USD debe enlazar a artefactos backend mediante IDs y referencias.

---

## 26. Relación con Dataset Factory

La calibración es prerrequisito para datasets físicamente realistas.

Flujo:

```text
EnergyModel base
→ CalibratedModel
→ DatasetCampaign
→ Simulaciones masivas
→ Dataset ML-ready
```

La calidad del dataset depende de:

```text
calidad del modelo calibrado;
calidad de datos reales;
calidad de parámetros calibrados;
validación temporal;
incertidumbre.
```

---

## 27. Relación con Surrogate Models

Los modelos surrogados deben entrenarse preferentemente sobre modelos calibrados.

La calibración aporta:

```text
inercia térmica más realista;
comportamiento por zonas;
respuesta HVAC aproximada;
sensibilidad a clima;
sensibilidad a ocupación;
dinámica temporal realista.
```

Esto permite surrogates más útiles para:

```text
predicción;
masking de sensores;
shadow mode;
recomendación;
control supervisado.
```

---

## 28. Relación con control

No debería permitirse control operativo sobre un modelo no calibrado.

Estados recomendados:

```text
uncalibrated;
partially_calibrated;
calibrated_for_analysis;
calibrated_for_prediction;
calibrated_for_shadow_mode;
calibrated_for_supervised_control.
```

Regla:

```text
Para análisis → calibración básica puede ser suficiente.
Para predicción → calibración validada temporalmente.
Para shadow mode → surrogate validado sobre modelo calibrado.
Para control supervisado → calibración robusta + límites + aprobación humana.
```

---

## 29. Relación con flujos agénticos

El Calibration Agent puede:

```text
analizar datos disponibles;
proponer periodos;
proponer zonas tipo;
proponer variables calibrables;
definir bounds iniciales;
lanzar CalibrationJobs;
resumir candidatos;
generar reportes;
detectar overfitting;
crear tareas de datos faltantes.
```

No debe poder:

```text
aprobar modelo calibrado final;
desplegar surrogate operativo;
activar control;
borrar datos reales;
ignorar diagnósticos críticos;
modificar parámetros fuera de bounds aprobados.
```

Todo debe pasar por:

```text
Tool Registry;
Policy Engine;
Evidence Registry;
Approval Gates;
Execution Inspector;
Roadmap Engine.
```

---

## 30. Workflow agéntico de calibración

Ejemplo completo:

```text
1. Usuario selecciona Roadmap: Calibración multizona.
2. Calibration Agent inspecciona sensores.
3. Agent propone zonas tipo.
4. Usuario aprueba zonas.
5. Agent propone variables y bounds.
6. Usuario aprueba rangos.
7. Calibration Engine lanza NSGA-II.
8. EnergyPlus Runner ejecuta candidatos.
9. Metrics Evaluator calcula errores.
10. Pareto Analyzer genera frente.
11. Agent resume resultados.
12. Usuario selecciona candidato.
13. Siamese crea CalibratedModel v1.
14. Approval Gate bloquea Dataset Factory hasta aprobación.
```

---

## 31. Arquitectura interna recomendada

```text
siamese_backend/calibration/
│
├── contracts/
│   ├── calibration_job.py
│   ├── calibration_target.py
│   ├── calibration_parameter.py
│   ├── calibration_candidate.py
│   ├── calibration_result.py
│   └── calibrated_model.py
│
├── data/
│   ├── reference_data_adapter.py
│   ├── sensor_alignment.py
│   ├── weather_alignment.py
│   ├── timeseries_windowing.py
│   └── data_quality.py
│
├── parameters/
│   ├── parameter_space.py
│   ├── bounds.py
│   ├── constraints.py
│   ├── global_parameters.py
│   ├── zone_group_parameters.py
│   └── local_parameters.py
│
├── metrics/
│   ├── cvrmse.py
│   ├── nmbe.py
│   ├── nmae.py
│   ├── rmse.py
│   ├── mae.py
│   ├── temporal_shape.py
│   ├── physical_penalty.py
│   └── multiobjective.py
│
├── optimizers/
│   ├── random_search.py
│   ├── genetic_algorithm.py
│   ├── nsga2.py
│   ├── bayesian.py
│   └── surrogate_assisted.py
│
├── campaign/
│   ├── candidate_generator.py
│   ├── simulation_campaign.py
│   ├── parallel_execution.py
│   ├── early_stopping.py
│   └── candidate_registry.py
│
├── reports/
│   ├── calibration_report.py
│   ├── pareto_report.py
│   ├── zone_error_map.py
│   ├── overfitting_report.py
│   └── approval_summary.py
│
└── registry/
    ├── calibrated_model_registry.py
    ├── calibration_history.py
    └── provenance.py
```

---

## 32. Contratos principales

### 32.1 CalibrationJob

```yaml
CalibrationJob:
  id: cal_job_001
  base_model_id: energy_model_v12
  reference_data_id: sensor_dataset_004
  target_period:
    start: 2026-04-22
    end: 2026-04-29
  validation_period:
    start: 2026-04-29
    end: 2026-05-06
  zones:
    - aula_3b
    - aula_4a
  optimizer: NSGA-II
  status: running
```

### 32.2 CalibrationTarget

```yaml
CalibrationTarget:
  id: target_aula_3b_temperature
  variable: zone_air_temperature
  reference_source: sensor_3b_temp
  simulated_variable: zone_air_temperature
  zone_id: aula_3b
  weight: 1.0
```

### 32.3 CalibrationParameter

```yaml
CalibrationParameter:
  id: infiltration_rate_aula_3b
  scope: zone
  zone_id: aula_3b
  min: 0.1
  max: 1.2
  unit: ach
  physical_constraint: plausible_range
```

### 32.4 CalibrationCandidate

```yaml
CalibrationCandidate:
  id: candidate_027
  generation: 8
  parameter_values:
    infiltration_rate_aula_3b: 0.42
    glazing_u_value: 2.8
  simulation_run_id: run_872
  metrics:
    CVRMSE: 8.4
    NMBE: 1.1
    NMAE: 4.6
  pareto_rank: 1
```

### 32.5 CalibratedModel

```yaml
CalibratedModel:
  id: calibrated_model_v03
  base_model_id: energy_model_v12
  calibration_job_id: cal_job_001
  selected_candidate_id: candidate_027
  status: pending_approval
  approved_by: null
  approved_at: null
```

---

## 33. MVP del módulo de calibración

### 33.1 Objetivo MVP

Calibrar una zona tipo contra datos reales de temperatura.

### 33.2 Alcance MVP

```text
1 modelo EnergyPlus;
1 zona objetivo;
1 sensor de temperatura;
1 periodo corto;
3-5 variables calibrables;
algoritmo genético simple;
CVRMSE, NMBE, NMAE;
curva real vs simulado;
modelo calibrado versionado;
reporte de calibración.
```

### 33.3 Fuera del MVP

```text
calibración multizona completa;
NSGA-II avanzado;
humedad;
consumo energético;
HVAC detallado;
calibración online;
surrogate-assisted calibration;
control.
```

### 33.4 Criterio de éxito

```text
Siamese puede tomar un modelo base,
compararlo contra un sensor real,
ajustar parámetros,
mostrar métricas,
generar un CalibratedModel versionado,
y bloquear módulos posteriores hasta aprobación.
```

---

## 34. Evolución por fases

### Fase 1 — Calibración simple

```text
una zona;
temperatura;
GA básico;
métricas simples;
reporte mínimo.
```

### Fase 2 — Multiobjetivo

```text
temperatura + humedad;
CVRMSE + NMBE + NMAE;
NSGA-II;
frente de Pareto.
```

### Fase 3 — Multizona

```text
zonas tipo;
parámetros globales/grupo/locales;
mapas de error por zona;
validación cruzada.
```

### Fase 4 — Consumo energético

```text
gas;
electricidad;
calefacción;
contadores reales;
comparación sensores + consumos.
```

### Fase 5 — Surrogate-assisted calibration

```text
modelo rápido de error;
reducción de simulaciones;
priorización de candidatos;
optimización más eficiente.
```

### Fase 6 — Recalibración y drift

```text
detección de degradación;
propuesta de recalibración;
comparación de modelos calibrados;
actualización versionada.
```

---

## 35. Riesgos principales

### 35.1 Overfitting

El modelo puede calibrarse demasiado al periodo seleccionado.

Mitigación:

```text
periodo de validación independiente;
regularización física;
validación cruzada;
alerta de overfitting.
```

### 35.2 Parámetros irreales

El algoritmo puede encontrar valores matemáticamente buenos pero físicamente absurdos.

Mitigación:

```text
bounds físicos;
penalty terms;
revisión humana;
Model Quality Report.
```

### 35.3 Coste computacional

La calibración puede requerir muchas simulaciones.

Mitigación:

```text
paralelización;
early stopping;
optimización bayesiana;
surrogate-assisted calibration;
calibración por etapas.
```

### 35.4 Datos reales pobres

Sensores con fallos, huecos o mala ubicación pueden degradar la calibración.

Mitigación:

```text
data quality checks;
sensor health;
outlier detection;
gap filling;
confidence score.
```

### 35.5 Incoherencia multizona

Calibrar zonas aisladas puede romper coherencia global.

Mitigación:

```text
parámetros jerárquicos;
zonas tipo;
constraints globales;
validación cruzada.
```

---

## 36. Valor estratégico

El módulo de calibración aporta a Siamese:

```text
credibilidad técnica;
conexión con datos reales;
base para modelos vivos;
base para datasets físicos;
base para surrogates útiles;
base para shadow mode;
diferenciación frente a simuladores tradicionales;
argumento comercial fuerte.
```

La calibración es una de las formas más claras de explicar por qué Siamese no es simplemente “otro software de simulación”.

---

## 37. Frases de presentación

Frase corta:

> Sin calibración, hay simulación. Con calibración, empieza el gemelo vivo.

Frase técnica:

> Siamese ajusta parámetros físicos, operativos y HVAC comparando simulaciones EnergyPlus contra datos reales, hasta obtener un modelo calibrado, versionado y validado.

Frase comercial:

> No solo modelamos el edificio. Ajustamos el modelo a cómo se comporta realmente.

---

## 38. Primeros tickets recomendados

### CAL-00 — Calibration module vision

Crear documentación base y frontera del módulo.

### CAL-01 — Calibration contracts

Definir `CalibrationJob`, `CalibrationTarget`, `CalibrationParameter`, `CalibrationCandidate` y `CalibratedModel`.

### CAL-02 — Reference data adapter

Preparar datos reales alineados temporalmente con resultados simulados.

### CAL-03 — Metrics MVP

Implementar CVRMSE, NMBE, NMAE, RMSE y MAE.

### CAL-04 — Parameter space MVP

Definir variables calibrables, bounds y constraints.

### CAL-05 — Genetic algorithm MVP

Implementar calibración monoobjetivo con algoritmo genético simple.

### CAL-06 — EnergyPlus campaign integration

Conectar candidatos con SimulationCase y EnergyPlus Runner.

### CAL-07 — Calibration report MVP

Generar informe real vs simulado y métricas.

### CAL-08 — Calibrated model registry

Versionar modelo calibrado y estado de aprobación.

### CAL-09 — Omniverse calibration visualization

Visualizar error por zona y curvas real/simulado en Kit.

### CAL-10 — NSGA-II research spike

Evaluar NSGA-II para multiobjetivo.

### CAL-11 — Multizone calibration architecture

Diseñar parámetros globales, por grupo y locales.

---

## 39. Decisión arquitectónica final

El módulo de calibración debe obedecer esta decisión:

```text
La calibración no es un script de ajuste.
Es una capa gobernada que convierte modelos energéticos en modelos observados, versionados y utilizables para predicción y operación.
```

Todo lo demás deriva de ahí:

```text
calibración usa EnergyPlus, no lo reemplaza;
calibración consume sensores, no los gestiona directamente;
calibración produce modelos versionados, no archivos sueltos;
calibración requiere métricas, validación y aprobación;
calibración desbloquea datasets, surrogates y shadow mode;
calibración debe ser visible en Omniverse;
calibración debe ser ejecutable por agentes, pero aprobada por humanos.
```

---

## 40. Referencias internas de proyecto

- `digital_twin_contexto_maestro.md` — visión general de Siamese y macroproyecto de calibración.
- `siamese_energyplus_context.md` — EnergyPlus como solver físico.
- `siamese_python_backend_context.md` — backend Python como capa de dominio, validación, compilación, ejecución y normalización.
- `siamese_omniverse_kit_context.md` — Omniverse Kit como interfaz visual, semántica y extensible.
- `Concienciación ambiental y optimización energética del CEP Divino Maestro.pdf` — origen técnico: sensórica, DesignBuilder, calibración con datos reales y algoritmos genéticos.
