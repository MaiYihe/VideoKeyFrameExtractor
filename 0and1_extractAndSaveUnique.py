import cv2
import os
import numpy as np
from collections import defaultdict
from skimage.metrics import structural_similarity as ssim

import tkinter as tk
from tkinter import scrolledtext
import threading

# 创建窗口
def create_window(name):
    root = tk.Tk()
    root.title(name)

    # 创建一个容器 Frame 放置两个文本框
    frame = tk.Frame(root)
    frame.pack()

    # 创建第一个文本框
    text_box1 = scrolledtext.ScrolledText(frame, wrap='word', height=20, width=40)
    text_box1.pack(side=tk.LEFT, padx=10)

    # 创建第二个文本框
    text_box2 = scrolledtext.ScrolledText(frame, wrap='word', height=20, width=40)
    text_box2.pack(side=tk.RIGHT, padx=10)

    # 用于更新第一个文本框的函数
    def update_text_box1(message):
        text_box1.insert(tk.END, message + "\n")
        text_box1.see(tk.END)

    # 用于更新第二个文本框的函数
    def update_text_box2(message):
        text_box2.insert(tk.END, message + "\n")
        text_box2.see(tk.END)

    return root, update_text_box1, update_text_box2


# 主程序部分
def main_program():

    # 指定视频文件路径
    video_path = r'C:\Users\myh26\Documents\999_fufuDoc\外建史\10-城市设计_建筑法规_设计基础_建筑物理.mp4'
    # video_path = r'C:\Program Files\Adobe\Adobe Illustrator 2024\Support Files\Required\UXP\extensions\com.adobe.ccx.rtt\assets\richtooltips\AddAnchorPoint.mp4'

    if not os.path.isfile(video_path):
        print(f"视频文件不存在: {video_path}")
        exit(1)

    # 指定保存图片的文件夹
    output_folder = r'C:\Users\myh26\Documents\999_fufuDoc\10.31_extractAndSaveUnique'
    # 创建文件夹如果不存在
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # 打开视频文件
    cap = cv2.VideoCapture(video_path)

    frame_count = 0  # 记录真实的读取帧数
    success = True

    count = 0  # 用于判断的区间
    period = 10000

    # 建立哈希表。创建一个 defaultdict，其默认值是空列表；list 是工厂函数，它会为每个缺失的键生成一个空列表 []
    distance_bins = defaultdict(list)

    white_frame = None  # 初始化第0张图片 white_frame

    # 视频总帧数
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))


    # ############## 在断电时启用 ##############
    # # 跳转到第 n 帧，n 需要手动输入
    # n = 146923
    # # 读取到 0.jpg
    # white_frame_path = r'C:\Users\myh26\Documents\999_fufuDoc\10.4_extractAndSaveUnique\0.jpg'
    # duanDian_white_frame_img = cv2.imread(white_frame_path)
    # cap.set(cv2.CAP_PROP_POS_FRAMES, n)
    # frame_count = n
    # ############## 在断电时启用 ##############

    ############## 正常时启用 ##############
    duanDian_white_frame_img = None
    ############## 正常时启用 ##############

    # 循环读取视频帧
    while success:
        if count <= period:
            # 读取一帧
            success, frame = cap.read()
            # 保存帧为图片文件
            frame_count += 1

            # 非断电情况
            if success and frame_count == 1:
                # 创建一个与原帧相同大小的白色图像
                white_frame = 255 * np.ones_like(frame, dtype=np.uint8)
                first_image_path = os.path.join(output_folder, '0.jpg')
                cv2.imwrite(first_image_path, white_frame)
                print("DDD")
                continue

            # 断电重启时的情况
            elif success and frame_count != 1 and white_frame is None:
                white_frame = duanDian_white_frame_img
                print("CCC")

            if success and white_frame is not None:
                score, diff = ssim(white_frame, frame, win_size=3, full=True)
                # 扩大差异
                enhanced_diff = (score * 10 ** 4)
                # 整除后放入哈希表
                bin_index = enhanced_diff // 10  # // 是整除运算符

                # 放入哈希表，且只保留桶中的第一项
                if not distance_bins[bin_index]:  # 检查桶是否为空
                    distance_bins[bin_index].append((bin_index, frame))
                    image_path = os.path.join(output_folder, f'{frame_count}.jpg')
                    success_save = cv2.imwrite(image_path, frame)

                    if not success_save:
                        print(f'保存第 {frame_count} 帧时失败。')
                        break

                    print(f'保存了 {frame_count} 帧图片，bin_index是{bin_index}')
                    update_text1(f'保存了第{frame_count} 帧图片，bin_index是{bin_index}')

            count = count + 1
        elif count > period:
            count = 0  # 重置 count
            distance_bins.clear()

        update_text0(f'处理了{frame_count}/{total_frames}张图片')

    cap.release()
    cv2.destroyAllWindows()

    # # 结束时关闭窗口
    # root.quit()  # 关闭 Tkinter 窗口


# 在单独的线程中运行窗口
process, update_text0, update_text1 = create_window("进度")
# 启动主程序线程
threading.Thread(target=main_program).start()

# 进入 Tkinter 主循环
# 为什么需要主循环？ 主循环是让图形用户界面 (GUI) 保持响应的核心。没有主循环，窗口就会在创建后立即关闭，程序无法处理任何事件，也无法更新界面
process.mainloop()