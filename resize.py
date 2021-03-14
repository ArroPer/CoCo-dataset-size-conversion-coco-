import mmcv
import cv2
import json
import os
import copy

def resize_bbox(a, ann, ratio_w, ratio_h):
    x, y, w, h = a["bbox"]
    new_x = x*ratio_w; new_y = y*ratio_h; new_w = w*ratio_w; new_h = h*ratio_h

    # keep one decimal place
    new_x= round(new_x, 1); new_y = round(new_y, 1); new_w= round(new_w, 1); new_h = round(new_h, 1)
    ann['bbox'] = [new_x, new_y, new_w, new_h]

    return new_w*new_h

def resize_img(img, new_w, new_h):

    # core
    new_img=cv2.resize(img, (new_w, new_h))

    return new_img

def append_image_json(new_json, json_original_file,new_w,new_h):
    # images information
    tmp_img = json_original_file['images'].copy()

    for img in tmp_img:
        image = {
            'id': int,
            'file_name': '',
            'width': int,
            'height': int,
            'date_captured': '',
            'license': '',
            'coco_url': '',
            'flickr_url': ''
        }

        image['id'] = img["id"]
        image['file_name'] = img["file_name"]
        image['width'] = new_w
        image['height'] = new_h
        image['date_captured'] = img["date_captured"]
        image['license'] = img["license"]
        image['coco_url'] = img["coco_url"]
        image['flickr_url'] = img["flickr_url"]

        # if necessary ,please delete unuserd parts by hand
        new_json['images'].append(image)

    print('------image json is done-----')

def append_ann_json(new_json, json_original_file, new_w,new_h):
    # Annotations information
    tmp_ann = json_original_file['annotations'].copy()

    # Here we look for the smallest bbox area(w*h)
    min_bbox_area=20000
    img_id=0

    for a in tmp_ann:
        ann = {
            'id': int,
            'image_id': int,
            'category_id': int,
            'iscrowd': int,
            'area': int,
            'bbox': [],
            'segmentation': [[]],
            'width': int,
            'height': int
        }
        ann['id'] = a["id"]
        ann['image_id'] = a["image_id"]
        ann['category_id'] = a["category_id"]
        ann['iscrowd'] = a["iscrowd"]
        ann['segmentation'] = a["segmentation"]
        ann['width'] = new_w
        ann['height'] = new_h
        ann['area'] = a["area"]

        # Calculate the scaling ratio of each image to calculate the correct position of each bbox
        ratio_w = new_w/a['width']
        ratio_h = new_h/a['height']

        # bbox
        wh = resize_bbox(a, ann, ratio_w, ratio_h)
        if min_bbox_area > wh:
            min_bbox_area = wh
            img_id = ann['image_id']

        # if necessary ,please delete unuserd parts by hand
        new_json['annotations'].append(ann)

    print('------ann json is done-----')
    print(min_bbox_area)
    print(img_id)

def write_new_jsonfile(write_jsonfile, save_path):
    json_fp = open(save_path, 'w')
    json_str = json.dumps(write_jsonfile)
    json_fp.write(json_str)
    json_fp.close()

def resize_json(load_path, save_path, new_w, new_h):
    # loading original json file
    json_original_file = json.load(open(load_path, 'r'))
    # copy whole file
    new_json = copy.deepcopy(json_original_file)

    #Annotation has five parts, and we only resize the two important parts
    append_image_json(new_json, json_original_file, new_w, new_h)
    append_ann_json(new_json, json_original_file, new_w, new_h)

    write_new_jsonfile(new_json, save_path)
    print('------already wrote json-----')

def resize_image(img_folder, img_save, new_w, new_h):
    print('------start image augment-----')
    imgs = os.listdir(img_folder)
    for img_name in imgs:
        img = mmcv.imread(img_folder + '/' + img_name)
        new_img = resize_img(img, new_w, new_h)

        # save img
        mmcv.imwrite(new_img, img_save + '/' + img_name)

    print('------image augmentation is done-----')

def main():
    # __init__
    json_load_path = '../data/coco/annotations/instances_train2017.json'
    json_save_path = '../data/coco/annotations/instances_train2017-1000.json'
    img_folder = '../data/coco/train2017'
    img_save = '../data/coco/train2017-1000'
    new_w = 1000
    new_h = 1000

    # resize json
    resize_json(json_load_path, json_save_path, new_w, new_h)

    # resize image
    resize_image(img_folder, img_save, new_w, new_h)

if __name__ == '__main__':
    main()