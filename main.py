import argparse

import settings
from util.generate_cst_project import generate_cst_project

# on the server, the job-id & partition is passed as an argument
if settings.is_running_on_desktop:
    job_id = 0
    partition_id = 0
else:
    parser = argparse.ArgumentParser()
    parser.add_argument("--job_id", help="server job id-number", type=int)
    parser.add_argument("--partition_id", help="server partition id", type=int)
    job_id = parser.parse_args().job_id
    partition_id = parser.parse_args().partition_id

# generate cst_projects
for idx in range(0, settings.n_projects):
    generate_cst_project(job_id, partition_id)
