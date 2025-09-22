import os
import pandas as pd
import json
import csv
import numpy as np
from sympy import factor

os.chdir("D:/WHCR_2025/12_WHCR_detection/")

# Inputs: csv_file= input of csv with annotation data;
# export_json= name of COCO json to export
# width = width of images (pixels), height = height of images (pixels)
# categories = link the name of classes related to its index
csv_file = '5_tile_annot_5perc_empty_train.csv'
export_json = '5_tile_annot_5perc_empty_train.json'
width = 1024
height = 1024

csv_data = pd.read_csv(csv_file)
print(csv_data)

categories = [{"label_id": 0, "name": "whcr"}]

#csv_data.columns = (['id','image_id','unique_image_jpg','xmin', 'ymin', 'w','h','label_id'])

#csv_data['image_id']= csv_data['image_id'].astype(int)
#csv_data['id']= csv_data['id'].astype(int)
#csv_data['xmin']= csv_data['xmin'].astype(int)
#csv_data['ymin']= csv_data['ymin'].astype(int)
#csv_data['w']= csv_data['w'].astype(int)
#csv_data['h']= csv_data['h'].astype(int)
#csv_data['label_id']= csv_data['h'].astype(int)
 #                    'bbname','unique_image_path'])
csv_data['annid'] = csv_data.index

# Create lists to fill in, including nested dictionaries
images = []
annotations = []

def image(row):
    image = {}
    image["width"] = width
    image["height"] = height
    image["id"] = row.image_id
    image["file_name"] = row.unique_image_jpg
  # image["observer"] = row.author # if needed
    return image

def annotation(row):
    annotation = {}
    annotation["id"] = row.id
    annotation["image_id"] = row.image_id
    annotation["category_id"] = row.label_id
   # annotation["segmentation"] = []
    annotation["bbox"] = [row.xmin, row.ymin, row.w, row.h]
    annotation["ignore"] = 0
    annotation["iscrowd"] = 0
    annotation["area"] = (row.h * row.w)
    return annotation

# Iterates through rows
for index, row in csv_data.iterrows():
    annotations.append(annotation(row))
    images.append(image(row))
len(images)

# remove duplicate images
images2 = []

imagedf = csv_data.drop_duplicates(subset=['image_id'])
for index, row in imagedf.iterrows():
    images2.append(image(row))
len(images2)

data_coco = {}
data_coco["images"] = images2
data_coco["categories"] = categories
data_coco["annotations"] = annotations

json.dump(data_coco, open(export_json,"w"), indent=0)
print ("Completed!")
