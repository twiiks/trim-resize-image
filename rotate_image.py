from PIL import Image
import argparse
import os


def rotate_PIL(image_input, angle):
    input_mode = image_input.mode
    image_output = image_input.convert('RGBA')
    image_output = image_output.rotate(angle)
    with Image.new('RGBA', image_output.size, (255, 255, 255, 255)) as canvas:
        image_output = Image.composite(image_output, canvas, image_output)
        image_output = image_output.convert(input_mode)
    return image_output


def parse_args():
    desc = "ttf/otf fonts to jpg images set (JUST KOREAN)"
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument(
        '--img_dir',
        type=str,
        help='directory that includes images',
        required=True)
    parser.add_argument(
        '--result_dir',
        type=str,
        default='results',
        help='directory where result images is stored to',
        required=False)
    parser.add_argument(
        '--angles',
        type=str,
        default='3,-3',
        help='angles to rotate seperated with \',\' (eg. 3,-5,-30,45)',
        required=False)
    return parser.parse_args()


def main():
    IMAGE_EXTENTION = ['.jpg', '.jpeg', '.png']
    args = parse_args()

    img_dir = args.img_dir
    result_dir = args.result_dir
    if not os.path.exists(img_dir):
        print("[Error] Can't find directory [ ./%s ]" % (img_dir))
        return

    if not os.path.exists(result_dir):
        os.makedirs(result_dir)

    angles = args.angles
    angles = angles.split(',')
    angles = list(map(int, angles))
    len_angles = len(angles)

    for path, _, images in os.walk(img_dir):
        count = 0
        for image in images:
            count += 1
            ext = os.path.splitext(image)[-1]
            if ext not in IMAGE_EXTENTION:
                continue
            if count % 10 == 0:
                print("WORKING:: %s" % (image))
                count = 0

            with Image.open("%s/%s" % (path, image)) as image_input:
                name = os.path.splitext(image)[0]
                if '/' in path:
                    path_out = path.split('/', 1)[-1]
                    if not os.path.exists(result_dir + '/' + path_out):
                        os.makedirs(result_dir + '/' +  path_out)
                else:
                    path_out = './'
                for i in range(len_angles):
                    angle = angles[i]
                    image_output = rotate_PIL(image_input, angle)
                    full_name = "%s/%s_rot_%d%s" % (path_out, name, angle, ext)
                    image_output.save(os.path.join(result_dir + '/', full_name))
    print("!!!done!!!")


if __name__ == '__main__':
    main()
