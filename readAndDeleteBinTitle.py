import cv2
import os

input_folder = r'C:\Users\myh26\Documents\999_fufuDoc\9.22_sorted_images'
output_folder = r'C:\Users\myh26\Documents\999_fufuDoc\9.22_sorted_images_noTitle'

# 确保输出文件夹存在
os.makedirs(output_folder, exist_ok=True)

# 获取文件夹内的所有图片文件,读取的是指定文件夹中的文件名列表
image_files = os.listdir(input_folder)
##############################################
def delete_bin_title(image):
    filename = str(image)
    last_part = filename.split("_")[-1]
    return last_part

################### main #####################
for img in image_files:

    # 读取图像文件
    image_path = os.path.join(input_folder, img)
    img_data = cv2.imread(image_path)

    output_path = os.path.join(output_folder, delete_bin_title(img))
    cv2.imwrite(output_path, img_data)
