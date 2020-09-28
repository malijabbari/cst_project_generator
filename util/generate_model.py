import time
from pathlib import Path
from typing import List

import numpy as np

import settings
import util.constants as constants
from .freecad import App, Gui, Part, Draft, Import
from .generate_object import generate_object
from .materials import Materials


def generate_model(dst: str, job_id: int, print_):
    documentname = 'model_generator'

    time_start = time.time()

    # check if dst file does not exist yet
    if Path(dst).exists():
        raise Exception('MODEL GENERATION ERROR: dst=%s already exists' % dst)

    # determine object_ids, placement & scales. These are chosen at random
    placements = _random_placements(settings.limit_placement,
                                    settings.n_objects)
    scales = _random_scales(settings.limit_scale, settings.n_objects)
    insert_order = _order_scales_by_magnitude(scales)

    # print_('-' * constants.Print.line_length)
    # for idx in range(len(scales)):
    #     xyz = placements[idx].Base
    #     rpy = placements[idx].Rotation.RawAxis
    #     print_('% -13s %i' % ('id:', idx))
    #     print_('% -13s x=% -7.2f y=% -7.2f z=% -7.2f' %
    #           ('placement:', xyz.x, xyz.y, xyz.z))
    #     print_('% -13s r=% -7.2f p=% -7.2f y=% -7.2f' % (
    #         '', rpy.x, rpy.y, rpy.z))
    #     print_('% -13s x=% -7.2f y=% -7.2f z=% -7.2f' % (
    #         'scale:', scales[idx].x, scales[idx].y, scales[idx].z))
    #     print_('% -13s %i' % ('insert_order', insert_order[idx]))
    #     print_('-' * constants.Print.line_length)

    # create document
    doc = App.newDocument(documentname)

    print_('\tgenerating objects...')
    objects, materials = _generate_objects(doc, job_id, print_)
    print_('\t\t...done')

    print_('\tmoving objects...')
    objects = _move_objects(objects, placements, print_)
    print_('\t\t...done')

    print_('\tchanging object scale...')
    objects = _scale_objects(objects, scales, print_)
    print_('\t\t...done')

    print_('\tinserting objects into one another...')
    for idx_insert in range(1, len(insert_order)):
        # insert objects[idx] into all object with index < idx
        for idx_base in range(idx_insert):
            objects[idx_base], objects[idx_insert] = _insert_object(
                objects[idx_base], objects[idx_insert], print_)
    print_('\t\t...done')

    print_('\tApplying cylindrical boundary...')
    objects = _bound_objects_by_cylinder(objects,
                                         settings.boundary_radius,
                                         settings.boundary_height)
    print_('\t\t...done')

    print_('\texporting model...')
    Import.export(objects, dst)
    print_('\t\t...done')

    print_('\tclosing document...')
    App.closeDocument(doc.Name)
    print_('\t\t...done')

    print_('\tfinished generating model in %.2f seconds' %
           (time.time() - time_start))
    # print_('\tFINISHED GENERATING MODEL (%.2f sec)'
    # % (time.time() - time_start))
    # print_('=' * constants.Print.line_length)

    return materials


def _random_placements(limit: [float, float], n: int) -> List[App.Placement]:
    displacements = []
    for _ in range(n):
        location = np.random.uniform(low=limit[0], high=limit[1], size=3)
        rotation = np.random.uniform(low=0, high=360, size=3)
        displacement = App.Placement(App.Vector(*location),
                                     App.Rotation(*rotation))
        displacements.append(displacement)
    return displacements


def _random_scales(limit: [float, float], n: int) -> List[App.Vector]:
    scales = []
    for _ in range(n):
        xyz = np.random.uniform(low=limit[0], high=limit[1], size=3)
        scales.append(App.Vector(*xyz))
    return scales


def _order_scales_by_magnitude(scales):
    magnitudes = []
    for scale in scales:
        x, y, z = scale.x, scale.y, scale.z
        magnitude = (x ** 2 + y ** 2 + z ** 2) ** 0.5
        magnitudes.append(magnitude)
    return np.argsort(-np.array(magnitudes))


def _move_objects(objects, placements, print_):
    for obj, placement in zip(objects, placements):
        xyz = placement.Base
        rpy = placement.Rotation.RawAxis
        print_('\t\tplacing %s at x=% -7.2f y=% -7.2f z=% -7.2f '
               'roll=% -7.2f pitch=% -7.2f yaw=% -7.2f' %
               (obj.Label, xyz.x, xyz.y, xyz.z, rpy.x, rpy.y, rpy.z))
        obj.Placement = placement
    return objects


def _scale_objects(objects, scales, print_):
    """
    weirdly, the objects can't be scaled directly. So instead, a clone is
    made, which is then scaled and the original object is deleted
    """
    for (object_idx, obj), scale in zip(enumerate(objects), scales):
        print_('\t\tscaling %s by x=% -7.2f y=% -7.2f z=% -7.2f' %
               (obj.Label, scale.x, scale.y, scale.z))
        label = obj.Label
        clone = Draft.clone(obj, forcedraft=True)
        clone.Scale = scale
        obj.Document.recompute()
        obj.Document.removeObject(obj.Name)
        clone.Label = label
        objects[object_idx] = clone
    # recompute needs to be called for the scaling to take effect
    objects[0].Document.recompute()
    return objects


def _insert_object(obj_base, obj_insert, print_):
    """
    Insert object1 into object2 is unfortunately not directly possible in
    FreeCAD. However, it is possible to cut one object from another.
    This function thus cuts object_insert from object_base, removes the
    original object_base (as it is replaced by object_cut) and returns the
    cut object and the insert object.
    """
    print_('\t\tInserting object %s into %s' %
           (obj_base.Label, obj_insert.Label))
    doc = obj_insert.Document
    # create & compute cut
    cut = doc.addObject('Part::Cut', 'Cut')
    cut.Base = obj_base
    cut.Tool = obj_insert
    doc.recompute()
    # change base shape to that of cut
    obj_base.Shape = Part.Solid(cut.Shape)
    # remove cut and set both objects to visible as they are hidden when
    # creating the cut
    doc.removeObject(cut.Name)
    # doc.recompute()
    if constants.setup_with_gui:
        gui_doc = Gui.getDocument(doc.Name)
        gui_doc.getObject(obj_insert.Name).Visibility = True
        gui_doc.getObject(obj_base.Name).Visibility = True
    doc.recompute()
    # return the new object_base and object_insert
    return obj_base, obj_insert


def _generate_objects(doc, job_id: int, print_):
    objects = []
    materials = Materials(settings.n_objects)
    for idx in range(settings.n_objects):
        label = settings.objectname_prefix + '%03i' % idx
        print_('\t\tgenerating %s' % label)
        generate_object(job_id)
        obj = Import.insert(constants.SrcPaths.object(job_id), doc.Name)[0][0]
        obj.Label = label
        materials.materials[idx].object_name = label
        objects.append(obj)
        App.setActiveDocument(doc.Name)
    return objects, materials


def _bound_objects_by_cylinder(objects, radius, height):
    doc = objects[0].Document
    # create cylinder, NOTE: it is created along the y-axis
    cylinder = doc.addObject('Part::Cylinder', 'cylinder')
    cylinder.Height = height[1] - height[0]
    cylinder.Radius = radius
    cylinder.Placement.Base = [0, height[0], 0]
    cylinder.Placement.Rotation = App.Rotation(App.Vector(1, 0, 0), -90)
    doc.recompute()
    # intersect the cylinder with each object
    for obj in objects:
        # intersect object and cylinder
        intersect = doc.addObject('Part::MultiCommon', 'intersect')
        intersect.Shapes = [obj, cylinder]
        doc.recompute()
        # change objects shape to that of the intersect and remove the
        # intersect
        obj.Shape = intersect.Shape
        doc.removeObject(intersect.Name)
        # make objects visible again since applying intersect will hide them
        if constants.setup_with_gui:
            gui_doc = Gui.getDocument(doc.Name)
            gui_doc.getObject(obj.Name).Visibility = True
            gui_doc.getObject(cylinder.Name).Visibility = True
        doc.recompute()
    # remove cylinder
    doc.removeObject(cylinder.Name)
    doc.recompute()
    return objects
