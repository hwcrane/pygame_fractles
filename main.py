import pygame as pg
import colorsys


def make_colour(n, max):
    n = [round(i * 255)
         for i in colorsys.hsv_to_rgb(n / max, 1, 1)]
    return n


def fract(x, y, max):
    c1 = complex(x, y)
    c2 = 0
    for n in range(1, max):
        if abs(c2) > 2:
            return make_colour(n, max)
        c2 = c2 * c2 + c1
    return (0, 0, 0)


if __name__ == '__main__':
    pg.init()
    window = pg.display.set_mode((1600, 900))

    central_point = (-200, 0)
    for i in range(1, 200, 50):
        print(i)
        topleft = [(central_point[0] - window.get_width() // 2) / 300,
                   (central_point[1] - window.get_height() // 2) / 300]
        step = 1 / 300

        for x in range(window.get_width()):
            for y in range(window.get_height()):
                colour = fract(topleft[0] + x * step,
                               topleft[1] + y * step, i)
                window.set_at((x, y), tuple(colour))

        pg.display.flip()

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
        pg.image.save(window, f'frame' + f'{i}'.rjust(3, '0') + '.png')

    running = True
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
    pg.quit()
