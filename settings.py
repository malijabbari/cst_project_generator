import os

from numpy.random import randint

import util.constants as constants

# project settings
project_folder_prefix = 'project_'
project_folder_name_n_zero_padding = 5
max_projects = 10000
is_running_on_desktop = os.name == 'nt'  # nt: Windows , posix: Linux
if is_running_on_desktop:
    n_projects = 1
    path_freecad = 'C:/Program Files/FreeCAD/FreeCAD_0.19.22474/bin'
    path_cst = 'C:/Program Files (x86)/CST Studio Suite 2020/' \
               'CST DESIGN ENVIRONMENT.exe'
    project_root = 'C:/Users/Dennis/Documents/generated_projects'
else:
    n_projects = 156
    n_projects = 1  # todo: delete
    path_freecad = '/home/tue/s111167/freecad/lib'
    path_cst = '/cm/shared/apps/cst/CST_STUDIO_SUITE_2020' \
               '/cst_design_environment'
    project_root = '/home/tue/s111167/generated_projects2'

# model settings
export_filename_prefix = 'model_'
limit_placement = [-50, 50]  # mm
limit_scale = [10, 100]  # mm
boundary_radius = 100  # mm
boundary_height = [-50, 50]  # mm
if is_running_on_desktop:
    n_objects = 2
else:
    n_objects = randint(low=8, high=len(constants.Materials) - 1)
    n_objects = 2  # todo: delete

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
