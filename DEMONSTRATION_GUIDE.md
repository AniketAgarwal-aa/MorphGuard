# MorphGuard — Demonstration & Evaluation Walkthrough Guide

This guide provides a structured, professional demonstration workflow for academic and technical project evaluations.

---

## 1. Launching the Application

On Windows PowerShell:
```powershell
cd "C:\Users\admin\Downloads\Code\MorphGuard"
.\.venv\Scripts\Activate.ps1
$env:PYTHONPATH = "src"
streamlit run app\main.py
```
Open your browser at `http://localhost:8501`.

---

## 2. Redesigned Sidebar & Theme System Walkthrough

1. **Collapsible Navigation Groups:**
   - **MAIN PROJECT (Operational Tools):** Overview, Face Analysis, Dataset Explorer, Annotation Review, Model Comparison, Model Insights, Experiments.
   - **ABOUT PROJECT (Research Governance):** About MorphGuard, How It Works, Datasets, Models & Technology, Methodology, Limitations & Privacy, Technical Documentation.
   - Click the section headers or chevron buttons to collapse or expand each group. The active page remains loaded and accessible.

2. **Application Theme System:**
   - Locate the **Application Theme** radio toggle in the sidebar footer.
   - Toggle between **Dark Mode** (biometric navy `#08121f` with cyan `#35d1c4` accents) and **Light Mode** (clean slate `#f8fafc` with deep blue `#0284c7` accents).
   - Observe how metric cards, charts, data tables, and input components adapt instantly across the entire application.

3. **Sidebar Footer Controls:**
   - Demonstrates project branding, version `v1.0.0 Research Edition`, and the pulsing `● In-Process Research Mode` system status indicator.

---

## 3. Face Analysis Walkthrough (Primary Showcase)

Navigate to **Face Analysis** in the sidebar.

### A. Single Image Analysis (Tab 1)
1. **Quick Sample Loading:**
   - Use the sidebar dropdown **Load pre-packaged sample** and select `Sample A: Genuine candidate (MONOT Gate_10)` or upload your own JPG/PNG.
2. **Section A — Image Previews & Face Localization:**
   - View the original image with dimensions and size metadata.
   - Observe the primary face detected and framed with a bounding box (OpenCV Haar Cascade).
   - View the normalized 224×224 RGB aligned face crop.
   - Expand `▾ Image Details & Geometry Specifications` to see exact coordinates and aspect ratio.
3. **Section B — Quality Assessment & Analysis Summary:**
   - Metric cards display: **Faces Detected (1)**, **Processing Time (~0.2s)**, **Sharpness (Laplacian Blur Variance)**, **Brightness (Mean Luminance)**, and **Contrast (Luminance Std Dev)**.
   - Clear quality badge: `SUITABLE` (or `WARNING` if blurred/underexposed).
   - Expand `▾ Quality Metrics & Threshold Explanations` for threshold logic.
4. **Section C — Multi-Scale Feature Extraction:**
   - Total extracted feature vector: **6,103 dimensions**.
   - Expand `▾ 1. Local Binary Patterns (LBP)` to inspect the 10-bin micro-texture histogram bar chart.
   - Expand `▾ 2. Histogram of Oriented Gradients (HOG)` to see 6,084 structural edge gradients and L2 vector norm.
   - Expand `▾ 3. Gray-Level Co-Occurrence Matrix (GLCM)` to see Contrast, Dissimilarity, Homogeneity, Energy, and Correlation.
   - Expand `▾ 4. Statistical Descriptors` and `▾ 5. Combined Feature Vector Summary`.
5. **Section D — Model Status & Research Safeguard:**
   - Prominently displays: `STATUS: MODEL UNAVAILABLE`.
   - Explains that feature extraction succeeded, but no validated morph classifier is installed.
   - Optional: enable `illustrative demonstration mode` in sidebar to demonstrate the isolated `DEMO PATTERN A/B` output without compromising research integrity.
6. **Section E — Reports & Audit Export:**
   - Click `📥 Download Analysis Report (JSON)` to export a complete, machine-readable JSON report.
   - Expand `▾ Technical JSON Payload` to review embedded metadata.

### B. Original-versus-Morphed Comparison (Tab 2)
1. Switch to **Original-versus-Morphed Comparison**.
2. Click **Load Sample A (Gate_10 Genuine)** and **Load Sample B (MONOT Morphed)** (or upload two images).
3. **Side-by-Side Visual Inspection:**
   - Inspect Image A (Original) and Image B (Morphed) side by side with their respective bounding boxes and face crops.
4. **Parameter Comparison Table:**
   - Direct side-by-side comparison of dimensions, detected face counts, brightness, contrast, sharpness, and feature dimensions.
   - Highlights the sharpness delta: morphed images exhibit lower Laplacian variance due to blending/interpolation smoothing.
5. **Feature Differences & Cosine Similarities:**
   - Expand the difference table to view cosine similarities and mean/max absolute differences across LBP, HOG, GLCM, and combined representations.
6. **Visual Comparisons:**
   - Inspect side-by-side comparative bar charts for LBP micro-texture histograms and GLCM spatial properties.
7. **Report Download:**
   - Download the differential comparison JSON report.

---

## 4. Dataset Explorer Walkthrough

Navigate to **Dataset Explorer**.
1. **Audited Inventory:**
   - Verified totals: **46,792 total images** (MONOT: 24,140; ONOT: 22,652; 0 corrupted).
2. **Category Distribution:**
   - Bar chart and filterable table displaying `Gate_10`, `Gate_25`, `Morphed`, `digital`, and `print-scan`.
   - Filter by dataset or category and download filtered CSV summaries.
3. **Feature Cache Coverage:**
   - Verifies the 500-sample resumable feature cache (`data/cache/image_features`).
4. **Sample Previews:**
   - Expand inventory tables to inspect raw sample metadata.

---

## 5. Model Insights & Exploratory PCA Walkthrough

Navigate to **Model Insights**.
1. **PCA 2D Feature Decomposition:**
   - Primary 2D scatter plot decomposing the 6,103-dimensional space from cached feature shards.
   - Displays variance explained: PC 1 (~31.8%), PC 2 (~17.2%), Total (~49.0%).
   - Transparent legend: `ONOT (acquisition)` vs `MONOT (strata/morph)`.
   - Emphasizes that PCA visualizes data origin clustering, not classifier separation.
2. **Feature Distributions:**
   - Expandable comparative histograms across LBP, GLCM, and pixel statistics.

---

## 6. Annotation Review Walkthrough

Navigate to **Annotation Review**.
1. Switch scope to **150-record evidence pilot**.
2. Inspect individual records, subject IDs, morph pair IDs, and existing preprocessing metrics.
3. Observe provenance safeguards: records flagged with `INSUFFICIENT_PROVENANCE` cannot be approved without verified external documentation.
4. Explains immutable history, `.bak` backups, and atomic writes.

---

## 7. Model Comparison Walkthrough

Navigate to **Model Comparison**.
1. Registry of **7 implemented architectures**:
   - Deep Learning: Custom CNN, ResNet-18, EfficientNet-B0 (PyTorch).
   - Classical ML: LBP + SVM, HOG + SVM, GLCM + RF, Combined + SVM (scikit-learn).
2. All architectures report: `Untrained (awaiting labels)` and `Evaluation unavailable`.
3. Outlines the target ISO/IEC 30107-3 evaluation metrics (APCER, BPCER, ACER, EER).

---

## 8. Governance & Documentation Pages

- **Overview:** Executive summary, pipeline ASCII flow, at-a-glance metrics.
- **About MorphGuard:** Problem statement, attack vectors, in-scope vs out-of-scope boundaries.
- **How It Works:** 7-stage technical workflow.
- **Datasets:** Deep dive into MONOT and ONOT characteristics and source confounding.
- **Methodology:** Complete scientific protocol and identity-leakage prevention.
- **Limitations & Privacy:** Current constraints, Haar detector boundaries, non-commercial licensing.
- **Technical Documentation:** Embedded source reports, directory structure, and running instructions.

---

## 9. Key Viva / Defense Points

1. **Why is the model status `MODEL UNAVAILABLE`?**
   - *Defense:* In high-stakes biometrics, reporting synthetic predictions or training on unverified folder names creates false confidence. MorphGuard provides a fully working image processing and feature extraction pipeline while maintaining strict research integrity until human-reviewed ground-truth labels are approved.
2. **How does MorphGuard prevent data leakage?**
   - *Defense:* Cross-validation splits must be grouped by subject ID and morph-pair ID. No person's images can appear in both training and test partitions.
3. **What is the significance of the 6,103-dimensional feature vector?**
   - *Defense:* It fuses micro-texture (LBP, 10 dims), structural edge contours (HOG, 6084 dims), spatial gray-level co-occurrence (GLCM, 5 dims), and statistical moments (4 dims), capturing both local interpolation seams and global facial geometry.
