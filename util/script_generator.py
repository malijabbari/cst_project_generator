from pathlib import Path
from typing import List

import settings
import util.constants as constants
from util.materials import Materials


def generate_script(dst_paths, materials: Materials, print_) -> None:
    """
    This function generates a script which will load the patient model into
    the cst project, adjust simulation/mesh settings, simulate the project,
    and export the e-fields.

    The script execute commands and there are two types of commands.
    Commands that need to be remembered when reloading the CST project,
    like loading the patient-model and the simulation settings. And commands
    that do not have to be remembered/redone when reloading the
    project, such as starting the simulation or exporting the e-fields.
    Commands that need to be remembered are added to the history of CST,
    the others are not.
    """

    # read script and history template
    print('\tReading templates...')
    with open('data/script_template.bas', 'r') as file:
        s = file.read()
    with open('data/history_template.bas', 'r') as file:
        h = file.read()
    print('\t\t...done')

    # fill in variables
    print('\tInserting project-specific variables into script')
    h = h.replace('$model_path', constants.FileNames.model)
    h = h.replace('$object_names', materials.object_names())
    h = h.replace('$permittivities', materials.permittivities())
    h = h.replace('$densities', materials.densities())
    h = h.replace('$conductivities', materials.conductivities())
    h = h.replace('$reds', materials.reds())
    h = h.replace('$greens', materials.greens())
    h = h.replace('$blues', materials.blues())
    h = h.replace('$n_materials', str(materials.n))
    s = s.replace('$project_path', dst_paths.project)
    s = s.replace('$macro_path', dst_paths.macro)
    s = s.replace('$model2d_path', dst_paths.model2d)
    s = s.replace('$model_path', constants.FileNames.model)
    s = s.replace('$history_inline', to_inline(h))
    s = s.replace('$history', indent(h))
    print('\t\t...done')

    # print script to console for logging purposes
    if settings.Print.script:
        print_('\tScript:')
        print_('\t\t| ' + s.replace('\n', '\n\t\t| '))
    print_('\t\t...done')

    # write generated script to project folder
    print_('\twriting script to project-folder...')
    print_('\t\t%s' % dst_paths.script)
    with open(dst_paths.script, 'w+') as file:
        file.write(s)
    if not Path(dst_paths.script).exists():
        raise Exception('ERROR: did not write script (%s) for some reason. '
                        'Hint make sure that folder has execution rights'
                        % dst_paths.script)
    print('\t\t...done')

def to_inline(basic_script: str) -> str:
    """
    convert the given basic_script string content to a single inline command.
    """
    s = basic_script

    # convert tabs to 4 spaces
    s = s.replace('\t', '    ')

    # split at newline (\n), double quote (") and single quotes (')
    #   gives a triple list of strings
    s___: List[List[List[str]]] = []
    for idx1, line in enumerate(s.split('\n')):
        s___.insert(idx1, [])
        for idx2, split in enumerate(line.split('"')):
            s___[idx1].insert(idx2, [])
            for idx3, elem in enumerate(split.split("'")):
                s___[idx1][idx2].insert(idx3, elem)

    # wrap each element in double quotes
    for idx1 in range(len(s___)):
        for idx2 in range(len(s___[idx1])):
            for idx3 in range(len(s___[idx1][idx2])):
                s___[idx1][idx2][idx3] = '"%s"' % s___[idx1][idx2][idx3]

    # previously, the script was split at single quotes ('), recombine it
    # with basic script type of char character: Chr(39)
    s__: List[List[str]] = []
    for idx1, double_list in enumerate(s___):
        s__.insert(idx1, [])
        for idx2, single_list in enumerate(double_list):
            s__[idx1].insert(idx2, '+Chr(39)+'.join(single_list))

    # do the same for double quotes
    s_: List[str] = []
    for array in s__:
        s_.append('+Chr(34)+'.join(array))

    # to the same but for newlines
    s = '+Chr(10)+'.join(s_)

    # remove double plus
    s = s.replace('++', '+')

    # return the obtained inline script
    return s


def indent(basic_script: str) -> str:
    """
    Indent basic_script
    """
    return '    ' + basic_script.replace('\n', '\n    ')
