import shutil
import zipfile
from pathlib import Path
import os
import random
from .materials import Materials

import settings
import util.constants as constants
from util.generate_model import generate_model


class DstPaths:
    def __init__(self, folder: Path):
        self.model = str(folder.joinpath(constants.FileNames.model))
        self.zip = str(folder)
        self.project = str(folder.joinpath(constants.FileNames.project))
        self.model = str(folder
                         .joinpath(constants.DstPaths.dir_3d)
                         .joinpath(constants.FileNames.model))
        self.script = str(Path(folder).joinpath(constants.FileNames.script))
        self.macro = str(Path(folder)
                         .joinpath(constants.DstPaths.dir_3d)
                         .joinpath(constants.FileNames.macro))


def generate_cst_project():
    if settings.project_folder_name_n_zero_padding:
        root = Path(settings.project_root_folder_desktop)
    else:
        root = Path(settings.project_root_folder_server)
    dst_paths = None

    # create new (non-existing) project folder
    for idx in range(settings.max_projects):
        folder_name = \
            settings.project_folder_prefix + \
            str(idx).zfill(settings.project_folder_name_n_zero_padding)
        folder_path = root.joinpath(folder_name)

        if not folder_path.exists():
            print('creating project-folder: %s', str(folder_path))
            Path.mkdir(folder_path)
            dst_paths = DstPaths(folder_path)
            del folder_path
            print('\t...Done')
            break

    # copy & extract project template to project-folder
    print('extracting cst project template to project-folder...')
    with zipfile.ZipFile(constants.SrcPaths.project, 'r') as file:
        file.extractall(dst_paths.zip)
    print('\t...done')

    # generate random model and place it into project-folder
    materials = []
    failed = True
    while failed:
        try:
            materials = generate_model(dst_paths.model)
            failed = False
        except Exception as error:
            print('!' * 30)
            print('WARNING: FAILED TO GENERATE MODEL, ERROR : ')
            print(error)
            print('END OF ERROR, TRYING AGAIN')
            print('!' * 30)
            failed = True
            exit()

    # load generated model into CST project
    print('loading generated model into CST project...')
    load_model_into_cst_project(dst_paths, materials)
    print('\t...done')

    # remove script
    os.remove(dst_paths.script)


def load_model_into_cst_project(dst_paths: DstPaths, materials: Materials):
    line = '-' * 50

    # first generate script and macro
    print('\t...generating script & macro')
    script, macro = generate_macro_and_script(dst_paths, materials)

    # print macro and script to console for debugging
    print('/' * 25 + ' SCRIPT START ' + '\\' * 25)
    print(script)
    print('\\' * 25 + ' SCRIPT END ' + '/' * 25)
    print('/' * 25 + ' MACRO START ' + '\\' * 25)
    print(macro)
    print('\\' * 25 + ' MACRO END ' + '/' * 25)

    # write generated script & macro to project folder
    print('\t...writing generated script & macro to project-folder')
    with open(dst_paths.script, 'w') as file:
        file.write(script)
    with open(dst_paths.macro, 'w') as file:
        file.write(macro)

    # run script, which executes the macro
    #   NOTE: these can't be combined because of a bug in CST
    print('\t...executing script/macro')
    if settings.is_running_on_desktop:
        cst_exe = settings.path_cst_exe_desktop
    else:
        cst_exe = settings.path_cst_exe_server
    command = '"%s" -m "%s"' % (str(Path(cst_exe)), dst_paths.script)
    os.system('"' + command + '"')


def generate_macro_and_script(dst_paths: DstPaths,
                              materials: Materials) -> [str, str]:
    s = ''  # script
    m = ''  # macro

    # read base script and macro into string
    with open(constants.SrcPaths.script, 'r') as file:
        s += file.read()
    with open(constants.SrcPaths.macro, 'r') as file:
        m += file.read()

    # insert path of CST project
    s = s.replace(constants.ScriptVariables.project_path, dst_paths.project)

    # insert path of randomly generated model
    m = m.replace(constants.MacroVariables.model_path, dst_paths.model)

    # insert material properties
    m = m.replace(constants.MacroVariables.densities, materials.densities())
    m = m.replace(constants.MacroVariables.reds, materials.reds())
    m = m.replace(constants.MacroVariables.greens, materials.greens())
    m = m.replace(constants.MacroVariables.blues, materials.blues())
    m = m.replace(constants.MacroVariables.n_materials, '"%i"' % materials.n)
    m = m.replace(constants.MacroVariables.object_names,
                  materials.object_names())
    m = m.replace(constants.MacroVariables.permittivities,
                  materials.permittivities())
    m = m.replace(constants.MacroVariables.conductivities,
                  materials.conductivities())

    return s, m
