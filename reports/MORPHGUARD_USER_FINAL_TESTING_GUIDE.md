# MorphGuard V3.2 — User Final Testing & Acceptance Guide

This manual testing guide is designed for the project owner to independently inspect, test, and verify the live **MorphGuard V3.2** application and its public model artifacts in a single testing session.

---

## 1. Authoritative System Endpoints

| Platform / Service | Canonical URL | Intended State |
| :--- | :--- | :---: |
| **Live Web Application** | [https://morphguard.streamlit.app/](https://morphguard.streamlit.app/) | **LIVE & OPERATIONAL** |
| **Hugging Face Model Hub** | [https://huggingface.co/AniketAgarwal-aa/MorphGuard-Models](https://huggingface.co/AniketAgarwal-aa/MorphGuard-Models) | **PUBLIC (21 Models)** |
| **GitHub Source Repository** | [https://github.com/AniketAgarwal-aa/MorphGuard](https://github.com/AniketAgarwal-aa/MorphGuard) | **v3.2 Published** |

---

## 2. Quick-Start User Testing Checklist (15-Minute Session)

Follow these concrete steps to test the application:

### Step 1: Open the Application & Check Sidebar Navigation
1. Navigate to [https://morphguard.streamlit.app/](https://morphguard.streamlit.app/) in your browser.
2. Verify the 6 sidebar navigation categories and 14 functional pages are rendered:
   - **OVERVIEW:** `Executive Dashboard`, `About MorphGuard`.
   - **ANALYSIS:** `Face Morph Analysis`.
   - **MODELS & BENCHMARKS:** `Model Benchmark`, `Model Insights`, `Research Experiments`.
   - **DATA & METHODOLOGY:** `Dataset Explorer`, `Detection Methodology`, `System Architecture`.
   - **DOCUMENTATION:** `Technology Deep Dive`, `Technical Documentation`, `Limitations & Privacy`.
   - **GOVERNANCE & REVIEW:** `Annotation Review`, `Dataset Governance`.

### Step 2: Test Single-Image Morph Detection
1. Click **Face Morph Analysis** (`1_Face_Morph_Analysis.py`) in the sidebar.
2. In the **Single Image Analysis** tab, upload any standard portrait photograph (`.jpg` or `.png`), or select **`Sample A: Synthetic Genuine Demonstration`** from the **Load pre-packaged sample** sidebar dropdown (100% procedurally synthesized, zero biometric exposure).
3. **Select a Model:**
   - In the model selection dropdown, select **`combined_svm.joblib`** (our top baseline, 96.49% test accuracy).
   - Alternatively, select a deep neural network such as **`efficientnet_b0.pt`** (91.58% test accuracy).
4. **Inspect the Output:**
   - Face detection crop will appear (or full image if Haar detection passes).
   - The predicted **Morph Probability $P(\text{Morphed})$** will be displayed alongside the **Calibrated Decision Threshold $\tau^*$** (`0.0051` for Combined SVM).
   - The definitive classification banner will state either **`GENUINE / BONA FIDE`** ($P < \tau^*$) or **`MORPH ATTACK DETECTED`** ($P \ge \tau^*$).
5. **Test Result Export:** Click **Export Results (JSON)** or **Export Results (CSV)** to verify that reports download cleanly.

### Step 3: Test Two-Image Comparison
1. Switch to the **Two-Image Comparison** tab on the same page.
2. Upload two portrait images (Image A and Image B), or click the **Load Sample A (Synthetic Genuine)** and **Load Sample B (Synthetic Morphed)** buttons.
3. Verify that the comparative feature analysis displays:
   - Cosine similarity between feature embeddings.
   - Euclidean feature distance.
   - Comparative interpretation noting whether the images share high facial similarity *(Note: High similarity alone does not constitute a morph attack)*.

### Step 4: Verify Negative Edge-Cases & Error Handling
1. **No-Face Image:** Upload an image with no human face (e.g. an abstract graphic, scenery, or blank canvas).
   - *Expected Behavior:* The pipeline safely catches the condition, displaying `FACE NOT DETECTED` or a clear warning without crashing the app.
2. **Corrupted / Invalid File:** Upload an arbitrary non-image text file renamed to `.png`.
   - *Expected Behavior:* Handled gracefully with a defensive validation alert.

### Step 5: Verify Multi-Model Benchmarking Page
1. Navigate to **Multi-Model Comparison** (`2_Model_Comparison.py`).
2. Verify that all 21 models are listed with their exact ISO/IEC 30107-3 metrics on the held-out test split (285 samples):
   - `Combined SVM`: 96.49% Acc, 0.0680 ACER, $\tau^* = 0.0051$.
   - `HOG SVM`: 96.14% Acc, 0.0899 ACER, $\tau^* = 0.0040$.
   - `EfficientNet-B0`: 91.58% Acc, 0.0987 ACER, $\tau^* = 0.0032$.

---

## 3. Understanding Probabilities and Thresholds

> [!IMPORTANT]
> **Why is the Combined SVM threshold `0.0051` instead of `0.5000`?**
> - In uncalibrated Platt-scaling or raw RBF decision spaces, genuine samples produce scores concentrated close to zero ($\approx 10^{-4}$ to $10^{-3}$), while morphed attack samples score significantly higher ($> 0.01$).
> - Minimizing ACER on the validation split yielded the mathematically optimal threshold $\tau^* = 0.0051$.
> - Evaluating with a naive default of $0.5000$ results in severe false rejection (21.05% accuracy). The application automatically enforces $\tau^* = 0.0051$.

---

## 4. What to Do If the Hosted Application Is Sleeping

Streamlit Community Cloud automatically hibernates free-tier applications when there is no user traffic for several days.

* **Symptom:** Visiting `https://morphguard.streamlit.app/` shows a blue button saying *"This app has gone to sleep"*.
* **Resolution:** Simply click the blue **"Yes, get this app back up!"** button. The container will boot up, restore environment dependencies, and be ready within 30–60 seconds.

---

## 5. Known Limitations & Research Boundaries

1. **Academic Research Prototype:** MorphGuard is an experimental research system trained on MONOT and ONOT datasets under CC BY-NC 4.0 terms. It is not an ISO/IEC certified commercial border-control product.
2. **Held-out Split Scope:** The reported 96.49% accuracy reflects performance on the 285 held-out test split (228 morphs, 57 genuine) under controlled research conditions, not unrestricted real-world scenarios.
3. **Biometric Privacy:** No raw facial imagery or identities are stored on or transmitted to external servers. All processing operates in-memory.
