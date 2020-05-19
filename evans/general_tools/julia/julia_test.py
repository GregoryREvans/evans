from collections import defaultdict
from math import ceil, floor

from PIL import Image, ImageDraw

from julia import julia


def linear_interpolation(color1, color2, t):
    return color1 * (1 - t) + color2 * t


# Image size (pixels)
WIDTH = 400
HEIGHT = 480

# Plot window
RE_START = -1
RE_END = 1
IM_START = -1.2

IM_END = 1.2

# c constant used to compute the julia set

c = complex(0.285, 0.01)
# Other interesting values:
# c = complex(-0.7269, 0.1889)
# c = complex(-0.8, 0.156)
# c = complex(-0.4, 0.6)

histogram = defaultdict(lambda: 0)
values = {}
for x in range(0, WIDTH):
    for y in range(0, HEIGHT):
        # Convert pixel coordinate to complex number
        z0 = complex(
            RE_START + (x / WIDTH) * (RE_END - RE_START),
            IM_START + (y / HEIGHT) * (IM_END - IM_START),
        )
        # Compute the number of iterations
        m = julia(c, z0, 80)

        values[(x, y)] = m
        if m < 80:
            histogram[floor(m)] += 1

total = sum(histogram.values())
hues = []
h = 0
for i in range(80):
    h += histogram[i] / total
    hues.append(h)
hues.append(h)

im = Image.new("HSV", (WIDTH, HEIGHT), (0, 0, 0))
draw = ImageDraw.Draw(im)

for x in range(0, WIDTH):
    for y in range(0, HEIGHT):
        m = values[(x, y)]
        # The color depends on the number of iterations
        hue = 255 - int(
            255 * linear_interpolation(hues[floor(m)], hues[ceil(m)], m % 1)
        )
        saturation = 255
        value = 255 if m < 80 else 0
        # Plot the point
        draw.point([x, y], (hue, saturation, value))

im.convert("RGB").save("julia.png", "PNG")
