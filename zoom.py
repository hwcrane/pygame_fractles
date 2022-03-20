import numpy as np
from matplotlib import cm
import pygame as pg

WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 1000

# Which matplotlip colourmao to use
# Can find maps at: https://matplotlib.org/stable/tutorials/colors/colormaps.html
COLOUR_MAP = cm.get_cmap('inferno')

# Central Point to zoom into
# MIDPOINT = (-0.789374599271466936740382412558,
#             0.163089252677526719026415054868)
MIDPOINT = (-0.9223327810370947027656057193752719757635,
            0.3102598350874576432708737495917724836010)


def setup_window(width: int, height: int, name: str) -> pg.surface.Surface:
    '''Sets up the pygame window'''

    pg.init()
    window = pg.display.set_mode((width, height))
    pg.display.set_caption(name)
    return window


def make_colour(n: int, max: int) -> tuple[int, int, int]:
    '''Creates an RGB colour tupple based on `n`, the number of iterations for a pixel to escape
        `max`: Max number of iterations
    '''
    return tuple(round(i * 255) for i in COLOUR_MAP(n/max)[:3])


def create_number_matrix(width: int, height: int, zoom: int, central_point: tuple[float, float]) -> np.array:
    '''Creates a matrix of complex numbers:
       - of width `width` and height `height` 
       - centered on `central point`
       - zoomed in by a factor of `zoom`'''

    xcenter = central_point[0]
    ycenter = central_point[1]

    give = 3 / 2**zoom

    xstart = xcenter - give
    xend = xcenter + give
    ystart = ycenter - give
    yend = ycenter + give

    # Create matrix of complex numbers representing pixel values
    x = np.linspace(xstart, xend, num=width,
                    dtype=np.complex128).reshape((1, width))
    y = np.linspace(ystart, yend, num=height,
                    dtype=np.complex128).reshape((height, 1))
    return x + 1j * y


def compute_pixels(C: np.array, iterations: int) -> np.array:
    '''Applies the Mandelbrot Set formula to each complex number in C for the set number of iterations'''

    # Array to store the complex numbers
    Z = np.zeros(C.shape, dtype=np.complex128)

    # Array to store which pixels have not escaped
    M = np.full(C.shape, True, dtype=bool)

    # Array to store which iteration each pixel escaped (Their colour)
    pixels = np.zeros(C.shape, dtype=int)
    for n in range(iterations):

        # Mandelbrot set formula, only applied to numbers which have not escaped
        Z[M] = Z[M] * Z[M] + C[M]

        # Finds all new pixels that have escaped
        has_left = np.greater(
            np.abs(Z), 2, out=np.full(C.shape, False), where=M)

        # Saves iteration the pixels left
        pixels[has_left] = n

        # Saves pixels that have escaped so their iteration is not overitten
        M[np.abs(Z) > 2] = False

    # Flips array so correct orientation
    return np.flipud(pixels)


def draw_pixels(pixels: np.array, window: pg.surface.Surface, num_iterations: int) -> None:
    '''Draws each pixel to the screen'''

    height, width = pixels.shape
    for x in range(width):
        for y in range(height):
            window.set_at((x, y), make_colour(pixels[y, x], num_iterations))
    pg.display.flip()


if __name__ == '__main__':
    window = setup_window(WINDOW_WIDTH, WINDOW_HEIGHT, 'Mandelbrot Set')

    for i in range(1, 59):
        num_iterations = round(25 * 4 * i)
        c_arr = create_number_matrix(
            WINDOW_WIDTH, WINDOW_HEIGHT, i, MIDPOINT)
        pixels = compute_pixels(c_arr, num_iterations)
        draw_pixels(pixels, window, num_iterations)
        pg.image.save(window, f'zoom2/zoom' + f'{i}'.rjust(3, '0') + '.png')
        print(i)

    print('done')
    pg.exit()
