# 🗺️ AIMATRY — Development Roadmap

## Vision
Transform AIMATRY from a curated knowledge-based prototype into a fully data-driven, predictive AI platform for protective textile design — powered by real Indian lab data.

---

## Current State: MVP (Today)

✅ 10 threat scenarios with curated material solutions  
✅ 5-property multi-objective optimization  
✅ Virtual synthesis route generation  
✅ Aging & durability prediction  
✅ Sustainability (ESG) scoring  
✅ Commercial benchmark comparison  
✅ Standards-aligned (ISO, BIS, EN, NFPA)  
✅ AI explainability ("Why Our AI Chose This")  

**Limitation:** All data is hardcoded from published literature — not trained on real experimental data yet.

---

## Phase 1: Data Collection Partnership (3–6 Months)

**Goal:** Partner with NITRA labs to collect real, structured test data.

| Action | Detail |
|:-------|:-------|
| Identify 3–5 key test types | LOI, ATPV, tensile strength, THL, wash-cycle degradation |
| Data format standardization | Create CSV/JSON templates for labs to fill with historical results |
| Target dataset size | 500–1,000 structured test records across multiple fiber types |
| Privacy & IP | All data anonymized; NITRA retains full IP over raw data |
| Deliverable | Cleaned, labeled dataset ready for ML training |

---

## Phase 2: Machine Learning Integration (6–12 Months)

**Goal:** Replace hardcoded scores with trained regression models.

| Action | Detail |
|:-------|:-------|
| Model type | XGBoost / Random Forest for property prediction |
| Input features | Fiber composition (%), weave type, coating, finish, GSM |
| Output targets | HTP score, THL score, tensile strength, LOI, ATPV |
| Validation | 5-fold cross-validation against held-out NITRA test data |
| Uncertainty | Knowledge uncertainty + natural variability reporting per prediction |
| Deliverable | Trained models with >85% R² on held-out test data |

---

## Phase 3: Generative AI Engine (12–18 Months)

**Goal:** Move from prediction to generation — AI proposes novel blends that don't exist yet.

| Action | Detail |
|:-------|:-------|
| Architecture | Variational Autoencoder (VAE) or Generative Adversarial Network (GAN) |
| Training data | Phase 2 dataset + augmented with published literature |
| Capability | Given a target property profile, generate novel fiber-blend recipes |
| Validation | Top 5 AI-generated blends physically manufactured and tested at NITRA |
| Deliverable | First AI-designed protective textile validated by physical testing |

---

## Phase 4: Industry API & Commercialization (18–24 Months)

**Goal:** Package AIMATRY as a SaaS product for textile manufacturers and defense procurement.

| Action | Detail |
|:-------|:-------|
| API development | RESTful API — input threat profile, output optimal material spec |
| Clients | Textile manufacturers, defense procurement (MoD), fire services |
| Revenue model | Subscription-based access + custom model training for enterprise |
| Certifications | Seek iDEX (Defence Innovation), DPIIT Startup India recognition |
| Deliverable | Revenue-generating product with pilot customers |

---

## Summary Timeline

```
TODAY           6 months        12 months       18 months       24 months
  │               │               │               │               │
  ▼               ▼               ▼               ▼               ▼
┌─────────┐  ┌──────────┐  ┌──────────────┐ ┌──────────────┐ ┌────────────┐
│  MVP    │  │  Data    │  │  ML Models   │ │  Generative  │ │  Industry  │
│  Demo   │→ │  Partner │→ │  Trained     │→│  AI Engine   │→│  API &     │
│  (Now)  │  │  with    │  │  on Real     │ │  Novel Blend │ │  SaaS      │
│         │  │  NITRA   │  │  Lab Data    │ │  Generation  │ │  Product   │
└─────────┘  └──────────┘  └──────────────┘ └──────────────┘ └────────────┘
Hardcoded     Real Data      Predictive       Creative         Commercial
Knowledge     Collection     Intelligence     Intelligence     Deployment
```

---

**Team AAK-AI** | NITRA Technical Campus  
*"From curated knowledge to learned intelligence — one dataset at a time."*
