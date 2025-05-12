
# image_folder = 'img_training'
# video_name = 'D:/9_shipping_thang_may/videos/video_shipping1.mp4'
import imageio
import os
import path
import remove

path_phan_mem = path.path_phan_mem


print("nhập tên video input")
name_video = input()
print("nhập folder output")
name_folder_output = input()
remove.tao_folder(path_phan_mem+"/"+str(name_folder_output))
remove.tao_folder(path_phan_mem+"/videos")
remove.tao_folder(path_phan_mem+"/"+str(name_folder_output))
if os.path.exists(path_phan_mem+"/videos/"+str(name_video)+".mp4") == True:
    reader = imageio.get_reader(path_phan_mem+"/videos/"+str(name_video)+".mp4")
    r = 0
    for frame_number, im in enumerate(reader):
        # im is numpy array
        if frame_number % 30 == 0:
            r = r + 1
            if r == 4:
                r = 0
                imageio.imwrite(path_phan_mem+"/"+str(name_folder_output)+str(f"/frame_{frame_number}.jpg"), im)
else:
    print("không có video")
# save_all_frames('D:/9_shipping_thang_may/videos/video_shipping1.mp4', 'D:/9_shipping_thang_may/img_training', 'video1')

