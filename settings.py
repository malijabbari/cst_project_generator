import os

from numpy.random import randint

import util.constants as constants

# project settings
project_root_folder_desktop = 'C:/Users/Dennis/Documents/generated_projects'
project_root_folder_server = '/home/tue/s111167/generated_projects2'
project_folder_prefix = 'project_'
project_folder_name_n_zero_padding = 5
is_running_on_desktop = os.name == 'nt'  # nt: Windows , posix: Linux
path_cst_exe_desktop = 'C:/Program Files (x86)/CST Studio Suite 2020/' \
                       'CST DESIGN ENVIRONMENT.exe'
path_cst_exe_server = '/cm/shared/apps/cst/CST_STUDIO_SUITE_2020' \
                      '/cst_design_environment'
path_freecad_desktop = 'C:/Program Files/FreeCAD/FreeCAD_0.19.22474/bin'
path_freecad_server = '/home/tue/s111167/freecad/lib'
max_projects = 10000
if is_running_on_desktop:
    n_projects = 1
else:
    n_projects = 156

# model settings
export_filename_prefix = 'model_'
limit_placement = [-50, 50]  # mm
limit_scale = [10, 100]  # mm
boundary_radius = 100  # mm
boundary_height = [-50, 50]  # mm
if is_running_on_desktop:
    n_objects = 2
else:
    n_objects = randint(low=8, high=len(constants.Materials)-1)

# object settings
f_max = 15
n_iter = 5
n_pnts = 15
frequency_power_decrease_rate = 1
objectname_prefix = 'object_'


# print settings
class Print:
    script = True
    macro = True
    cst_output = True
