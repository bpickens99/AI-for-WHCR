import torch
from sahi import AutoDetectionModel
import sahi.predict
import csv
import pandas as pd
import os

# Inputs: root_dir = folder with images;
#         new_csv = detection csv to output
#         model_path = path to YOLOv8 weights file
# from torch import init_num_threads

# root_dir = "D:/WHCR_2025/12_WHCR_detection/f_model_results/test_parent_images/"

root_dir = "D:/WHCR_2025/1_parent_images/JPG_20250122_095400"
new_csv = "D:/WHCR_2025/12_WHCR_detection/g_inference/yolov11s_Aug3_095400.csv"

visual_path = "D:/WHCR_2025/12_WHCR_detection/g_inference/yolo11s_Aug_3_viz_131500/"

#new_csv = "D:/WHCR_2025/12_WHCR_detection/8_inference/survey_095400_yolo10x_conf_20.csv"
model_path= "D:/WHCR_2025/12_WHCR_detection/f_model_results/YOLO11s_Aug3_conf20/weights/best.pt"

device = "cpu"
print(f"Using {device} device")

if not os.path.exists(visual_path):
    os.mkdir(visual_path)

#x1 = numexpr.detect_number_of_threads()
# print("Found ", x1, "cores!")

detection_model = AutoDetectionModel.from_pretrained(
    model_type='yolov11',
    model_path=model_path,
    confidence_threshold=0.20,
    device=device, # or 'cuda:0'
)

with open(new_csv, 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['unique_image_jpg', "bbox", "class", "score"])
x=0
for root, dirs, files in os.walk(root_dir):
    for file in files:
        if file.endswith("jpg"):
            source = os.path.join(root, file)
            print(source)
            x = x + 1
            print(x)
            result = sahi.predict.get_sliced_prediction(
                source,
                detection_model,
                slice_height=1024,
                slice_width=1024,
                overlap_height_ratio=0.1,
                overlap_width_ratio=0.1,
            )
            object_prediction_list = result.object_prediction_list
            base = os.path.basename(file)
           # result.export_visuals(file_name=base, export_dir= visual_path,
            #       hide_labels=False, hide_conf=False, rect_th=3)

            with open(new_csv, 'a', newline='') as file:
                writer = csv.writer(file)
                for result1 in object_prediction_list:
                    writer.writerow([source, result1.bbox, result1.category, result1.score])

print("OKAY")
csv_data = pd.read_csv(new_csv)
print(csv_data)
csv_data['unique_image_jpg'] = csv_data['unique_image_jpg'].apply(os.path.basename)
bbox = csv_data['bbox']
csv_data['score'] = csv_data['score'].str.replace(r"PredictionScore: <value: ", '', regex=True)
csv_data['score'] = csv_data['score'].str.replace(r">", '', regex=True)

csv_data['class'] = csv_data['class'].str.replace(r"Category: <id:", '', regex=True)
csv_data['class'] = csv_data['class'].str.replace(r" 0, name: ", '', regex=True)
csv_data['class'] = csv_data['class'].str.replace(r" 1, name: ", '', regex=True)
csv_data['class'] = csv_data['class'].str.replace(r" 2, name: ", '', regex=True)
csv_data['class'] = csv_data['class'].str.replace(r">", '', regex=True)

csv_data['bbox'] = csv_data['bbox'].str.replace(r"BoundingBox: <", '', regex= True)
csv_data['bbox'] = csv_data['bbox'].str.replace(r">", '', regex= True)

csv_data[['xmin', 'ymin', 'xmax', 'ymax', 'w', 'h']] = csv_data['bbox'].str.split(',', expand=True)
csv_data['h'] = csv_data['h'].str.replace(r"h: ", '', regex= True)
csv_data['w'] = csv_data['w'].str.replace(r"w: ", '', regex= True)
csv_data['xmin'] = csv_data['xmin'].str.replace(r"(", '', regex= False)

csv_data['temp_name'] = csv_data['unique_image_jpg'].str.replace(r".jpg", '', regex= True)

csv_data['xmin'] = csv_data['xmin'].astype(float).round().astype(int).astype(str)
csv_data['ymin'] = csv_data['ymin'].astype(float).round().astype(int).astype(str)
csv_data['w'] = csv_data['w'].astype(float).round().astype(int).astype(str)
csv_data['h'] = csv_data['h'].astype(float).round().astype(int).astype(str)

csv_data['unique_BB'] = csv_data['temp_name'] + "_" + csv_data['xmin'] + "_" + csv_data['ymin'] + "_" + csv_data['w']+ "_" + csv_data['h']
del csv_data['bbox']
del csv_data['xmax']
del csv_data['ymax']
del csv_data['temp_name']

csv_data.to_csv(new_csv)

