import glob,os

# Input dir where file extensions need to be changed
os.chdir("D:/WHCR_2025/12_WHCR_detection/5_tiles_5perc_empty/")

source_dir = "D:/WHCR_2025/12_WHCR_detection/5_tiles_5perc_empty/"
export_dir = "D:/WHCR_2025/12_WHCR_detection/5_tiles_5perc_empty/"

if not os.path.exists(export_dir):
    os.makedirs(export_dir)

for filename in glob.glob('*..jpg'):
    print(filename)
    pre, ext = os.path.splitext(filename)
    rename1 = pre  + 'jpg'
    print("Rename: ", rename1)
    os.rename(os.path.join(source_dir, filename),
              os.path.join(export_dir, rename1))  # enter the new filename extension

#for filename in glob.glob('*.jpg.jpg'):
# print(filename)
#    pre, ext = os.path.splitext(filename)
#   rename1 = pre #+ '.jpg'
#  print ("Rename: ", rename1)
# os.rename(os.path.join(source_dir, filename),
#          os.path.join(export_dir, rename1)) # enter the new filename extension
#