#!/usr/bin/bash

module load anaconda
source activate '/home/tue/s111167/.conda/envs/conda-env'
python main.py --job_id $job_id --partition_id $partition_id