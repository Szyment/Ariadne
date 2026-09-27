#!/bin/sh
# Regenerates the detector results from the published CSV data. Run from the repository root:
#   pip install -r requirements.txt && sh analysis/reproduce.sh
# Drift analysis per session (results/S-NN_*_drift_analysis.txt) needs the raw .bin logs, published with the frozen dataset.
set -e
cd "$(dirname "$0")/.."
mkdir -p analysis/results/detector
python3 analysis/degradation_detector.py data/ARIADNE_E1_*.csv --plots analysis/results/detector --csv analysis/results/detector_v0.2_all.csv
echo "done: analysis/results/detector_v0.2_all.csv and analysis/results/detector/*.png"
