from datetime import datetime
from tkinter.colorchooser import askcolor
from tkinter import filedialog
from database import *
from cv2 import imread, imwrite
import numpy as np


def item_name(event_name):
    current_time = datetime.now().strftime("%H-%M-%S")
    name = f'{event_name}-{current_time}.csv'
    return name


def change_value(variable):
    colors = askcolor(title="Choose Color")
    if colors[1] is not None:
        Database.update_meta_value(variable, colors[1])


def change_font(button_font, button_font_value):
    Database.update_meta_value(button_font, button_font_value.get())


def save_profile(dictionary):
    for key in dictionary.keys():
        Database.update_meta_value(key, dictionary[key].get())


def combine_images(image_path):
    max_size = [0, 0, 3]
    for image in image_path:
        im = imread(image)
        max_size = (max(max_size[0], im.shape[0]), max(max_size[1], im.shape[1]), 3)

    resulted_image = np.full(fill_value=255, shape=(max_size[0], max_size[1] * len(image_path), max_size[2]),
                             dtype='int')
    y = 0
    for i in range(len(image_path)):
        image_name = image_path[i]
        image = imread(image_name)
        image_shape = image.shape
        mid_range = ((max_size[0] - image_shape[0]) // 2, (max_size[1] - image_shape[1]) // 2)
        resulted_image[mid_range[0]:mid_range[0] + image_shape[0], y + mid_range[1]:y + mid_range[1] + image_shape[1], :] =\
            image

        y += image_shape[1] + mid_range[1] * 2
    imwrite(os.path.join(app_data_location, 'QR_codes.png'), resulted_image)


def browse_files():
    filenames = filedialog.askopenfilenames(initialdir="/", title="Select a File",
                                            filetypes=(("PNG files", "*.png*"), ("all files", "*.*")))

    # It returns a tuple of selected files
    combine_images(list(filenames))


def get_upi_ids(upi_ids):
    upi_ids = upi_ids.strip().split(',')
    res = ['', '', '']
    for upi in upi_ids:
        if upi.split('@')[-1] == 'ybl':
            res[0] = upi
        elif upi.split('@')[-1][:2] == 'ok':
            res[1] = upi
        elif upi.split('@')[-1] == 'paytm':
            res[2] = upi
    return res
