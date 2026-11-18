# Architecture

```text
Upload -> validation -> face detection -> quality -> preprocessing -> LBP/HOG/GLCM
                                      -> approved artifact (future) -> classification
Audit metadata -> Dataset Explorer
Annotation inventory -> review history -> approved-only manifest -> leakage-safe splits
```

Streamlit is the presentation layer; `src/morphguard` contains preprocessing, features, models, training, evaluation and inference safeguards. Raw datasets are never required by the inference container.
