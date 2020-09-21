from pathlib import Path

import matplotlib.pyplot as plt
import meshzoo
import mpl_toolkits
import numpy as np
import pyshtools
import scipy.interpolate
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from numpy import pi, sqrt, cos, sin, arccos, arctan2

import settings
import util.constants as constants
from .freecad import App, Part, Import


def generate_object():
    # generate mesh with equally distributed points on surface
    mesh, n_points = generate_unity_sphere(settings.n_iter)
    r0, phi0, theta0 = cartesian_to_spherical_coordinates(
        *points_to_xyz(mesh['points']))

    # generate random radii
    r, theta, phi = generate_random_radii(
        settings.f_max,
        settings.n_pnts,
        settings.frequency_power_decrease_rate)

    # map random radii on the equal distributed mesh
    r_new = interpolate(theta, phi, r, theta0, phi0)

    # change the mesh
    mesh['points'] = np.vstack(
        spherical_to_cartesian_coordinates(r_new, theta0, phi0)).T

    # create and save step file
    step_file = generate_step_file(mesh)
    with open(constants.SrcPaths.object, 'w') as file:
        file.write(step_file)

    convert_shell_stp_to_object_stp(constants.SrcPaths.object)

    # return the mesh
    return mesh


def generate_unity_sphere(n):
    xyz, v = meshzoo.icosa_sphere(n)
    return {'points': xyz, 'vertices': v}, xyz.shape[0]


def cartesian_to_spherical_coordinates(x, y, z):
    r = sqrt(x ** 2 + y ** 2 + z ** 2)
    phi = arctan2(y, x)
    theta = arccos(z / r)
    return r, phi, theta


def spherical_to_cartesian_coordinates(r, theta, phi):
    x = r * sin(theta) * cos(phi)
    y = r * sin(theta) * sin(phi)
    z = r * cos(theta)
    return x, y, z


def mesh_to_tri(mesh):
    """
    returns triangles with shape (n, v, xyz)
        n: number of triangles,
        v: 3 vertices
        xyz: x, y, z coordinate
    """
    xyz = mesh['points']
    x = xyz[:, 0]
    y = xyz[:, 1]
    z = xyz[:, 2]
    triangles = []
    for ids in mesh['vertices']:
        triangle = []
        for idx in ids:
            triangle.append([x[idx], y[idx], z[idx]])
        triangles.append(triangle)
    return np.array(triangles)


def points_to_xyz(points):
    return points[:, 0], points[:, 1], points[:, 2]


def plot_mesh(mesh):
    ax = mpl_toolkits.mplot3d.Axes3D(plt.figure(num='plot_mesh'))
    xyz = mesh['points']
    x, y, z = xyz[:, 0], xyz[:, 1], xyz[:, 2]
    v = mesh['vertices']
    ax.plot_trisurf(x, y, z, triangles=v)


def plot_radii(r, theta, phi):
    ax = mpl_toolkits.mplot3d.Axes3D(plt.figure(num='plot_radii'))
    ax.plot_surface(theta * 180 / pi, phi * 180 / pi, r)
    ax.set_xlabel('theta [deg]')
    ax.set_ylabel('phi [deg]')
    ax.set_zlabel('r')


def generate_random_radii(f_max, n_points, rate):
    power = np.exp(-rate * np.arange(f_max))
    if n_points > f_max:
        n = n_points - f_max
        power = np.append(power, [0] * n)
    cilm = pyshtools.SHCoeffs.from_random(power, kind='complex')
    r = np.absolute(cilm.expand().data)
    t = np.linspace(0, pi, r.shape[0])
    p = np.linspace(-pi, pi, r.shape[1])
    phi, theta = np.meshgrid(p, t)
    return r, theta, phi


def plot_transformed_radii(r, theta, phi, r_, theta_, phi_):
    ax = mpl_toolkits.mplot3d.Axes3D(plt.figure())
    ax.plot_surface(theta_ * 180 / pi, phi_ * 180 / pi, r_)
    ax.scatter(theta * 180 / pi, phi * 180 / pi, r)
    ax.set_xlabel('theta')
    ax.set_ylabel('phi')
    ax.set_zlabel('r')


def interpolate(x, y, z, x_new, y_new):
    x_flat = x.reshape(-1, 1)
    y_flat = y.reshape(-1, 1)
    z_flat = z.reshape(-1, 1)
    return scipy.interpolate.griddata(
        np.hstack((x_flat, y_flat)),
        z_flat,
        (x_new, y_new),
        method='cubic'
    ).reshape(-1)


def normal(triangle):
    a, b, c = triangle[0, :], triangle[1, :], triangle[2, :]
    n = np.cross((b - a), (c - a))
    n = n / sqrt(n[0] ** 2 + n[1] ** 2 + n[2] ** 2)
    return n


def normal2(triangle):
    a = (triangle[0, :] - triangle[1, :])
    return a / sqrt(a[0] ** 2 + a[1] ** 2 + a[2] ** 2)


def generate_step_file(mesh):
    # read empty step file into string
    empty_step_file_str = ''
    with open(constants.SrcPaths.step, 'r') as file:
        empty_step_file_str += file.read() + '\n'

    # generate content for step file as string
    idx0 = 33
    step = 11
    triangles = mesh_to_tri(mesh)
    s = ''
    idx = idx0
    tri_str = ''
    for idx2, tri in enumerate(triangles):
        if idx2 != 0:
            tri_str += ','
        tri_str += '#%i' % (idx + 4)
        idx += step
    s += "#%i = CLOSED_SHELL('',(%s));\n" % (idx0, tri_str)
    idx = idx0 + 1
    for tri in triangles:
        n1 = normal(tri)
        n2 = normal2(tri)
        c = (tri[0, :] + tri[1, :] + tri[2, :]) / 3
        for idx2, point in enumerate(tri):
            s += "#%i = CARTESIAN_POINT('',(%.8f,%.8f,%.8f));\n" % \
                 (idx + idx2, point[0], point[1], point[2])
        s += "#%i = ADVANCED_FACE('',(#%i),#%i,.T.);\n" % \
             (idx + 3, idx + 4, idx + 6)
        s += "#%i = FACE_BOUND('',#%i,.T.);\n" % \
             (idx + 4, idx + 5)
        s += "#%i = POLY_LOOP('', (#%i, #%i, #%i));\n" % \
             (idx + 5, idx, idx + 1, idx + 2)
        s += "#%i = PLANE('',#%i);\n" % \
             (idx + 6, idx + 7)
        s += "#%i = AXIS2_PLACEMENT_3D('',#%i,#%i,#%i);\n" % \
             (idx + 7, idx + 8, idx + 9, idx + 10)
        s += "#%i = CARTESIAN_POINT('',(%.8f,%.8f,%.8f));\n" % \
             (idx + 8, c[0], c[1], c[2])
        s += "#%i = DIRECTION('',(%.8f,%.8f,%.8f));\n" % \
             (idx + 9, n1[0], n1[1], n1[2])
        s += "#%i = DIRECTION('',(%.8f,%.8f,%.8f));\n" % \
             (idx + 10, n2[0], n2[1], n2[2])
        idx += step

    # place content into empty step file
    step_file_str = empty_step_file_str.replace(
        constants.StepVariables.content, s)
    return step_file_str


def convert_shell_stp_to_object_stp(filename: str):
    documentname = 'converter'

    # create unnamed document
    doc = App.newDocument(documentname)

    object_name = Path(filename).stem

    # import shape
    Import.insert(filename, documentname)[0][0]

    # make solid
    __s__ = doc.Compound.Shape.Faces
    __s__ = Part.Solid(Part.Shell(__s__))
    __o__ = doc.addObject("Part::Feature", object_name)
    __o__.Label = object_name
    __o__.Shape = __s__
    del __s__, __o__

    # export
    __objs__ = []
    __objs__.append(doc.getObject(object_name))
    Import.export(__objs__, filename)
    del __objs__

    # remove all objects
    for obj in doc.findObjects():
        doc.removeObject(obj.Name)

    # close document
    App.closeDocument(documentname)
