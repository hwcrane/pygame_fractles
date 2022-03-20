import numpy as np
from matplotlib import cm
import pygame as pg
import colorsys

WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 1000
COLOUR_MAP = cm.get_cmap('inferno')


def setup_window(width: int, height: int, name: str) -> pg.surface.Surface:
    pg.init()
    window = pg.display.set_mode((width, height))
    pg.display.set_caption(name)
    return window


def make_colour(n, max):
    # if n == -1:
    #     return (0, 0, 0)
    # n = [round(i * 255)
    #      for i in colorsys.hsv_to_rgb(1 - (n / max), (n / max), 1)]
    return [round(i * 255) for i in COLOUR_MAP(n/max)[:3]]


def create_number_array(width: int, height: int, zoom: int, central_point: tuple[float, float]) -> np.array:
    x = np.linspace(central_point[0] - 3 / 2**zoom,
                    central_point[0] + 3 / 2**zoom, num=width, dtype=np.complex128).reshape((1, width))
    y = np.linspace(central_point[1] - 3 / 2**zoom, central_point[1] +
                    3 / 2**zoom, num=height, dtype=np.complex128).reshape((height, 1))
    return x + 1j * y


def compute_pixels(C: np.array, iterations: int) -> np.array:
    Z = np.zeros(C.shape, dtype=np.complex128)
    M = np.full(C.shape, True, dtype=bool)
    pixels = np.zeros(C.shape, dtype=int)
    for n in range(iterations):
        Z[M] = Z[M] * Z[M] + C[M]
        has_left = np.greater(
            np.abs(Z), 2, out=np.full(C.shape, False), where=M)
        pixels[has_left] = n
        M[np.abs(Z) > 2] = False
    # pixels[np.abs(Z) <= 2] = -1
    return np.flipud(pixels)


def draw_pixels(pixels: np.array, window: pg.surface.Surface, num_iterations: int) -> None:
    height, width = pixels.shape
    for x in range(width):
        for y in range(height):
            window.set_at((x, y), make_colour(pixels[y, x], num_iterations))
    pg.display.flip()


if __name__ == '__main__':
    window = setup_window(WINDOW_WIDTH, WINDOW_HEIGHT, 'Mandelbrot Set')
    for i in range(1, 100):
        num_iterations = round(25 * 4 * i)
        c_arr = create_number_array(
            WINDOW_WIDTH, WINDOW_HEIGHT, i, (-0.789374599271466936740382412558, 0.163089252677526719026415054868))
        pixels = compute_pixels(c_arr, num_iterations)
        draw_pixels(pixels, window, num_iterations)
        pg.image.save(window, f'zoom/zoom' + f'{i}'.rjust(3, '0') + '.png')
        print(i)
    print('done')
    while True:
        pass
