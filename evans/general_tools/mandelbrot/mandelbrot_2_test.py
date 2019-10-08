import numpy as np
from matplotlib import pyplot as plt
from matplotlib import colors
from mandelbrot_2 import mandelbrot_set


image_counter = 30


def save_image(fig):
    global image_counter
    filename = "mandelbrodt_%d.png" % image_counter
    image_counter += 1
    fig.savefig(filename)


def mandelbrot_image(xmin, xmax, ymin, ymax, width=10, height=10, maxiter=256):
    dpi = 72
    img_width = dpi * width
    img_height = dpi * height
    x, y, z = mandelbrot_set(xmin, xmax, ymin, ymax, img_width, img_height, maxiter)

    fig, ax = plt.subplots(figsize=(width, height), dpi=72)
    ticks = np.arange(0, img_width, 3 * dpi)
    x_ticks = xmin + (xmax - xmin) * ticks / img_width
    plt.xticks(ticks, x_ticks)
    y_ticks = ymin + (ymax - ymin) * ticks / img_width
    plt.yticks(ticks, y_ticks)

    ax.imshow(z.T, origin="lower")

    save_image(fig)


mandelbrot_image(-2.0, 0.5, -1.25, 1.25)
mandelbrot_image(-0.8, -0.7, 0, 0.1, maxiter=1024)
