import mmcv
import numpy as np
import cv2
import json


def main():
    json_load_path = '../data/coco/annotations/instances_train2017.json'
    img = mmcv.imread('../data/coco/train2017/J48E023004_wow_142_zx.jpeg', 1)
    json_file = json.load(open(json_load_path, 'r'))

    for json_ann in json_file['annotations']:
        if json_ann['image_id'] == 766:
            cv2.rectangle(img, (int(json_ann['bbox'][0]), int(json_ann['bbox'][1])),(int(json_ann['bbox'][0]+json_ann['bbox'][2]),int(json_ann['bbox'][1]+json_ann['bbox'][3])), (0, 0, 255),2)
    res = cv2.resize(img, (600, 600), interpolation=cv2.INTER_CUBIC)
    mmcv.imshow(res)

if __name__ == '__main__':
    main()





