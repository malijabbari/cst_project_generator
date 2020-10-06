import argparse

import settings
from util.generate_cst_project import generate_cst_project

# on the server, the job-id & partition is passed as an argument
if settings.is_running_on_desktop:
    job_id = 0
    partition_id = 0
    n_cpus = 4
    n_gpus = 1
else:
    parser = argparse.ArgumentParser()
    parser.add_argument("--job_id", help="server job id-number", type=int)
    parser.add_argument("--partition_id", help="server partition id", type=int)
    parser.add_argument("--n_cpus", help="number of cpus used", type=int)
    parser.add_argument("--n_gpus", help="number of gpus used", type=int)
    job_id = parser.parse_args().job_id
    n_cpus = parser.parse_args().n_cpus
    n_gpus = parser.parse_args().n_gpus
    partition_id = parser.parse_args().partition_id

# generate cst_projects
for idx in range(0, settings.n_projects):
    generate_cst_project(job_id, partition_id, n_cpus, n_gpus)
