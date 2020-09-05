try:
    print("Elementary imports: ")
    import os
    import json
    import glob
    import argparse

    print("numpy/scipy/cv2 imports:")
    import numpy as np
    from scipy import signal as sg
    import scipy.ndimage as ndimage
    from scipy.ndimage.filters import maximum_filter
    import cv2

    print("PIL imports:")
    from PIL import Image

    print("matplotlib imports:")
    import matplotlib.pyplot as plt

    print("kernel import:")
    from kernel import kernel
except ImportError:
    print("Need to fix the installation")
    raise

print("All imports okay. Yay!")


def get_light_coordinate(c_image: np.ndarray):
    
    gray_image = cv2.cvtColor(c_image, cv2.COLOR_BGR2GRAY)
    tophat_image = cv2.morphologyEx(c_image, cv2.MORPH_TOPHAT, kernel)
    ret, thresh = cv2.threshold(tophat_image, 120, 255, cv2.THRESH_BINARY)
    dist_transform = cv2.distanceTransform(thresh, cv2.DIST_L2, 5)
    ret, markers = cv2.connectedComponents(np.uint8(dist_transform))
    markers += 1
    watershed_image = cv2.watershed(c_image, markers)
    values, counts = np.unique(watershed_image, return_counts=True)
    segment_indices = np.where(counts <= 500)
    markers = values[segment_indices]
    coordinates = []

    for marker in markers:
        y_coordinates, x_coordinates = np.where(watershed_image == marker)
        coordinates.append((int(np.median(x_coordinates)), int(np.median(y_coordinates))))

    cv2.imshow('Binary', thresh)
    cv2.imshow('Marks', c_image)

    if cv2.waitKey(0) & 0xff == 27:  
        cv2.destroyAllWindows() 
    
    return coordinates



def find_tfl_lights(c_image: np.ndarray, **kwargs):
    """
    Detect candidates for TFL lights. Use c_image, kwargs and you imagination to implement
    :param c_image: The image itself as np.uint8, shape of (H, W, 3)
    :param kwargs: Whatever config you want to pass in here
    :return: 4-tuple of x_red, y_red, x_green, y_green
    """

    coordinates = get_light_coordinate(c_image)
    x = [coordinate[0] for coordinate in coordinates]
    y_red = y_green = [coordinate[1] for coordinate in coordinates]

    return x, y_red, x, y_green


def show_image_and_gt(image, objs, fig_num=None):
    plt.figure(fig_num).clf()
    plt.imshow(image)
    labels = set()
    if objs is not None:
        for o in objs:
            poly = np.array(o['polygon'])[list(np.arange(len(o['polygon']))) + [0]]
            plt.plot(poly[:, 0], poly[:, 1], 'r', label=o['label'])
            labels.add(o['label'])
        if len(labels) > 1:
            plt.legend()


def test_find_tfl_lights(image_path, json_path=None, fig_num=None):
    """
    Run the attention code
    """
    image = np.array(Image.open(image_path))
    if json_path is None:
        objects = None
    else:
        gt_data = json.load(open(json_path))
        what = ['traffic light']
        objects = [o for o in gt_data['objects'] if o['label'] in what]

    show_image_and_gt(image, objects, fig_num)

    red_x, red_y, green_x, green_y = find_tfl_lights(image, some_threshold=42)
    plt.plot(red_x, red_y, 'ro', color='r', markersize=4)
    plt.plot(green_x, green_y, 'ro', color='g', markersize=4)


def main(argv=None):
    """It's nice to have a standalone tester for the algorithm.
    Consider looping over some images from here, so you can manually exmine the results
    Keep this functionality even after you have all system running, because you sometime want to debug/improve a module
    :param argv: In case you want to programmatically run this"""
    parser = argparse.ArgumentParser("Test TFL attention mechanism")
    parser.add_argument('-i', '--image', type=str, help='Path to an image')
    parser.add_argument("-j", "--json", type=str, help="Path to json GT for comparison")
    parser.add_argument('-d', '--dir', type=str, help='Directory to scan images in')
    args = parser.parse_args(argv)
    default_base = '../../data'
    if args.dir is None:
        args.dir = default_base
    flist = glob.glob(os.path.join(args.dir, '*_leftImg8bit.png'))
    for image in flist:
        json_fn = image.replace('_leftImg8bit.png', '_gtFine_polygons.json')
        if not os.path.exists(json_fn):
            json_fn = None
        test_find_tfl_lights(image, json_fn)
    if len(flist):
        print("You should now see some images, with the ground truth marked on them. Close all to quit.")
    else:
        print("Bad configuration?? Didn't find any picture to show")
    plt.show(block=True)


if __name__ == '__main__':
    main()
