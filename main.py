import sys
import argparse

from PIL import Image
import numpy as np
import rgb_mappings as mappings

MAPPING_DICT = {
        "average": mappings.average,
        "lightness": mappings.lightness,
        "luminosity": mappings.luminosity,
    }

def main():
    parser = argparse.ArgumentParser(description="Convert an image into ASCII art.")
    parser.add_argument('image_path', help="Path to image.")
    parser.add_argument('-method', '-m', dest="mapping_method", choices=["average", "lightness", "luminosity"], 
                        help="Method of mapping RGB channels to single channel values.")
    # TODO: fix resize argument
    parser.add_argument('-resize', '-r', dest="target_size", type=tuple,
                        help="Resize image to a specific size for display. Results in M by N image")

    args = vars(parser.parse_args())
    image_path = args.get("image_path")
    mapping_method = MAPPING_DICT.get(args.get("mapping_method"), mappings.average)
    target_size = args.get("target_size")

    if image_path == None:
        raise ValueError("Image path not provided.")

    imported_image = Image.open(image_path)
    print(f"Successfully imported image, size: {imported_image.size}")
    
    pixel_array = np.asarray(imported_image)
    print(f"Successfully loaded pixels")
    # convert into single channel image with average over RGB values
    single_channel_image = np.apply_along_axis(mapping_method, 2, pixel_array)

    print(f"Successfully converted image to single channel")
    print(single_channel_image)

    ascii_character_image = get_brightness_matrix(single_channel_image)

    print(f"Successfully converted to ascii characters")
    print_final_image(ascii_character_image)

def print_final_image(img):
    for i in range(img.shape[0]):
        print("".join(np.repeat(img[i], 2)))


def get_brightness_matrix(single_channel_image: np.array):
    brightness_matrix = "`^\",:;Il!i~+_-?][}{1)(|\\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$"
    brightness_matrix = list(brightness_matrix)

    # normalise pixel values
    normalised_array = single_channel_image / 255
    converted_array = np.zeros(single_channel_image.shape, dtype=str)

    matrix_length = len(brightness_matrix)
    for i in range(normalised_array.shape[0]):
        for j in range(normalised_array.shape[1]):
            # get matching character from brightness matrix
            character_index = int(np.round(matrix_length * normalised_array[i, j]))
            converted_array[i, j] = brightness_matrix[character_index]

    return converted_array


if __name__ == "__main__":
    main()