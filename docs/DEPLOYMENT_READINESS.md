# Deployment readiness

## Architecture

`app/` is the presentation layer; `src/morphguard/inference` owns inference; `src/morphguard/preprocessing` owns image preparation; training scripts and raw data remain outside the runtime package. The runtime loads an explicit model artifact and never starts training.

## Configuration

Copy `.env.example` to a local `.env` (never commit it). `MORPHGUARD_ROOT`, `MORPHGUARD_MODEL_DIR`, `MORPHGUARD_MODEL`, `MORPHGUARD_LOG_LEVEL`, and upload/Streamlit settings are configurable. No secret is required for local inference.

## Docker

`Dockerfile` uses Python 3.10 CPU runtime dependencies, excludes MONOT/ONOT through `.dockerignore`, packages only safe audit summaries, runs as `appuser`, creates empty runtime model directories, and starts Streamlit on port 8501. The user reports a successful image build and container startup; this session could not independently re-verify because the Docker Desktop Linux engine pipe returned access denied. Model artifacts should be mounted or copied into `models/trained/` in the deployment packaging step.

## Runtime requirements

The deployment package needs a selected serialized model, its preprocessing metadata, roughly 1–2 GB RAM for CPU inference, and ephemeral storage only for the application. Large raw datasets are not required at runtime. Uploads should remain in memory and be capped by `MORPHGUARD_MAX_UPLOAD_MB`.

## Readiness checklist

- [ ] Create and validate a trained model artifact.
- [ ] Record model/preprocessing version metadata.
- [ ] Build and smoke-test the Docker image.
- [ ] Configure HTTPS and platform access controls.
- [ ] Load-test CPU/RAM and upload limits.
- [ ] Confirm dataset licensing and privacy review.

Deployment has not been performed.

The inference dependency now uses `opencv-python-headless` so Linux containers do not require GUI libraries such as `libGL.so.1`. The Streamlit frontend uses shared components and cached audit loading; it does not rescan raw datasets on page navigation.
