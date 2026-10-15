# HAR — Decisiones arquitectónicas y contrato del primer ámbito

Fecha de preparación: 2026-10-15 (Europe/Madrid). Ticket: **HAR-00**.
Estado: **PROPOSED — READY FOR HUMAN REVIEW**. Propietario de las decisiones: Pablo.

Este documento es el propietario canónico de las decisiones HAR. El
[roadmap](harness_refactor_roadmap.md) conserva el backlog y sus gates; el
[manifiesto](harness_refactor_verification_manifest.json) contiene las selecciones
comprobadas y deuda histórica. Los documentos de `HAR/` son entradas humanas
preservadas, no un segundo catálogo de decisiones vigentes.

## 1. Autoridad, alcance y baseline

El ticket humano fija la dirección B (contratos declarativos) mediante A
(adaptación incremental), con C limitado (coordinación durable). No autoriza una
reescritura, event sourcing completo ni la aceptación unilateral de D01–D10.
Todas las decisiones de este documento siguen **PROPOSED**, sin aprobación
registrada. HAR-01 y posteriores requieren su ticket completo y revisión humana.

Baseline canónico inspeccionado: rama
`p18-manual-to-hermes-workflow-migration`, HEAD
`64debea2b3ae184b95c4eeb4cb1d9b58938c9aec`, asunto
`P18.9.13-C94 Reconcile material revision authority`. Índice y archivos rastreados
sin cambios al comenzar. La comparación de cada ticket posterior usará su padre
aceptado; este SHA no se convierte en baseline permanente de HAR.

WSL fue inspeccionado de nuevo, mediante Git read-only, el 2026-10-15:
`/home/pablo/work/AGENT-PLATFORM` continúa en
`75185e79e46424e7f495dfaad59ebdde7f45db93`, en la misma rama, con candidatos C94
sin commit y sin el objeto del HEAD canónico. Estado:
**HUMAN_SYNC_REQUIRED_BEFORE_HAR01_VERIFICATION**. Se puede completar HAR-00 desde
Windows. No se sincroniza WSL ni se valida ejecución contra su fuente atrasada.

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

**Estado:** PROPOSED. **Propietario/aprobador:** Pablo. **Aprobación:** pendiente.

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

**Estado:** PROPOSED. **Propietario/aprobador:** Pablo. **Aprobación:** pendiente.

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

**Estado:** PROPOSED. **Propietario/aprobador:** Pablo. **Aprobación:** pendiente.

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

**Estado:** PROPOSED. **Propietario/aprobador:** Pablo. **Aprobación:** pendiente.

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

**Estado:** PROPOSED. **Propietario/aprobador:** Pablo. **Aprobación:** pendiente.

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

**Estado:** PROPOSED. **Propietario/aprobador:** Pablo. **Aprobación:** pendiente.

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

**Estado:** PROPOSED. **Propietario/aprobador:** Pablo. **Aprobación:** pendiente.

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

**Estado:** PROPOSED. **Propietario/aprobador:** Pablo. **Aprobación:** pendiente.

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

**Estado:** PROPOSED. **Propietario/aprobador:** Pablo. **Aprobación:** pendiente.

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

**Recomendación pendiente:** alternativa 2 como política conceptual. Definir en
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

**Estado:** PROPOSED. **Propietario/aprobador:** Pablo. **Aprobación:** pendiente.

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

## 6. Checklist de decisión del propietario

Revisar D01–D10 registrando para cada una aceptada/rechazada/alternativa y alcance,
sin interpretar silencio como aceptación. Son especialmente bloqueantes:
ubicación y dirección de dependencias (HAR-04), política pública HAR-02/C26
(HAR-02/03), trust/concurrencia (HAR-04/12) y garantías durables (HAR-12/13).
HAR-01 puede preparar su corte de fixtures solo tras revisión HAR-00 y
sincronización humana del checkout de verificación; jamás relajando guards.

Resultado documental: las propuestas y los gaps quedan concretos para revisar;
no se declara verde el baseline ni implementado el arnés TO-BE.
