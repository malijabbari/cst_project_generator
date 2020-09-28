import json
import subprocess
import time
import zipfile
from pathlib import Path
from typing import Union

import settings
import util.constants as constants
from util.freecad import Part
from util.generate_model import generate_model
from util.print import Print
from util.script_generator import generate_script


def join_path(*pieces: Union[str, Path]) -> str:
    # convert first piece to Path obj if it's a string, if it is already a
    # Path obj, use that
    path = Path(pieces[0]) if isinstance(pieces[0], str) else pieces[0]
    for piece in pieces[1:]:
        path = path.joinpath(piece)
    return str(path)


class DstPaths:
    def __init__(self, folder: Path):
        self.model = join_path(folder, constants.FileNames.model)
        self.zip = str(folder)
        self.project = join_path(folder, constants.FileNames.project)
        self.materials = join_path(folder, constants.FileNames.materials)
        self.model2d = join_path(folder, constants.FileNames.model2d)
        self.script = join_path(folder, constants.FileNames.script)
        self.log = join_path(folder, constants.FileNames.log)
        self.model = join_path(folder,
                               constants.RelativePaths.model,
                               constants.FileNames.model)
        self.macro = join_path(folder,
                               constants.RelativePaths.macro,
                               constants.FileNames.macro)


def generate_cst_project(job_id: int, partition_id: int):
    time_start = time.time()
    root = Path(settings.project_root)
    dst_paths = None
    print_ = None
    print('\n')
    print('#' * constants.Print.line_length)
    print('GENERATING CST PROJECT\n')

    # create new (non-existing) project folder
    for idx in range(settings.max_projects):
        folder_name = \
            settings.project_folder_prefix + \
            str(idx).zfill(settings.project_folder_name_n_zero_padding)
        folder_path = root.joinpath(folder_name)

        try:
            Path.mkdir(folder_path)
            dst_paths = DstPaths(folder_path)
            print_ = Print(dst_paths.log, job_id, partition_id).log
            print_('creating project-folder...')
            print_('\t%s' % str(folder_path))
            del folder_path
            print_('\t...Done')
            break
        except FileExistsError:
            pass

    # copy & extract project template to project-folder
    print_('extracting cst project template to project-folder...')
    with zipfile.ZipFile(constants.SrcPaths.project, 'r') as file:
        file.extractall(dst_paths.zip)
    print_('\t...done')

    # generate random patient model and place it into project-folder
    materials = generate_patient_model(dst_paths.model, job_id, print_)

    # export materials
    print_('exporting materials...')
    print_('\t%s' % dst_paths.materials)
    with open(dst_paths.materials, 'w+') as file:
        json.dump(materials.to_dict_arr(), file)
    print_('\t...done')

    # generate basic script which loads the patient model into CST,
    #   starts the simulation and exports the e-fields
    print_('generating script...')
    generate_script(dst_paths, materials, print_)
    print_('\t...done')

    print_('executing script...')
    execute_script(dst_paths, print_)
    print('\t...done')

    print_('\nFINISHED GENERATING MODEL IN %.2f min' %
           ((time.time() - time_start) / 60.0))
    print_('#' * constants.Print.line_length)
    print_('\n')


def execute_script(dst_paths: DstPaths, print_) -> None:
    # define command that executes the script
    command = '"%s" -m -withgpu=%i -numthreads=%i "%s"' % \
              (settings.path_cst, settings.n_gpu, settings.n_threads,
               dst_paths.script)
    print_('\tCommand: %s' % command)

    # execute script
    cst_msg = subprocess.check_output(command, shell=True).decode('utf-8')

    # print output cst
    print('\t\toutput CST:')
    if settings.Print.cst_output:
        cst_msg = '\t\t\t| ' + \
                  cst_msg.replace('\r', '').replace('\n', '\n\t\t\t| ')
        print_(cst_msg)


def generate_patient_model(path_model, job_id, print_):
    materials = []
    failed = True
    print_('generating random patient-model...')
    while failed:
        try:
            materials = generate_model(path_model, job_id, print_)
            failed = False
        except Part.OCCError:
            print_('...FAILED: Part.OCCError occurred')
            print_('Attempting to generate different model')
        except Exception as error:
            print_('!' * constants.Print.line_length)
            print_('WARNING: FAILED TO GENERATE MODEL, ERROR : ')
            print_(error)
            print_('END OF ERROR, TRYING AGAIN')
            print_('!' * constants.Print.line_length)
    print_('\t...done')

    return materials
