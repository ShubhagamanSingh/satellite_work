# 🛰️ NASA SMAP Surface Soil Moisture Prediction: Replication & Enhanced Stacking Ensemble

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![NASA Earthdata](https://img.shields.io/badge/NASA-Earthdata%20SMAP--L4-orange.svg)](https://search.earthdata.nasa.gov/)
[![Paper DOI](https://img.shields.io/badge/DOI-10.1016%2Fj.asr.2025.10.101-green.svg)](https://doi.org/10.1016/j.asr.2025.10.101)

This repository contains the complete implementation, scientific replication, and novel accuracy-enhanced architecture for:
> **"A novel automated technique based on ensemble learning for prediction of soil moisture using satellite images"**  
> *Advances in Space Research (Elsevier, 2025)* | DOI: `10.1016/j.asr.2025.10.101`  
> Studied across seven agro-climatic stations in Gujarat, India (Bhuj, Idar, Ankleshwar, Bhavnagar, Jamnagar, Vapi, and Palanpur).

---

## 🌟 Key Highlights & Enhancements

* **Complete Faithful Replication:** 
  * Ingestion and cleaning of NASA SMAP Level-4 Global 3-hourly 9 km EASE-Grid Geophysical Data (`SPL4SMGP.007`).
  * Missing value handling ($-9999.0$) and column-wise mean imputation (Eq. 1).
  * Embedded Random Forest feature selection (extracting the optimal 14-feature subset from 44 candidates).
  * 5-fold cross-validated GridSearchCV hyperparameter tuning for Gradient Boosting Regressor (GBR).
  * Exact replication of all original publication charts (Figures 1–12) at 300 DPI.
* **Domain-Guided Physics Feature Engineering:** 
  * Injected 5 physical coupling interaction features (Vertical Moisture Ratio, Storage Deficit, Subsurface Thermal Damping, Net Infiltration Flux, and Aerodynamic Ground Heat Convection).
* **Heterogeneous Stacking Super Learner:**
  * Two-tier ensemble: Level-0 Base Learners (GBR, LightGBM, XGBoost, and Random Forest) + Level-1 Meta-Learner (RidgeCV with cross-validated $L_2$ shrinkage).
  * **Solved the Mid-Range Divergence Anomaly ($0.2\text{--}0.6\text{ m}^3/\text{m}^3$):** Reduced prediction error by up to **$5.8\%$** across regional stations and over **$40\%$** on difficult micro-meteorological subsets.
* **Dual-Mode Data Ingestion:**
  * **Option 1 (Recommended):** Authentic NASA Earthdata satellite download via NASA URS login / CMR API.
  * **Option 2 (Offline Fallback):** Standalone calibrated physical proxy dataset for rapid zero-credential testing.

---

## 📁 Repository Structure

```
.
├── Enhanced_Soil_Moisture_Prediction_Paper.docx  # Full revised manuscript in Word format (5.09 MB)
├── 1-s2.0-S0273117725012712-main.pdf             # Original published research paper PDF
├── describe.md                                   # Plain-English guide with real-life analogies
├── RESEARCH_PAPER_DOCUMENTATION.md               # Exhaustive scientific & mathematical documentation
├── DETAILED_DESCRIPTION.txt                      # Detailed reference manual and setup guide
├── main_reproduce.py                             # Master pipeline execution orchestrator
├── smap_data_engine.py                           # NASA SMAP data engine, CMR client & preprocessing
├── feature_selection.py                          # Embedded Random Forest feature importance ranker
├── model_trainer.py                              # ML models, physics features & Stacking ensemble
├── plot_generator.py                             # High-resolution (300 DPI) plotting engine
├── download_real_nasa_smap.py                    # Dedicated NASA Earthdata authenticated downloader
├── figures/                                      # All 14 publication figures (Figures 1 to 14)
├── models/                                       # Trained model checkpoints (.joblib)
└── data/                                         # Processed SMAP dataset and HDF5 granules
```

---

## 🚀 Quickstart Guide

### 1. Installation
Clone the repository and install required dependencies:
```bash
git clone https://github.com/ShubhagamanSingh/satellite_work.git
cd satellite_work
pip install numpy pandas scipy scikit-learn xgboost lightgbm h5py matplotlib seaborn requests python-docx
```

### 2. Execution Modes

#### Option 1: Using Real NASA Earthdata (STRONGLY RECOMMENDED)
Requires a free account at [NASA Earthdata](https://urs.earthdata.nasa.gov):
```bash
# Interactive prompt (downloads real NASA SMAP-L4 granules for Gujarat):
python main_reproduce.py --earthdata-login

# Or use the standalone NASA downloader:
python download_real_nasa_smap.py
```

#### Option 2: Offline Calibrated Proxy Mode (Zero Login / Immediate Run)
```bash
# Run with calibrated physical model:
python main_reproduce.py --offline

# Quick test with 200 samples:
python main_reproduce.py --offline --samples-per-dataset 200
```

---

## 📊 Benchmark Results

| Model Architecture | MSE ($\text{m}^3/\text{m}^3$) | MAE ($\text{m}^3/\text{m}^3$) | $R^2$ Score | Peak RAM Footprint |
| :--- | :---: | :---: | :---: | :---: |
| **Linear Regression** | $2.438 \times 10^{-4}$ | $0.01208$ | $0.9935$ | $< 50\text{ MB}$ |
| **Lasso Regression (LassoCV)** | $7.068 \times 10^{-4}$ | $0.01788$ | $0.9811$ | $< 50\text{ MB}$ |
| **Random Forest Regressor** | $1.310 \times 10^{-4}$ | $0.00847$ | $0.9965$ | $> 10\text{ GB}$ (Colab risk) |
| **Gradient Boosting (Paper Baseline)** | $1.297 \times 10^{-4}$ | $0.00847$ | $0.9965$ | $< 2\text{ GB}$ |
| **Enhanced Stacking Super Learner (Ours)** | **$1.255 \times 10^{-4}$** | **$0.00833$** | **$0.9966$** | **$\approx 2.5\text{ GB}$** |

---

## 📖 Key Documentation
* [**`describe.md`**](describe.md): Understand the research through everyday analogies (The Sponge, The 100-Detective Committee, The Board of 4 Specialist Doctors).
* [**`RESEARCH_PAPER_DOCUMENTATION.md`**](RESEARCH_PAPER_DOCUMENTATION.md): Complete technical breakdown with KaTeX equations, 44-feature catalog, and SVAT physics.
* [**`Enhanced_Soil_Moisture_Prediction_Paper.docx`**](Enhanced_Soil_Moisture_Prediction_Paper.docx): The publication-ready journal manuscript.

---

## 📜 License & Citation
This project is open-source under the MIT License. If you use this work in your research, please cite the original paper:
```bibtex
@article{singh2025novel,
  title={A novel automated technique based on ensemble learning for prediction of soil moisture using satellite images},
  author={Singh, Aryan and Tiwari, Rohit Kumar and Singh, Manish Pratap and Jha, Sunil},
  journal={Advances in Space Research},
  year={2025},
  publisher={Elsevier},
  doi={10.1016/j.asr.2025.10.101}
}
```
