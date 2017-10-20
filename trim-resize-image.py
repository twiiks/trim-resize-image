from PIL import Image, ImageChops, ImageOps
import argparse
import os


def scale(image, max_size, method=Image.ANTIALIAS):
    im_aspect = float(image.size[0]) / float(image.size[1])
    out_aspect = float(max_size[0]) / float(max_size[1])
    if im_aspect >= out_aspect:
        scaled = image.resize(
            (max_size[0], int((float(max_size[0]) / im_aspect) + 0.5)), method)
    else:
        scaled = image.resize((int((float(max_size[1]) * im_aspect) + 0.5),
                               max_size[1]), method)

    offset = (int((max_size[0] - scaled.size[0]) / 2), int(
        (max_size[1] - scaled.size[1]) / 2))
    # print(offset)
    back = Image.new("RGB", max_size, "white")
    back.paste(scaled, offset)
    return back


# trim from PIL image
def trim_resize_PIL(image_input, width, height):
    bg = Image.new(image_input.mode, image_input.size,
                   image_input.getpixel((0, 0)))
    diff = ImageChops.difference(image_input, bg)
    diff = ImageChops.add(diff, diff, 2.0, -100)
    bbox = diff.getbbox()
    image_output = image_input.crop(bbox)
    image_output = scale(image_output, [width, height])
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
        '--width',
        type=int,
        default=256,
        help='width after resize',
        required=False)
    parser.add_argument(
        '--height',
        type=int,
        default=256,
        help='height after resize',
        required=False)
    parser.add_argument(
        '--border',
        type=int,
        default=0,
        help='white space around result images',
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

    width = args.width
    height = args.height
    border = args.border
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
                image_output = trim_resize_PIL(image_input, width, height)
                image_output = ImageOps.expand(
                    image_output, border=border, fill='white')
                name = os.path.splitext(image)[0]
                full_name = "%s_%dx%d.%s" % (name, width, height, ext)
                image_output.save(os.path.join(result_dir + '/', full_name))
    print("!!!done!!!")


if __name__ == '__main__':
    main()
