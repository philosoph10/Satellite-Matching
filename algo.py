import imageio
import numpy as np
from skimage.feature import match_descriptors, corner_harris, corner_peaks
from skimage import color
from skimage.transform import resize
from skimage.feature import BRIEF
import matplotlib.pyplot as plt


def read_image(image_path):
    """
    read an image
    :param image_path: the path to the image file, like jp2
    :return: an array of pixel intensities
    """
    return imageio.v2.imread(image_path)


def detect_and_match_keypoints(image1, image2, target_size=None, min_distance=50,
                               save_to=None):
    """
    detect keypoints on 2 images and match them
    :param image1: first image
    :param image2: second image
    :param target_size: resize images to the given size, if not None
    :param min_distance: a parameter for corner detector, the larger the param the less keypoints
                         will be detected
    :param save_to: the path to the image of matches, if None do not save
    :return: the matches, numpy array
    """
    # resize the images to the given size
    if target_size is not None:
        image1 = resize(image1, target_size)
        image2 = resize(image2, target_size)

    # Convert images to grayscale, unless they are already grayscaled
    gray1 = color.rgb2gray(image1) if image1.ndim == 3 else image1
    gray2 = color.rgb2gray(image2) if image2.ndim == 3 else image2

    # Detect keypoints using Harris corner detector with adjusted min_distance
    keypoints1 = corner_peaks(corner_harris(gray1), min_distance=min_distance)
    keypoints2 = corner_peaks(corner_harris(gray2), min_distance=min_distance)

    # Extract local descriptors using BRIEF
    # Local descriptors capture the information about the neighbourhood of a keypoint
    extractor = BRIEF()
    extractor.extract(gray1, keypoints1)
    keypoints1 = keypoints1[extractor.mask]
    descriptors1 = extractor.descriptors

    extractor.extract(gray2, keypoints2)
    keypoints2 = keypoints2[extractor.mask]
    descriptors2 = extractor.descriptors

    # Match keypoints based on their descriptors
    matches = match_descriptors(descriptors1, descriptors2, cross_check=True)

    # Visualize matches
    fig, ax = plt.subplots(nrows=1, ncols=1)

    plt.gray()

    # stack images side by side
    ax.imshow(np.hstack((gray1, gray2)), cmap='gray')

    for i in range(len(matches)):
        # plot the matches counting for the shift
        idx1, idx2 = matches[i]
        ax.plot([keypoints1[idx1, 1], keypoints2[idx2, 1] + gray1.shape[1]],
                [keypoints1[idx1, 0], keypoints2[idx2, 0]], 'r-')

    ax.axis('off')

    # Save or display the image
    if save_to is not None:
        plt.savefig(save_to, bbox_inches='tight', pad_inches=0)
    else:
        plt.show()

    return matches
