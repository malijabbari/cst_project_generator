#!/usr/bin/bash

# verify that argument (number of tasks) is passed
if [ -z "$1" ]
then
  echo "ERROR: number of tasks needs to be passed as an argument"
  exit 1
fi

# verify that only 1 argument is passed
if [ $# -gt 1 ]
then
  echo "ERROR: $# arguments are given, only 1 is required"
fi

# verify that number of tasks is > 0
if [ $1 -lt 1 ]
then
  echo "ERROR: number of tasks is < 1"
  exit 1
fi

# execute tasks
#sbatch  --partition=elec.gpu.q
#sbatch  --job-name=CST_project_generation
#sbatch  --nodes=1
#sbatch  --ntasks=2
#sbatch  --cpus-per-task=2 \
#sbatch  --time=10-00:00:00 \
#sbatch  --gpus-per-task=1
#sbatch  --output=output/task_%j.txt \
#sbatch  --error=output/error_task_%j.txt \
#sbatch  --mail-user=d.m.n.v.d.vorst@student.tue.nl \
#sbatch  --mail-type=ALL \

srun -n 2 ./task.sh