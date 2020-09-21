import numpy as np
import matplotlib.pyplot as plt
import mpl_toolkits


def normal_distribution(n):
    x = np.linspace(0, 3, n)
    return np.exp(-0.5 * x ** 2)


def random_2d_shapes():
    n_points = 21
    f_max = 11
    f = normal_distribution(f_max) * np.exp(
        1j * np.random.normal(0, 2 * np.pi, f_max))
    s = np.fft.ifft(f, n_points)
    a = np.linspace(0, 2 * np.pi, n_points + 1)
    s = np.append(s, s[0])
    A = np.absolute(s)
    x = A * np.cos(a)
    y = A * np.sin(a)
    plt.plot(s.real)
    plt.plot(s.imag)
    plt.plot(np.absolute(s))
    fig, axs = plt.subplots(1, 2)
    axs[0].stem(np.absolute(f))
    axs[1].plot(np.absolute(np.angle(f)) * 180 / np.pi)
    plt.figure()
    plt.plot(x, y)
    plt.show()


def random_2d_shapes2():
    n = 20
    r = np.random.normal(4, 1, n - 1)
    r = np.append(r, r[0])
    t = np.linspace(0, 2 * np.pi, n)
    plt.figure()
    plt.plot(r * np.cos(t), r * np.sin(t))
    plt.show()


def random_3d_shapes2():
    n = 20
    r = np.random.normal(8, 1, (n - 1, n - 1))
    r = np.vstack((r, r[0, :]))
    r = np.vstack((r.T, r[:, 0]))

    theta = np.linspace(0, np.pi, n)
    phi = np.linspace(0, 2 * np.pi, n)
    theta, phi = np.meshgrid(theta, phi)

    x = r * np.sin(theta) * np.cos(phi)
    y = r * np.sin(theta) * np.sin(phi)
    z = r * np.cos(theta)

    fig = plt.figure()
    ax = fig.gca(projection='3d')

    ax.plot_surface(x, y, z)
    plt.show()


def normal_distribution_2d(n):
    t = np.linspace(0, 5, n)
    x, y = np.meshgrid(t, t)
    # return np.exp(-0.5 * (y ** 2))
    return np.exp(-0.5 * (x ** 2 + y ** 2))


def generate_frequencies_2d(f_max):
    amplitude = normal_distribution_2d(f_max)
    phases = np.random.normal(0, 2 * np.pi, (f_max, f_max))
    frequencies = amplitude * np.exp(1j * phases)
    return frequencies


def scatter_plot_3d(x, y, z):
    ax = mpl_toolkits.mplot3d.Axes3D(plt.figure())
    ax.scatter(x, y, z)
    ax.set_box_aspect((1.0, 1.0, 1.0))
    ax.set_xlim(-1, 1)
    ax.set_ylim(-1, 1)
    ax.set_zlim(-1, 1)
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_zlabel('z')


def scatter_plot_2d(phi, theta):
    plt.figure()
    plt.scatter(phi * 180 / pi, theta * 180 / pi)
    plt.xlabel('phi')
    plt.ylabel('theta')
    plt.xlim(-180, 180)
    plt.ylim(0, 180)


def frequencies_to_samples(f, n_points):
    s = np.fft.ifft2(f, (n_points - 1, n_points - 1))
    s = np.vstack((s, s[0, :]))
    s = np.vstack((s.T, s[:, 0]))
    # s[:, 0] = np.mean(s[:, 0])
    # s[:, -1] = np.mean(s[:, -1])
    return s


def plot_frequencies(f, f_max):
    # only plots amplitudes for now
    f1, f2 = np.meshgrid(np.arange(f_max), np.arange(f_max))
    ax = mpl_toolkits.mplot3d.Axes3D(plt.figure())
    ax.plot_surface(f1, f2, np.absolute(f))
    ax.set_xlabel('f1')
    ax.set_ylabel('f2')
