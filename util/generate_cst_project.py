import subprocess
import json
import os
import time
import zipfile
from pathlib import Path

import settings
import util.constants as constants
from util.freecad import Part
from util.generate_model import generate_model
from .materials import Materials


class DstPaths:
    def __init__(self, folder: Path):
        self.model = str(folder.joinpath(constants.FileNames.model))
        self.zip = str(folder)
        self.project = str(folder.joinpath(constants.FileNames.project))
        self.model = str(folder
                         .joinpath(constants.RelativePaths.model)
                         .joinpath(constants.FileNames.model))
        self.script = str(Path(folder).joinpath(constants.FileNames.script))
        self.macro = str(Path(folder)
                         .joinpath(constants.RelativePaths.macro)
                         .joinpath(constants.FileNames.macro))
        self.materials = str(Path(folder)
                             .joinpath(constants.FileNames.materials))
        self.model2d = str(Path(folder).joinpath(constants.FileNames.model2d))


def generate_cst_project(job_id: int):
    print('\n')
    print('#' * constants.Print.line_length)
    print('GENERATING CST PROJECT\n')
    time_start = time.time()
    if settings.is_running_on_desktop:
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

        try:
            Path.mkdir(folder_path)
            print('creating project-folder')
            print('\t%s' % str(folder_path))
            dst_paths = DstPaths(folder_path)
            del folder_path
            print('\t...Done')
            break
        except FileExistsError:
            pass

    # copy & extract project template to project-folder
    print('extracting cst project template to project-folder...')
    with zipfile.ZipFile(constants.SrcPaths.project, 'r') as file:
        file.extractall(dst_paths.zip)
    print('\t...done')

    # generate random model and place it into project-folder
    materials = []
    failed = True
    print('generating random patient-model...')
    while failed:
        try:
            materials = generate_model(dst_paths.model, job_id)
            failed = False
        except Part.OCCError:
            print('...FAILED: Part.OCCError occurred')
            print('Attempting to generate different model')
        except Exception as error:
            print('!' * constants.Print.line_length)
            print('WARNING: FAILED TO GENERATE MODEL, ERROR : ')
            print(error)
            print('END OF ERROR, TRYING AGAIN')
            print('!' * constants.Print.line_length)
    print('\t...done')

    # export materials
    print('exporting materials...')
    print('\t%s' % dst_paths.materials)
    with open(dst_paths.materials, 'w+') as file:
        json.dump(materials.to_dict_arr(), file)
    print('\t...done')

    # load generated model into CST project
    print('loading generated model into CST project...')
    load_model_into_cst_project(dst_paths, materials)
    print('\t...done')

    print('\nFINISHED GENERATING MODEL IN %.2f min' %
          ((time.time() - time_start) / 60.0))
    print('#' * constants.Print.line_length)
    print('\n')


def load_model_into_cst_project(dst_paths: DstPaths, materials: Materials):
    # first generate script and macro
    print('\tgenerating script & macro')
    script, macro = generate_macro_and_script(dst_paths, materials)
    # print macro and script
    if settings.Print.script:
        print('\t\tScript:')
        print('\t\t\t| ' + script.replace('\n', '\n\t\t\t| '))
    if settings.Print.macro:
        print('\t\tMacro:')
        print('\t\t\t| ' + macro.replace('\n', '\n\t\t\t| '))
    print('\t\t...done')

    # write generated script & macro to project folder
    print('\twriting generated script & macro to project-folder')
    print('\t\twriting script: %s' % dst_paths.script)
    with open(dst_paths.script, 'w+') as file:
        file.write(script)
    if not Path(dst_paths.script).exists():
        raise Exception('ERROR: did not write script (%s) for some reason. '
                        'Hint make sure that folder has execution rights'
                        % dst_paths.script)
    print('\t\twriting macro: %s' % dst_paths.macro)
    with open(dst_paths.macro, 'w+') as file:
        file.write(macro)
    if not Path(dst_paths.macro).exists():
        raise Exception('ERROR: did not write macro (%s) for some reason. '
                        'Hint make sure that folder has execution rights'
                        % dst_paths.macro)
    print('\t\t...done')

    # run script, which executes the macro
    #   NOTE: these can't be combined because of a bug in CST
    print('\texecuting script/macro')
    if settings.is_running_on_desktop:
        cst_exe = settings.path_cst_exe_desktop
    else:
        cst_exe = settings.path_cst_exe_server
    command = '"%s" -m "%s"' % (str(Path(cst_exe)), dst_paths.script)
    print('\t\trunning command: %s' % command)
    if settings.is_running_on_desktop:
        cst_msg = subprocess.check_output(command).decode('utf-8')
    else:
        cst_msg = subprocess.check_output(command, shell=True).decode('utf-8')
    # format & print cst_msg
    if settings.Print.cst_output:
        cst_msg = '\t\t\t| ' + \
                  cst_msg.replace('\r', '').replace('\n', '\n\t\t\t| ')
        print(cst_msg)
    # else:
    #     os.system(command)
    print('\t\t...done')

    # remove script
    print('\tRemoving script...')
    os.remove(dst_paths.script)
    print('\t\t...Done')


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

    # insert path of exported 2D model
    s = s.replace(constants.ScriptVariables.model2d_path, dst_paths.model2d)

    # insert RELATIVE path of randomly generated model
    #   if not relative: model can't be loaded on windows if generated in
    #   linux and vice versa
    m = m.replace(constants.MacroVariables.model_path,
                  constants.FileNames.model)

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
