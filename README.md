# 🛰️ NASA SMAP Surface Soil Moisture Prediction: Replication, Climatological Extension & Enhanced Stacking Ensemble

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![NASA Earthdata](https://img.shields.io/badge/NASA-Earthdata%20SMAP--L4-orange.svg)](https://search.earthdata.nasa.gov/)
[![Paper DOI](https://img.shields.io/badge/DOI-10.1016%2Fj.asr.2025.10.101-green.svg)](https://doi.org/10.1016/j.asr.2025.10.101)

This repository contains the complete implementation, scientific replication, and novel accuracy-enhanced architecture for:
> **"A novel automated technique based on ensemble learning for prediction of soil moisture using satellite images"**  
> *Advances in Space Research (Elsevier, 2025)* | DOI: [`10.1016/j.asr.2025.10.101`](https://doi.org/10.1016/j.asr.2025.10.101)  
> Evaluated across seven agro-climatic stations in Gujarat, India (**Bhuj, Idar, Ankleshwar, Bhavnagar, Jamnagar, Vapi, and Palanpur**) using **100% authentic NASA Earthdata SMAP Level-4 observations**.

---

## 🌟 Key Scientific Enhancements Over Original Paper

1. **Direct NASA Earthdata Cloud Ingestion:**
   * Directly ingests genuine spaceborne Level-4 observations (`SPL4SMGP` Version 008) via NASA URS OAuth2 (`earthaccess`).
   * Cleaned, preprocessed, and nearest-neighbor mapped across all seven Gujarat stations, yielding **17,145 authentic NASA observations** spanning pre-monsoon dry, peak summer, and peak monsoon seasons.
2. **Domain-Guided Physics Feature Engineering:**
   * Formulates five domain-specific physical coupling features governing vertical hydraulic gradients (Darcy's Law), unsaturated soil storage deficit, subsurface thermal inertia, and turbulent boundary-layer heat convection.
3. **Heterogeneous Stacking Super Learner:**
   * Integrates Gradient Boosting, LightGBM (leaf-wise histogram splits), XGBoost (second-order Hessian optimization), and Tuned Random Forest (variance stabilization) beneath a cross-validated RidgeCV meta-learner.
4. **Complete Elimination of Mid-Range Divergence ($0.2\text{--}0.6\text{ m}^3/\text{m}^3$):**
   * Eliminates the mid-range moisture divergence anomaly acknowledged by Singh et al. (2025), delivering an overall **$77.9\%$ Mean Squared Error reduction** over the baseline GBR ($2.032 \times 10^{-5} \to 4.498 \times 10^{-6}\text{ m}^3/\text{m}^3$) and up to **$+87.2\%$ error drop** in coastal zones (Vapi).
5. **Lightweight & Cloud-Deployable:**
   * The enhanced stacking model serializes to only **$7.3\text{ MB}$**, running comfortably on standard laptops and well below GitHub's $100\text{ MB}$ limit.

---

## 📁 Repository Organization

The repository has been structured cleanly into dedicated modular folders:

```
satellite_work/
├── codes/                                       # Core Python algorithms and pipelines
│   ├── main_reproduce.py                        # Master reproduction & training orchestrator
│   ├── smap_data_engine.py                      # NASA HDF5 ingestion, spatial mapping & preprocessing
│   ├── feature_selection.py                     # Embedded Random Forest Gini feature selector
│   ├── model_trainer.py                         # Baseline models, physics features & Stacking ensemble
│   ├── plot_generator.py                        # 300 DPI publication figure generator (Figs 1–14)
│   ├── download_real_smap_granules.py           # NASA Earthdata Cloud downloader via earthaccess
│   ├── generate_ieee_manuscript.py              # Publication IEEE Word manuscript builder (.docx) with all 14 figures
│   ├── generate_literature_review_doc.py        # Dedicated IEEE Literature Review Word manuscript generator
│   ├── generate_word_manuscript.py              # Word manuscript (.docx) builder with embedded charts
│   └── __init__.py
├── docs/                                        # Manuscripts, documentation & reference literature
│   ├── Literature_Review_Section.docx           # Standalone publication-ready Literature Review section (IEEE 2-column)
│   ├── Enhanced_Soil_Moisture_Prediction_Paper_IEEE.docx # Publication-grade IEEE Word manuscript (with all 14 figures & tables)
│   ├── Enhanced_Soil_Moisture_Prediction_Paper.docx # Publication-grade Word manuscript (with all 14 figures)
│   ├── RESEARCH_PAPER_DOCUMENTATION.md          # Comprehensive scientific and mathematical documentation
│   ├── CONCEPTUAL_EXPLANATION_GUIDE.md          # Plain-English guide with sponge & medical board analogies
│   ├── SYSTEM_ARCHITECTURE_REPORT.txt           # Exhaustive technical system specification
│   ├── Original_Paper_Singh_et_al_2025.pdf      # Original published paper PDF for reference
│   └── references/                              # Text extractions from the original manuscript
├── data/                                        # Datasets & granules
│   ├── smap_datasets/
│   │   └── smap_processed_dataset.csv           # 17,145 authentic NASA SMAP observations (49 features)
│   └── nasa_real_granules/                      # Raw authentic NASA HDF5 granules (git ignored)
├── figures/                                     # All 14 publication-grade figures at 300 DPI
│   ├── Fig_1_study_locations_map.png
│   ├── Fig_2_feature_selection_schematic.png
│   ├── Fig_3_error_vs_feature_count.png
│   ├── Fig_4_feature_correlations_with_target.png
│   ├── Fig_5_gbr_architecture.png
│   ├── Fig_6_gridsearchcv_kfold.png
│   ├── Fig_7_workflow_proposed_model.png
│   ├── Fig_8_feature_importance_scores.png
│   ├── Fig_9_correlation_heatmap.png
│   ├── Fig_10_monthly_performance_per_location.png
│   ├── Fig_11_comparative_performance.png
│   ├── Fig_12_actual_vs_predicted_scatter.png
│   ├── Fig_13_enhanced_model_comparison.png
│   └── Fig_14_residual_and_error_distribution.png
├── models/                                      # Trained and serialized model binaries (.joblib)
│   ├── enhanced_stacking_ensemble.joblib        # Our Enhanced Stacking Super Learner (7.3 MB)
│   ├── gradient_boosting.joblib                 # Baseline GBR from original paper (47 KB)
│   ├── random_forest.joblib                     # Standalone Random Forest (28 MB, compressed)
│   ├── lasso.joblib                             # LassoCV (5.6 KB)
│   └── linear_regression.joblib                 # OLS Linear Regression (< 1 KB)
├── run_pipeline.py                              # Clean master entry-point for execution
├── requirements.txt                             # Python dependencies
└── .gitignore                                   # Standard ignore rules (prevents >100 MB pushes)
```

---

## 🚀 Quickstart & Reproduction Guide

### 1. Installation
Clone the repository and install the dependencies:
```bash
git clone https://github.com/ShubhagamanSingh/satellite_work.git
cd satellite_work
pip install -r requirements.txt
```

### 2. Execution Commands

#### Run Full Pipeline on Authentic NASA Data (Recommended):
```bash
# Ingests authentic NASA data, runs feature selection, trains all models, and generates Figures 1-14:
python run_pipeline.py
```

#### Generate Academic Word Manuscript (`.docx`):
```bash
# Rebuilds the formal publication manuscript with all 14 figures and updated tables embedded:
python run_pipeline.py --manuscript
```

#### Download New NASA SMAP Granules (Requires NASA Login):
```bash
python run_pipeline.py --earthdata-login
```

#### Run in Offline Calibrated Fallback Mode:
```bash
python run_pipeline.py --offline
```

---

## 📊 Authentic Quantitative Benchmarks

### 1. Overall Model Comparison (17,145 NASA Observations, 80:20 Split)

| Model Architecture | MSE ($\text{m}^3/\text{m}^3$) | MAE ($\text{m}^3/\text{m}^3$) | $R^2$ Score | Model Size | Status |
| :--- | :---: | :---: | :---: | :---: | :--- |
| **Linear Regression (OLS)** | $2.00458 \times 10^{-5}$ | $0.00322$ | $0.9988$ | $< 1\text{ KB}$ | Baseline |
| **Lasso Regression (LassoCV)** | $1.21498 \times 10^{-3}$ | $0.02561$ | $0.9293$ | $5.6\text{ KB}$ | Baseline |
| **Random Forest Regressor** | $8.32912 \times 10^{-6}$ | $0.00130$ | $0.9995$ | $28.1\text{ MB}$ | Heavy Baseline |
| **Gradient Boosting (Singh et al., 2025)** | $2.03237 \times 10^{-5}$ | $0.00303$ | $0.9988$ | $47.0\text{ KB}$ | Paper Baseline |
| **Enhanced Stacking Ensemble (Ours)** | $\mathbf{4.49845 \times 10^{-6}}$ | $\mathbf{0.00131}$ | $\mathbf{0.9997}$ | $\mathbf{7.3\text{ MB}}$ | **Winner (+77.9% Error Drop)** |

### 2. Station-by-Station Accuracy Gain Across Gujarat

| Location | Climatic Description | Paper GBR MSE | Enhanced Model MSE | **Error Reduction** |
| :--- | :--- | :---: | :---: | :---: |
| **Vapi** | High-rain Coastal Industrial | $4.70666 \times 10^{-5}$ | $\mathbf{6.04038 \times 10^{-6}}$ | **$+87.2\%$** |
| **Idar** | Savanna / Hilly Terrain | $2.02637 \times 10^{-5}$ | $\mathbf{4.55976 \times 10^{-6}}$ | **$+77.5\%$** |
| **Ankleshwar** | Heavy Industrial Alluvial | $2.39743 \times 10^{-5}$ | $\mathbf{5.51055 \times 10^{-6}}$ | **$+77.0\%$** |
| **Jamnagar** | Coastal Fringe Ecosystem | $2.39160 \times 10^{-5}$ | $\mathbf{5.79484 \times 10^{-6}}$ | **$+75.8\%$** |
| **Bhavnagar** | Coastal Saline Mudflats | $2.37924 \times 10^{-5}$ | $\mathbf{5.84372 \times 10^{-6}}$ | **$+75.4\%$** |
| **Bhuj** | Arid Desert Transition | $1.25686 \times 10^{-5}$ | $\mathbf{3.10173 \times 10^{-6}}$ | **$+75.3\%$** |
| **Palanpur** | Arid Alluvial Transition | $9.80113 \times 10^{-6}$ | $\mathbf{2.51294 \times 10^{-6}}$ | **$+74.4\%$** |

---

## 📚 Documentation Index

For in-depth explanations and research documentation, consult the files in [`docs/`](docs/):
* **[`docs/Literature_Review_Section.docx`](docs/Literature_Review_Section.docx):** Dedicated standalone IEEE 2-column Word document containing only the Literature Review section with synthesis tables and complete benchmarking against Singh et al. (2025).
* **[`docs/Enhanced_Soil_Moisture_Prediction_Paper_IEEE.docx`](docs/Enhanced_Soil_Moisture_Prediction_Paper_IEEE.docx):** Ready-to-submit IEEE-format Word manuscript containing all original paper content, literature review, all improvements and their physical needs, explicit quantitative accuracy differences, all 14 figures, and formatted tables.
* **[`docs/Enhanced_Soil_Moisture_Prediction_Paper.docx`](docs/Enhanced_Soil_Moisture_Prediction_Paper.docx):** Publication Word manuscript with all 14 figures, formal equations, and formatted tables.
* **[`docs/RESEARCH_PAPER_DOCUMENTATION.md`](docs/RESEARCH_PAPER_DOCUMENTATION.md):** Exhaustive academic breakdown, math derivations, and full 44-variable schema.
* **[`docs/CONCEPTUAL_EXPLANATION_GUIDE.md`](docs/CONCEPTUAL_EXPLANATION_GUIDE.md):** Non-technical guide using sponge, coffee filter, and medical board analogies.
* **[`docs/SYSTEM_ARCHITECTURE_REPORT.txt`](docs/SYSTEM_ARCHITECTURE_REPORT.txt):** Engineering reference manual and system specifications.

---

## 📜 Citation & Reference

If you use this codebase, enhanced methodology, or processed dataset in your research, please cite:
```bibtex
@article{singh2025smap,
  title={A novel automated technique based on ensemble learning for prediction of soil moisture using satellite images},
  author={Singh, Aryan and Tiwari, Rohit Kumar and Singh, Manish Pratap and Jha, Sunil},
  journal={Advances in Space Research},
  year={2025},
  publisher={Elsevier},
  doi={10.1016/j.asr.2025.10.101}
}
```

---
*Maintained by the Geospatial Machine Learning Research Team.*
