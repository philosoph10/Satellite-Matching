import algo
import argparse
from PIL import Image


# Set a higher image size limit, for PIL not to treat satellite images as DOS attack
Image.MAX_IMAGE_PIXELS = 10980*10980*3


def parse_args():
    """
    parse arguments
    :return: the dictionary with parsed args
    """
    parser = argparse.ArgumentParser(description="Keypoint detection and matching for pairs of images.")

    parser.add_argument("--image1", required=True, help="Path to the first image.")
    parser.add_argument("--image2", required=True, help="Path to the second image.")
    parser.add_argument("--save-to", default=None, help="Path to save the image of keypoints matches")

    parsed_args = parser.parse_args()

    return parsed_args


if __name__ == '__main__':
    args = parse_args()

    # read the images
    image1 = algo.read_image(args.image1)
    image2 = algo.read_image(args.image2)

    # process the images, and show the result; optionally save
    algo.detect_and_match_keypoints(image1, image2, target_size=(1000, 1000), save_to=args.save_to)
