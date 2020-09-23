setup_with_gui = False


class SrcPaths:
    project = 'data/project_template.zip'
    script = 'data/script_template.bas'
    macro = 'data/macro_template.mcs'
    step = 'data/step_template.stp'
    object = 'data/tmp_object.stp'


class FileNames:
    project = 'project.cst'
    project_dir = 'project'
    model = 'model.stp'
    macro = 'macro.mcs'
    script = 'script.bas'
    materials = 'materials.json'


class RelativePaths:
    macro = 'project/Model/3D'
    model = 'project'


class StepVariables:
    content = '$content'


class ScriptVariables:
    project_path = '$project_path'


class MacroVariables:
    model_path = '$model_path'
    object_names = '$object_names'
    permittivities = '$permittivities'
    densities = '$densities'
    conductivities = '$conductivities'
    reds = '$reds'
    greens = '$greens'
    blues = '$blues'
    n_materials = '$n_materials'


class Print:
    line_length = 80


class Colors:
    maroon = (128, 0, 0)
    brown = (170, 110, 40)
    olive = (128, 128, 0)
    teal = (0, 128, 128)
    navy = (0, 0, 128)
    black = (0, 0, 0)
    red = (230, 25, 75)
    orange = (245, 120, 48)
    yellow = (255, 255, 25)
    lime = (210, 245, 60)
    green = (60, 180, 75)
    cyan = (70, 240, 240)
    blue = (0, 120, 200)
    purple = (145, 30, 180)
    magenta = (240, 50, 230)
    grey = (128, 128, 128)
    pink = (250, 190, 212)
    apricot = (255, 215, 180)
    beige = (255, 250, 200)
    mint = (170, 255, 195)
    lavender = (220, 190, 255)
    white = (255, 255, 255)


class Material:
    def __init__(self,
                 name,
                 permittivity,
                 density,
                 conductivity,
                 color):
        self.name = name
        self.object_name = None
        self.permittivity = permittivity
        self.density = density
        self.conductivity = conductivity
        self.red = color[0] / 255.0
        self.green = color[1] / 255.0
        self.blue = color[2] / 255.0

    def to_dict(self):
        return {'name': self.name,
                'object_name': self.object_name,
                'permittivity': self.permittivity,
                'density': self.density,
                'conductivity': self.conductivity,
                'red': self.red,
                'green': self.green,
                'blue': self.blue}


Materials = [
    Material('air', 1, 0, 0, Colors.blue),
    Material('bone', 13, 0.09, 1990, Colors.beige),
    Material('fat', 12, 0.08, 916, Colors.yellow),
    Material('muscle', 57, 0.80, 1041, Colors.red),
    Material('bloodvessel', 47, 0.57, 1060, Colors.maroon),
    Material('bonemarrow', 6, 0.03, 1027, Colors.grey),
    Material('brain', 57, 0.75, 1039, Colors.purple),
    Material('cartilage', 45, 0.60, 1100, Colors.teal),
    Material('esophagus', 67, 1.01, 1040, Colors.orange),
    Material('spinalcord', 42, 0.45, 1043, Colors.lavender),
    Material('thyroid', 61, 0.89, 1050, Colors.olive),
    Material('tooth', 13, 0.09, 2160, Colors.mint),
    Material('tumour', 59, 0.89, 1050, Colors.magenta)
]
