# MorphGuard V3.2 — UI/UX Redesign & Navigation Report

**Project:** MorphGuard — Facial Morph Attack Detection System  
**Date:** November 19, 2026  
**Auditor:** MorphGuard Design & Engineering  
**Application Entrypoint:** `app/main.py`  

---

## 1. Executive Summary

MorphGuard's user interface was systematically upgraded from a research-prototype aesthetic to a polished, modern, product-grade biometric analysis application. The primary focus of this redesign was the **complete overhaul of the sidebar navigation system**, eliminating an unorganized two-bucket list and establishing a structured, intuitive 6-group information architecture that guides the user naturally through Analysis, Benchmarks, Data Methodology, Documentation, and Governance.

---

## 2. Before-and-After Observations

### 2.1 Navigation & Sidebar Architecture

| Dimension | Before Redesign | After V3.2 Redesign | Usability Impact |
| :--- | :--- | :--- | :--- |
| **Section Grouping** | Only 2 generic buckets: `MAIN PROJECT` (7 pages) & `ABOUT PROJECT` (7 pages) | **6 functional groups:**<br>1. OVERVIEW<br>2. ANALYSIS<br>3. MODELS & BENCHMARKS<br>4. DATA & METHODOLOGY<br>5. DOCUMENTATION<br>6. GOVERNANCE & REVIEW | Users instantly find relevant tools without scrolling through an undifferentiated list. |
| **Visual Hierarchy** | Flat links with mixed icon semantics | Uppercase category headers, consistent Material 3 biometric & security icons, clear active page indicators | Clean visual hierarchy matching professional enterprise tools. |
| **System Status & Version** | Displayed outdated "v1.0.0 · MONOT/ONOT Corpora" | Updated to "MORPHGUARD V3.2 · Local Research Pipeline (46,792 Images · 21 Calibrated Models)" | Communicates current verified capabilities and build status. |
| **Theme Controls** | Generic radio buttons at the bottom | Polished Dark / Light mode toggle integrated with consistent CSS accent variables (`#35d1c4` dark, `#0284c7` light) | Responsive, high-contrast, theme-aware rendering across all 14 pages. |

### 2.2 Page Hierarchy Mapping (14 Pages)

```text
OVERVIEW
├── Executive Dashboard      (pages/overview.py)
└── About MorphGuard         (pages/about.py)

ANALYSIS
└── Face Morph Analysis      (pages/1_Face_Morph_Analysis.py)

MODELS & BENCHMARKS
├── Model Benchmark          (pages/2_Model_Comparison.py)
├── Model Insights           (pages/3_Explainability.py)
└── Research Experiments     (pages/5_Research_Experiments.py)

DATA & METHODOLOGY
├── Dataset Explorer         (pages/4_Dataset_Explorer.py)
├── Detection Methodology    (pages/6_Methodology.py)
└── System Architecture      (pages/how_it_works.py)

DOCUMENTATION
├── Technology Deep Dive     (pages/models_technology.py)
├── Technical Documentation  (pages/technical_documentation.py)
└── Limitations & Privacy    (pages/7_Limitations_And_Info.py)

GOVERNANCE & REVIEW
├── Annotation Review        (pages/annotation_review.py)
└── Dataset Governance       (pages/datasets.py)
```

---

## 3. Key Page Redesigns

### 3.1 Executive Dashboard (`app/pages/overview.py`)
- **Before:** Contained outdated placeholder text claiming "Morphing classification will be enabled when an approved detection model is available" and listed trained models as "Pending approval / development".
- **After:** Modern executive dashboard featuring:
  - **4 Top KPI Cards:** 46,792 Audited Images (100% cached), 21 Trained Models, 96.49% Top Test Accuracy (Combined SVM), 91.58% Top Deep Accuracy (EfficientNet-B0).
  - **Hero CTA:** Quick-launch buttons to open Face Morph Analysis, Model Benchmarks, or Dataset Explorer directly.
  - **Interactive Workflow Diagram:** Visual SVG/CSS flow depicting Image Ingestion $\to$ Face Localization & Align $\to$ Multi-Scale Texture (6,103D) $\to$ Calibrated Threshold ($\tau^*$) $\to$ Authoritative Binary Decision.
  - **Top Performing Benchmark Snapshot:** Clean table showing test accuracy, calibrated ACER, ROC-AUC, and status.

### 3.2 Face Morph Analysis (`app/pages/1_Face_Morph_Analysis.py`)
- **Model Selection:** Sidebar model dropdown ordered logically by verified test accuracy, placing top classical performers (`combined_svm`, `hog_svm`, `logistic_regression`, `hist_gradient_boosting`) and top deep vision architectures (`efficientnet_b0`, `voting_ensemble`, `custom_cnn`) first.
- **Section D 4-Metric Diagnostic Grid:**
  1. Morph-Class Probability ($P(\text{morphed})$)
  2. Verified Decision Threshold ($\tau^*$)
  3. Active Detection Model
  4. Inference Status (`SUCCESS`)
- **Clear Binary Classification:**
  - $P(\text{morphed}) \ge \tau^* \implies$ Bold Red **MORPH ATTACK DETECTED** banner.
  - $P(\text{morphed}) < \tau^* \implies$ Bold Green **AUTHENTIC / GENUINE** banner.
- **Two-Image Feature Comparison:** Side-by-side card layout with HOG, LBP, and GLCM cosine similarities and radar chart representation.

### 3.3 Model Benchmark Comparison (`app/pages/2_Model_Comparison.py`)
- Live benchmark data dynamically loaded from `models/metadata/model_registry.json`.
- Accurately reports metrics derived from the 285 held-out test split with zero identity leakage and validation-calibrated thresholds.

---

## 4. Design System & CSS Components

- **Color Palette:**
  - Dark Mode: Background `#071521` with radial gradient, Card backgrounds `rgba(18,48,74,0.72)`, Primary Accent `#35d1c4`, Warning `#ffd27b`, Danger `#ff9ca9`.
  - Light Mode: Background `#f8fafc`, Card backgrounds `#ffffff`, Primary Accent `#0284c7`, Warning `#b45309`, Danger `#b91c1c`.
- **Component Primitives:**
  - `page_header(eyebrow, title, subtitle)`
  - `metric_card(label, value, hint, tone)`
  - `status_badge(text, tone)`
  - `section_title(title, caption)`
  - `render_sidebar_controls()`
  - `footer()`

---

## 5. Verification & Responsive Testing

- Headless page rendering verified across all 14 pages using `scripts/test_all_pages.py`: **14 / 14 passed (100%)**.
- Desktop, tablet, and mobile viewport responsive behavior confirmed; no horizontal table overflow or clipped text.
- Memory consumption remains well within the 8 GB host memory envelope.
