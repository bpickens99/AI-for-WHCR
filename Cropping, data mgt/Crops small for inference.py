import pandas
import cv2 as cv
import os

##Input: path = dir with parent images; csv_data = detection csv from inference
# export_path_[bird/nonbird/artif] = specify folders for each class
image_path = "D:/WHCR_2025/15_WHCR_survey/final_whcr_parents/"

csv_data = pandas.read_csv("D:/WHCR_2025/15_WHCR_survey/whcr_locations_formal_survey_744.csv")
export_path = "D:/WHCR_2025/15_WHCR_survey/whcr_formal_survey_crops_744/"

if not os.path.exists(export_path):
    os.mkdir(export_path)

#csv_data.columns = (['class', 'score', 'xmin', 'ymin', 'w', 'h', 'unique_image_jpg', 'unique_BB'])
# print(csv_data)

dirs = os.listdir(image_path)  # get all files in folder
print(len(dirs))

# Get all of the image names without the path
file_list = []
for file in dirs:
    basename = os.path.splitext(file)[0] + ".jpg"  # take basename (not path) and add .jpg
    print(basename)
    file_list.append(basename)

matches = csv_data[csv_data['unique_image_jpg'].isin(file_list)]
print("Matches: ", len(matches))

for index, row in matches.iterrows():  ## iterrows: Pandas iterate over rows
    source_path = image_path + row['unique_image_jpg']  # +'.jpg'
    print("Source: ", source_path)
    temp1 = cv.imread(source_path, cv.IMREAD_COLOR)  # this is good

    temp1.shape
    xmin = row['xmin'] - 10
    if xmin < 0:
        xmin = 0
    ymin = row['ymin'] - 10
    if ymin < 0:
        ymin = 0

    w = row['w'] + 20
    h = row['h'] + 20
    print(xmin, ymin, w, h)

    crops = temp1[ymin:(ymin + h), xmin:(xmin + w)]
    dest = export_path + row['unique_BB'] #+ '.jpg'
    print("destination: ", dest)
    cv.imwrite(dest, crops, [int(cv.IMWRITE_JPEG_QUALITY), 99])
