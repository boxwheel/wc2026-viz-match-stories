#!/usr/bin/env bash
# Pull the Kaggle FIFA WC-2026 bundle into ~/research/fifa_data
set -euo pipefail
cd ~/research
set -a && . ./.env && set +a
curl -sSL -H "Authorization: Bearer $KAGGLE_API_TOKEN" \
  "https://www.kaggle.com/api/v1/datasets/download/mominullptr/fifa-world-cup-2026-dataset" \
  -o fifa.zip
unzip -o fifa.zip -d fifa_data
