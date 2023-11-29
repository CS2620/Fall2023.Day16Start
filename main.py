# This program requires pillow
# `python -m pip` to install pillow

from PIL import Image
from container import Container
from layer import Layer
from color_conversion import rgb_to_cmyk
import time
import numpy as np
import os
import math


def one_scaling_transforms():
    file = "band.jpg"

    container = get_layer_from_file("./images/" + file)
    container.layers[0].scale_backward(.5,.5)
    container.pack()
    container.save("done_" + file + "_scale_backward.png")

    container = get_layer_from_file("./images/" + file)
    container.layers[0].scale_forward(.5,.5)
    container.pack()
    container.save("done_" + file + "_scale_forward.png")

def one_advanced_transforms():
    file = "beaches.jpg"

    container = get_layer_from_file("./images/" + file)
    container.layers[0].rotate_same_size(45*2*math.pi/360)
    container.pack()
    container.save("done_" + file + "_rotate_same_size.png")

    container = get_layer_from_file("./images/" + file)
    container.layers[0].rotate_expand(45*2*math.pi/360)
    container.pack()
    container.save("done_" + file + "_rotate_expand.png")

def one_simple_transforms():
    file = "beak.jpg"

    container = get_layer_from_file("./images/" + file)
    container.layers[0].flip_horizontal_axis()
    container.pack()
    container.save("done_" + file + "_flip_horizontal.png")

    container = get_layer_from_file("./images/" + file)
    container.layers[0].flip_vertical_axis()
    container.pack()
    container.save("done_" + file + "_flip_vertical.png")

    container = get_layer_from_file("./images/" + file)
    container.layers[0].rotate_counter_clockwise()
    container.pack()
    container.save("done_" + file + "_rotate_90.png")

def one_adjust():
    file = "band.jpg"

    container = get_layer_from_file("./images/" + file)
    container.add_layer(container.layers[0].alter_hue(.1))
    container.pack()
    container.save("done_" + file + "_h_adjusted.png")

    container = get_layer_from_file("./images/" + file)
    container.add_layer(container.layers[0].alter_saturation(-.5))
    container.pack()
    container.save("done_" + file + "_s_adjusted.png")


    container = get_layer_from_file("./images/" + file)
    container.add_layer(container.layers[0].alter_value(-.1))
    container.pack()
    container.save("done_" + file + "_v_adjusted.png")

def one_hsv():
    file = "leather.jpg"

    container = get_layer_from_file("./images/" + file)
    container.add_layer(container.layers[0].hue_channel())
    container.pack()
    container.save("done_" + file + "_h.png")

    container = get_layer_from_file("./images/" + file)
    container.add_layer(container.layers[0].saturation_channel())
    container.pack()
    container.save("done_" + file + "_s.png")


    container = get_layer_from_file("./images/" + file)
    container.add_layer(container.layers[0].value_channel())
    container.pack()
    container.save("done_" + file + "_v.png")

def one_cmyk():
    file = "leather.jpg"

    container = get_layer_from_file("./images/" + file)
    container.add_layer(container.layers[0].cyan_channel())
    container.pack()
    container.save("done_" + file + "_c.png")

    container = get_layer_from_file("./images/" + file)
    container.add_layer(container.layers[0].magenta_channel())
    container.pack()
    container.save("done_" + file + "_m.png")


    container = get_layer_from_file("./images/" + file)
    container.add_layer(container.layers[0].yellow_channel())
    container.pack()
    container.save("done_" + file + "_y.png")

    container = get_layer_from_file("./images/" + file)
    container.add_layer(container.layers[0].black_channel())
    container.pack()
    container.save("done_" + file + "_k.png")

def many():
    print("Start")

    dir = "./images/"
    files = os.listdir(dir)
    stop = 0
    count = 0
    for file in files:
        container = get_layers_in_a_row(2, dir + file)
        # container.layers[1].brighten(-100)
        # container.layers[1].add_contrast(1.5)
        # container.layers[1].auto_tune_brightness()
        container.layers[1].gamma_encode(2.5*.5)
        container.add_layer(container.layers[0].generate_histogram())
        container.add_layer(container.layers[1].generate_histogram(), container.layers[0].width, 0)
        container.pack()

        # Finally, save the image
        print("Done with " + file)
        container.save("done_" + file + ".png")
        count += 1
        if count > stop:
          break
        
def get_layer_from_file(filename):
    image = Image.open(filename)
    """ Load the image and get its height and width"""
    width = image.size[0]
    height = image.size[1]

    """ Building a container for the image"""
    container: Container = Container(width, height)
    
    layer: Layer = Layer(width, height, 0, 0)
    layer.pixels = list(image.getdata())
    container.add_layer(layer)
    
    return container

def get_layers_in_a_row(count, filename):
    if count <= 0:
        return print("You need to generate more than 0 layers")
    if not filename:
        return print("You forgot to all a filename")
    
    layers = []

    image = Image.open(filename)
    """ Load the image and get its height and width"""
    width = image.size[0]
    height = image.size[1]

    """ Building a container for the image"""
    container: Container = Container(width, height)
    for i in range(count):
        layer: Layer = Layer(width, height, 0, 0)
        layer.pixels = list(image.getdata())
        container.add_layer(layer, layer.width * i)
    
    return container

start = time.time()
one_adjust()
end = time.time()
print(str(end - start) + " " + " seconds")
    



