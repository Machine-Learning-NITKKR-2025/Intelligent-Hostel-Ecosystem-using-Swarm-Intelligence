# Smart Energy Prediction System for Campus Hostels



## Overview
This project builds short-term and month-long (<=1 month) energy consumption forecasting models for a campus hostel using the provided dataset.

## Structure
```
smart_energy_project/
├─ data/
│  └─ hostel_energy_data_3hourly.csv   # original dataset (not included by default, placed by user)
├─ scripts/
│  ├─ data_prep.py
│  ├─ features.py
│  ├─ train_models.py
│  ├─ evaluate.py
│  └─ utils.py
├─ models/
├─ outputs/
├─ requirements.txt
├─ run_all.sh
└─ README.md
```

## How to run
1. Put the dataset at `data/hostel_energy_data_3hourly.csv` (or update path in scripts).
2. Create a virtualenv and install dependencies:
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
3. Run the full pipeline:
```bash
bash run_all.sh
```
This runs data prep, feature engineering, trains baseline models, and saves outputs under `outputs/` and models under `models/`.

## Notes
- The scripts use time-aware splitting for forecasting tasks.
- Two forecasting horizons are supported:
  - Short-term (3-hour ahead)
  - Long-term (up to 1 month ahead) implemented as a daily aggregated forecast using lag features
- You can customize models and hyperparameters inside `scripts/train_models.py`.
