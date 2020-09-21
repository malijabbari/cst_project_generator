import os
from numpy.random import randint

# project settings
project_root_folder_desktop = 'C:/Users/Dennis/Documents/generated_projects'
project_root_folder_server = '/home/tue/s111167/generated_projects'
project_folder_prefix = 'project_'
project_folder_name_n_zero_padding = 5
max_projects = 10000
is_running_on_desktop = os.name == 'nt'  # nt: Windows , posix: Linux
path_cst_exe_server = '/cm/shared/apps/cst/CST_STUDIO_SUITE_2020' \
                      '/cst_design_environment.exe'
path_cst_exe_desktop = 'C:/Program Files (x86)/CST Studio Suite 2020/' \
                       'CST DESIGN ENVIRONMENT.exe'

# model settings
export_path_model = 'C:/Users/Dennis/Documents/generated_models'
export_filename_prefix = 'model_'
n_objects = randint(low=10, high=15)
limit_placement = [-50, 50]  # mm
limit_scale = [10, 100]  # mm
boundary_radius = 100  # mm
boundary_height = [-50, 50]  # mm

# object settings
f_max = 15
n_iter = 5
n_pnts = 15
frequency_power_decrease_rate = 1
objectname_prefix = 'object_'
