#!/usr/bin/bash

echo "activating anaconda"
module activate anaconda
echo "list environments"
conda list env
echo "activating conda-env"
conda activate conda-env
echo "running main.py"
python main.py