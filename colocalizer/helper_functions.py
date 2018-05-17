"""Helper functions to show and save images
"""
import os
from skimage.viewer import ImageViewer
from skimage.io import imsave
from skimage import img_as_uint

def show_image(image):
    """Displays an image

    Arguments:
        image {ndarray} -- the image data
    """

    viewer = ImageViewer(image)
    viewer.show()

def save_binary_image(filename, image):
    """Saves an image as uint

    Arguments:
        filename {str} -- the filename to save to, folders will be created
        image {ndarray} -- the image data
    """

    os.makedirs(os.path.dirname(filename), exist_ok=True)
    imsave(filename, img_as_uint(image))

def get_append_or_write(filename, logfunction=None):
    """Gets file mode depending on whether a file already exists or not
    
    Arguments:
        filename {str} -- the file name
    
    Keyword Arguments:
        logfunction {fun} -- a function to display logmessages (default: {None})
    
    Returns:
        str -- a if file exists, otherwise w
    """

    if os.path.exists(filename):
        if logfunction:
            logfunction("Appending to statisticsfile {0}".format(filename))
        return 'a'
    else:
        return 'w'