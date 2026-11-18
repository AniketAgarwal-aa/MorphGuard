# Limitations

- Dataset category names are not automatically converted into ground truth.
- A classifier trained with genuine samples from ONOT and attacks from MONOT may learn source characteristics rather than morph artifacts.
- Haar-cascade face detection is a local conservative baseline and can fail on pose, occlusion, or low-quality images.
- No experimental metrics are created until a labelled protocol is explicitly established and models complete training.
- The user reports a successful Docker build and container startup; repeat verification depends on Docker Desktop's `desktop-linux` engine being available to the current session.
- Public hosting requires an explicit privacy, licensing, authentication, and HTTPS review because uploads are sensitive biometric data.
