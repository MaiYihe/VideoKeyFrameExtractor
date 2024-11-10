import os
import cv2 as cv
import numpy as np
import re
from collections import defaultdict


#########################################################

def get_img_p_hash(img):
    """
    Get the pHash value of the image, pHash : Perceptual hash algorithm(感知哈希算法)
    :param img: img in MAT format(img = cv2.imread(image))
    :return: pHash value
    """
    hash_len = 128
    # GET Gray image
    gray_img = cv.cvtColor(img, cv.COLOR_RGB2GRAY)
    # Resize image, use the different way to get the best result
    resize_gray_img = cv.resize(gray_img, (hash_len, hash_len), cv.INTER_AREA)
    # Change the int of image to float, for better DCT
    h, w = resize_gray_img.shape[:2]
    vis0 = np.zeros((h, w), np.float32)
    vis0[:h, :w] = resize_gray_img
    # DCT: Discrete cosine transform(离散余弦变换)
    vis1 = cv.dct(cv.dct(vis0))
    vis1.resize(hash_len, hash_len)
    img_list = vis1.flatten()
    # Calculate the avg value
    avg = sum(img_list) * 1. / len(img_list)
    avg_list = []
    for i in img_list:
        if i < avg:
            tmp = '0'
        else:
            tmp = '1'
        avg_list.append(tmp)
    # Calculate the hash value
    p_hash_str = ''
    for x in range(0, hash_len * hash_len, 4):
        p_hash_str += '%x' % int(''.join(avg_list[x:x + 4]), 2)
    return p_hash_str


def ham_dist(x, y):
    """
    Get the hamming distance of two values.
        hamming distance(汉明距)
    :param x:
    :param y:
    :return: the hamming distance
    """
    assert len(x) == len(y)
    return sum([ch1 != ch2 for ch1, ch2 in zip(x, y)])


def compare_img_p_hash(img1, img2):
    hash_img1 = get_img_p_hash(img1)
    hash_img2 = get_img_p_hash(img2)
    return ham_dist(hash_img1, hash_img2)


#########################################################

# 将哈希表转化为列表，然后根据列表的 filename的数字 进行排序
def save_sorted_images(distance_bins):
    sorted_bins = []
    for bin_key in sorted(distance_bins.keys()):
        sorted_bins.extend(distance_bins[bin_key])

    # 按照文件名中的数字部分排序
    sorted_items = sorted(sorted_bins, key=lambda x: extract_number(x[0]))
    return sorted_items

#########################################################

# 从文件名中提取数字
def extract_number(filename):
    match = re.search(r'\d+', filename)
    return int(match.group()) if match else 0

#########################################################

# 设置图片文件夹导入和输出路径
image_folder = r'C:\Users\myh26\Documents\999_fufuDoc\9.16_test'
output_folder = r'C:\Users\myh26\Documents\999_fufuDoc\9.16_sorted_images'
# 确保输出文件夹存在
os.makedirs(output_folder, exist_ok=True)

# 获取文件夹内的所有图片文件，并按文件名中的数字排序
image_files = sorted(os.listdir(image_folder), key=extract_number)

# 遍历文件夹中的文件
first_image_saved = False

# 建立哈希表。创建一个 defaultdict，其默认值是空列表；list 是工厂函数，它会为每个缺失的键生成一个空列表 []
distance_bins = defaultdict(list)

# 遍历所有图片并计算汉明距dif，
for filename in image_files:
    image_path = os.path.join(image_folder, filename)
    # 读取图片
    img = cv.imread(image_path)
    if img is None:
        print(f"无法读取文件: {filename}")
        continue
    if not first_image_saved:
        img0 = img
        first_image_saved = True
    dif = compare_img_p_hash(img0, img)

    # 整除后放入哈希表
    bin_index = dif // 10  # // 是整除运算符

    # 只保留桶中的第一项
    if not distance_bins[bin_index]:  # 检查桶是否为空
        distance_bins[bin_index].append((filename, img))

    print(f"图片: {filename} 的 汉明距 值是: {dif}")

# 哈希表转化为列表
sorted_images = save_sorted_images(distance_bins)
for filename, img in sorted_images:
    if img is not None:
        output_path = os.path.join(output_folder, filename)
        cv.imwrite(output_path, img)
    else:
        print(f"无法读取文件: {filename}")
    print(filename)

#########################################################

