# HAR — Decisiones arquitectónicas y contrato del primer ámbito

Fecha de preparación: 2026-10-15 (Europe/Madrid). Ticket: **HAR-00**.
Estado: **HUMAN_APPROVED_ARCHITECTURAL_DIRECTION** (registrado por HAR-01 el
2026-10-15). Propietario de las decisiones: Pablo. D09 conserva detalles pendientes
de HAR-02/HAR-03; aprobación conceptual no equivale a implementación ni a G0.

Este documento es el propietario canónico de las decisiones HAR. El
[roadmap](harness_refactor_roadmap.md) conserva el backlog y sus gates; el
[manifiesto](harness_refactor_verification_manifest.json) contiene las selecciones
comprobadas y deuda histórica. Los documentos de `HAR/` son entradas humanas
preservadas, no un segundo catálogo de decisiones vigentes.

## 1. Autoridad, alcance y baseline

El ticket humano fija la dirección B (contratos declarativos) mediante A
(adaptación incremental), con C limitado (coordinación durable). No autoriza una
reescritura, event sourcing completo ni la aceptación unilateral de D01–D10.
En HAR-00 las decisiones quedaron propuestas. El ticket humano HAR-01, secciones
1 y 6.5, comunica la aceptación, commit y push de HAR-00 y aprueba la dirección
D01–D10. Esta es una decisión del proyecto HAR, no un registro de aprobación
Pepper. D09 aprueba solo la separación conceptual de ejecución/objetivo humano;
la matriz C26 y las garantías públicas siguen pendientes de HAR-02/HAR-03.
Cada ticket posterior requiere su alcance completo y revisión humana propios.

Baseline canónico inspeccionado: rama
`p18-manual-to-hermes-workflow-migration`, HEAD
`64debea2b3ae184b95c4eeb4cb1d9b58938c9aec`, asunto
`P18.9.13-C94 Reconcile material revision authority`. Índice y archivos rastreados
sin cambios al comenzar. La comparación de cada ticket posterior usará su padre
aceptado; este SHA no se convierte en baseline permanente de HAR.

Observación histórica HAR-00, superada por el preflight HAR-01 siguiente:
WSL fue inspeccionado mediante Git read-only el 2026-10-15:
`/home/pablo/work/AGENT-PLATFORM` continúa en
`75185e79e46424e7f495dfaad59ebdde7f45db93`, en la misma rama, con candidatos C94
sin commit y sin el objeto del HEAD canónico. Estado:
**HUMAN_SYNC_REQUIRED_BEFORE_HAR01_VERIFICATION**. Se puede completar HAR-00 desde
Windows. No se sincroniza WSL ni se valida ejecución contra su fuente atrasada.

**Preflight HAR-01 (2026-10-15):** Windows y WSL se verificaron en
`4e640c41a43a8c999a21f11988f825c5dd3bd3bf`, misma rama, índices y árboles
rastreados limpios antes de editar. La sincronización fue realizada por el humano;
la necesidad histórica de sincronización queda resuelta para este padre. Las
pruebas HAR-01 usan reconstrucciones independientes del padre mediante lectura
Git y HOME temporal, nunca el checkout servido ni el estado vivo. Resultados y
metadatos frescos constan en el manifiesto, sin sustituir la evidencia HAR-00/C94.

HAR-00 solo produce este documento, el roadmap y el manifiesto declarativo.
No ejecuta tests, imports del proyecto, builds, Graphify, Docker, instalaciones,
proveedores, lectores vivos o mutaciones Git. No hay cambio de código ni despliegue.

El contexto P18.9.13 R0002/run45 y sus hashes procede del ticket humano; no fue
revalidado. Permanece congelado. HAR no publica un ticket Pepper ni consume
consentimiento para REQUEST, RECONCILE, REVISE, aprobación, start, validación,
review o handoff. Sincronizar el checkout de pruebas no es desplegar Pepper.

Se preservan C64/C80-R1, los dos documentos de entrada `HAR/` y los tres PNG
preexistentes. Sus hashes iniciales constan en el manifiesto. No se usa su
presencia como autorización de edición o discovery.

## 2. Evidencia acotada

Las referencias son relativas al producto `2_products/pepper-agent`, salvo las
indicadas como raíz. Los números de línea describen el baseline anterior.
**OBSERVED** significa inspección estática; **HISTORICAL_TEST_EVIDENCE**, logs ya
existentes; **PROPOSED**, diseño pendiente. No se repite la auditoría completa.

| ID | Fuente y punto inspeccionado | Qué respalda |
|---|---|---|
| E01 | [pyproject.toml](../../pyproject.toml), 307–313 y 356–357 | Entrada `hermes_cli.main`; descubrimiento de `hermes_cli.*`, sin paquete plataforma independiente adoptado. |
| E02 | [tools/registry.py](../../tools/registry.py), `ToolEntry` 87–116 y `dispatch` 614–632 | Catálogo Hermes ya existente; disponibilidad no es autorización de workflow. |
| E03 | [product_runtime.py](../../hermes_cli/agent_platform/product_runtime.py), `build_workflow_control_snapshot` 33028–33524; overlays 33506–33520 | Estado operativo y precedencia distribuidos; F01/F08/F12. |
| E04 | [governed_state_machine.py](../../hermes_cli/agent_platform/workflow/governed_state_machine.py), estados 147–168 y tabla desde 1102 | Modelo formal no ejecutor, distinto de dimensiones operativas. |
| E05 | [command_validation.py](../../hermes_cli/agent_platform/command_validation.py), `identity` 32–49, `dependencies` 109–124, `inspect` 221–251, `execute` 255–298 | Binding, inferencia histórica, consentimiento, resultado y replay; F02. |
| E06 | [command_validation_context.py](../../hermes_cli/agent_platform/command_validation_context.py), 17–59 | Contexto canónico especial y fingerprint amplio; F05/F13. |
| E07 | [manual_validation.py](../../hermes_cli/agent_platform/manual_validation.py), `binding` 53–91, `inspect` 145–170, `persist` 173–210 | Atestación humana e identidad/dependencias de evidencia. |
| E08 | [post_execution_material_revision.py](../../hermes_cli/agent_platform/post_execution_material_revision.py), `context` 81–138, `request` 188–223, `apply_workflow` 226–265 | Defecto cualificado, gate previo a review y solicitud separada. |
| E09 | [material_revision_reconciliation.py](../../hermes_cli/agent_platform/material_revision_reconciliation.py), `source_only` 29–38, `context` 96–117, `inspect` 120–143, `reconcile` 147–187 | Reconciliación C94 por origen y deriva de fuente, no recuperación universal. |
| E10 | [approved_artifact_inspection.py](../../hermes_cli/agent_platform/approved_artifact_inspection.py), `inspect` 6–77 | Contrato aprobado exacto, binding, chunks y revalidación. |
| E11 | [pepper_workflow_tools.py](../../tools/pepper_workflow_tools.py), 762–777, 1094–1119, 1148–1179 y 1541–1556 | Herramientas/suboperaciones reales y nombres de argumentos. |
| E12 | [ticket_architect_bridge.py](../../hermes_cli/agent_platform/workflow/ticket_architect_bridge.py), contrato 344–481, revisión 2499–2711, promoción 2643–2655, `_write_json_atomic` 6088–6100 | Revisión estructurada, promoción por etapas y procedencia embebida. |
| E13 | [zero_change_decision.py](../../hermes_cli/agent_platform/zero_change_decision.py), `persist` 41–45 y `decision_lock` 483–499 | Creación exclusiva y lock; no transacción entre todos los stores. |
| E14 | [product_runtime.py](../../hermes_cli/agent_platform/product_runtime.py), lecturas 5725–5839, revisión 5952–6027, gate 25385–25433 | Lectura/mantenimiento, selector por origen y guards de review. |
| E15 | [review_readiness.py](../../hermes_cli/agent_platform/review_readiness.py), 252–287 | Sustitución PREPARE por diagnóstico RESOLVE si falta elegibilidad. |
| E16 | [test_agent_platform_ticket_architect_bridge.py](../../tests/hermes_cli/test_agent_platform_ticket_architect_bridge.py), fixture 5207–5260 y casos 5372–5460 | Expectativas C26 y limitación del fixture con proyección parcial. |
| E17 | [validation_command_runner.py](../../hermes_cli/agent_platform/work_packet/validation_command_runner.py), 672–703; [tests](../../tests/hermes_cli/test_agent_platform_work_packet_validation_command_runner.py), 510–550 | Archivo regular/intérprete actual, rechazo de directorio y symlink. |
| E18 | Raíz: `9_artifacts/c94/results-summary.json`, `broad-current.txt`, `broad-head.txt`, `broad-comparison.json` | 771/19/1327 históricos; comparación con C93, no ejecución HAR-00. |
| E19 | [retry_material_revision.py](../../hermes_cli/agent_platform/retry_material_revision.py), 445–464; [post_accept_material_revision.py](../../hermes_cli/agent_platform/post_accept_material_revision.py), 498–515 | Mismo ID de reconciliación proyectado fuera del origen soportado. |
| E20 | [human_git_handoff.py](../../hermes_cli/agent_platform/work_packet/human_git_handoff.py) y [product_runtime.py](../../hermes_cli/agent_platform/product_runtime.py), 11739–12195 | Política específica de handoff software, sin conceder Git al worker. |

## 3. Decisiones D01–D10

### D01 — Frontera plataforma/producto y ubicación del paquete

**Estado:** HUMAN_APPROVED. **Propietario/aprobador:** Pablo.
**Aprobación:** ticket humano HAR-01 (§1/§6.5), registrada el 2026-10-15.

- **Problema/evidencia:** F06/F08/F11; E01–E04. Los contratos ejecutables actuales
  viven en el producto; `3_platform/_governed_skeleton/core/README.md` declara un
  placeholder, no un runtime importable que ya gobierne Pepper.
- **Alternativas:** extender el archivo runtime; introducir un nuevo paquete raíz
  con packaging propio; crear un subpaquete puro dentro del paquete ya distribuido.
- **Recomendación:** proponer `hermes_cli/agent_platform/harness/` para HAR-04,
  inicialmente contratos/evaluación puros. Nombre/lugar aún no existen por HAR-00.
  No crear otro catálogo de herramientas. Adaptadores Pepper/Hermes importan el
  núcleo; el núcleo no importa `product_runtime`, selectores privados, clientes,
  stores ni herramientas. Packaging existente permite ese subpaquete sin adoptar
  una plataforma nueva. La ubicación transitoria no convierte políticas Pepper
  en contratos genéricos ni promete independencia de distribución ya conseguida.
- **Consecuencias:** portabilidad lógica inmediata; extracción física posterior
  requerirá ticket/packaging y decisión propios. No mover código ahora.
- **Pruebas/invariantes:** dependencias permitidas, importación sin efectos en
  futuros tests aislados, sin IDs P18/Cxx ni rama por dominio en contratos puros.
- **Tickets afectados:** HAR-04, HAR-06, HAR-09, HAR-16, HAR-22, HAR-28.

### D02 — Estado y tipos de continuación

**Estado:** HUMAN_APPROVED. **Propietario/aprobador:** Pablo.
**Aprobación:** ticket humano HAR-01 (§1/§6.5), registrada el 2026-10-15.

- **Problema/evidencia:** F01/F03/F12; E03–E04/E09/E19. Enums, hechos Kanban y
  overlays no comparten un significado único de acción disponible.
- **Alternativas:** ampliar un enum plano; conservar overlays sin contrato;
  dimensiones ortogonales y continuaciones tipadas.
- **Recomendación:** separar publicación/aprobación, ejecución, validación,
  revisión, finalización y vigencia de autoridad. Continuaciones propuestas:
  `EXECUTABLE_CAPABILITY`, `HUMAN_DECISION`, `OBSERVATION`,
  `EXTERNAL_REMEDIATION`, `SAFE_STOP`. Una decisión humana registra autoridad;
  no dispara por transitividad el efecto siguiente. Gate pendiente no es deadlock.
- **Primer ámbito:** operaciones O01–O08 y puertos P01–P03 de la sección 4.
  Generación general, dispatch, retry, autonomía, UI completa y control físico
  quedan fuera de ese primer corte; no se confunden con lo cubierto por el catálogo.
- **Consecuencias:** misma etiqueta de texto no demuestra igual capacidad. Los
  orígenes no soportados deben mostrar stop/remediación con razón explícita.
- **Pruebas/invariantes:** cada continuación no terminal tiene tipo y condición;
  ninguna ejecutable carece de inspector/policy/executor. Alcance explorado finito.
- **Tickets afectados:** HAR-04, HAR-06–HAR-09, HAR-14, HAR-19, HAR-21, HAR-23.

### D03 — Admisibilidad compartida y revalidación en el efecto

**Estado:** HUMAN_APPROVED. **Propietario/aprobador:** Pablo.
**Aprobación:** ticket humano HAR-01 (§1/§6.5), registrada el 2026-10-15.

- **Problema/evidencia:** F01/F03/F10/F12; E03/E05/E11/E14–E15. La proyección y
  los guards del ejecutor se deciden en rutas distintas.
- **Alternativas:** duplicar comprobaciones por superficie; usar la proyección
  como permiso; compartir una evaluación pura y mantener comprobaciones finales.
- **Recomendación:** proyección y preflight consumen el mismo resultado
  `allow/deny/wait/safe_stop`, con referencias de autoridad, versión y razones.
  El adaptador vuelve a leer/validar justo antes de efectos. Un snapshot viejo
  o un resultado `allow` sin consentimiento no concede ejecución.
- **Diferencias intencionales propuestas:** retirar ofertas ejecutables para
  orígenes no cualificados; mantener diagnósticos como no invocables; separar
  observación de mantenimiento. No paridad ciega con un placeholder engañoso.
- **Consecuencias:** rechazos cerca del efecto siguen siendo posibles por deriva;
  no se exige que una observación anterior garantice éxito futuro.
- **Pruebas/invariantes:** mismos hechos/policy/versiones, misma decisión;
  deriva concurrente denegada; ninguna doble ejecución durante shadow.
- **Tickets afectados:** HAR-05–HAR-09, HAR-14, HAR-18, HAR-21, HAR-23.

### D04 — Actor, recurso y confianza

**Estado:** HUMAN_APPROVED. **Propietario/aprobador:** Pablo.
**Aprobación:** ticket humano HAR-01 (§1/§6.5), registrada el 2026-10-15.

- **Problema/evidencia:** F06/F10; E11/E14. El handler usa convenciones como
  `pepper-chat-human` y validadores específicos; ello no acredita autenticación
  multiusuario ni aislamiento multi-tenant.
- **Alternativas:** asumir identidad del texto del agente; implementar identidad
  distribuida ahora; explicitar el ámbito local confiable y reservar el contrato.
- **Recomendación:** operador local confiable, un escritor/operación y un ticket
  mutador por checkout; concurrencia únicamente dentro del sustrato local que
  llegue a verificarse. Bindings incorporarán workflow/proyecto/recurso, actor
  validado y alcance del efecto. El adaptador confiable emite autoridad; el modelo
  no puede fabricarla copiando una frase ni ampliarla por delegación.
- **Consecuencias:** se conserva la convención heredada donde corresponda hasta
  migración aprobada. No se declara resuelta identidad remota, multi-tenant,
  aislamiento de red/procesos ni autorización de recursos físicos.
- **Pruebas/invariantes:** cruces de proyecto/recurso denegados; invocación directa
  y por tool no saltan policy; actor/binding conflictivos no promueven estado.
- **Tickets afectados:** HAR-04, HAR-07, HAR-12–HAR-13, HAR-18, HAR-20–HAR-21,
  HAR-23, HAR-26–HAR-28.

### D05 — Dependencias y significado de la validación

**Estado:** HUMAN_APPROVED. **Propietario/aprobador:** Pablo.
**Aprobación:** ticket humano HAR-01 (§1/§6.5), registrada el 2026-10-15.

- **Problema/evidencia:** F02/F07; E05/E07. C91 deriva referencias/rangos y deuda
  desde prosa. Evidencia existente puede ser fallida y permitir clasificación,
  sin satisfacer aceptación.
- **Alternativas:** ampliar regex; alterar contratos antiguos; DAG versionado con
  productor, ID, dependencia y predicado de aceptación explícitos.
- **Recomendación:** DAG para contratos nuevos; distinguir `evidence_present`,
  `failure_classified`, `requirement_satisfied` y aceptación humana. No inventar
  paso passed, ni V11-equivalente automático. Productores requeridos deben ser
  alcanzables antes de gates consumidores; rechazar ciclos/productores ausentes.
- **Compatibilidad:** conservar cuerpos, hashes e interpretación histórica con
  lector/adaptador versionado que declare límites. Una semántica histórica
  ambigua se expone; cambiarla exige revisión material/autoridad propia, no rehash.
- **Consecuencias:** el grafo no sustituye a validadores de comando, contexto,
  sustrato ni atestación manual. Evidencia de fuente distinta no se transporta
  como si acreditara la ejecución original.
- **Pruebas/invariantes:** ciclo C91 detectado; comandos alcanzables con manual
  pendiente; resultado fallido no acepta; dependencia cambiada invalida conclusión.
- **Tickets afectados:** HAR-08, HAR-10, HAR-15, HAR-23, HAR-25.

### D06 — Identidad e invalidación de autoridad

**Estado:** HUMAN_APPROVED. **Propietario/aprobador:** Pablo.
**Aprobación:** ticket humano HAR-01 (§1/§6.5), registrada el 2026-10-15.

- **Problema/evidencia:** F05/F10/F13; E06/E08–E10. El fingerprint amplio liga
  la solicitud humana a cambios de implementación además de inputs consumidos.
- **Alternativas:** mantener siempre el árbol entero; eximir documentos por
  extensión; separar identidades con manifiestos transitivos completos.
- **Recomendación:** distinguir intención humana, autoridad inmutable de workflow,
  implementación ejecutable/policy/parser, inputs de validación y ubicación del
  recurso. Validación conjunta antes del efecto; invalidez tipada por dependencia.
  Una función aislada no es identidad suficiente; parser/policy compartido invalida
  todos sus dependientes. Mantener fingerprint amplio si el comando consume ese
  árbol. No introducir exención general para documentación o archivos sin track.
- **Consecuencias:** no aceptar la fuente nueva con consentimiento viejo. C94
  conserva su semántica exacta hasta migración; reconciliación futura requiere
  evidencia de elegibilidad, consentimiento fresco y supersesión verificable.
  Estos documentos HAR también entran en el fingerprint amplio actual si se
  observan desde ese árbol; su creación no autoriza reconciliar ni reutilizar
  evidencia/consentimiento anterior. No se ha leído la autoridad viva.
- **Pruebas/invariantes:** deriva relevante/irrelevante clasificada con manifiesto
  completo; inputs cambiados requieren evidencia nueva; originales inmutables;
  historias/chains corruptas no caen hacia consentimiento anterior.
- **Tickets afectados:** HAR-09, HAR-11, HAR-14, HAR-19, HAR-23–HAR-24.

### D07 — Durabilidad, concurrencia y replay

**Estado:** HUMAN_APPROVED. **Propietario/aprobador:** Pablo.
**Aprobación:** ticket humano HAR-01 (§1/§6.5), registrada el 2026-10-15.

- **Problema/evidencia:** F04; E12–E13. Exclusividad de archivo y rename protegen
  pasos locales; promoción, eliminación de aprobación, history y proceso cruzan
  fronteras distintas. RLock no coordina procesos independientes.
- **Alternativas:** mantener convenciones por operación; event sourcing completo;
  journal mínimo de una operación seleccionada con versión esperada y recibos.
- **Recomendación:** journal limitado y versionado, un propietario del efecto,
  operation ID, expected authority version, etapas y recibo. Conservar stores
  actuales. Acreditar inicialmente fallos de proceso/reinicio y conflictos locales
  sobre el sustrato probado. Elegir la operación concreta en HAR-12, no ahora.
- **Replay:** resultado confirmado se reutiliza; conflicto se rechaza; efecto
  externo de resultado desconocido exige observación/recuperación específica o
  safe stop. Nunca reintento ciego ni promesa exactly-once externo.
- **Consecuencias:** lock huérfano no se elimina automáticamente; no se promete
  tolerancia a pérdida de energía sin pruebas y política de flush/sustrato.
- **Pruebas/invariantes:** interrupciones antes/después de cada etapa, proceso
  muerto tras efecto, recibo ausente, writers concurrentes y decisiones opuestas;
  no promoción parcial anunciada como completa ni duplicación confirmada.
- **Tickets afectados:** HAR-12–HAR-14, HAR-16–HAR-19, HAR-23, HAR-25.

### D08 — Historia, versiones y rollout

**Estado:** HUMAN_APPROVED. **Propietario/aprobador:** Pablo.
**Aprobación:** ticket humano HAR-01 (§1/§6.5), registrada el 2026-10-15.

- **Problema/evidencia:** F04/F11; E08–E12. Los registros llevan policy/schema y
  digests históricos; cambiar serialización o interpretación puede invalidarlos.
- **Alternativas:** convertir todo al formato nuevo; mantener dos escritores;
  lectores/adaptadores explícitos y cambio de propietario por capacidad.
- **Recomendación:** soportar primero los schema/policy existentes que cubre el
  corpus comprobado del manifiesto, incluidos originales C91–C94. Inventariar
  versiones antes de prometer soporte fuera del corpus. Originales sin reescritura;
  envelope nuevo los referencia. Versión desconocida: error/stop, no negociación
  o actualización silenciosa. Shadow calcula decisiones, sin ejecutar efectos.
- **Corte:** una ruta y un escritor por capacidad en HAR-14, tras G1, identidad,
  journal/recovery y aprobación humana. Rollback a lector/implementación compatible
  o contención; no restaurar archivos para borrar decisiones posteriores.
- **Pruebas/invariantes:** corpus de formatos originales, digests estables,
  ausencia de doble writer y diferencias shadow explicadas/aprobadas.
- **Tickets afectados:** HAR-04, HAR-09, HAR-14, HAR-16, HAR-22–HAR-27.

### D09 — Semántica C26 y compatibilidad pública

**Estado:** HUMAN_APPROVED_CONCEPT_ONLY; detalles HAR-02/HAR-03 pendientes. **Propietario/aprobador:** Pablo.
**Aprobación:** ticket humano HAR-01 (§1/§6.5), registrada el 2026-10-15.

**Problema/evidencia:** F01/F07/F11/F12; E14–E18. Los resultados siguientes son
históricos de la candidatura C94 contra C93, no una reproducción HAR-00.

| Caso exacto de `test_agent_platform_ticket_architect_bridge.py` | Aserción existente | Resultado del log histórico | Evidencia estática y elección |
|---|---|---|---|
| `test_c26_rejected_successor_revision_preempts_stale_review_prepare_projection` | `current_ticket_id is None`; después espera sucesor P18.9.2, `awaiting_correction`, `REVISE_P18_9_2` | Primera aserción: P18.9.1 en vez de None; el log no acredita qué habrían dado las aserciones posteriores | Fixture instala predecesor stale y proyección parcial; selección de sucesor y vigencia de predecesor deben resolverse con hechos durables, no solo nombre/order del overlay. |
| `test_c26_active_execution_still_preempts_pending_successor_projection` | Mantener P18.9.1/active=1 y `PREPARE_P18_9_1_REVIEW` | Acción `RESOLVE_P18_9_1_REVIEW_BLOCKER` | Gate de review rechaza active!=0 y el overlay convierte PREPARE en diagnóstico; la proyección parcial también puede producir un blocker anterior. No se atribuye el resultado exacto a un guard concreto sin reproducción. |

**Alternativas concretas:**

1. Conservar el contrato legado de foco: sucesor rechazado reemplaza contexto stale
   y `current_ticket_id=None`; PREPARE puede ser solo una sugerencia no admisible
   durante ejecución. Exigir otra representación de disponibilidad para no engañar.
2. Hacer explícitos ticket de ejecución y objetivo de decisión; una ejecución
   realmente activa no se desplaza. Si no queda ejecución/autoridad incompleta
   válida del predecesor y el sucesor fue rechazado, foco humano es su revisión.
   PREPARE ejecutable solo si el gate completo permite review; en otro caso wait,
   diagnóstico o safe stop con razón.
3. Mantener conducta actual provisionalmente, sin declarar resueltas las dos
   discrepancias; bloquear G0 hasta adjudicación y fixtures representativas.

**Dirección conceptual aprobada:** separar ejecución y objetivo de decisión,
como en alternativa 2. Sus valores de campos/compatibilidad concretos continúan
como recomendación pendiente, no como resolución de C26. Definir en
HAR-03 la matriz y traducción del campo legado antes de cambiar código/tests.
Usar campos conceptuales separados de ejecución/decisión no obliga a romper APIs.
En el escenario sin ejecución válida, recomendar compatibilidad `current_ticket_id`
None con objetivo REVISE del sucesor; en ejecución activa válida, conservar su
identidad y no anunciar PREPARE invocable. Una proyección contradictoria/parcial
no acredita por sí misma ninguna de las dos situaciones. La política debe
aprobarse explícitamente, no por buscar verde.

**Las cuatro expectativas estructurales son un problema separado (HAR-02):**

| Nodo exacto | Log histórico | Contrato a decidir antes de sustituirlo |
|---|---|---|
| `test_agent_platform_work_packet_validation_command_runner.py::test_prior_113_exports_remain_exact_prefix` | 114 frente a 113 | Símbolos y comportamientos públicos comprometidos, no cantidad global. |
| `test_agent_platform_work_packet_diff_artifact_review.py::test_prior_172_exports_remain_exact_prefix` | 173 frente a 172 | Igual criterio; conservar compatibilidad real del review. |
| `test_agent_platform_work_packet_human_git_handoff.py::test_p17_0_through_p17_6_exports_remain_exact_prefix` | 202 frente a 201 | API heredada soportada y retirada explícita, no orden incidental. |
| `test_agent_platform_work_packet_human_git_handoff.py::test_legacy_instruction_renderer_is_not_public_or_package_level` | Posición 227 contiene `validate_human_git_handoff_result`, espera renderer | Adjudicar renderer público/privado y símbolos permitidos/prohibidos; no inferir que todo el test es inválido por una posición. |

**Consecuencias/pruebas:** conservar tests negativos y compatibilidad comprometida;
nueva prueba debe fallar si se retira un símbolo soportado. No cambiar publicness
sin decisión. HAR-01 reproducirá; HAR-02 tratará estructura; HAR-03 semántica/G0.
Tickets posteriores afectados: HAR-07, HAR-17, HAR-21–HAR-23.

### D10 — Finalización por dominio y alcance de efectos

**Estado:** HUMAN_APPROVED. **Propietario/aprobador:** Pablo.
**Aprobación:** ticket humano HAR-01 (§1/§6.5), registrada el 2026-10-15.

- **Problema/evidencia:** F06/F10; E20. La política software de Pepper no puede
  convertirse en requisito universal de Git para aceptar un artefacto técnico.
- **Alternativas:** Git para todo; cada plugin decide completion sin control;
  completion policy explícita del producto/dominio sobre evidencia gobernada.
- **Recomendación:** separar resultado técnico, aceptación humana y finalización.
  Una simulación ficticia puede completar con artefacto/evidencia/aceptación;
  Pepper mantiene su handoff Git humano aplicable. Workers nunca reciben Git
  mutador por cumplir validación o por delegación.
- **Efectos:** primer piloto Siamese determinista/simulado, sin solver real,
  credenciales externas, control BMS/HVAC ni llamadas a recursos reales. Observar,
  simular, recomendar, shadow y controlar no comparten consentimiento transitivo.
- **Consecuencias/pruebas:** adaptador desmontable con inputs/resultados tipados,
  presupuesto, recursos, timeout/cancel/retry y procedencia; una capacidad nueva
  no modifica selectores privados ni omite policy; ningún handoff Git ficticio.
- **Tickets afectados:** HAR-04, HAR-15, HAR-18, HAR-20, HAR-23, HAR-28–HAR-29.

## 4. Inventario contractual del primer ámbito (AS-IS)

Todas las filas describen implementaciones actuales, no contratos ya migrados.
La tipificación de continuación es **PROPOSED**. Tool disponible no implica
admisibilidad/consentimiento. Inspección hace lecturas y revalidaciones; no crea
consentimiento. No se invocó ninguna operación al construir este inventario.

| ID / continuación propuesta | Tool público y suboperación real / familia de acción | Inspector y binding | Policy/consentimiento y ejecutor | Efectos/evidencia; invalidación y recuperación actuales |
|---|---|---|---|---|
| O01 OBSERVATION | `prepare_current_ticket_review`, `operation=inspect_commands`; descubre `VALIDATE_<token>_COMMANDS` | `command_validation.inspect`; binding B-CV descrito abajo | Sin consentimiento de ejecución; handler E11 → inspector E05 | Preview de specs/planes/evidencia; no run ni review nuevo. Candidato/zero-change, autoridad inválida o manual failed bloquean. No rematerializar ni ejecutar para inspeccionar. |
| O02 EXECUTABLE_CAPABILITY con HUMAN_DECISION previa | Mismo tool, `operation=run_commands`; `VALIDATE_<token>_COMMANDS` | O01; argumento exacto `binding` | `pepper-pre-review-command-validation-v1`; texto `VALIDATE_<token>_COMMANDS BINDING <cv.digest(binding)>`; `cv.execute` → runner gobernado | Ejecuta comandos aprobados shell=False y persiste resultado acotado, no worker/review. Relee binding tras proceso; replay de registro válido evita ejecución nueva. Resultado fallido puede existir sin pasar contrato; deriva o crash sin recibo no autoriza retry ciego. |
| O03 OBSERVATION | `inspect_pending_approval_artifact_section`, `authority_scope=current_approved`; `section_id=ticket_spec|validation_steps` | `approved_artifact_inspection.inspect`; API usa `approval_id` como ticket ID, no un path; `expected_binding` opcional para fijar chunks | Solo generación actual aprobada; E10 valida cuerpos/publicación/WorkPacket/decisión; sin consentimiento mutador | Devuelve objeto exacto o JSON chunks con SHA256; no revisión/aprobación. Pending/supersedido/corrupto/mismatch/deriva concurrente falla cerrado. No fallback histórico. No familia de acción mutadora propia. |
| O04 OBSERVATION | `request_current_ticket_material_revision`, `origin=post_execution`, `operation=inspect` | E08 `inspect/context`; devuelve B-REQUEST | Prueba defecto explícito de referencias tests ausentes en contrato inmutable, terminal inactivo y antes de review; no consentimiento mutador | `requestable`, binding y acción REQUEST/REVISE; no solicitud ni revisión nueva. Ausencia de defecto no se transforma en permiso. |
| O05 EXECUTABLE_CAPABILITY con HUMAN_DECISION previa | Mismo tool/origin, `operation=request` (default); `REQUEST_<token>_POST_EXECUTION_MATERIAL_REVISION` | O04; argumentos `request_binding`, `next_action_id`, `human_authorization_text` | `pepper-post-execution-material-revision-v1`; `<action> BINDING <cv.digest(binding)>`; E08 `request` | Crea solicitud immutable y `awaiting_material_revision`, conserva historia, no genera sucesor. Actor/replay/conflicto y doble revalidación. Deriva tras solicitud bloquea; únicamente O07 cuando cualificada. |
| O06 OBSERVATION | Mismo tool/origin, `operation=inspect_reconciliation`; descubre `RECONCILE_MATERIAL_REVISION_AUTHORITY` | E09 `inspect/context`; B-RECON y SHA aprobado de validation_steps | Valida petición previa y cambios solo en fingerprint fuente; historia/artefacto idénticos; sin consentimiento consumido | Binding, disponibilidad y consentimiento exacto; payload acotado. `reconciliation_available=false` es stop/remediación, no reconciliador universal. |
| O07 EXECUTABLE_CAPABILITY con HUMAN_DECISION previa | Mismo tool/origin, `operation=reconcile`; `RECONCILE_MATERIAL_REVISION_AUTHORITY` | O06; argumento público **`reconciliation_binding`**, no `request_binding` | `pepper-material-revision-authority-reconciliation-v1`; `RECONCILE_MATERIAL_REVISION_AUTHORITY BINDING <cv.digest(binding)>`; E09 `reconcile` | Appended link por SHA predecesor, solicitud efectiva derivada; devuelve REVISE sin generar/ejecutar. Replay exacto; deriva sucesiva exige consentimiento nuevo; máximo 8 links/4 MiB; corrupción/conflicto/otra identidad falla cerrado, sin fallback. |
| O08 EXECUTABLE_CAPABILITY con HUMAN_DECISION separada | `revise_current_ticket_for_material_contract_failure`; `REVISE_<token>` | Workflow/material authority actual y O03 para construir overlay; `revision_contract` y guards project/ticket/action | Consentimiento explícito REVISE validado por handler/bridge; no reutiliza REQUEST/RECONCILE. E14 → E12 `revise_current_ticket_for_material_contract_failure` | Nueva publicación/WorkPacket pendiente de aprobación; procedencia anterior embebida, aprobación actual retirada, history adicional. Campos permitidos y guard de autoridad actual. Mutaciones de varios registros no son transacción global; no run ni aprobación sucesor. |
| P01 OBSERVATION | `inspect_current_ticket_manual_validation` | E07/E14; contrato/completion e ítems exactos, evidencia dependiente | Inspector actual; no atestación | Interfaz de prerequisitos consumida por O01/O02/review; lectura no crea passed ni nuevo consentimiento. |
| P02 HUMAN_DECISION | `attest_current_ticket_manual_validation` | Binding por ítem B-MANUAL; texto passed/failed y evidencia explícitos | `manual_validation.persist`, validadores E07; actor y texto exactos | Registro inmutable por ítem; dependencias cambiadas invalidan conclusión. Failed requiere resolución gobernada existente (fuera de los ejecutores migrados iniciales). No aceptar V10/V11 automáticamente. |
| P03 OBSERVATION / HUMAN_DECISION para preparar | `get_workflow_control(blockers_only=true)`, `get_review_status`; `prepare_current_ticket_review(operation=prepare)` y `PREPARE_<token>_REVIEW` | E14 gate/E15; R/V/S, contrato completo, inactivity, candidato, manual/command evidence | Lectura solo observa; preparar exige petición humana y guards actuales. `operation=prepare` no equivale a `run_commands` | Preparación persiste package y espera decisión humana, nunca acepta por sí misma. Gate actual convierte PREPARE no admisible en RESOLVE diagnóstico. Observación general heredada puede inicializar/reconciliar (E14); el puerto nuevo HAR-05 debe ser puro. |

### Bindings exactos relevantes

- **B-CV (E05 `identity`):** `project_id`, `ticket_id`, `ticket_spec_SHA256`,
  `work_packet_id`, `work_packet_SHA256`, `projection_SHA256`,
  `kanban_board_slug`, `kanban_task_id`, `revision` numérica de publicación,
  `run_id`, `completion_SHA256`, `validation_contract_SHA256` y, cuando
  corresponde, `canonical_validation_source`. Este último lleva `policy_id`,
  `source_root`, `source_files_SHA256`, `source_file_count`, `source_bytes`.
  No reinterpretar ese source como snapshot retrospectivo del worker.
- **B-ARTIFACT (E10):** se incluyen
  `project_id`, `ticket_id`, `ticket_spec_SHA256`, `work_packet_id`,
  `work_packet_SHA256`, `bridge_SHA256`, `revision` textual Rnnnn,
  `publication_id`, `publication_artifact_SHA256`, `approval_publication_SHA256`,
  `approval_publication_id`, `approval_SHA256`. No convertirlo en B-CV ni añadir
  `projection_SHA256`. Digest de sección y pagination son campos de respuesta.
- **B-REQUEST (E08):** B-CV más `defect_category`, `defects` (validation_id,
  defect_locus, source_command, command_authority_SHA256, execution_plan_SHA256,
  missing_paths), `requested_material_fields=[validation_steps]`. Historia
  projection/completion/zero-change/validation contract queda en registro durable.
- **B-RECON (E09):** `old_material_revision_request_SHA256`, `old_request_binding`,
  `current_request_binding`, `approved_artifact_binding`,
  `validation_steps_SHA256`. Solo campos source del fingerprint pueden variar;
  mismo root/policy, SHA realmente distinto, resto/historia idénticos.
- **B-MANUAL (E07):** project/ticket/spec/packet, run/board/task,
  completion_SHA256 original, terminal_result_SHA256 independiente de metadata,
  validation_id, validation_item y validation_contract_SHA256. Evidencia
  dependiente se almacena separadamente sin cambiar bindings históricos.
- **B-REVISE (E12/E14):** autoridad cargada server-side por origen, predecessor
  publication/generation/approval/request, human text y `revision_contract`
  tipado. `validation_steps` es reemplazo completo si se suministra, no patch
  ambiguo de un ítem. Los guards opcionales no son una autorización genérica.

### Continuaciones no soportadas o diagnósticas

E19 proyecta `RECONCILE_MATERIAL_REVISION_AUTHORITY` para retry/post-accept.
E11 rechaza `operation` fuera de `origin=post_execution`; no existe aquí un
reconciliador general para esos orígenes. C94 no repara autoridad corrupta ni
identidad inmutable cambiada. Catalogar esas condiciones como stop/remediación
es una propuesta HAR-06/07/19, no implementación HAR-00.

`RESOLVE_<token>_REVIEW_BLOCKER` y `RESOLVE_RECOVERY_AUTHORITY_BLOCKER` son
instrucciones diagnósticas, sin ejecutor universal identificado. Una espera humana
o parada segura justificada no debe forzarse hasta permitir ejecución.

## 5. Contrato de ejecución HAR y revisión humana

1. Un ticket completo manualmente invocado; verificar raíz, branch, HEAD, index,
   candidate/procedencia y exclusiones antes de editar. Padre exacto por ticket.
2. Solo allowlist y entregable autorizados; un escritor por checkout/operación;
   ningún subagente mutador o ticket paralelo implícito.
3. Verificación aislada con paths/manifiesto explícitos y wrapper canónico cuando
   corresponda. HAR-00 es estático: ninguna selección fue ejecutada.
4. Entregar diff/stat y evidencia limitada a lo probado, deuda/risks y gate.
5. Pablo revisa/acepta; solo el humano stagea paths exactos y hace commit/push.
   No comandos de staging inventados a partir de un backlog futuro.
6. Generar el siguiente ticket completo solo después de revisión del anterior
   y autorización humana. El roadmap no ejecuta HAR-01 ni HAR-04 transitivamente.
7. No byte-swapping en un árbol servido por el proceso vivo; sincronización de
   pruebas no implica despliegue/restart/reconciliación de Pepper.
8. G4/G5 necesitan autorización específica: HAR-26 lectura real separada,
   HAR-27 consentimiento fresco por operación. No prometer autoridad R0002 para R0003.

## 6. Registro de aprobación y gates que permanecen pendientes

HAR-00 está aceptado y comprometido en el padre HAR-01 según el ticket humano.
D01 conserva la ubicación transitoria bajo el paquete existente y la dirección
de dependencias: contratos puros no importan selectores privados Pepper.
D02–D08/D10 están aprobadas como dirección arquitectónica, no implementadas.
D09 está aprobada en concepto; las dos aserciones C26 y las cuatro expectativas
estructurales públicas siguen sin resolver, con propietarios HAR-03 y HAR-02.
No se aprueban por transitividad los valores de campos legados recomendados.

HAR-01 solo corrige construcción de fixtures autorizadas y reproduce selecciones;
no relaja guards ni inicia HAR-02. Revisión y commit/push humano de HAR-01 siguen
siendo obligatorios antes del siguiente ticket. G0 queda pendiente hasta HAR-03.
No se concede consentimiento para ninguna operación viva P18.9.13 ni para un
refactor de producción por registrar esta aprobación.

## 7. HAR-02 — Contrato público comprobable (candidatura para revisión humana)

Preflight 2026-10-15: Windows y WSL coinciden en el padre aceptado HAR-01
`20706caca7e2399e75b961825af7c5fd31662694`, rama
`p18-manual-to-hermes-workflow-migration`, índices y árboles rastreados limpios.
La aceptación/commit/push de HAR-01 procede del ticket humano HAR-02; los
resultados originales HAR-00/HAR-01 del manifiesto se conservan íntegros.
D08 y las aprobaciones D01–D10 permanecen vigentes. Este apartado documenta una
corrección de tests autorizada; no declara aceptada por el humano su candidatura.

### Disposición de los siete fallos

Referencias relativas al producto. Los nombres de test se conservan para mantener
los node IDs históricos aunque sus aserciones ya no usan prefijos/posiciones.
Cada nodo se clasifica **STRUCTURAL_ASSERTION_ONLY** por los motivos siguientes:

| Archivo / nodo exacto | Contrato conservado y evidencia |
|---|---|
| `test_agent_platform_work_packet_validation_command_runner.py::test_prior_113_exports_remain_exact_prefix` | P17.0–P17.4: nombres históricos de compiler, allocator, permisos, ejecución y runner, con identidad del módulo canónico. `work_packet/__init__.py:3–29,198–291,322–412` reexporta explícitamente esos objetos. |
| `test_agent_platform_work_packet_diff_artifact_review.py::test_prior_172_exports_remain_exact_prefix` | P17.0–P17.6, incluidos outcomes/review; `__init__.py:31–60,293–320` y `diff_artifact_review.__all__` establecen la superficie. |
| `test_agent_platform_work_packet_human_git_handoff.py::test_p17_0_through_p17_6_exports_remain_exact_prefix` | P17.0–P17.7, conservando cada nombre anterior y la API human-only; `__init__.py:62–89` y `human_git_handoff.py:120–148`. |
| `test_agent_platform_work_packet_human_git_handoff.py::test_legacy_instruction_renderer_is_not_public_or_package_level` | Renderer PowerShell público canónico; nombre legado ausente del paquete y del módulo. Solo la posición 227 era incorrecta; evidencia histórica y matriz más abajo. |
| `test_agent_platform_work_packet_tool_permissions.py::test_public_export_prefix_and_counts` | Nombres P17.0–P17.2, identidad y unicidad; ejecutores genéricos prohibidos. `__init__.py:232–257` mantiene los reexports; el prefijo truncado perdía `validate_tool_permission_decision` en la comparación. |
| `test_agent_platform_work_packet_tool_permissions.py::test_import_smoke_exact_output` | Import real del paquete y todos los nombres históricos de esas tres capacidades, identidad de objetos, sin ejecutores genéricos. El test anterior no lanzaba un proceso ni prometía stdout: comparaba una tupla y un prefijo. |
| `test_agent_platform_work_packet_governed_autonomy.py::test_01ah_exports_append_after_p17_r` | Contrato acumulado P17.0–P17.8/cierre/01AH, incluidos los símbolos del piloto. Nombres 01AH explícitos independientes de `autonomy.__all__`; reexports `__init__.py:91–196` y módulos respectivos. |

La causa está documentada en el commit histórico
`1d32ba9a34617996e6fb73265a93d047a5fed69a` (C36): añadió explícitamente
`WorkPacketValidationCommandAuthority` tanto a los imports/exports del paquete
como a `EXPECTED_EXPORTS`, los modelos públicos y las pruebas del compilador.
No se trata de asumir que cualquier símbolo añadido es seguro por ser importable.
Los prefijos antiguos conservaron cantidades/índices anteriores a esa adición.
No hay evidencia de obligación contractual de orden de enumeración. Los nombres
históricos soportados y su módulo canónico sí constituyen una obligación.

### Matriz del renderer

| Pregunta | Decisión basada en evidencia |
|---|---|
| ¿Es público el renderer? | `render_human_git_handoff_powershell` sí: commit de introducción P17.7 `9b995fc`, `human_git_handoff.__all__:147`, reexport de paquete y documentación `work_packet_human_git_handoff.md:49`. |
| ¿Es intencional la ausencia del nombre legado en el paquete? | Sí: el test histórico ya exigía `not hasattr(work_packet, "render_human_git_handoff_instructions")` y ausencia en `hgh.__all__`. No existe definición con ese nombre en P17.7 ni en el padre HAR-01. |
| ¿Cambió la visibilidad en HAR-02? | No. Producción no se modifica. El módulo original P17.7 conserva la misma lista y el mismo renderer; el paquete conserva el reexport. |
| ¿Solo era incorrecto el índice? | Sí: posición 227 contiene el validador; la adición C36 desplazó el renderer. |
| ¿Preserva el límite una prueba directa? | Sí: nombre público en `__all__` e identidad con `hgh`; nombre legado ausente en ambos `__all__` y atributos de paquete/módulo. No existe ruta de import explícito del nombre legado. |

Consumidores existentes: `product_runtime.py:27542–27609` importa y usa el
renderer público del paquete. Las rutas canónicas de import se mantienen.
Las pruebas de determinismo/render, modelos, esquemas, bindings, firmas usadas
por los consumidores, rechazo de datos y autoridad human-only permanecen intactas.
No se introduce una promesa de compatibilidad sobre todos los detalles internos.

### Invariante y sensibilidad

El helper compartido vive en el test permitido de permisos; varias capacidades
comparten exactamente el contrato de nombre/identidad/unicidad. Consulta módulos
canónicos por sus rutas establecidas, nunca obtiene las expectativas históricas
del `__all__` vigente. Para módulos antiguos sin `__all__`, el contrato se expresa
por los reexports explícitos del paquete; para los que lo declaran también exige
la pertenencia al `__all__` del módulo. Ningún helper de producción cambia.

Interfaces sintéticas, sin modificar módulos reales, prueban: retirar un símbolo;
sustituir su objeto; exponer un atributo privado incluso sin exportarlo; exportar
un privado; duplicar un export; retirar funcionalidad histórica de otra capacidad.
Una interfaz con adiciones y orden diferente conserva el contrato. Los resultados
frescos y node IDs constan en la sección `har02_verification` del manifiesto y la
evidencia externa HAR-02. Las versiones intermedias están marcadas superseded.

D09 conserva **C26 pendiente de HAR-03**. Esta candidatura resuelve únicamente las
aserciones estructurales de API autorizadas, sin alterar publicness, aliases,
schemas, implementaciones ni política de Git. G0 continúa pendiente; no se inicia
HAR-03 ni se lee o muta autoridad Pepper viva.

Comparación aislada HAR-02: las expectativas acumuladas cubren todos los nombres
públicos del padre (330 observados; no es una cantidad exigida por los tests).
Inventarios runtime padre/candidato comparan iguales: superficie, módulo/objeto
canónico, firmas de funciones, schemas JSON de modelos y valores de enums.
`public-api-comparison.json` e inventarios adjuntos conservan la observación.
La búsqueda acotada en `hermes_cli/` y `tools/` no encontró consumidores de
índices de `work_packet.__all__`. Los tests nuevos permiten reordenar nombres
manteniendo identidad, unicidad y ausencia de las superficies prohibidas.

## 8. HAR-03 — Semántica C26 cualificada y candidatura G0

Padre aceptado, verificado read-only el 2026-10-15 en Windows y WSL:
`4d9f5192aac30d5c7b7ae9cb192b1f34771db83b`, rama
`p18-manual-to-hermes-workflow-migration`; índices y árboles rastreados limpios.
HAR-00–HAR-02 aceptados/commit/push según el ticket humano HAR-03. Sus resultados,
hashes y aprobaciones anteriores permanecen históricos, sin reclasificarlos.
Esta sección prepara revisión humana de G0; no lo declara aprobado ni inicia HAR-04.

### Hechos, objetivos y traducción del campo legado

D02/D03/D08 permanecen vigentes. Se distinguen tres conceptos sin crear otro
registro ni adoptar prematuramente contratos HAR-04:

- **Execution target:** generación aprobada, TicketSpec/WorkPacket vinculados,
  proyección Kanban validada y task/run/start de ese ticket. Un contador o un
  overlay no sustituye esos registros. Con un run activo válido, el contexto
  primario permanece en ese ticket y su acción existente es `MONITOR_*_EXECUTION`.
- **Decision target:** generación/publicación canónica y decisión de aprobación o
  rechazo validada contra esa generación. Un rechazo requiere `REVISE` independiente;
  no concede ejecución. Con otro ticket activo, esa decisión sigue existiendo en
  sus registros/overlay de publicación y espera; no desplaza el monitor ni se ejecuta.
- **Review target:** proyección/run terminal vigente, contrato satisfecho,
  atestaciones humanas exigidas y gate completo de review. No se deriva del texto
  `execution_completed` o del nombre PREPARE en una proyección vieja.

`current_ticket_id` conserva su traducción por contexto; no se redefine como un
campo universal de permiso de ejecución. Para un sucesor pendiente sin precedencia
activa se conserva la publicación vigente como contexto (C61). Para un sucesor
rechazado cualificado sin precedencia vigente del anterior se conserva el mapping
existente `current_ticket_id=None`, `next_ticket_id=<sucesor>` y
`next_action.target_ticket_id=<sucesor>`, acción `REVISE_<sucesor>`.
Consumidores: `product_runtime._workflow_ticket`/`build_lead_agent_operational_context`,
`tools/pepper_workflow_tools._get_current_ticket`/`_get_workflow_control` y
`web/src/agent-platform/runtime-overview/contract.ts::parseWorkflowControl`.
El campo nullable y los IDs de acción/contexto permanecen utilizables sin nuevos
campos de execution_target/decision_target ni un registry de lifecycle paralelo.

### Matriz de precedencia y continuación

Las etiquetas OBSERVATION/HUMAN_DECISION/SAFE_STOP siguientes explican semántica;
no son tipos de runtime nuevos de HAR-04. Todos los registros son de fixtures
sintéticas aisladas; no se consultó autoridad P18.9.13 viva.

| Escenario | Autoridad/objetivos | Review y continuación |
|---|---|---|
| Predecesor activo válido, sucesor pendiente | Approval/generation/WorkPacket/projection/start/task.current_run_id/run coherentes; decisión separada en generación sucesora pendiente | `current_ticket_id` del activo; `MONITOR_<activo>_EXECUTION` como observación/wait. Review denegado; no aprobar/start sucesor. |
| Predecesor activo válido, sucesor rechazado | Misma ejecución retenida; rechazo vinculado a generación sucesora, decisión `REVISE` separada | Monitor del activo. El rechazo no se pierde ni se convierte en ejecución/revisión automática. |
| Predecesor terminal, sucesor rechazado | Validez del terminal/review/completion se comprueba en loaders y precedencia durable; publicación sucesora debe ser canónica | Solo gate completo habilita review. Sin precedencia vigente retenida, decisión cualificada `REVISE`; autoridad contradictoria bloquea. Ningún PREPARE stale acredita elegibilidad. |
| Predecesor stale sin ejecución/review vigentes, sucesor rechazado | Fixture real de generación aprobada/proyección/task en cola sin runs/start/terminal; overlay UI antiguo se declara derivado; rechazo real del sucesor | Mapping legado null y REVISE del sucesor. Todos los permisos de ejecución siguen false. Inspección no escribe. |
| Run activo con validación incompleta/fallida | El run activo se acredita por la cadena durable, no por validation_state inyectado | Monitor/wait, nunca PREPARE. Gate/executor de preparación deniega incluso con una invocación explícita. |
| Terminal review-ready sin decisión competidora | Run terminal exacto, evidencia de comandos y atestaciones manuales construidas por infraestructura existente | PREPARE del terminal solo tras `_review_prepare_workflow_blocker`; observar no crea review ni acepta nada. |
| Identidad actual conflictiva/start ausente o corrupto | No heredar permiso de proyección. Un run persistido sin start no equivale a «nunca iniciado» | Blocker explícito y contexto diagnóstico; nueva traducción pública aprobada abajo. Sin START, PREPARE, executor o reconciliación implícita. |
| Proyección parcial/contradictoria | Contador/status no acreditan autoridad; blocker derivado permite diagnóstico | RESOLVE_REVIEW_BLOCKER es diagnóstico; guard real rechaza ese ID como request de PREPARE. Inspección explícita usa conexiones read-only. |

### Causas y alcance ejecutado

Caso A: `_correction_successor_records_for_precedence` llamaba a
`generated_record_to_workflow_overlay` sin importarlo. `except Exception` ocultaba
el NameError, por lo que el selector devolvía cero rechazos. Se añade el import
local; el mapping null/REVISE ya estaba implementado. Se valida con generación,
rechazo y proyección durables; no con ausencia asumida de información.

Caso B: el fixture anterior solo insertaba `active_execution_count=1` en un
snapshot también marcado completed. No tenía approval/proyección/start/run que
acreditara ejecución vigente. El fixture corregido usa la infraestructura existente
con spawn/PID sintéticos; construye y valida aprobación, WorkPacket, proyección y
run activo. El resultado MONITOR ya existía en producción y en tests de Kanban;
PREPARE durante ejecución contradecía el gate. No se altera ese guard para verde.

Las pruebas nuevas descubrieron otra contradicción: start ausente, run activo,
status queued y oferta START sin blocker. Antes de ejecutar su cambio público se
pidió la decisión exigida por HAR-03 §§4/7. **Pablo aprobó durante HAR-03** conservar
`current_ticket_id` como contexto diagnóstico y publicar:

- `workflow_status=execution_authority_blocked`;
- `next_action.id=RESOLVE_<ticket>_EXECUTION_AUTHORITY`;
- `next_action.executable=false`, `next_action.read_only=true`;
- blocker explícito y retirada de START/PREPARE, sin nuevo executor, permiso ni
  reconciliación automática.

La aprobación textual y su pregunta exacta constan en `human-semantic-decision.json`
del directorio externo HAR-03. No se infirió esta decisión desde D09 conceptual.
Se conserva el contador observado; flags de permiso quedan false. La lectura
específica del run reutiliza `execution_evidence.connection`/`evidence_sqlite`
(imagen DB/WAL en memoria), sin crear DB/sidecars, reap ni recrear start authority.
El bloqueo se aplica al ticket actual con ejecución activa y blocker de su start,
al final de overlays y antes de publicar elegibilidad de review.

Solo cambian tres funciones de `product_runtime.py`: selector de correcciones,
`_current_ticket_execution_start_overlay` y `build_workflow_control_snapshot`.
No cambia `review_readiness.py`, el bridge de generación, ningún executor,
consentimiento/approval/retry/review guard, ni mecanismos C91–C94. No hay rama
nueva por P18.9.1/P18.9.2/C26 ni mutación de los registros inspeccionados.

### Evidencia, límites y gate siguiente

Dos nodos originales corregidos; cinco funciones nuevas aportan siete casos de
regresión. Con los otros C26, la selección focalizada tiene 12 casos. Registros
sintéticos se comparan por bytes antes/después de observar; los casos negativos
corrompen/retiran únicamente su propia autoridad temporal para comprobar rechazo.
Las cuatro selecciones y comparaciones frescas constan en `har03_verification`.
Todos los campos históricos del manifiesto HAR-00/HAR-01/HAR-02 se conservan.

Límite observado: un dashboard general sin scope read-only puede inicializar una
DB vacía; el bootstrap de `model_tools.handle_function_call` también puede crear
SOUL/state antes del handler. Eso no se presenta como inspección global sin efectos
ni se corrige en este ámbito. La inspección explícita de blockers usa el scope
read-only ya existente; su núcleo y las observaciones con autoridad construida
se verifican sin cambios durables. Evidencia/limites no equivalen a garantías sobre
un runtime vacío o todos los callers del repositorio.

G0 solo puede quedar **READY_FOR_HUMAN_REVIEW** con la baseline seleccionada sin
fallos/errores y sin regresiones nuevas. Cualquier cierre de G0 y habilitación de
HAR-04 requiere aceptación humana separada. HAR-03 no inicia HAR-04 ni operaciones
Pepper vivas, Git, deploy/restart, proveedores, Docker o Graphify.


## 9. HAR-04 — Contratos puros versionados de plataforma

### Autoridad y límite de activación

El ticket humano HAR-04 declara HAR-00–HAR-03 aceptados, committed/pushed y G0
**HUMAN APPROVED**. Padre verificado en Windows/WSL:
`0dd2a42c16cba6921dc9cdf60ba8d837aa76d4e2`, rama
`p18-manual-to-hermes-workflow-migration`. Esta aceptación posterior se registra
en `har04_verification`; el estado pendiente histórico de HAR-03 no se reescribe.
HAR-04 deja una candidatura para revisión humana. G1 aún no es elegible.

El paquete `hermes_cli.agent_platform.harness` no tiene consumidores de producción.
No modifica enums, schemas, exports ni algoritmos TicketSpec/WorkPacket anteriores.
Los futuros adaptadores dependen del harness; el harness no importa adaptadores.
No contiene registry, executor, dispatch, evaluator, journal, reconciliación,
consentimiento ni intérprete de predicados. No hay requisito Git de completitud.

### Reutilización y estructura

Se inspeccionaron `workflow/governed_state_machine.py`, `work_packet/`,
`runtime_adapter/contracts.py`, `provider_worker/contracts.py`,
`ticket_factory/specs.py` y `tools/registry.py`. Sus vínculos de dominio, políticas,
handlers, imports y hashes no son contratos genéricos intercambiables.
Se reutilizan las convenciones Pydantic ya instaladas de inmutabilidad, campos
cerrados y versiones explícitas; no sus clases ni serializaciones especializadas.
Pydantic evita implementar otro parser de modelos, validación y errores tipados;
no se instala dependencia ni se cambia packaging. La búsqueda setuptools vigente
incluye `hermes_cli.*` y descubre el subpaquete nuevo sin alterar la configuración.

Grafo de imports directos comprobado por AST fuera de los tests:

- `harness/__init__.py` → `contracts`, `validation` (exports propios explícitos).
- `contracts.py` → `enum`, `typing`, `pydantic`.
- `validation.py` → `contracts`, `hashlib`, `hmac`, `json`, `typing`.

### Inventario y semántica

Todos los modelos públicos tienen `schema_version=1` y son inmutables mediante
las APIs validadas. El inventario de campos/tipos exactos se conserva en
`contract-inventory.json` de la evidencia HAR-04; el resumen siguiente distingue
identidades, observaciones y solicitudes sin introducir un permiso ejecutable.

| Modelo | Información |
|---|---|
| ContractRef | contract_id, version externa opaca |
| ContentRef | content_id, sha256 |
| ActorRef | actor_id, trust_model=trusted_local_operator |
| Scope | project_id, workflow_id, resource_ids explícitos |
| CapabilityDescriptor | capability, input_schema, output_schema, effect, required_authority_kinds, evidence_contract, execution_adapter, recovery_policy opcional |
| TransitionDescriptor | transition, source_requirement, capability, prerequisites, required_authority_kinds, effect, target_rule, failure_code, conflict_code, continuation_rule |
| StateDimension | definition, value, support SUPPORTED/UNKNOWN/UNSUPPORTED |
| WorkflowState | publication, execution, validation, review, completion, authority_currentness independientes |
| Continuation | continuation_id, scope, actor, kind, reason_code, policy, capability/decision_target según tipo |
| AuthorityReference | authority_id, kind, issuer, subject, scope, policy, record, dependencies, currentness, superseded_by |
| AdmissibilityDecision | decision_id, scope, actor, capability, transition, outcome, reason_code, policy, required_authority_kinds, current_authorities, expected_authority_version, prerequisites, effect, observational |
| ExecutionRequest | operation_id, capability, scope, actor, authorities, input, implementation, effect, admissibility_observation, expected_authority_version, idempotency_key, replay_ref |
| EvidenceReference | evidence_id, evidence_type, sha256, producer_operation_id, producer_capability, producer_actor, scope, input, storage_locator, integrity, retention |
| ExecutionResult | operation_id, capability, scope, actor, request, input, outcome, effect_status, reason_code, output, evidence, replay_ref |
| WorkflowProjection | projection_id, scope, actor, observed_authority_version, observed_state_version, state, continuations, pending_human_decisions, wait_conditions, safe_stops, diagnostics, observational |

Los efectos OBSERVE/COMPUTE/WRITE_ARTIFACT/EXTERNAL_WRITE/PHYSICAL_CONTROL son
clasificaciones independientes; una simulación no autoriza control físico.
Las continuaciones distinguen exactamente EXECUTABLE_CAPABILITY, HUMAN_DECISION,
OBSERVATION, EXTERNAL_REMEDIATION y SAFE_STOP. Solo una oferta ejecutable lleva
capability; solo HUMAN_DECISION lleva decision_target. Ninguna lleva handler.
Un ID `RESOLVE_*` permanece metadato opaco y no adquiere executor ni consentimiento.

### Versiones, transporte y límites

La versión de envelope admitida es el entero estricto 1 (no bool, float ni string).
Una ContractRef admite versión externa entera 1–65535 sin resolverla o afirmar su
soporte. StateDimension hace explícita esa incertidumbre. Campos desconocidos,
coerciones Python, callbacks, expresiones de código y campos requeridos ausentes
se rechazan. Identificadores: 1–128 caracteres ASCII alfanuméricos con `._:-`;
digests: exactamente 64 hex minúsculas. Locators: texto opaco de 1–512 caracteres,
sin controles; nunca se abren. Cada colección tiene máximo 32 elementos; Scope
requiere 1–32 recursos distintos. No hay campos recursivos ni dicts arbitrarios.

`parse_contract(tipo_confiable, JSON)` limita el transporte UTF-8 a 1 MiB y rechaza
claves duplicadas antes de validar. No carga código según nombres serializados.
Usar este helper es requisito para el límite de transporte; los métodos nativos
Pydantic no sustituyen ese límite. `canonical_json` revalida, ordena claves y usa
JSON compacto UTF-8; recursos se normalizan como conjunto ordenado, otras secuencias
conservan el orden declarado. Igualdad es estructural, sin timestamp aleatorio.
`sha256_bytes` y `verify_content_digest` solo reciben bytes suministrados: una
referencia bien formada no permite detectar contenido alterado sin esos bytes.
Un SHA coincidente no es firma, autenticación ni aprobación humana.

### Invariantes de autoridad y límites de garantía

AuthorityReference conserva issuer y subject separados y dependencias explícitas.
Superseded requiere successor; CURRENT es solo una afirmación de quien produce los
datos. Solicitudes y observaciones ALLOW rechazan referencias declaradas históricas,
no verificadas, conflictivas o superseded; ALLOW exige versión esperada y los kinds
requeridos. Esto detecta contradicciones locales, no evalúa políticas ni demuestra
vigencia. DENY/WAIT/SAFE_STOP pueden conservar observaciones históricas sin elevarlas.

Scope y actor coinciden exactamente entre envelope y sus referencias vinculadas;
ni un proyecto más amplio ni otro recurso heredan permiso. La proyección valida
kinds y ámbitos de continuaciones; pendiente humano no es aprobación. Descriptores,
proyecciones, decisiones y continuaciones no son AuthorityReference ni ExecutionRequest.
Construir una ExecutionRequest tampoco autoriza ejecución: un adaptador futuro debe
revalidar autoridad actual y versión esperada inmediatamente antes de los efectos.
La validez del contenido, issuer, versión externa, policy o claim CURRENT no se
resuelve aquí. No se ofrece autenticación remota ni aislamiento multiusuario.

UNKNOWN exige effect_status UNKNOWN; SUCCESS exige efectos confirmados y referencias
a output/evidence. DENIED exige NOT_APPLIED. FAILURE/CANCELLED pueden conservar
incertidumbre sobre efectos sin autorizar retry. La evidencia de un resultado debe
coincidir en operación, capability, input, actor y scope. Éxito no promueve review,
completitud, evidencia verificada ni autoridad. Replay es una referencia; no se ejecuta.

La inmutabilidad cubre la API normal validada. `model_construct`, `model_copy` sin
validación y manipulación hostil de objetos Python no son fronteras de confianza;
el transporte canónico revalida, pero el código Python en el proceso sigue siendo
confiable. Ninguno de estos modelos debe aceptarse como un token de autorización.

### Verificación y siguiente gate

Los tests nuevos HAR-04 ejercitan todos los modelos, round-trip, límites, errores,
invariantes y relaciones, sin leer texto de fuentes. El probe separado arranca un
intérprete `-I -B`, HOME temporal y origen de código comprobado. Intercepta imports
privados/provider/storage y audita escrituras, red y procesos antes de importar el
paquete. Canarios comprueban que esos controles fallan; mutaciones en copias
independientes añaden imports prohibidos y eliminan guards para probar sensibilidad.
Esta prueba cubre el import observado, no es un sandbox contra Python hostil ni
una afirmación sobre la pureza de todo Hermes. El inicializador ancestral conserva
su lógica UTF-8 histórica; el entorno comprobado usa UTF-8.

Resultados exactos, comandos, entorno, hashes y comparaciones padre/candidato están
en `har04_verification` y su evidencia externa. Las cuatro selecciones son explícitas,
no aceptación de toda la suite; usan archivos comprometidos en reconstrucciones
separadas, sin incluir C64/C80-R1 untracked. El wrapper permanece intacto; su
precompile opcional emite el aviso esperado de archivo sin `.git` y continúa.

HAR-05 requiere revisión y aceptación humana separadas de HAR-04 y Git humano.
HAR-05–HAR-09 podrán consumir estas referencias mediante adaptadores; HAR-07 hará
la evaluación real y HAR-12 el journal. G1 permanece abierto. No se activa el core,
no se inspecciona ni muta P18.9.13 vivo y no se ejecuta HAR-05, Graphify, Docker,
proveedores, deploy ni restart.


## 10. HAR-05 — Puerto de observación y fuentes explícitas sin inicialización

### Aceptación previa y dirección de dependencias

El ticket humano HAR-05 declara HAR-04 aceptado, committed/pushed y G0 CLOSED.
Padre verificado Windows/WSL: `3a3b10fda7f2c010b48a1b8da886ef6aa6f475f4`,
rama `p18-manual-to-hermes-workflow-migration`; índice y archivos rastreados limpios.
Los estados históricos HAR-00–HAR-04 se conservan; `har05_verification` registra
esta aceptación posterior. El roadmap HAR-05 coincide con este ámbito: observación
separada de inicialización/mantenimiento/reconciliación, versiones/frescura y
medición inicial; no migración simultánea de endpoints ni transacción global.

Se añaden solamente `harness/observation.py`, `observation_adapter.py` fuera del
núcleo y `tests/hermes_cli/test_har05_observation.py`. Los contratos, exports y
tests HAR-04 permanecen intactos. No hay consumidor/route nuevo ni activación.

- `harness.observation` → `harness.contracts`, enum, typing, Pydantic.
- `observation_adapter` → puertos/contratos puros, `evidence_sqlite` existente y
  stdlib (Path, SQLite, JSON, hashing, dataclass, regex).
- `evidence_sqlite` → stdlib; nunca runtime, registry o bootstrap.
- Ninguna arista desde el núcleo hacia SQLite, Kanban, runtime o herramientas.

### Contratos y puerto puro

Los modelos nuevos heredan versión de envelope 1, frozen/strict/extra=forbid y
transporte canónico HAR-04 sin cambiarlo. SourceRef contiene source_id, kind
(FACT/AUTHORITY/EVIDENCE) y format ContractRef. ObservationRequest contiene source,
scope, actor, expected_content opcional y hasta cuatro related_sources únicos.
ObservedRecord contiene record_id, content ContentRef y state opcional opaco.

Observation contiene source/scope/actor, status, reason_code, source_content,
observed_schema_version, records, authority opcional, integrity, structure, binding,
consistency, completeness, currentness y observational. Cada check distingue
UNVERIFIED/VERIFIED/FAILED; status distingue ABSENT/PRESENT/INVALID/CONFLICT/
UNSUPPORTED/UNSTABLE/UNAVAILABLE. PRESENT significa fuente estable observada;
no significa validación completa del dominio. Requiere contenido, scope vinculado,
STABLE_CAPTURE y BOUND_SOURCE_ONLY. Un fallo/ausencia no publica registros completos.
Las versiones desconocidas no se migran. No hay reloj o ID aleatorio en los hechos.

ObservationPort es un Protocol inyectable con observe_fact, observe_authority y
observe_related. No tiene inicialización, mantenimiento, dispatch, reparación o
método de ejecución. El puerto admite readers sintéticos sin arrancar el producto.
Los imports se hacen desde el módulo nuevo explícito; __init__/__all__ HAR-04
no se amplían. No hay registry ni framework de inyección.

### Adaptador y alcance de fuentes

BoundObservationReader recibe de un caller local confiable una tupla de hasta 16
SourceBinding inmutables. Cada binding registra request de identidad/scope/actor,
root absoluto, 1–8 componentes literales de ruta, record_format y task_id cuando
corresponda. No obtiene HOME desde entorno ni busca directorios, perfiles, tickets,
boards o autoridad adicional. Sin binding exacto se rechaza antes de abrir fuentes.
No se admiten componentes de escape, rutas absolutas embebidas ni symlinks en la
ruta o sus ancestros. El binding no equivale a autenticación del operador o ACL.

Formatos iniciales explícitos, versión externa 1:

| Formato | Lectura y calificación |
|---|---|
| harness-authority | AuthorityReference HAR-04 validada, actor sujeto y scope exactos; un claim CURRENT se devuelve UNVERIFIED en la observación; original sin reescribir |
| pepper-projection | Cabecera v1/policy pepper-workpacket-kanban-projection-v1, project/ticket/task vinculados; structure UNVERIFIED, sin validar ni recomputar todos los digests/dependencias históricos |
| json-evidence | JSON opaco v1 con project/workflow/resources/actor explícitos; structure UNVERIFIED, ningún ALLOW/consentimiento/callback contenido se interpreta |
| kanban-task | DB explícita y exactamente un task resource; body project/ticket/task coherente; runs solo de ese task con metadata ticket coincidente; status se conserva como hecho opaco |

Las referencias de contenido calculan SHA256 de bytes de archivo, o un digest
nuevo con framing de la captura SQLite DB/WAL/SHM/journal. No sustituyen hashes
TicketSpec/WorkPacket/projection/start históricos. VERIFIED en integrity exige un
expected_content suministrado que coincida; sin él el hash es identidad observada,
no integridad contrastada. structure VERIFIED se limita al formato HAR-04 que se
ha validado; binding VERIFIED cubre el scope/actor registrado y los campos de
vínculo inspeccionados, no una cadena de autoridad completa.

El resultado siempre tiene currentness UNVERIFIED. Referencias históricas o
superseded pueden conservar su clasificación negativa sin adquirir vigencia.
Ni presencia, hash, claims CURRENT/ALLOW, proyección START, aprobación textual ni
contadores demuestran permiso. La evidencia dependiente se solicita explícitamente,
sin recorrer relaciones: profundidad máxima uno, hasta cuatro fuentes hijas, cada
una con su propio binding. No se afirma consistencia transaccional entre fuentes.
HAR-07 y adaptadores futuros deben revalidar autoridad antes del efecto.

### SQLite, filesystem y límites

Se reutiliza `evidence_sqlite.connect` sin modificarlo: reconstruye DB/WAL en
memoria, valida frames/checksums/commits y deriva una imagen rollback query_only.
Nunca se abre la fuente mediante SQLite normal, URI mode=ro o fallback writable.
No se migra, checkpointa, limpia locks/journals, reap PID/run, agenda retry o
reconstruye autoridad. Journal no vacío, imagen corrupta o cambiante falla cerrada.
SHM no participa en reconstruir páginas: su corrupción no se repara ni impide
leer una imagen DB/WAL válida; sus bytes/existencia sí se conservan y vigilan.

Capturas externas comparan stamps (device/inode/size/mtime/ctime) y bytes antes y
después, incluyendo sidecars; drift conocido devuelve UNSTABLE. JSON usa lecturas
acotadas a 1 MiB, profundidad 16, objetos y claves únicas, sin NaN. DB/sidecar:
16 MiB por archivo para capturas externas, cuatro nombres fijos como máximo por
fuente SQLite. El helper compartido conserva su propio límite previo de 512 MiB;
si un writer hace crecer la fuente durante su lectura puede existir asignación
transitoria mayor que 16 MiB antes de rechazar deriva. No se promete un límite de
memoria contra crecimiento hostil ni timeout de I/O del sistema operativo.

Consultas fijas parametrizadas sobre tablas tasks/task_runs reales, sin SQL del
caller; authorizer rechaza otras acciones/tablas, longitud de columna máxima
1 MiB y presupuesto de 100000 pasos VM. Hasta 32 registros incluyendo task; un
exceso se rechaza completo, sin truncar y afirmar completitud. Tipos SQLite JSON
malformados producen INVALID. Metadatos ausentes/incoherentes no se adivinan.
Una captura estable detecta deriva observada, no prueba atomicidad global ni
inmutabilidad futura; atime del filesystem no forma parte de la garantía de bytes.

Medición sintética inicial: archivo JSON existente, dos opens rb; fuente con
DB/WAL/SHM, tres opens DB, tres WAL, dos SHM y una conexión :memory:, cero escaneos
de directorios. Journal ausente no se abre. Datos exactos: source-read-metrics.json.
Se prioriza coherencia y reutilización del decoder existente sobre optimizar estas
relecturas en HAR-05; no se crea cache ALLOW.

### Inventario de rutas heredadas y deuda explícita

read-path-inventory.json contiene entry point, propósito, storage, comportamiento,
efectos, ausencia, interpretación de autoridad, tratamiento y fuentes/líneas para
12 grupos. read-path-probes.json conserva auditoría/stacks de probes fríos
sintéticos; model-tools-import-probe.json separa importación de dispatch.

- Dashboard: build_workflow_control_snapshot → _execution_operational_summary →
  build_execution_collection_source → init_db/connect crea kanban.db e init.lock.
  El reconciler no scoped puede detectar workers caídos y reconciliar runs
  huérfanos. Lo primero se observó en frío; lo segundo está caracterizado por
  código y no se ejecutó contra workers vivos ni se declara medido globalmente.
- scoped_read_only_connections evita init/migration y salta ese reconciler. El
  dashboard frío bajo ese scope no produjo archivos en el caso probado. No cubre
  el bootstrap de otros callers ni habilita usar el dashboard como nuevo puerto.
- load_config y load_config_readonly comparten _load_config_impl → ensure_hermes_home:
  ambos crean skeleton/chmod y SOUL.md en frío. readonly significa evitar deepcopy,
  no ausencia de efectos persistentes. Crear perfiles también es inicialización
  explícita; no se llama desde el adaptador.
- Importar model_tools ya alcanza process_registry → restore_undelivered_completions
  → async_delegation._connect/recover_abandoned_delegations, creando state.db.
  Importar tools.approval carga allowlist/config y puede sembrar SOUL. Se observó
  también con un tool inexistente; ningún handler real se invocó. El probe bloqueó
  socket.__new__, introspección gethostname y preparación de /dev/null de una
  introspección platform/subprocess; no acredita llamadas externas realizadas.
- Tool Search config llama load_config; availability check_fn y discovery son
  callbacks con potencial I/O, no contratos puros. No se afirma que todas las
  herramientas o proveedores se hayan sondeado.
- Los loaders de generación/publicación/approval/projection/start/review y evidencia
  manual/comandos siguen conservando sus validadores y semántica histórica. Algunos
  read_text no están acotados y sus validadores recorren otras fuentes privadas;
  no se importan ni reutilizan como lectores generales dentro del nuevo límite.

No se cambia una entrada pública: separar bootstrap/recuperación y observation
necesita inventariar dependencia de callers y autorización propia. Se propone el
ámbito HAR-BOOTSTRAP-OBSERVATION-01 para imports/availability/config-state; catálogo
HAR-06 revisará descriptores/checks sin ejecutarlos, y HAR-09 calificará adaptadores
históricos completos. No se abre ni implementa automáticamente otro ticket.
La barrera HAR-03 de execution_authority_blocked/RESOLVE diagnóstico permanece.

### Verificación, preservación y gate

Tests nuevos ejercitan fuentes sintéticas reales, DB/WAL/SHM antes/después,
ausencia/corrupción/drift/errores/bounds y scope; un proceso fresco rechaza cualquier
conexión SQLite a disco, escritura, import privado/provider, red o proceso durante
la observación calificada. El módulo puro nuevo pasa el guard de importación HAR-04.
Mutaciones desechables comprueban sensibilidad al scope, deriva, conexión writable
e inicialización oculta. No se debilita ningún test o guard histórico.

El manifiesto añade solamente har05_verification; evidencia y estados previos se
conservan. Las selecciones canónicas comparan código histórico sin cambios en
archives aislados; los tests focalizados verifican los bytes finales nuevos.
No hay consumidor existente de esos módulos. No hay acceso/copia de autoridad viva
P18.9.13, Git mutador, Graphify, Docker, instalación, deploy/restart ni proveedor.
HAR-06 requiere revisión/aceptación humana separada de HAR-05. G1 sigue OPEN y no
es elegible para cierre; HAR-06 no se implementa aquí.


## 11. HAR-06 — Catálogo declarativo y correspondencia pasiva Hermes

### Alcance reformulado y autoridad humana

Padre Windows/WSL verificado: `b9a297690582882db68666b94e77b395f306aa0d`, rama
`p18-manual-to-hermes-workflow-migration`; índice y archivos rastreados limpios.
El ticket humano declara HAR-05 aceptado/commit/push y G0 cerrado. Los namespaces
y estados históricos permanecen intactos; HAR-06 no cierra G1 ni inicia HAR-07.

Se detectó que el ticket inicial excluía el binding mientras el roadmap HAR-06
exige descriptores pre-review/material revision y correspondencia con handlers.
El humano rechazó una excepción al roadmap y posteriormente **aprobó expresamente**
la reformulación: catálogo puro, descriptores concretos, correspondencia pasiva
fuera del núcleo, continuaciones reales y procedencia con resultados calificados.
La ampliación autoriza nuevos módulos bajo agent_platform; ningún módulo histórico
de ejecución/registro cambia. No se modifica el roadmap ni se difiere esta
correspondencia a HAR-09. human-scope-approval.txt y esta conversación conservan
la aprobación de alcance; no equivalen a aceptación del resultado HAR-06.

### Arquitectura y separación de responsabilidades

- `harness/catalog.py`: catálogo genérico puro; depende solo de contratos/validación
  HAR-04, enum/hashlib/typing/Pydantic. No contiene IDs Pepper ni imports de producto.
- `handler_correspondence.py`: adaptador de análisis estático de bytes explícitos;
  AST/stdlib y modelos HAR-04. No abre rutas ni importa el registro inspeccionado.
- `pre_review_catalog.py`: declaraciones del primer ámbito y plantillas tipadas;
  depende del catálogo puro y del adaptador pasivo. Nunca registra herramientas.
- Dos módulos nuevos de tests HAR-06; HAR-04/HAR-05 y sus exports intactos.

El registro Hermes existente sigue siendo el único propietario de handlers.
No se crea registry global, dispatcher, service locator, catálogo de herramientas
alternativo ni vínculo invocable de Python dentro del núcleo. Los nombres públicos
se conservan mediante HandlerDeclaration.tool_name; O01–O08/P01–P03 son IDs de
operaciones de la matriz AS-IS, no nombres de herramientas registrados nuevos.

| Etapa | HAR-06 |
|---|---|
| Declaración | Descriptor y versión exacta, consistencia y contenido de snapshot |
| Correspondencia | Referencia de herramienta/selector y símbolo de handler comprobados pasivamente contra fuente explícita |
| Disponibilidad | No comprobada; ningún check_fn, override dinámico, salud de proveedor o recursos |
| Admisibilidad | No evaluada; requiere hechos/actor/autoridad/política de HAR-07 |
| Ejecución | No realizada ni activada; requiere revalidación final y executor histórico |

### Catálogo y API pura

CatalogSnapshot contiene schema_version=1, catalog ContractRef, capabilities y
transitions canónicas HAR-04 y declaration_inputs ContentRef opcionales. No se crean
descriptores paralelos. Colecciones: hasta 64 capabilities, 128 transitions y 16
inputs de declaración; referencias internas de cada descriptor conservan límites
HAR-04 de 32. El catálogo vacío está explícitamente admitido.

Rechaza duplicados idénticos o contradictorios por identidad/versión, capability
no declarada de una transición, efecto diferente y autoridad de transición que
omita kinds requeridos por su capability. Varias versiones pueden coexistir; no
hay latest automático. Los namespaces capability/transition se resuelven por API
tipada. Solo transition.capability es una referencia que el catálogo promete
resolver. Schemas, policies, inspector/prerrequisitos, adapter, evidence y recovery
son referencias externas opacas, no implementaciones disponibles inferidas.

build_catalog construye y valida; list_capabilities/list_transitions devuelven
modelos inmutables; resolve_capability/resolve_transition exigen ContractRef exacta;
transitions_for lista coincidencias exactas y external_references explicita refs
no resueltas aquí. CatalogLookup distingue DECLARED/NOT_DECLARED/UNSUPPORTED_VERSION/
INVALID_REFERENCE/CATALOG_INCONSISTENCY. UNSUPPORTED_VERSION significa ID conocido
sin esa versión declarada en el snapshot, no incompatibilidad global del proveedor.
Un fallo no muta el snapshot ni produce descriptor, ALLOW o ExecutionRequest.

Entradas e inputs de declaración se ordenan canónicamente por identidad/versión;
las secuencias internas de descriptores conservan su orden HAR-04. Snapshot máximo
900000 bytes: CatalogDocument(snapshot, content) mantiene el transporte global
HAR-04 de 1 MiB, sin ampliarlo. Su digest SHA256 usa el prefijo nuevo
harness-catalog-snapshot-v1 y JSON canónico, excluyendo únicamente el campo derivado
de digest que está fuera del snapshot. deserialize_catalog comprueba ese digest.
No cambia ningún algoritmo histórico. Se revalidan objetos directamente antes de
serializar, evitando normalizar copias Pydantic no validadas en los límites nuevos.

### Descriptores concretos e integración del primer ámbito

ProductOperation agrupa descriptor HAR-04, transición, HandlerDeclaration, inspector,
policy e invalidation; recovery/evidence figuran también en el descriptor canónico.
Policy e inspector se incluyen como referencias de prerrequisitos. El snapshot
incorpora un ContentRef del contenido completo de las declaraciones de producto,
incluidos selectores y referencias de política, usando identidad nueva separada.
Cambiar esos metadatos cambia la identidad; cambiar una implementación externa
cambia la prueba de fuente, sin convertir el catálogo declarativo en identidad de
implementación ni permiso. Las reglas externas aún requieren resolución futura.

15 descriptores cubren la matriz aprobada de sección 4:

| Operaciones | Herramienta / selección |
|---|---|
| O01/O02 | prepare_current_ticket_review, inspect_commands / run_commands |
| O03.ticket_spec/O03.validation_steps | inspect_pending_approval_artifact_section, current_approved y section_id exacto |
| O04/O05 | request_current_ticket_material_revision, post_execution, inspect / request |
| O06/O07 | Mismo tool/origin, inspect_reconciliation / reconcile |
| O08 | revise_current_ticket_for_material_contract_failure |
| P01 | inspect_current_ticket_manual_validation |
| P02.passed/P02.failed | attest_current_ticket_manual_validation, status passed / failed |
| P03.workflow/P03.review/P03.prepare | get_workflow_control(blockers_only=true), get_review_status, prepare_current_ticket_review(operation=prepare) |

Las plantillas clasifican inspecciones como OBSERVATION; decisiones pendientes
como HUMAN_DECISION con decision_target; operaciones solicitadas como
EXECUTABLE_CAPABILITY solo con referencia y correspondencia comprobada. La
construcción de una continuación ejecutable exige volver a comprobar los bytes
explícitos suministrados, no confiar en un status de evidencia copiado. Esto sigue
siendo construcción de datos, no evaluación del consentimiento o del estado actual.
RESOLVE_EXECUTION_AUTHORITY se clasifica SAFE_STOP y RESOLVE_REVIEW_BLOCKER como
EXTERNAL_REMEDIATION: familias diagnósticas sin binding invocable. Son plantillas,
no sustituciones ni nuevos IDs de dispatch de las acciones legadas por ticket.
Los templates no se seleccionan automáticamente desde el workflow vivo.

### Correspondencia estática y calificación de evidencia

inspect_correspondence recibe bytes y HandlerDeclaration explícitos, sin discovery,
rutas, eval/exec/import dinámico ni ejecución del código fuente. Límites: 2 MiB,
100000 nodos AST, hasta ocho selectores y ocho enlaces de asignación de schemas.
Verifica registro top-level único, propietario declarado tools.registry.registry,
símbolo de handler local/único/no decorado/definido antes del registro, ausencia de
reasignaciones/imports ambiguos y selectores literales enum/const/boolean cuando
se han declarado. No evalúa predicados, cuerpos ni expresiones de creación de schemas.

BindingEvidence contiene declaración, status, reason_code, ContentRef de fuente,
líneas de import del registro/registro/handler y SHA256 AST del registro y handler.
Estados: VERIFIED, ABSENT, AMBIGUOUS, CONTRADICTORY, UNVERIFIABLE. VERIFIED acredita
correspondencia declarada en esa fuente, no el contenido de un registry ya cargado,
importabilidad, disponibilidad, ABI ejecutable ni corrección de control de flujo.
Las comprobaciones de selectores son de pertenencia de propiedades, no validación
completa de oneOf ni demostración de cada ruta del handler. Sin selectores el
schema puede seguir opaco, como el schema construido de O08; no se evalúa para
obtener una falsa validación completa. Las combinaciones del primer ámbito se
corresponden con la matriz AS-IS y conservan los guards históricos comprobados.

Se verificaron las 15 correspondencias contra bytes de fuente del archive aceptado
y contra Windows. Los SHA raw pueden distinguir CRLF; sus huellas AST coinciden.
final-product-correspondence.json registra ambas procedencias y todos los resultados.
No se importó tools.registry, pepper_workflow_tools o model_tools para descubrirlas.
No se ejecutaron availability callbacks, handlers, comandos o workflow vivo.

### Verificación y límites

registry-investigation.json inventaría diez representaciones: identidad, versión,
metadata/implementación, schemas, efectos, autoridad, disponibilidad, registro,
executor, efectos laterales y reutilización. Hallazgos estáticos se distinguen de
la evidencia dinámica histórica HAR-05; no se repite bootstrap para descubrir tools.
get_definitions y discover_builtin_tools permanecen excluidos: ejecutan callbacks
u otras importaciones. get_entry/get_schema pasivos existentes no se invocan aquí.

Tests HAR-06 verifican modelos públicos, versiones/digests, referencias, monotonía
de autoridad, límites reales de bytes, no ejecución de fuente/callbacks, pruebas
negativas del propietario y procedencia y continuaciones sin concesión de autoridad.
Un intérprete nuevo importa y opera catálogo/adaptadores bajo guard de imports y
auditoría de escrituras/SQLite/red/procesos. Mutaciones en copias desechables prueban
fallos por imports privados/storage/registry/provider/adaptador HAR-05 y eliminación
de guards de efecto, autoridad o selector; nunca se muta el candidato para ello.
Resultados y comparaciones canónicas constan en har06_verification y evidencia externa.

El catálogo prueba declaraciones, no verdad externa ni vigencia de autoridad. Los
hashes no son firmas o aprobación. Las referencias externas no resueltas no se
convierten en disponibilidad. No hay cache ALLOW, evaluación HAR-07, journal,
recuperación, migración de consumidores, activación, aprobación ni ejecución.
Se preservan contratos/exports HAR-04, puerto/adaptador HAR-05, C26 y C91–C94,
roadmap, entradas HAR originales, C64/C80-R1 y PNGs. Git sigue humano; P18.9.13
permanece congelado sin lectura/copia de autoridad viva. HAR-07 requiere aceptación
humana separada; G1 sigue abierto y no elegible para cierre.
