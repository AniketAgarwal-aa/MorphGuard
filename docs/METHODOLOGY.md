# Methodology

The pipeline validates paths incrementally, detects a largest face with OpenCV, produces a quality warning independently of class prediction, and uses the same crop/resize route for inference. Feature extraction creates LBP, HOG, GLCM and statistical vectors in small NPZ shards. Conventional models and PyTorch model definitions are separate, with checkpoints intended per epoch in extended training runs.

Positive class is `morphed`; threshold selection belongs on validation data only. Accuracy, precision, recall, specificity, F1, ROC-AUC, and PR-AUC are calculated only after a test evaluation.
