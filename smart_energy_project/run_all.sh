#!/bin/bash
set -e
echo "Running full pipeline..."
python3 scripts/data_prep.py
python3 scripts/features.py
python3 scripts/train_models.py
python3 scripts/evaluate.py
echo "Pipeline finished. Check models/ and outputs/ folders."
