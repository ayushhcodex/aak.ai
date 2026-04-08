# AIMATRY: Generative Polymer Designer — v3.0

![AIMATRY Banner](https://img.shields.io/badge/Status-Conference--Ready-brightgreen?style=for-the-badge&logo=dna)
![Streamlit](https://img.shields.io/badge/Built%20with-Streamlit-FF4B4B?style=for-the-badge&logo=streamlit)
![Python](https://img.shields.io/badge/Python-3.8%2B-3776AB?style=for-the-badge&logo=python)

**AIMATRY** is a high-fidelity, scientifically credible "Wizard of Oz" prototype designed for materials informatics and textile science research. It leverages Artificial Intelligence in Material Discovery (AAK.AI) to autonomously generate synthetically accessible polymers for next-generation protective textiles.

---

## 📖 Table of Contents
- [Overview](#-overview)
- [Key Features](#-key-features)
- [Project Structure](#-project-structure)
- [Installation & Setup](#-installation--setup)
- [Contribution Guide](#-contribution-guide)
  - [Adding New Scenarios](#adding-new-scenarios)
  - [Updating Fiber Data](#updating-fiber-data)
- [Internal Architecture](#-internal-architecture)
- [Tech Stack](#-tech-stack)
- [License](#-license)

---

## 🌟 Overview
AIMATRY simulates an AI-driven discovery engine that screens millions of monomers to find optimal material blends for extreme environments. Developed for the **AgriDrone AI Architecture** initiative, it bridges the gap between material science research and industrial application.

---

## 🛡️ Key Features
- **10 Extreme Threat Scenarios**: From Arctic Combat to Hypersonic Re-entry.
- **Advanced Analytics**: Radar charts, Pareto frontiers, and aging predictions using Plotly.
- **Material Engineering**: Multi-layer stack visualization and synthetic route generation.
- **Professional Standards**: Aligned with ISO, EN, and Indian BIS standards.
- **Sustainability/ESG**: Detailed scoring for CO₂ and water footprint.

---

## 📂 Project Structure
```text
.
├── app.py              # Main Streamlit application (UI, Styling, Logic)
├── data.py             # Knowledge Base (Scenarios, Fibers, Benchmarks)
├── requirements.txt    # Python dependencies
└── README.md           # Documentation
```

---

## 🚀 Installation & Setup

### Prerequisites
- Python 3.8+
- [Conda](https://docs.conda.io/en/latest/) or [venv](https://docs.python.org/3/library/venv.html) (Recommended)

### Local Setup
1. **Clone the repository**:
   ```bash
   git clone https://github.com/ayushhcodex/aak.ai.git
   cd aak.ai
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the app**:
   ```bash
   streamlit run app.py
   ```

---

## 🤝 Contribution Guide

We welcome contributions from material scientists, chemists, and AI researchers!

### Adding New Scenarios
All scenario data is stored in `data.py` under the `SCENARIOS` dictionary. To add a new threat:
1. Open [data.py](file:///Users/ayushsingh/Developer/AgriDrone_AI_Architecture.pdfAgriDrone_AI_Architecture/AAK-AI%20/AAK.AI_MVP/data.py).
2. Follow the existing schema:
   ```python
   "Scenario Name": {
       "blend": "Description of polymer material",
       "feature": "Unique selling point",
       "scores": { ... }, # Normalized 0-100 scores
       "confidence": 90,
       "status": "✅ Commercial",
       "sustainability": { ... },
       "layers": [ ... ],
       "aging": { ... },
       "synth_route": [ ... ],
       "chat_explanation": [ ... ]
   }
   ```
3. The UI will automatically detect and list your new scenario in the sidebar.

### Updating Fiber Data
Add or edit fibers in `FIBER_DATABASE` (line 335 of `data.py`) to update the reference table used in the "Fiber Database" tab.

---

## 🏗️ Internal Architecture

### Virtual Forward Synthesis (VFS)
The "synthesis" shown in the app is a high-fidelity simulation. In `app.py`, the `st.status` component mimics the computation of:
1. Monomer screening (14.2M database).
2. Retrosynthetic feasibility.
3. Pareto frontier optimization.

### Visualization Engine
- **Radar Charts**: Powered by `go.Scatterpolar` to show trade-offs between HTP, THL, Strength, and Flexibility.
- **Pareto Front**: Uses `go.Scatter` to visualize the efficiency frontier of performance vs. accessibility.

### Styling
The application uses a **Cyber-Industrial Theme** built with custom CSS injected via `st.markdown`. It uses Google Fonts:
- **Orbitron**: For headers and data values.
- **Inter**: For body text and descriptions.
- **JetBrains Mono**: For SMILES strings and technical specs.

---

## 🧬 Tech Stack
- **Framework**: [Streamlit](https://streamlit.io/)
- **Visuals**: [Plotly Express/Graph Objects](https://plotly.com/python/)
- **Data Handling**: [Pandas](https://pandas.pydata.org/), [NumPy](https://numpy.org/)
- **Typography**: [Google Fonts API](https://fonts.google.com/)

---

## 📜 License
This project is currently for internal research and conference demonstration. See the `LICENSE` file (if available) for specific terms.

---

© 2026 **AIMATRY** — Materials Intelligence Platform. Developed for [AgriDrone AI Architecture](https://github.com/ayushhcodex).
