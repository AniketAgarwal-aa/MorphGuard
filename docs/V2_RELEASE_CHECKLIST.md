# MorphGuard V2 Showcase Checklist

- [x] 500-record feature cache retained and validated.
- [x] 150-record annotation pilot retained; zero approvals.
- [x] Evidence package and contact sheets generated.
- [x] Face Analysis supports upload, detection, quality, features and JSON report.
- [x] Dataset Explorer exposes audit and processing coverage.
- [x] Model Insights exposes actual cached-feature PCA as exploratory only.
- [x] Experiments page distinguishes exploratory processing from blocked supervised experiments.
- [x] 17 automated tests pass; compilation and Streamlit health pass.
- [ ] Human review of pilot evidence.
- [ ] Approved labels, leakage-safe split and validated detector.

Launch with `streamlit run app/main.py`. Present image quality and feature outputs as analysis evidence, never as morph probabilities.
