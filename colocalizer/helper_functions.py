from skimage.viewer import ImageViewer
from skimage.io import imsave
from skimage import img_as_uint
from skimage.color import label2rgb
import os

def show_image(image):
    viewer = ImageViewer(image)
    viewer.show()

def save_binary_image(filename, image):
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    imsave(filename, img_as_uint(image))

def get_append_or_write(filename, logfunction = None):
    if os.path.exists(filename):
        if logfunction:
            logfunction("Appending to statisticsfile {0}".format(filename))
        return 'a'
    else:
        return 'w'