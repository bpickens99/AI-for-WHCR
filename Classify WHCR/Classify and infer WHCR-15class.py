import torch
import PIL
from PIL import Image
from torchvision import transforms
import csv
from os.path import basename
import os
import shutil
import pandas
import csv

# image_dir = directory of images to apply inference to
# root_export = directory where species folders are set up
# Optional (if new model is applied): idx_to_label = index to the corresponding label in the model
# model_path = pytorch classification model saved as script file
# transform_test = transform to be applied prior to inference

## New inputs: drive_path = root directory, flight_name = flight folder, model_path = model to apply
root_path = "D:/WHCR_2025/11_WHCR_2025_CLASSIFICATION/"
flight_name = "test_whcr_crops"

root_export = root_path + flight_name + "/whcr_test_data/"

new_csv = root_export + "/whcr_test_data" + ".csv"
print(new_csv)

image_dir = root_path + flight_name
# image_dir = root_path + flight_name + "/still_missing_crops/"

image_context = image_dir
        # root_path + flight_name + "/whcr_infer_crops_test/")
#image_context = root_path + flight_name + "/crops_w_context_birds/"

model_path = "D:/WHCR_2025/model_weights/whcr_classifier_Aug22_swin_s_rd3.pt"

prob_threshold = 1.00
max_label_index = 15
unlisted_object_index =12

if not os.path.exists(root_export):
    os.mkdir(root_export)

device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"Using {device} device") # must print "Using cuda device" to work

# load model
model = torch.jit.load(model_path)
model.to(device)

transform_test = transforms.Compose([
    transforms.Resize((224,224)), transforms.ToTensor(),
    transforms.Normalize(mean= (0.2335, 0.2444, 0.2143), std=(0.1369,0.1149, 0.1031))
])

idx_to_label = {0: "Accipitridae", 1: "Anatidae", 2: "Ardeidae",
                            3: "artificial", 4: "Charadriiformes",
                            5: "Laridae", 6: "Pelecanidae",
                            7: "Phalacrocoracidae", 8: "Podicipedidae",
                            9: "Skimmer",
                            10: "Sterninae",
                            11: "Threskiornithidae", 12: "Unlisted_object",
                            13: "SACR", 14: "WHCR", 15: "ROSP"
                            }

species_list = list(idx_to_label.values())

with open(new_csv, 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['unique_image_jpg', 'label1', 'label2', 'score1', 'score2'])

def classify(model, transform_test, source):
    model = model.eval()
    image = PIL.Image.open(source)
    image = transform_test(image).float()
    image = image.to(device)
    image = image.unsqueeze(0)
    output = model(image)
    # print(output.data)
    softmax = torch.nn.functional.softmax(output, dim=1)

    top3_prob, top3_label = torch.topk(softmax, 3)
    # print("tops: ", top3_prob,top3_label)
    label1 = top3_label[0, 0]
    label2 = top3_label[0, 1]
    score1 = top3_prob[0, 0]
    score2 = top3_prob[0, 1]
    label1 = label1.data.cpu().numpy()
    label2 = label2.data.cpu().numpy()
   # print(label1, label2)
    if label1 > max_label_index or label2 > max_label_index:
        label1 = unlisted_object_index
        label2 = unlisted_object_index

    score1 = score1.data.cpu().numpy()
    score2 = score2.data.cpu().numpy()
    species_list = list(idx_to_label.values())

    label1 = species_list[label1]
    label2 = species_list[label2]

    print(label1, label2)

    with open(new_csv, 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([name, label1, label2, score1, score2])
x = 0
for root, dirs, files in os.walk(image_dir):
    for file in files:
        if file.endswith(".jpg"):
            source = os.path.join(root, file)
            name = os.path.basename(source)
            print ("name: ", name)
            classify(model, transform_test, source)
            x = x+1
            print(x, "are classified")
        else:
            pass
###############
# This part does the moving
dirs = os.listdir(image_dir)  # get all files in folder

csv_data = pandas.read_csv(new_csv)

for index, row in csv_data.iterrows():
    score1 = row['score1']
    print(score1)
    if score1 <  prob_threshold:
        target = image_context + "/" + row['unique_image_jpg']  # +'.jpg'
        print('Target : ', target)
        cat1 = row['label1']
        print("Class: ", cat1)

        for folders, subfolders, files in os.walk(image_context):
            name = basename(target)
            print ("name: ", name)
            if name in files:
                dir2 = root_export + "/" + row['label1']
                if not os.path.exists(dir2):
                    os.makedirs(dir2)
                dest = root_export + "/" + row['label1'] + '/' + name

                print ("Destination : ", dest)
                shutil.copy(target, dest)  # this can be changed to: shutil.move
            else:
                pass
    else:
        print("Too high!")
