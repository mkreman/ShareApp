from datetime import datetime
from tkinter import filedialog
from database import *
from PIL import Image


def item_name(event_name):
    current_time = datetime.now().strftime("%H-%M-%S")
    name = f'{event_name}-{current_time}.csv'
    return name


def combine_images(image_path):
    """This function saves combined qr code if multiple images are selected or single qr code if not
       in UserAppDataFolder/MkReman/Share App folder.
       If image_path is None then this function will not be called from share.py"""
    image_path = image_path.split(',')
    images = [Image.open(x) for x in image_path]
    widths, heights = zip(*(i.size for i in images))

    x_offset = 0
    total_width = sum(widths) + (len(images) - 1) * 10
    max_height = max(heights)

    new_im = Image.new('RGB', (total_width, max_height))

    for im in images:
        y_offset = (max_height - im.size[1]) // 2
        new_im.paste(im, (x_offset, y_offset))
        x_offset += im.size[0] + 10

    new_im.save(os.path.join(app_data_location, 'QR_codes.png'))


def browse_qr_codes():
    filenames = filedialog.askopenfilenames(initialdir="/", title="Select a File",
                                            filetypes=(("PNG files", "*.png*"), ("all files", "*.*")))

    # It returns a tuple of selected files
    return list(filenames)


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
