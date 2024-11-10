import cv2
import os

# 指定视频文件路径
video_path = r'C:\Users\myh26\Documents\999_fufuDoc\中建史\第三节\中建史第三节.mp4'
# video_path = r'C:\Program Files\Adobe\Adobe Illustrator 2024\Support Files\Required\UXP\extensions\com.adobe.ccx.rtt\assets\richtooltips\AddAnchorPoint.mp4'

if not os.path.isfile(video_path):
    print(f"视频文件不存在: {video_path}")
    exit(1)

# 指定保存图片的文件夹
output_folder = r'C:\Users\myh26\Documents\999_fufuDoc\9.26'
# 创建文件夹如果不存在
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# 打开视频文件
cap = cv2.VideoCapture(video_path)

frame_count = 0
success = True

# 循环读取视频帧
while success:
    success, frame = cap.read()
    if success:
        # 保存帧为图片文件
        image_path = os.path.join(output_folder, f'{frame_count}.jpg')
        success_save = cv2.imwrite(image_path, frame)
        if not success_save:
            print(f'保存第 {frame_count} 帧时失败。')
            break
        frame_count += 1
        print(f'保存了 {frame_count} 帧图片。')
cap.release()
cv2.destroyAllWindows()

print(f'提取完成，共保存了 {frame_count} 帧图片。')
