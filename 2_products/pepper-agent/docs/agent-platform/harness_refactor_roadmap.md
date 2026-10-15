# HAR — Roadmap canónico de refactorización del arnés

Fecha de adopción documental: 2026-10-15 (Europe/Madrid). Ticket: HAR-00.
Estado: **PROPOSED — pendiente de revisión humana de D01–D10 y de cada gate**.

Este archivo es el propietario canónico del roadmap HAR. Conserva, en la sección siguiente, el contenido del plan humano de entrada
`HAR/HAR_roadmap_refactorizacion_harnes.md`, versión 1.0 de 2026-10-09,
SHA256 `3bc700b77e6e36ba297bf0e3f6f2c85e1b25b497679db3912a5399a167b72513`.
En esta copia, los saltos Markdown de dos espacios se expresan con `<br>`;
no cambia el contenido, la secuencia ni los gates. La entrada humana permanece
intacta; copiar el backlog aquí no crea tickets
Pepper ni tickets ejecutables futuros. Las referencias originales a artefacto
adjunto describen la entrada HAR-00; el ticket fuente está en
`HAR/HAR-00_architecture_decisions_and_execution_baseline.md`.

Decisiones y primer ámbito: [arquitectura](harness_refactor_architecture.md).
Selecciones/deuda/evidencia: [manifiesto](harness_refactor_verification_manifest.json).
Las 30 entradas mantienen su orden, dependencias, entregables, exclusiones y
aceptación originales. HAR-00 no propone split ni adelanto de ningún corte.
Todos los cortes HAR-01–HAR-29 siguen **NOT_STARTED** en esta entrega.
HAR-00 queda preparado documentalmente para revisión, no aceptado por el humano.

Baseline inicial comprobado: `64debea2b3ae184b95c4eeb4cb1d9b58938c9aec`.
WSL observado el 2026-10-15 en C93: **HUMAN_SYNC_REQUIRED_BEFORE_HAR01_VERIFICATION**.
No tests ejecutados por HAR-00. Las cifras del plan son históricas.

## Plan humano preservado

# HAR — Refactorización del arnés gobernado de AGENT PLATFORM para Siamese

**Versión del plan:** 1.0 — 2026-10-09<br>
**Tipo:** proyecto de ingeniería con tickets ejecutados manualmente mediante Codex.<br>
**Estado:** roadmap propuesto para ejecución incremental; cada ticket completo se revisa y entrega por separado.<br>
**Primer ticket ejecutable:** HAR-00, en el artefacto adjunto independiente.

## 1. Identidad y propósito

`HAR` es el identificador de esta campaña de refactorización. No es una revisión de P18.9.13, no crea un ticket en Pepper y no renumera el roadmap gobernado. El proyecto aplica la recomendación de la auditoría: **contratos declarativos B introducidos mediante migración incremental A, con coordinación durable limitada C**. No es una reescritura total ni event sourcing completo.

Objetivo: conectar de forma verificable hechos/estado, capacidad, política, autoridad, efectos, evidencia y continuación; mantener los componentes existentes que ya protegen integridad y consentimiento; demostrar extensibilidad horizontal a Siamese sin añadir ramas por ticket, proyecto o herramienta al núcleo.

Este desglose es una propuesta de implementación elaborada a partir de la auditoría `P18.9.13-ARCH-AUDIT-01`. Los nombres de tickets, cortes de entrega y gates son decisiones de planificación, no hechos ya implementados. La auditoría reconstruye caminos importantes, no una prueba exhaustiva de todos los estados posibles.

## 2. Referencia de partida

- Repositorio: `AGENT-PLATFORM`.
- Rama: `p18-manual-to-hermes-workflow-migration`.
- Baseline inicial documentado: `64debea2b3ae184b95c4eeb4cb1d9b58938c9aec` (C94).
- Baseline de cada ticket posterior: HEAD completo aceptado y publicado de su predecesor; no reutilizar automáticamente el SHA inicial durante todo el proyecto.
- WSL fue observado por la auditoría en `75185e79e46424e7f495dfaad59ebdde7f45db93` con bytes C94 sin commit. Es observación histórica, no una lectura actual. El operador debe sincronizarlo antes de pruebas ejecutables. Codex no hará pull, checkout ni limpieza.
- Exclusiones conocidas: `2_products/pepper-agent/tests/hermes_cli/test_c64_validation_authority_boundary.py` y `2_products/pepper-agent/web/src/agent-platform/c80-r1-chat-lifecycle.test.tsx`. Preservar bytes y excluir del candidate y del discovery accidental. Su presencia, por sí sola, no bloquea el trabajo.

Estado vivo de referencia, NO revalidado por este plan: P18.9.13 R0002, task `t_236e7e49`, run45, zero-change atestado, solicitud C92 `7a74fd5229fb642a966afc11c04bb7d1951dd8aa38ff1e762b3e433d22f0fa8c`, última condición `material_revision_authority_blocked`. Se mantiene congelado hasta el piloto específicamente autorizado. No se usa el workflow vivo como entorno de pruebas.

## 3. Reglas de ejecución comunes

1. Un ticket de implementación activo y un propietario de cambios por checkout. El roadmap expresa dependencias, no autoriza ejecución paralela. La revisión de documentos puede organizarse separadamente, pero no habrá dos agentes mutando las mismas fuentes.
2. El usuario envía un ticket completo a Codex. Codex inspecciona HEAD, scope y estado, implementa solo ese ticket, prueba en almacenamiento/runtime aislados, entrega informe y se detiene. No genera ni ejecuta el siguiente.
3. Revisión del resultado → aceptación humana → staging de paths exactos → commit/push humano. Los comandos de staging se generan a partir de la candidatura real, no de una lista supuesta de este roadmap.
4. La sincronización de un checkout de pruebas y el despliegue del servicio vivo son operaciones distintas. Se mantiene el checkout de verificación coherente; no se reinicia Pepper ni se ejecuta conciliación viva al terminar cada ticket.
5. Codex no ejecuta `git add/commit/push/reset/checkout/restore/clean/stash`, no crea ramas/worktrees y no sincroniza Git. Se permiten lecturas como status, log, rev-parse, diff, show y ls-files. No Git mutation, Docker, Graphify, instalación de dependencias ni reparación de red sin autorización separada.
6. Tests por `scripts/run_tests.sh` donde sea el wrapper canónico. Rutas comprobadas contra el repo, manifiestos explícitos, nuevos tests añadidos deliberadamente. No elegir un comando más estrecho para ocultar fallos. No imports que abran HERMES_HOME vivo.
7. Comparación candidate/HEAD en copias aisladas o mecanismo que preserve verificablemente los bytes; no byte-swapping en un árbol servido por el proceso vivo. Documentar fuente y sustrato de cada ejecución. Ningún fallo es preexistente solo por parecer conocido.
8. Pruebas aisladas pueden simular humanos/proveedores/efectos con fixtures. Eso no genera consentimiento ni evidencia real de P18.9.13. No provider calls vivos, auto-approval, live command validation o control de recursos reales.
9. Los lectores históricos conservan originales y algoritmos de digest. Nuevos envelopes referencian historia; no la reserializan para convertirla en autoridad nueva. Rollback no borra decisiones posteriores: lector compatible o safe stop.
10. Cada ticket entrega: causa/objetivo, paths exactos, contratos afectados, decisiones vigentes, tests/comandos/entorno/resultados, clasificación de fallos, pruebas de preservación, diff/stat, riesgos y siguiente gate. Marcador de éxito solo cuando el criterio se cumple; un bloqueo se informa como tal.

## 4. Política de diseño y decisiones pendientes

La dirección está fijada: reutilizar el registro Hermes, un evaluador/coordinador y adaptadores de autoridad/evidencia; no añadir un catálogo independiente. La primera migración cubre pre-review y revisión material, no todo product_runtime de una vez.

HAR-00 prepara decisiones revisables sobre ubicación de contratos, alcance de concurrencia, actor/trust model, versiones históricas, reglas C26 y garantías de persistencia. Hasta su aprobación son propuestas. El alcance inicial recomendado es un sustrato local de confianza con aislamiento por proyecto/recurso y concurrencia local explícitamente cualificada. El diseño permite una futura identidad multiusuario sin declarar autenticación multi-tenant implementada.

Disponibilidad no es autorización. Proyección y preflight comparten admisibilidad; el ejecutor vuelve a validar al producir efectos. Una acción se tipa como capacidad invocable, decisión humana, observación, instrucción externa o safe stop. Los dominios técnicos pueden añadir contratos, políticas y adaptadores, pero no permisos nuevos por inferencia.

## 5. Qué cuenta como éxito

La meta no es cero condicionales, cero bugs o un número menor de líneas. Es que las acciones ejecutables estén conectadas a sus contratos; la validación tenga dependencias explícitas; lectura y mantenimiento estén separados; los efectos tengan un único escritor y política de recuperación; y un dominio simulado de Siamese pueda añadirse sin cambiar el núcleo.

El informe auditado clasificó 1.327 errores y 13 fallos relacionados con el intérprete, cuatro fallos estructurales y dos desacuerdos C26 dentro de una selección ampliada. HAR-01–HAR-03 deberán reproducir/clasificar ese punto de partida. No son cifras actuales garantizadas ni resultados del conjunto completo del repositorio.

No se promete exactly-once externo, aislamiento de procesos/red no implementado, ni control físico seguro. Una evidencia de tests limitada acredita solo sus escenarios, versiones y sustratos publicados.

## 6. Fases y gates

| Fase | Tickets | Resultado/gate |
|---|---|---|
| 0 — Decisiones y línea base | HAR-00–HAR-03 | G0 — Semántica de referencia decidida y verificación seleccionada confiable. |
| 1 — Núcleo contractual y evaluación paralela | HAR-04–HAR-09 | G1 — Primer ámbito conectado en modo shadow, sin nueva autoridad de efectos. |
| 2 — Validación, identidad y coordinación durable | HAR-10–HAR-14 | G2 — Primer ámbito migrado con un único escritor y recuperación verificada. |
| 3 — Migración del resto de las operaciones de Pepper | HAR-15–HAR-22 | G3 — Operaciones migradas con contratos completos y compatibilidad explícita. |
| 4 — Verificación global y rendimiento | HAR-23–HAR-25 | G4 — Candidato de despliegue cualificado en escenarios aislados y acotados. |
| 5 — Piloto P18.9.13 con autorización separada | HAR-26–HAR-27 | G5 — Compatibilidad viva comprobada sin consentimiento transitivo. |
| 6 — Extensión Siamese y cierre | HAR-28–HAR-29 | G6 — Extensión simulada sin ramas de dominio en el núcleo y cierre documentado. |

Los gates bloquean activación/cambio de autoridad, no el razonamiento o las propuestas de diseño. Toda excepción a un criterio requiere decisión explícita y evidencia; ninguna cuarentena convierte un fallo en éxito.

## 7. Backlog completo

Cada entrada define un corte de trabajo y su aceptación. No sustituye el ticket completo con HEAD, allowlist y comandos verificados que se emitirá al llegar a ella.

### Fase 0 — Decisiones y línea base

#### HAR-00 — Decisiones arquitectónicas y contrato de ejecución del proyecto

**Dependencias:** Auditoría aceptada.<br>
**Trazabilidad:** F01–F13.

**Objetivo:** Convertir la auditoría en decisiones revisables, un mapa de responsabilidades y un manifiesto reproducible de verificación. No repetir la auditoría ni comenzar una reescritura.

**Entregable:** Documentación canónica breve de arquitectura y roadmap; manifiesto de suites/casos derivados de rutas reales; decisiones aceptadas frente a propuestas pendientes; preflight Windows/WSL.

**Aceptación:** Cada decisión pendiente tiene alternativas, evidencia y responsable. El ámbito inicial, límites de compatibilidad y política de estados/acciones quedan explícitos. No se afirma haber ejecutado tests. No cambia código de producción ni estado vivo.

**Fuera de alcance:** Refactor, dependencias nuevas, ejecutar pruebas, decidir unilateralmente los dos desacuerdos C26.

**Riesgo/gate:** Ubicación de contratos, política C26 y garantías iniciales deben revisarse humanamente antes de los tickets que dependan de ellas.

#### HAR-01 — Reparar fixtures de intérprete y hacer reproducible la verificación

**Dependencias:** HAR-00.<br>
**Trazabilidad:** F07, F11.

**Objetivo:** Corregir la incompatibilidad de las fixtures con el contrato del intérprete, sin relajar el guard de archivo regular ni su política de enlaces simbólicos.

**Entregable:** Fixtures/factorías de test corregidas, tests negativos de la protección preservados y ejecución fresca del manifiesto seleccionado con entorno e intérprete registrados.

**Aceptación:** Los errores atribuidos al intérprete desaparecen o quedan reclasificados con evidencia fresca. Los casos negativos siguen siendo rechazados. Comparación sobre HEAD exacto y ausencia de nuevas regresiones dentro de la selección.

**Fuera de alcance:** Cambiar la política de seguridad para poner los tests en verde, editar V2/R0002 o instalar dependencias automáticamente.

**Riesgo/gate:** La clasificación de la auditoría procede de logs; cualquier causa adicional descubierta se documenta, no se oculta.

#### HAR-02 — Sustituir snapshots estructurales por contratos públicos de comportamiento

**Dependencias:** HAR-00; ejecutar después de HAR-01 en el checkout compartido.<br>
**Trazabilidad:** F07, F11.

**Objetivo:** Revisar las cuatro aserciones de cantidades/prefijos/posiciones de exportación y expresar la compatibilidad pública que realmente debe mantenerse.

**Entregable:** Contrato de símbolos/comportamientos soportados y pruebas equivalentes orientadas a esa compatibilidad, con trazabilidad de cada aserción sustituida.

**Aceptación:** Una exportación pública comprometida sigue comprobándose. Quitar o desplazar un símbolo relevante provoca un fallo; un cambio de orden no contractual deja de impedir una refactorización. Sin pérdida silenciosa de API.

**Fuera de alcance:** Borrar tests para ocultar roturas o declarar privada una API previamente comprometida sin decisión humana.

**Riesgo/gate:** Una expectativa estructural puede codificar compatibilidad real; debe resolverse antes de reemplazarla.

#### HAR-03 — Resolver C26 y sellar la línea base G0

**Dependencias:** HAR-00, HAR-01, HAR-02; decisión humana C26.<br>
**Trazabilidad:** F01, F07, F11, F12.

**Objetivo:** Implementar la política decidida para selección del ticket vigente y precedencia PREPARE/RESOLVE; cerrar el manifiesto de referencia del primer ámbito.

**Entregable:** Tests de comportamiento C26, matriz de selección/precedencia y resultados reproducibles por selección, junto con registro de deuda residual asignada.

**Aceptación:** Ninguna discrepancia semántica del ámbito crítico queda sin resolver. Todos sus requisitos de aceptación pasan. Los fallos externos a ese ámbito tienen evidencia, propietario e impacto explícito; una cuarentena no cuenta como éxito.

**Fuera de alcance:** Cambiar implementación o test por conveniencia sin decidir antes cuál representa el comportamiento correcto.

**Riesgo/gate:** G0 bloquea sustituciones de arquitectura si la línea base del ámbito migrado no permite detectar regresiones.

**Salida de fase:** G0 — Semántica de referencia decidida y verificación seleccionada confiable.

### Fase 1 — Núcleo contractual y evaluación paralela

#### HAR-04 — Contratos mínimos versionados y límite plataforma/producto

**Dependencias:** HAR-03 / G0.<br>
**Trazabilidad:** F01, F06, F08, F10.

**Objetivo:** Definir los envelopes mínimos de capacidad, transición, referencias de autoridad, decisión, evidencia y proyección en la ubicación acordada; conservar políticas específicas en adaptadores.

**Entregable:** Modelos versionados y validadores puros; contrato de actor/ámbito/efecto; reglas de dependencia de módulos y adaptación de contratos históricos.

**Aceptación:** El núcleo contractual no importa selectores privados de Pepper ni clientes de proveedores. No incluye IDs P18/Cxx como lógica. Identidades desconocidas o versiones no soportadas se rechazan explícitamente.

**Fuera de alcance:** Ocho registros redundantes, nueva plataforma de workflows, implementación de autenticación multi-tenant completa o rehash de historia.

**Riesgo/gate:** El modelo debe ser pequeño pero capaz de distinguir disponibilidad, autorización y ejecución.

#### HAR-05 — Lecturas de hechos y autoridad sin efectos secundarios

**Dependencias:** HAR-04.<br>
**Trazabilidad:** F09, F04, F10.

**Objetivo:** Separar observación de inicialización, mantenimiento y reconciliación. Construir puertos de lectura para hechos/evidencias del primer ámbito.

**Entregable:** Snapshot observable con versiones y frescura; adaptadores read-only; operaciones de mantenimiento identificadas como tales; mediciones iniciales de lecturas/escaneos.

**Aceptación:** Los caminos migrados de observación no crean DB, locks, registros, contadores ni reconciliaciones. Pruebas antes/después y detección de deriva. La ausencia de datos no se convierte en permiso.

**Fuera de alcance:** Cambiar todos los endpoints de golpe, afirmar transacción global a partir de relecturas, mantenimiento oculto durante lectura.

**Riesgo/gate:** Los timestamps observacionales y los hechos normalizados no deben alterar identidades históricas.

#### HAR-06 — Catálogo de operaciones gobernadas sobre el registro Hermes

**Dependencias:** HAR-04, HAR-05.<br>
**Trazabilidad:** F01, F03, F06, F12.

**Objetivo:** Registrar operaciones/suboperaciones con inspector, esquemas, política, ejecutor, efectos, evidencia e invalidación/recuperación, reutilizando el catálogo de herramientas existente.

**Entregable:** Descriptores del ámbito pre-review/material revision; verificación de correspondencia con handlers existentes y clasificación tipada de continuaciones.

**Aceptación:** Una acción ejecutable sin política o ejecutor es configuración inválida. Una instrucción externa o safe stop no se presenta como tool invocable. No se duplican nombres o catálogos de herramientas.

**Fuera de alcance:** Conceder autorización por estar registrado, parser de shell genérico o catálogo paralelo no integrado.

**Riesgo/gate:** Compatibilidad de los nombres públicos existentes y de las suboperaciones debe quedar preservada.

#### HAR-07 — Evaluador puro de admisibilidad y proyección tipada

**Dependencias:** HAR-05, HAR-06.<br>
**Trazabilidad:** F01, F03, F10, F12.

**Objetivo:** Obtener allow/deny/wait/safe-stop a partir de un snapshot, política y autoridad explícitos; definir precedencia determinista sin overlays que se sobrescriban implícitamente.

**Entregable:** Evaluador compartible por proyección y preflight; decisiones explicables; traducción a las acciones públicas actuales.

**Aceptación:** Mismos hechos/versiones/políticas producen igual admisibilidad. Consentimiento ausente no ejecuta. Orígenes de reconciliación no cualificados se tipan como stop/remediación, nunca como C94 ejecutable.

**Fuera de alcance:** Relajar verificaciones cercanas al efecto, desplegar nuevos efectos o introducir un if por ticket/dominio.

**Riesgo/gate:** Las diferencias deliberadas respecto a proyecciones antiguas necesitan política y aprobación, no solo paridad ciega.

#### HAR-08 — Verificador de cobertura y modelo de referencia inicial

**Dependencias:** HAR-06, HAR-07.<br>
**Trazabilidad:** F01, F02, F03, F07.

**Objetivo:** Hacer ejecutables las invariantes iniciales: correspondencia acción-capacidad, productores de evidencia alcanzables, prerrequisitos consistentes y salidas wait/stop explícitas.

**Entregable:** Modelo acotado del primer ámbito, generador determinista de escenarios y tests negativos para clases C91–C94.

**Aceptación:** El verificador detecta un ejecutor ausente, un consumidor cuyo productor es inaccesible y un ciclo de prerrequisitos. Se publican estados/transiciones/límites explorados y supuestos; no se afirma exhaustividad infinita.

**Fuera de alcance:** Añadir una dependencia de property testing sin autorización o ejecutar escenarios contra Pepper vivo.

**Riesgo/gate:** El modelo no puede limitarse a copiar las ramas de producción y validar esa misma copia.

#### HAR-09 — Adaptadores del primer ámbito y comparación shadow G1

**Dependencias:** HAR-08.<br>
**Trazabilidad:** F01, F03, F08, F12.

**Objetivo:** Envolver inspección/ejecución de comandos, inspección aprobada, request post-ejecución, reconciliación y revisión estructurada. Comparar decisiones nuevas con las existentes sin doble ejecución.

**Entregable:** Adaptadores y comparador shadow sobre corpus aislado; discrepancias clasificadas; rutas de entrada con nuevo modo desactivado por defecto.

**Aceptación:** El nuevo camino calcula decisiones pero no escribe ni despacha. C91–C94 mantienen digests/políticas. No quedan diferencias inexplicadas del ámbito; toda diferencia intencional tiene decisión humana.

**Fuera de alcance:** Reemplazar writers, activar feature flags vivos, ejecutar comandos como parte del shadow.

**Riesgo/gate:** G1 acredita coherencia del primer ámbito, no migración completa del arnés.

**Salida de fase:** G1 — Primer ámbito conectado en modo shadow, sin nueva autoridad de efectos.

### Fase 2 — Validación, identidad y coordinación durable

#### HAR-10 — Grafo explícito de validación y compatibilidad histórica

**Dependencias:** HAR-09 / G1.<br>
**Trazabilidad:** F02, F07.

**Objetivo:** Representar dependencias por IDs de evidencia, productor, condición y criterio de aceptación; separar evidencia existente de evidencia aprobatoria.

**Entregable:** DAG versionado, detección de ciclos/productores ausentes y adaptador de contratos antiguos con interpretación congelada y trazable.

**Aceptación:** Nuevos contratos no dependen del texto descriptivo. Evidencia fallida puede habilitar clasificación humana sin habilitar aceptación. V11-equivalente no se autoaprueba. R0002 y sus hashes no se modifican; ambigüedad histórica se expone.

**Fuera de alcance:** Insertar dependencias nuevas silenciosamente en WorkPackets firmados o cambiar descripciones para alterar el flujo.

**Riesgo/gate:** La migración semántica de contratos históricos exige autoridad propia cuando realmente cambia su significado.

#### HAR-11 — Identidades de autoridad, implementación e inputs separadas

**Dependencias:** HAR-10.<br>
**Trazabilidad:** F05, F10.

**Objetivo:** Separar intención humana, autoridad inmutable, implementación ejecutable, inputs de validación y ubicación de recursos, manteniendo validación conjunta donde haya efectos.

**Entregable:** Manifiestos de dependencias transitivas de capacidades; clasificación tipada de invalidación; referencias versionadas con lectores históricos.

**Aceptación:** Un parser/política compartido invalida todos sus dependientes. Cambiar inputs exige nueva evidencia. Consentimiento histórico no se hereda a fuente nueva. Un fingerprint amplio sigue usándose cuando la validación consume realmente todo el árbol.

**Fuera de alcance:** Hash de función aislada como garantía suficiente, exenciones generales de documentación o borrado del registro C92.

**Riesgo/gate:** La optimización de invalidación solo se acepta después de demostrar que el manifiesto no omite dependencias relevantes.

#### HAR-12 — Diario durable de operaciones y control de versión esperada

**Dependencias:** HAR-11.<br>
**Trazabilidad:** F04.

**Objetivo:** Introducir coordinación limitada para una operación seleccionada que cruce registros/DB/proceso, con IDs, etapas e identificadores de efectos. Mantener almacenes existentes.

**Entregable:** Journal versionado con control de conflicto y recibos, estado de resultado desconocido cuando corresponda y adaptadores de efectos aislados.

**Aceptación:** Un único propietario/escritor por operación. La versión esperada se comprueba antes del efecto. No se reescribe evidencia histórica. La semántica de idempotencia y entrega queda explícita por adaptador.

**Fuera de alcance:** Event sourcing completo, servicio distribuido nuevo, promesa de exactly-once externo o activación sobre workflow vivo.

**Riesgo/gate:** Un efecto realizado sin recibo durable no puede repetirse ciegamente: requiere observación/recuperación específica o safe stop.

#### HAR-13 — Recuperación, replay y fallos entre etapas durables

**Dependencias:** HAR-12.<br>
**Trazabilidad:** F04, F07.

**Objetivo:** Validar reinicios, interrupciones antes/después de cada etapa, concurrencia y replays conflictivos del journal y los adaptadores seleccionados.

**Entregable:** Pruebas de crash/fault injection en almacenamiento aislado, políticas de recuperación de locks y resultados parciales, matriz de garantías.

**Aceptación:** No se duplica un efecto confirmado ni se promueve una transición parcial como completa. Replay conflictivo se rechaza. Recuperación de lock no elimina autoridad ajena. Garantías limitadas al sustrato probado.

**Fuera de alcance:** Simular todos los fallos únicamente con excepciones anteriores al write, eliminar registros dañados automáticamente o afirmar tolerancia a apagado físico no probada.

**Riesgo/gate:** Hay que diferenciar fallo de proceso, concurrencia y pérdida de energía; no son la misma garantía.

#### HAR-14 — Cambiar el enrutamiento del primer ámbito G2

**Dependencias:** HAR-09, HAR-10, HAR-11, HAR-13; aprobación del corte.<br>
**Trazabilidad:** F01–F05, F09, F12.

**Objetivo:** Hacer que proyección y preflight utilicen el modelo nuevo para el primer ámbito, manteniendo los efectos en sus adaptadores y las verificaciones finales.

**Entregable:** Ruta única por capacidad migrada; política de activación del nuevo código sin tocar flags vivos; compatibilidad de wrappers y eliminación acotada de decisión duplicada.

**Aceptación:** Pruebas sin doble escritor, paridad o diferencias aprobadas, consentimientos exactos y registros antiguos válidos. Rollback a implementación compatible o safe stop, nunca restaurar archivos para borrar una decisión.

**Fuera de alcance:** Reconciliar P18.9.13, generar R0003 o retirar lectores históricos.

**Riesgo/gate:** G2 permite seguir migrando código; no autoriza el piloto vivo.

**Salida de fase:** G2 — Primer ámbito migrado con un único escritor y recuperación verificada.

### Fase 3 — Migración del resto de las operaciones de Pepper

#### HAR-15 — Migrar zero-change, evidencia manual, review y finalización

**Dependencias:** HAR-14 / G2.<br>
**Trazabilidad:** F01, F02, F08, F10.

**Objetivo:** Envolver las decisiones humanas y las políticas de aceptación/finalización, conservando sus fronteras independientes y los contratos de evidencia.

**Entregable:** Capacidades registradas para atestación, preparación/decisión de review y completion policy; Git handoff como adaptación de desarrollo de software.

**Aceptación:** Completar ejecución o no producir cambios no significa aceptar. Una simulación puede finalizar por evidencia/model acceptance sin Git. El flujo Pepper conserva su handoff humano aplicable.

**Fuera de alcance:** Generalizar todo resultado a un commit, automatizar aprobaciones o modificar reglas del ticket vivo.

**Riesgo/gate:** Separar finalización genérica de la política de producto no debe debilitar el handoff existente.

#### HAR-16 — Migrar generación, publicación y aprobación

**Dependencias:** HAR-15.<br>
**Trazabilidad:** F01, F04, F08, F11.

**Objetivo:** Adaptar el bridge a contratos estables de publicación/revisión/decisión, con roadmap y selección de producto fuera del núcleo y promoción durable explícita.

**Entregable:** Operaciones de generación y aprobación registradas, continuidad de historia y plan de recuperación para promoción de varios registros.

**Aceptación:** No hay aprobación implícita de sucesores. La autoridad anterior conserva bytes/digests. Un fallo entre publicación, aprobación e historial no anuncia una revisión completa sin prueba.

**Fuera de alcance:** Reescribir todo el bridge, cambiar contenidos de TicketSpec o recalcular historia bajo serialización nueva.

**Riesgo/gate:** El alcance se limita a los puntos de entrada/decisión/efecto definidos, no a trasladar miles de líneas por estética.

#### HAR-17 — Migrar admisión, dependencias y proyección Kanban

**Dependencias:** HAR-16.<br>
**Trazabilidad:** F01, F04, F08, F12.

**Objetivo:** Unificar admisión y vínculo WorkPacket–tarea, coordinando el cruce SQLite/JSON sin confundir columnas operativas con estado gobernado.

**Entregable:** Admisión por autoridad y recursos; proyección con operación durable; reparación gobernada de publicación incompleta y diagnostics coherentes.

**Aceptación:** Una tarea existente no implica proyección vigente. WorkPacket local por defecto no sustituye identidad gobernada. Reintento de promoción no duplica tareas.

**Fuera de alcance:** Dar start por el hecho de que una tarea esté ready/done o mutar tableros vivos.

**Riesgo/gate:** La selección del ticket y precedencia acordadas en C26 deben mantenerse en todas las rutas.

#### HAR-18 — Migrar dispatch, ejecución, resultados y cancelación

**Dependencias:** HAR-17.<br>
**Trazabilidad:** F01, F04, F06, F10.

**Objetivo:** Envolver start/dispatch y resultados en ejecución autorizada por capacidad, con recursos, plazos y recibos; distinguir pedido, proceso iniciado y resultado terminal.

**Entregable:** Adaptadores de runtime/proveedor existentes detrás del contrato de ejecución, con cancelación y resultado parcial/desconocido tipados.

**Aceptación:** No se inicia un task distinto del autorizado. No se duplica start tras timeout ambiguo. Cancelar requiere autoridad y no borra evidencia. Sustrato simulado en pruebas; sin nuevas llamadas a proveedor vivo.

**Fuera de alcance:** Cambiar modelos/proveedores, desplegar runtime distribuido o prometer aislamiento de red/procesos no implementado.

**Riesgo/gate:** Los límites reales del adaptador deben declararse, no ser ocultados por el envelope genérico.

#### HAR-19 — Migrar retry, recovery y corrección por origen

**Dependencias:** HAR-18.<br>
**Trazabilidad:** F03, F04, F08.

**Objetivo:** Expresar recuperación, autorización de reintento y ejecución correctiva como capacidades distintas con políticas por origen y continuación explícita.

**Entregable:** Registro de políticas soportadas y safe stops para las no soportadas; trazabilidad run previo/nuevo y workspace fresco cuando corresponda.

**Aceptación:** Recovery no despacha por sí mismo. Un reconciliador de fuente post-ejecución no se usa para un origen incompatible. Fallos y correcciones preservan evidencia del intento anterior.

**Fuera de alcance:** Añadir un recuperador universal permisivo o implementar rollback de todo el ticket por defecto.

**Riesgo/gate:** La cobertura se acredita por origen/clase de fallo; no por compartir la cadena RECONCILE.

#### HAR-20 — Migrar autonomía, delegación y presupuestos

**Dependencias:** HAR-19.<br>
**Trazabilidad:** F01, F06, F10.

**Objetivo:** Conectar las capacidades de autonomía existentes a decisión/recursos/política sin convertirlas en bypass del control humano.

**Entregable:** Contratos de delegación, presupuesto, alcance y parada; adaptador del proveedor-worker especializado, no scheduler universal.

**Aceptación:** Un agente no amplía su autoridad mediante delegación. Consentimientos de start, review y Git no se heredan. Límites y ramas wait/stop se verifican con simulación.

**Fuera de alcance:** Activar autonomía viva, paralelismo no cualificado, nuevos servicios de scheduling o ampliar herramientas del worker.

**Riesgo/gate:** La separación perfil/autonomía no demuestra aislamiento entre tenants; no se hará esa afirmación.

#### HAR-21 — Alinear herramientas, API y UI con la proyección tipada

**Dependencias:** HAR-20.<br>
**Trazabilidad:** F01, F09, F10, F12.

**Objetivo:** Consumir el mismo contrato de observación y admisibilidad desde chat, HTTP y dashboard, conservando compatibilidad de entrada donde se haya comprometido.

**Entregable:** Handlers/serializadores y frontend de estados/acciones ajustados, diagnósticos tipados y mantenimiento separado de lectura.

**Aceptación:** Las superficies coinciden en autoridad y acciones. El frontend no inventa permisos. Una remediación no invocable no aparece como ejecución. Pruebas de esquemas/contratos y build solo si fuente frontend cambia.

**Fuera de alcance:** Rediseñar Pepper Graphite, cambiar navegación de producto ajena al contrato o un endpoint alternativo sin policy.

**Riesgo/gate:** Compatibilidad no significa conservar etiquetas engañosas; las diferencias deben estar aprobadas y documentadas.

#### HAR-22 — Retirar decisiones duplicadas y cerrar límites G3

**Dependencias:** HAR-21.<br>
**Trazabilidad:** F08, F11, F12.

**Objetivo:** Eliminar ramas antiguas que ya no son propietarias de decisiones, separar implementaciones privadas y cerrar importaciones recíprocas del ámbito migrado.

**Entregable:** Mapa final de propiedad; reglas de importación; wrappers históricos justificados y plan de retirada; tests de ausencia de rutas duplicadas.

**Aceptación:** Un único evaluador/propietario por decisión migrada y un único escritor por efecto. Contratos de plataforma no importan Pepper privado. Se preservan lectores/esquemas históricos. Residuales fuera de alcance quedan explícitos.

**Fuera de alcance:** Métricas de éxito basadas solo en líneas borradas, borrar taxonomía fundacional o alias públicos sin contrato de retirada.

**Riesgo/gate:** La reducción del archivo es consecuencia, no criterio suficiente de arquitectura.

**Salida de fase:** G3 — Operaciones migradas con contratos completos y compatibilidad explícita.

### Fase 4 — Verificación global y rendimiento

#### HAR-23 — Verificación global por secuencias, concurrencia e invariantes

**Dependencias:** HAR-22 / G3.<br>
**Trazabilidad:** F01–F12.

**Objetivo:** Ampliar el modelo de referencia a las familias migradas, generando secuencias de eventos, fallos, deriva de fuente, decisiones conflictivas y reinicios.

**Entregable:** Corpus versionado de compatibilidad, generador con seeds reproducibles y matriz de cobertura de estados/transiciones/efectos/autoridad.

**Aceptación:** Ninguna continuación ejecutable del ámbito carece de executor/policy. Los waits y stops son explícitos. Pruebas de separación entre proyectos/recursos y no bypass por invocación directa. Límites de exploración publicados.

**Fuera de alcance:** Garantía absoluta de ausencia de errores o prueba de multi-tenant/producción física a partir de fixtures locales.

**Riesgo/gate:** La evidencia tiene que contrastar modelo y sistema; no validar dos copias de la misma función.

#### HAR-24 — Optimización medida de lecturas, fingerprints y evaluación

**Dependencias:** HAR-23.<br>
**Trazabilidad:** F13, F09, F05.

**Objetivo:** Medir y mejorar el coste real de observación/evaluación, identificando escaneos repetidos y reuso seguro de manifiestos inmutables.

**Entregable:** Benchmark reproducible antes/después; límites acordados antes del cambio; cache/optimización solo donde aporte evidencia y conserve invalidación.

**Aceptación:** Mejoras medibles o descarte razonado de optimizaciones sin beneficio. Cache stale, cambios de parser/source/inputs y concurrencia cubiertos por tests. Ningún TTL sustituye la validación final de autoridad.

**Fuera de alcance:** Objetivos porcentuales inventados, quitar revalidaciones para bajar latencia, benchmark contra workflow vivo.

**Riesgo/gate:** El journal puede añadir coste necesario; se comparan garantías equivalentes y variabilidad del entorno.

#### HAR-25 — Ensayo aislado P18.9.13 y candidato de despliegue G4

**Dependencias:** HAR-23, HAR-24.<br>
**Trazabilidad:** F01–F12.

**Objetivo:** Reproducir el recorrido representativo R0002/run45/zero-change/V2 defect/request/source drift/reconcile/revise/aprobación/validación/review/finalización en almacenamiento aislado.

**Entregable:** Piloto reproducible con C91–C94 como casos, alternativa de resultado sin cambios y runbook de despliegue/contención compatible.

**Aceptación:** Historia original preservada; no evidencia migrada como passed; revisión/aprobación/start independientes. Se demuestra el camino y fallos alternativos. Fixtures no se presentan como auditoría byte-exacta del estado vivo.

**Fuera de alcance:** Leer o copiar HERMES_HOME vivo sin autorización separada; resolver V2 real durante el ensayo.

**Riesgo/gate:** Una nueva revisión puede requerir nuevo run/zero-change según contrato; no se promete reutilización de run45.

**Salida de fase:** G4 — Candidato de despliegue cualificado en escenarios aislados y acotados.

### Fase 5 — Piloto P18.9.13 con autorización separada

#### HAR-26 — Cualificación read-only del despliegue y del piloto vivo

**Dependencias:** HAR-25 / G4; despliegue humano y autorización específica de lectura.<br>
**Trazabilidad:** F04, F07, F10.

**Objetivo:** Preparar/verificar la versión desplegable y, solo tras autorización, inspeccionar el estado real congelado sin resolverlo. Separar HEAD de código, proceso en ejecución y autoridad durable.

**Entregable:** Runbook humano, fingerprints/identidades actuales, compatibilidad de lectores y preflights del piloto; consentimiento/bindings obtenidos pero no consumidos.

**Aceptación:** El operador verifica despliegue coherente y ausencia de mutación en inspecciones. Deriva respecto al estado histórico se informa; no se sobrescribe. La lectura no se convierte en reconciliación automática.

**Fuera de alcance:** Codex despliega/sincroniza Git, invoca REVISE o interpreta el envío de este ticket como autorización de todas las etapas vivas.

**Riesgo/gate:** Este ticket es cualificación, no ejecución del piloto. Un bloqueo legítimo no se elimina mediante código ad hoc.

#### HAR-27 — Piloto P18.9.13 con decisiones humanas por frontera G5

**Dependencias:** HAR-26; autorización independiente en cada operación viva.<br>
**Trazabilidad:** F01–F12.

**Objetivo:** Validar el recorrido real usando las capacidades migradas. Codex prepara/analiza evidencias; Pablo y Pepper ejecutan las operaciones gobernadas con autoridad expresa.

**Entregable:** Traza de conciliación, revisión estructurada V2, nueva aprobación y etapas posteriores que realmente exija el backend, hasta la política de finalización aplicable.

**Aceptación:** Cada binding se inspecciona fresco. Ninguna aprobación/start/atestación deriva del ticket anterior. Se registra resultado real; fallos requieren clasificación antes de continuar. No se promete que R0003 pueda reutilizar autoridad R0002.

**Fuera de alcance:** Autorización global para cerrar P18, autoaprobar V8/V10/V11, commit/push por Codex o cambios C95 para forzar el recorrido.

**Riesgo/gate:** Si el piloto revela una clase no modelada, se vuelve al contrato/plan correspondiente; el workflow se contiene, no se fuerza.

**Salida de fase:** G5 — Compatibilidad viva comprobada sin consentimiento transitivo.

### Fase 6 — Extensión Siamese y cierre

#### HAR-28 — Piloto Siamese simulado por plugin/adaptador

**Dependencias:** HAR-23, HAR-25; realizar después de HAR-27 en el plan secuencial.<br>
**Trazabilidad:** F06, F10.

**Objetivo:** Registrar una capacidad técnica ficticia y determinista de simulación con inputs tipados, recursos, presupuesto, evidencia y aceptación humana. No usar un solver real en este piloto.

**Entregable:** Adaptador desmontable y contrato/evidence policy; pruebas éxito/denegación/timeout/cancelación/retry y finalización por artefacto sin handoff Git obligatorio.

**Aceptación:** La extensión solo modifica su contrato/registro autorizado/adaptador/tests, no el núcleo ni selectores privados de Pepper. No accede a stores/recursos fuera de su permiso. Separación de proyecto/recurso probada.

**Fuera de alcance:** Integración real EnergyPlus/GNN/BMS/HVAC, credenciales externas, control físico o condición if domain == ... en el núcleo.

**Riesgo/gate:** El piloto demuestra una frontera de extensión gobernada, no capacidad de control industrial ni aislamiento multi-tenant completo.

#### HAR-29 — Cierre arquitectónico, manual operativo y deuda residual G6

**Dependencias:** HAR-27, HAR-28.<br>
**Trazabilidad:** F01–F13.

**Objetivo:** Consolidar arquitectura as-built, contratos versionados, evidencia de cobertura, garantías de persistencia y reglas de extensión/migración.

**Entregable:** Documentación canónica actualizada, registro F01–F13 con evidencia de cierre o limitación, guía de nuevos adaptadores y runbook de operaciones/incident response.

**Aceptación:** No hay afirmaciones globales sin cobertura. Los residuales tienen propietario/alcance y safe-stop cuando corresponda. Se preservan fuentes históricas. Cierre del proyecto HAR no equivale a aprobar todo Siamese.

**Fuera de alcance:** Reportes Markdown temporales duplicados, declarar todo production-ready o ampliar el roadmap automáticamente.

**Riesgo/gate:** El cierre mide coherencia, compatibilidad y extensibilidad demostradas; no número de tickets ni líneas reducidas.

**Salida de fase:** G6 — Extensión simulada sin ramas de dominio en el núcleo y cierre documentado.

## 8. Orden operativo

La secuencia inicial es `HAR-00 → revisión humana de decisiones → HAR-01 → HAR-02 → HAR-03 → G0 → HAR-04…`.

A partir de HAR-04 el plan de implementación es secuencial por defecto. Se puede refinar un ticket futuro por evidencia del precedente, pero no introducir una nueva excepción a la arquitectura sin registrar decisión, impacto y pruebas de invariantes. Encontrar un bloqueo legítimo tampoco autoriza eliminarlo.

HAR-26 y HAR-27 son etapas de cualificación/operación humana, no licencias para que Codex mute Pepper. Las operaciones reales requieren cada una su binding actual y consentimiento específico. La generación de una nueva revisión, su aprobación, start, validaciones humanas y handoff siguen separados. El proyecto HAR no autoriza esos pasos por transitividad.

## 9. Evidencia de cierre por clase de riesgo

| Hallazgo de auditoría | Entregas principales | Prueba de resolución o limitación |
|---|---|---|
| F01 — Contrato de lifecycle | 04, 06–09, 14–23 | Cobertura acción/inspector/policy/executor y decisiones concordantes. |
| F02 — Dependencias de validación | 08, 10, 15, 23 | DAG, productores alcanzables, ciclos rechazados, evidencia ≠ aceptación. |
| F03 — Recuperación por origen | 06–09, 13–14, 19, 23 | Reconciliación cualificada o safe stop; no recuperación universal. |
| F04 — Durabilidad entre stores | 12–13, 16–19, 23 | Fallos entre etapas, conflictos, replay y resultados desconocidos. |
| F05 — Invalidación amplia | 11, 24 | Dependencias transitivas completas, consentimiento nuevo y conservación histórica. |
| F06 — Frontera de dominio | 04, 06, 18, 20, 28 | Adaptador no puede ampliar permisos ni saltar policy. |
| F07 — Línea base | 00–03, 08, 23–25 | Selecciones reproducibles y deuda asignada sin fingir verde. |
| F08 — Concentración | 04–22 | Responsabilidades reales separadas, no solo archivos divididos. |
| F09 — Efectos de lectura | 05, 21, 23 | Snapshots antes/después, mantenimiento explícito. |
| F10 — Actor/invocación | 04, 07, 18, 20–21, 26–28 | Autoridad de entrada validada y coherencia entre superficies. |
| F11 — Compatibilidad | 02, 04, 16, 22–25 | Corpus versionado, APIs comprometidas e historia válida. |
| F12 — Diagnósticos | 06–09, 21–23 | Tipos de continuación distintos; no botones/acciones ficticias. |
| F13 — Rendimiento | 05, 09, 24 | Mediciones comparables e invalidación segura. |

## 10. Fuentes y límites

Base documental: auditoría `P18.9.13-ARCH-AUDIT-01`, entregada en cuatro partes (A–C; D; E–K; L–P) y tres diagramas AS-IS/TO-BE. Son especialmente relevantes: E (registro frente a contrato de acción), F (autoridad y durabilidad), H (C91–C94), I (pruebas y fallos), J–K (arquitectura recomendada), L (fases), N (F01–F13) y P (primer ámbito propuesto).

Los diagramas son representaciones de dependencias y propuestas, no autorización de efectos ni prueba formal de todos los caminos. Este plan no ha inspeccionado de nuevo el repositorio o el servicio vivo y no sustituye las comprobaciones del ticket inicial.


## Contrato de entrega HAR-00 y gates pendientes

La dirección B mediante A con C limitado procede del ticket humano. D01–D10 son
propuestas en el documento de arquitectura: ninguna se acepta por haber escrito
este roadmap. La semántica C26 y las cuatro expectativas públicas son decisiones
separadas antes de HAR-02/HAR-03; no se arreglan unilateralmente para lograr verde.

Secuencia inmediata: revisión humana HAR-00 → sincronización humana del checkout
si procede → ticket completo HAR-01. G0 continúa después de HAR-01/02/03; HAR-04
no empieza antes. La primera migración abarca O01–O08 y consume P01–P03; el mapa
exacto de tools, bindings, efectos y continuaciones no soportadas está en
[sección 4 de arquitectura](harness_refactor_architecture.md#4-inventario-contractual-del-primer-ámbito-as-is).

G1 conserva shadow sin efectos; G2 requiere identidad, journal/recovery y un único
writer; G3 conserva historia y contratos públicos; G4 es prueba aislada, no acceso
vivo; G5 requiere HAR-26 autorizado y consentimiento específico por frontera
HAR-27; G6 demuestra únicamente un adaptador Siamese simulado y cierre acotado.

Cada ticket: padre exacto aceptado, allowlist real, preservación, verificación
seleccionada aislada, informe/diff, revisión/aceptación humana, staging de paths
exactos y commit/push por el humano. No iniciar otro ticket automáticamente.
Sincronizar el checkout de pruebas no despliega ni reinicia el servicio. Ningún
commit HAR exige una conciliación viva rutinaria. Nuevos documentos bajo Pepper
pueden participar en el fingerprint amplio actual; ello no autoriza reusar
consentimiento antiguo ni ejecutar reconciliación.

D01–D10 bloquean solo los trabajos que dependen de la elección correspondiente;
un gap expresado honestamente no se convierte en una implementación permitida.
Las futuras revisiones de este archivo deberán reflejar decisiones humanas
explícitas y el padre aceptado, preservando la trazabilidad del plan original.
