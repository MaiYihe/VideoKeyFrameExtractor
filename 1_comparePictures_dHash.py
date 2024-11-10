import cv2
from skimage.metrics import structural_similarity as ssim
import os
import re
from collections import defaultdict

#########################################################

# 从文件名中提取数字
def extract_number(filename):
    match = re.search(r'\d+', filename)
    return int(match.group()) if match else 0

#########################################################

# 设置图片文件夹导入和输出路径
# image_folder = r'C:\Users\myh26\Documents\999_fufuDoc\9.16_test'
image_folder = r'C:\Users\myh26\Documents\999_fufuDoc\9.22'
output_folder = r'C:\Users\myh26\Documents\999_fufuDoc\9.22_sorted_images'
# 确保输出文件夹存在
os.makedirs(output_folder, exist_ok=True)

# 获取文件夹内的所有图片文件，并按文件名中的数字排序
image_files = sorted(os.listdir(image_folder), key=extract_number)

# 遍历文件夹中的文件
first_image_saved = False

# 建立哈希表。创建一个 defaultdict，其默认值是空列表；list 是工厂函数，它会为每个缺失的键生成一个空列表 []
distance_bins = defaultdict(list)


# 将哈希表转化为列表，然后根据列表的 filename的数字 进行排序
def save_sorted_images(distance_bins):
    sorted_bins = []
    for bin_key in sorted(distance_bins.keys()):
        sorted_bins.extend(distance_bins[bin_key])

    # 按照文件名中的数字部分排序
    sorted_items = sorted(sorted_bins, key=lambda x: extract_number(x[1]))
    return sorted_items



######################### main #############################

count =0
# 遍历所有图片并计算偏差dif，
for filename in image_files:
    if count <= 10000:
        image_path = os.path.join(image_folder, filename)
        # 读取图片
        img = cv2.imread(image_path)
        img_compare= cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

        if img_compare is None:
            print(f"无法读取文件: {filename}")
            continue
        if not first_image_saved:
            img0_compare = img_compare
            first_image_saved = True

        score, diff = ssim(img0_compare, img_compare, full=True)
        enhanced_diff = (score*10 ** 4)

        # 整除后放入哈希表
        bin_index = enhanced_diff // 10  # // 是整除运算符

        # 只保留桶中的第一项
        if not distance_bins[bin_index]:  # 检查桶是否为空
            distance_bins[bin_index].append((bin_index, filename, img))

        print(f"{filename},SSIM: {enhanced_diff}")
        count = count + 1

    else:
        # 哈希表转化为列表
        sorted_images = save_sorted_images(distance_bins)
        for bin_index, filename, img in sorted_images:
            if img is not None:
                output_path = os.path.join(output_folder, str(bin_index) + "_" + str(filename))
                cv2.imwrite(output_path, img)
            else:
                print(f"无法读取文件: {filename}")
            print(filename)

        distance_bins.clear()
        count = 0




