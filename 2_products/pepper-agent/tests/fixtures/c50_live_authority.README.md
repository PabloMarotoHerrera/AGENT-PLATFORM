# C50 durable authority regression

Captured read-only from `/home/pablo/.pepper-hermes` with repository HEAD
`7169c70ef7e4620ae9b0ba13c6e7067edd4e81a8` on 2026-09-26.

`c50_live_authority.json.gz` is a gzip-compressed JSON map from relative file
paths to their exact UTF-8 contents. `manifest.json` records the SHA-256 of each
of the 81 source files. Tests verify those hashes before restoring the records
under a temporary `HERMES_HOME`. The fixture contains Pepper workflow authority
JSON/JSONL only; it excludes credentials, profiles, sessions, and databases.

Material characteristics retained:

- Generated tickets P18.9.0 through P18.9.5, with their approval decisions.
- Bootstrap and successor projections, including P18.9.5's R0005 projection.
- Rejected-successor and material-revision histories, including the approved
  R0005 → rejected R0006 → corrected, approved R0007 lineage.
- Execution-start, review, recovery, governed-autonomy and human-handoff evidence.
- Earlier predecessor completion evidence and reconciliation records.

The original selectors return P18.9.5 R0007, approved, with TicketSpec SHA
`5e4d7d1b474dc2f7efb4d5849766a2ce85fe8e7a45161ad8e75091cb43153eee`
and WorkPacket SHA
`a5612bf5fa0d645d041ec7a801d4b4512d1930d1e9639a517ffdaaaf09229f31`.
The existing P18.9.5 projection instead binds R0005. This distinction is missing
from the earlier synthetic C49 fixture, which has no current-ticket projection.

Before the fix, the loader test raises exactly:

```
WorkPacketKanbanProjectionConflict: projection ticket_spec_SHA256 mismatch
```

The independent snapshot test also fails because
`kanban_projection_authority.ticket_id == "P18.9.0"` while
`current_ticket_id == "P18.9.5"`.

There is no demonstrated switch of the preparation target to bootstrap:
C (approved selector), D (wrapper overlay), E (resolver), F (generation), and G
(projection lookup target) all use P18.9.5. G reads the obsolete R0005 mapping.
Separately, the snapshot's shallow overlay retains bootstrap projection metadata
when the current generation has no valid current projection.

Tests exercise the real registered preparation tool with these records and a
fresh temporary Kanban database/profile. All subprocesses, execution starts and
worker dispatch are prohibited. A new R0007 projection must preserve generation
identity, the previous projection must remain historically readable, and
bootstrap bytes must remain unchanged. No live preparation action was called.
