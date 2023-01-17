import pytesseract
import cv2
import os
import pandas as pd
pd.options.mode.chained_assignment = None


# get the path/directory
im_box = ['X00016469612', 'X00016469622', 'X00016469672']
folder_dir = "../train"; box_dir = "../train/box"; vis_box = "../train/vis_box"
try:
    os.makedirs(box_dir); os.makedirs(vis_box)
except OSError:
    pass
for im in os.listdir(folder_dir):
    if im.endswith(".jpg"):
        file_name = im[:im.find('.')]
        f = open(os.path.join(box_dir, file_name + ".txt"), mode = "w")
        img = cv2.imread(folder_dir + '/' + im)

        d = pytesseract.image_to_data(img, output_type='data.frame')
        n_boxes = len(d['block_num'])

        text = d[d.conf != -1]
        lines = text.groupby(['page_num', 'block_num', 'par_num', 'line_num'])['text'] \
                                  .apply(lambda x: ' '.join(list(x))).tolist()
        
        text['right'] = text['left'] + text['width']
        text['y2'] = text['top'] + text['height']

        x1 = text.groupby(['page_num', 'block_num', 'par_num', 'line_num'])['left'].min().tolist()
        x2 = text.groupby(['page_num', 'block_num', 'par_num', 'line_num'])['right'].max().tolist()
        y1 = text.groupby(['page_num', 'block_num', 'par_num', 'line_num'])['top'].min().tolist()
        y2 = text.groupby(['page_num', 'block_num', 'par_num', 'line_num'])['y2'].max().tolist()

        for i in range(len(lines)):  
            f.write(f'{x1[i]},{y1[i]},{x2[i]},{y1[i]},{x2[i]},{y2[i]},{x1[i]},{y2[i]}, {lines[i]}\n')
        f.close()
        if file_name in im_box:
            print(vis_box + '/' + file_name + '.jpg')
            for i in range(len(lines)):
                cv2.rectangle(img, (x1[i],y1[i]), (x2[i],y2[i]) , (0,255,0), 2)
            cv2.imwrite(vis_box + '/' + file_name + '.jpg', img)
