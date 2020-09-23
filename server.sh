#!/usr/bin/bash

# verify that argument (number of jobs) is passed
if [ -z "$1" ]
then
  echo "ERROR: number of jobs needs to be passed as an argument"
  exit 1
fi

# verify that only 1 argument is passed
if [ $# -gt 1 ]
then
  echo "ERROR: $# arguments are given, only 1 is required"
fi

# verify that number of jobs is > 0
if [ $1 -lt 1 ]
then
  echo "ERROR: number of jobs is < 1"
  exit 1
fi

# execute jobs
for (( job_id=0; job_id<$1; job_id++ ))
do
  export job_id=$job_id
  sbatch  --job-name=CST_project_generator_$job_id \
          --nodes=1 \
          --ntasks=1 \
          --cpus-per-task=1 \
          --time=2-00:00:00 \
          --partition=elec.gpu.q \
          --output=output/task_$job_id.txt \
          --error=output/error_task_$job_id.txt \
          --mail-user=d.m.n.v.d.vorst@student.tue.nl \
          --mail-type=ALL \
          task.sh
done