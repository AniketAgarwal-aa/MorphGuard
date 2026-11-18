# Implementation review

Reviewed 2026-11-18. The existing implementation was retained and extended rather than rebuilt. Core strengths are streaming path discovery, explicit MONOT/ONOT-only scope, protocol-neutral labels for ambiguous folders, grouped split support, lazy face preprocessing, and separate inference/model modules.

Known issues requiring the local environment: the host system Python is protected and did not successfully install the declared dependencies; create `.venv` and install there. The full audit was not completed in this tool session because scanning the raw dataset exceeded the execution window. No fabricated counts or metrics are present. `--resume` is accepted by the audit CLI, while generated CSVs are replaced atomically on a new run; a future production run should add row-level checkpointing for interrupted scans.

Deployment files now separate inference dependencies, support `MORPHGUARD_ROOT`/`MORPHGUARD_MODEL_DIR`, avoid copying raw datasets into Docker, run as a non-root user, and expose readiness information in the Streamlit sidebar.

The project-local `.venv` now installs the CPU inference set successfully. Pytest passes 3/3, Streamlit startup was smoke-tested, and a Docker build was attempted but blocked by the unavailable Docker Desktop engine.
