import argparse
from typing import List
import os
import cv2
import matplotlib.pyplot as plt
from path import Path

from __init__ import detect, prepare_img, sort_multiline
list_img_names_serial=[]

def get_img_files(data_dir: Path) -> List[Path]:
    """Return all image files contained in a folder."""
    res = []
    for ext in ['*.png', '*.jpg', '*.bmp']:
        res += Path(data_dir).files(ext)
    return res


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--data', type=Path, default=Path('InputImages'))
    parser.add_argument('--kernel_size', type=int, default=25)
    parser.add_argument('--sigma', type=float, default=11)
    parser.add_argument('--theta', type=float, default=5)
    parser.add_argument('--min_area', type=int, default=100)
    parser.add_argument('--img_height', type=int, default=1000)
    parsed = parser.parse_args()

    for fn_img in get_img_files(parsed.data):
        print(f'Processing file {fn_img}')

        # load image and process it
        img = prepare_img(cv2.imread(fn_img), parsed.img_height)
        detections = detect(img,
                            kernel_size=parsed.kernel_size,
                            sigma=parsed.sigma,
                            theta=parsed.theta,
                            min_area=parsed.min_area)

        # sort detections: cluster into lines, then sort each line
        lines = sort_multiline(detections)

        # plot results
        plt.imshow(img, cmap='gray')
        num_colors = 7
        colors = plt.cm.get_cmap('rainbow', num_colors)
        for line_idx, line in enumerate(lines):
            for word_idx, det in enumerate(line):
                xs = [det.bbox.x, det.bbox.x, det.bbox.x + det.bbox.w, det.bbox.x + det.bbox.w, det.bbox.x]
                ys = [det.bbox.y, det.bbox.y + det.bbox.h, det.bbox.y + det.bbox.h, det.bbox.y, det.bbox.y]
                plt.plot(xs, ys, c=colors(line_idx % num_colors))
                plt.text(det.bbox.x, det.bbox.y, f'{line_idx}/{word_idx}')
                print(det.bbox.x,det.bbox.y,det.bbox.w,det.bbox.h)
                crop_img=img[det.bbox.y:det.bbox.y+det.bbox.h,det.bbox.x:det.bbox.x+det.bbox.w]
                desired_folder = "Outputs2"
                os.makedirs(desired_folder, exist_ok=True)
                filename="line"+str(line_idx)+"word"+str(word_idx)+".jpg"
                file_path = os.path.join(desired_folder, filename)
                cv2.imwrite(file_path,crop_img)
                full_img_path="line"+str(line_idx)+"word"+str(word_idx)+".jpg"
                list_img_names_serial.append(full_img_path)
                print(list_img_names_serial)
                list_img_names_serial_set=set(list_img_names_serial) 
                # textfile=open("/content/Outputs/img_names_sequence.txt","w")
                # for element in list_img_names_serial:
                #    textfile.write(element+"\n")
                # textfile.close()

        plt.show()


if __name__ == '__main__':
    main()
