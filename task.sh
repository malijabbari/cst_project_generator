#!/usr/bin/bash

module activate anaconda
conda activate '/home/tue/s111167/.conda/envs/conda-env'
conda list
python main.py