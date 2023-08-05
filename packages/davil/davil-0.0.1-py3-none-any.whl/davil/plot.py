import matplotlib.pyplot as plt

from src.davil.types import is_list


def plot_imgs(imgs, shape=None):
    if is_list(imgs):
        plots = imgs
    else:
        plots = [imgs]

    if shape is None:
        sh = (1, len(plots))
    else:
        if len(plots) > shape[0] * shape[1]:
            raise ValueError('Can\'t show more images than there are cells in shape {}'.format(repr(shape)))
        sh = shape

    row = 0
    col = 0
    for img in plots:

        plt.subplot2grid(sh, (row, col))

        if img is not None:
            plt.imshow(img)

        if col+1 == sh[1]:
            col = 0
            row += 1
        else:
            col += 1
    plt.show()
